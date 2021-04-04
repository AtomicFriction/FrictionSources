import numpy as np
import numpy.linalg as LA
import globals
from substrate import Subs
from interactions import SubstrateForce


""" lemme psuedocode here
pos_plus = pos[j] + h
pos_minus = pos[j] - h
hessian[i][j] = (F(pos_plus)[i] - F(pos_minus)[i]) / (2 * h)
"""


def GetEigen():
    h = 1e-5
    # Create an empty array of proper size.
    hessian = np.empty([3 * (globals.num ** 2) * Subs.layers, 3 * (globals.num ** 2) * Subs.layers])
    # Nested loop used for indexing.
    for i in range(3 * (globals.num ** 2) * Subs.layers):
        for j in range(3 * (globals.num ** 2) * Subs.layers):
            print("Execution is at: i = " + str(i) + ", j = " + str(j))
            # Flatten the position array for easier indexing.
            subs_pos_flat = Subs.R.flatten()
            print("Without alteration: " + str(subs_pos_flat[j]))
            # Define "plus" and "minus" position elements here.
            pos_plus = subs_pos_flat[j] + h
            pos_minus = subs_pos_flat[j] - h

            # Calculate the "plus" force element for differentiation later on.
            subs_pos_flat[j] = pos_plus
            print("pos_plus = " + str(pos_plus))
            plus_pos_mat = np.reshape(subs_pos_flat, ((globals.num ** 2) * Subs.layers, 3))
            print("plus_pos_mat = " + str(plus_pos_mat))
            plus_force_calc = SubstrateForce(plus_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L) # The force function needs to take the altered position element as an input here.
            print("plus_force_calc = " + str(plus_force_calc))
            plus_force_flat = plus_force_calc.ravel()
            plus_force = plus_force_flat[i]
            print("plus_force[i] = " + str(plus_force))

            # Calculate the "minus" force element for differentiation later on.
            subs_pos_flat[j] = pos_minus
            print("pos_minus = " + str(pos_minus))
            min_pos_mat = np.reshape(subs_pos_flat, ((globals.num ** 2) * Subs.layers, 3))
            print("min_pos_mat = " + str(min_pos_mat))
            minus_force_calc = SubstrateForce(min_pos_mat, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L) # The force function needs to take the altered position element as an input here.
            print("minus_force_calc = " + str(minus_force_calc))
            minus_force_flat = minus_force_calc.ravel()
            minus_force = minus_force_flat[i]
            print("minus_force[i] = " + str(minus_force))

            # Perform the actual differentiation here.
            ij_val = (plus_force - minus_force) / (pos_plus - pos_minus)
            print("This is the second derivative ij: " + str(ij_val))

            # Insert the calculated value to its place inside the Hessian matrix.
            hessian[i][j] = ij_val

    #hessian = 0.5 * (hessian + np.transpose(hessian))

    _, eigvec = LA.eig(hessian)
    """
    print("//////////////////////////////////////////////////////////////////////////////")
    print("//////////////////////////////////////////////////////////////////////////////")
    print("//////////////////////////////////////////////////////////////////////////////")

    print("Hessian: " + str(hessian))
    print("//////////////////////////////////////////////////////////////////////////////")
    print("//////////////////////////////////////////////////////////////////////////////")
    print("//////////////////////////////////////////////////////////////////////////////")

    print("For h = " + str(h) + ":    " + str(eigvec))
    """
    return eigvec

def ProjectEigen(eigvec, subs_pos):
    subs_pos_flat = subs_pos.flatten()
    vec_proj = np.dot(eigvec, subs_pos_flat) / (LA.norm(eigvec) * LA.norm(subs_pos))
    return vec_proj
