import numpy as np
import numpy.linalg as LA
from tqdm import tqdm
from math import sqrt

import globals
from substrate import Subs
from interactions import SubstrateForce


# These functions are here to make the analysis process easier. They will be removed later on.

# Creates an array of tuples that can be used to print forces and the atoms that those forces belong to.
def IndexedArray(arr, number_of_atoms):
    num_elements = sum(len(x) for x in arr)
    flat_ind = np.arange(0, num_elements / 3)
    ind = np.reshape(flat_ind, (number_of_atoms, 1))
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


# Returns "True" if the matrix is symmetric.
def check_symmetric(M, rtol=1e-05, atol=1e-08):
    return np.allclose(M, M.transpose(), rtol=rtol, atol=atol)


# Returns "True" if the matrix is diagonal.
def check_diagonal(M):
    i, j = np.nonzero(M)
    return np.all(i == j)


def GetEigen():
    h = 1e-6
    # Create an empty array of proper size.
    hessian = np.zeros([3 * Subs.bound.shape[0], 3 * Subs.bound.shape[0]])
    # Nested loop used for indexing.
    for i in tqdm(range(3 * Subs.bound.shape[0])):
        for j in range(3 * Subs.bound.shape[0]):

            Divider()
            print("Execution is at: i (outer loop) = " + str(i) + ", j (inner loop) = " + str(j))
            atom_num = FindEffectedComponent(j)
            ShowWhere((Subs.bound.shape[0]), atom_num)

            # Flatten the position array for easier indexing.
            subs_pos_flat = Subs.R.flatten()
            print("Without alteration: " + str(subs_pos_flat[j]))
            # Define "plus" and "minus" position elements here.
            pos_plus = subs_pos_flat[j] + h
            pos_minus = subs_pos_flat[j] - h

            # Calculate the "plus" force element for differentiation later on.
            subs_pos_flat[j] = pos_plus
            plus_pos_mat = np.reshape(subs_pos_flat, (Subs.R.shape[0], 3))
            plus_force_calc = SubstrateForce(plus_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound]
            IndexedArray(plus_force_calc, Subs.bound.shape[0])
            plus_force_flat = plus_force_calc.ravel()
            plus_force = plus_force_flat[i]

            # Calculate the "minus" force element for differentiation later on.
            subs_pos_flat[j] = pos_minus
            min_pos_mat = np.reshape(subs_pos_flat, (Subs.R.shape[0], 3))
            minus_force_calc = SubstrateForce(min_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound]
            IndexedArray(minus_force_calc, Subs.bound.shape[0])
            minus_force_flat = minus_force_calc.ravel()
            minus_force = minus_force_flat[i]

            # Perform the actual differentiation here.
            ij_val = (plus_force - minus_force) / (2 * h)
            print("This is the second derivative ij: " + str(ij_val))

            # Insert the calculated value to its place inside the Hessian matrix.
            hessian[i][j] = -ij_val


    print(check_symmetric(hessian))
    #print(check_diagonal(hessian))


    hessian = 0.5 * (hessian + np.transpose(hessian))

    eigval, eigvec = LA.eig(hessian)

    # Ascending sort.
    idx = np.argsort(eigval)
    eigvaln = eigval[idx]
    eigvecn = eigvec[:,idx]

    np.savetxt("hessian.csv", hessian)

    #print(np.nonzero(hessian))

    print(np.array2string(hessian.round(), suppress_small=True, formatter={'float': '{:0.4f}'.format}))

    return eigvaln, eigvecn


def ProjectEigen(eigvec, subs_pos, subs_bound, initial_pos, eigvec_num):
    eigvec_select = eigvec[:, 0:(eigvec_num)]
    vec_proj = abs(np.dot((subs_pos[subs_bound] - initial_pos[subs_bound]).ravel(), eigvec_select)) / (LA.norm(subs_pos[subs_bound]))
    return vec_proj
