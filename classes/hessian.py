import numpy as np
import numpy.linalg as LA
from tqdm import tqdm
from math import sqrt

import globals
from substrate import Subs
from interactions import SubstrateForce


""" lemme psuedocode here
pos_plus = pos[j] + h
pos_minus = pos[j] - h
hessian[i][j] = (F(pos_plus)[i] - F(pos_minus)[i]) / (2 * h)
"""

# These functions are here to make the analysis process easier. They will be removed later on.

# Creates an array of tuples that can be used to print forces and the atoms that those forces belong to.
def IndexedArray(arr):
    num_elements = sum(len(x) for x in arr)
    flat_ind = np.arange(0, num_elements / 3)
    ind = np.reshape(flat_ind, ((globals.num ** 2) * Subs.layers, 1))
    indexed = []
    for i in range(len(arr)):
        indexed.append((list(arr[i]), list(ind[i])))
    list_indexed = list(indexed)
    print(list_indexed)


# Simple divider to organize the prints.
def Divider():
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


# Prints the properties of the effected atom.
def FindEffectedComponent(ind):
    remainder = ind % 3
    atom_number = (ind - remainder) / 3
    component = {"0":"x", "1":"y", "2":"z"}
    print("Atom " + str(atom_number) + " " + component[str(remainder)] + " component.")
    return atom_number


# Shows the whereabouts of the atom in question.
def ShowWhere(number_of_atoms, atom_number):
    arr = np.zeros((number_of_atoms))
    arr[int(atom_number)] = 1
    shaped = np.reshape(arr, (int(sqrt(number_of_atoms)), int(sqrt(number_of_atoms))))
    print(shaped)


def check_symmetric(M, rtol=1e-05, atol=1e-08):
    return np.allclose(M, M.T, rtol=rtol, atol=atol)


def check_diagonal(M):
    i, j = np.nonzero(M)
    return np.all(i == j)


def GetEigen():
    h = 1e-3
    # Create an empty array of proper size.
    hessian = np.zeros([3 * Subs.bound.shape[0], 3 * Subs.bound.shape[0]])
    # Nested loop used for indexing.
    for i in tqdm(range(3 * Subs.bound.shape[0])):
        for j in range(3 * Subs.bound.shape[0]):
            """
            Divider()
            print("Execution is at: i (outer loop) = " + str(i) + ", j (inner loop) = " + str(j))
            atom_num = FindEffectedComponent(j)
            ShowWhere((globals.num ** 2) * Subs.layers, atom_num)
            """
            # Flatten the position array for easier indexing.
            subs_pos_flat = Subs.R[Subs.bound].flatten()
            #print("Without alteration: " + str(subs_pos_flat[j]))
            # Define "plus" and "minus" position elements here.
            pos_plus = subs_pos_flat[j] + h
            pos_minus = subs_pos_flat[j] - h

            # Calculate the "plus" force element for differentiation later on.
            subs_pos_flat[j] = pos_plus
            plus_pos_mat = (np.reshape(subs_pos_flat, (Subs.bound.shape[0], 3)))
            plus_force_calc = SubstrateForce(plus_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L) # The force function needs to take the altered position element as an input here.
            #IndexedArray(plus_force_calc)
            plus_force_flat = plus_force_calc.ravel()
            plus_force = plus_force_flat[i]

            # Calculate the "minus" force element for differentiation later on.
            subs_pos_flat[j] = pos_minus
            min_pos_mat = np.reshape(subs_pos_flat, (Subs.bound.shape[0], 3))
            minus_force_calc = SubstrateForce(min_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L) # The force function needs to take the altered position element as an input here.
            #IndexedArray(minus_force_calc)
            minus_force_flat = minus_force_calc.ravel()
            minus_force = minus_force_flat[i]

            # Perform the actual differentiation here.
            ij_val = (plus_force - minus_force) / (pos_plus - pos_minus)
            #print("This is the second derivative ij: " + str(ij_val))

            # Insert the calculated value to its place inside the Hessian matrix.
            hessian[i][j] = -ij_val

    hessian = 0.5 * (hessian + np.transpose(hessian))

    eigval, eigvec = LA.eig(hessian)


    return eigval.real, eigvec.real

"""
def ProjectEigen(eigvec, subs_pos, interval, eigvec_num, step_num):
    if (step_num % interval == 0):
        subs_pos_flat = subs_pos.flatten()
        eigvec_select = eigvec[:, 0:(eigvec_num + 1)]
        globals.vec_proj = np.dot(eigvec_select, subs_pos_flat) / (LA.norm(eigvec_select) * LA.norm(subs_pos))
        return globals.vec_proj
"""
