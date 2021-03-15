import numpy as np
import numpy.linalg as LA
import globals
from substrate import Subs
from interactions import SubstrateForce

h = 1e-3
dim = 2


""" lemme psuedocode here
pos_plus = pos[j] + h
pos_minus = pos[j] - h
hessian[i][j] = (F(pos_plus)[i] - F(pos_minus)[i]) / (2 * h)
"""
def SubstrateForceH(R):
    subs_force = np.zeros(R.shape)

    R_N = R[Subs.N]
    R_A = R[Subs.trap].reshape((R_N.shape[0], 1, 3))
    dist = R_N - R_A
    dist[dist > Subs.L/2] -= Subs.L
    dist[dist < -Subs.L/2] += Subs.L
    norm = LA.norm(dist, axis=2)[:, np.newaxis]
    norm[norm[:, :, -1] == 0, -1] = Subs.latt_const

    dR = (norm - Subs.latt_const) / norm @ dist
    subs_force[Subs.trap] = np.squeeze(Subs.k * dR, axis=1)

    lj_force = globals.lj_force
    subs_force_fin = subs_force - lj_force

    return subs_force_fin


def Hessian():
    # Flatten the position array for easier indexing.
    subs_pos_flat = Subs.R.flatten()
    # Create an empty array of proper size.
    hessian = np.empty([3 * (globals.num ** (dim)), 3 * (globals.num ** (dim))])
    # Nested loop used for indexing.
    for i in range(3 * (globals.num ** (dim))):
        for j in range(3 * (globals.num ** (dim))):
            # Define "plus" and "minus" position elements here.
            pos_plus = subs_pos_flat[j] + h
            pos_minus = subs_pos_flat[j] - h

            # Calculate the "plus" force element for differentiation later on.
            subs_pos_flat[j] = pos_plus
            plus_pos_mat = np.reshape(subs_pos_flat, (globals.num * globals.num, 3))
            plus_force_calc = SubstrateForceH(plus_pos_mat) # The force function needs to take the altered position element as an input here.
            plus_force_flat = plus_force_calc.flatten()
            plus_force = plus_force_flat[i]


            # Calculate the "minus" force element for differentiation later on.
            subs_pos_flat[j] = pos_minus
            min_pos_mat = np.reshape(subs_pos_flat, (globals.num * globals.num, 3))
            minus_force_calc = SubstrateForceH(min_pos_mat) # The force function needs to take the altered position element as an input here.
            minus_force_flat = minus_force_calc.flatten()
            minus_force = minus_force_flat[i]

            # Perform the actual differentiation here.
            ij_val = (plus_force - minus_force) / (2 * h)

            # Insert the calculated value to its place inside the Hessian matrix.
            hessian[i][j] = ij_val

    _, eigvec = LA.eig(hessian)
    vec_proj = np.dot(eigvec, Subs.R) / (LA.norm(eigvec) * LA.norm(Subs.R))

    print(vec_proj)

    return hessian, vec_proj
