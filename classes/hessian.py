import numpy as np
import numpy.linalg as LA
from tqdm import tqdm
from math import sqrt

import globals
from substrate import Subs
from interactions import SubstrateForce


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
            subs_pos_flat = Subs.R.flatten()
            #print("Without alteration: " + str(subs_pos_flat[j]))
            # Define "plus" and "minus" position elements here.
            pos_plus = subs_pos_flat[j] + h
            pos_minus = subs_pos_flat[j] - h

            # Calculate the "plus" force element for differentiation later on.
            subs_pos_flat[j] = pos_plus
            plus_pos_mat = np.reshape(subs_pos_flat, (Subs.R.shape[0], 3))
            plus_force_calc = SubstrateForce(plus_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound] # The force function needs to take the altered position element as an input here.
            #IndexedArray(plus_force_calc)
            plus_force_flat = plus_force_calc.ravel()
            plus_force = plus_force_flat[i]

            # Calculate the "minus" force element for differentiation later on.
            subs_pos_flat[j] = pos_minus
            min_pos_mat = np.reshape(subs_pos_flat, (Subs.R.shape[0], 3))
            minus_force_calc = SubstrateForce(min_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound] # The force function needs to take the altered position element as an input here.
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

    idx = eigval.argsort()[::1]
    eigval = eigval[idx]
    eigvec = eigvec[:,idx]

    return eigval, eigvec

"""
def ProjectEigen(eigvec, subs_pos, eigvec_num, interval, step_num):
    if (step_num % interval == 0):
        subs_pos_flat = subs_pos.flatten()
        eigvec_select = eigvec[:, 0:(eigvec_num + 1)]
        globals.vec_proj = np.dot(eigvec_select, subs_pos_flat) / (LA.norm(eigvec_select) * LA.norm(subs_pos))
        return globals.vec_proj
"""
