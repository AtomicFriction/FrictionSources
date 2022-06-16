import numpy as np
import numpy.linalg as LA

import globals
from substrate import Subs, Substrate
from interactions import SubstrateForce
from input_parser.input_parser import parse

def get_hessian():
    h = 1
    bound_num = Subs.bound.shape[0]
    # Create an empty array of proper size.
    H = np.zeros([3 * bound_num, 3 * bound_num])

    # Define an array for increment/discrement step
    S = h * np.eye(3*bound_num, 3*bound_num).reshape(3*bound_num, bound_num, 3)

    R_plus = np.repeat(Subs.R[np.newaxis], 3*bound_num, axis=0)
    R_minus = np.repeat(Subs.R[np.newaxis], 3*bound_num, axis=0)

    R_plus[:, Subs.bound, :] = Subs.R[Subs.bound] + S
    R_minus[:, Subs.bound, :] = Subs.R[Subs.bound] - S

    """ v_F = np.vectorize(SubstrateForce, otypes=list)
    F_plus = v_F(R_plus, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound] """
    for slice_p, slice_m in zip(R_plus, R_minus):
        F_p = SubstrateForce(slice_p, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound]
        F_m = SubstrateForce(slice_m, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound]

        H_i = (F_p - F_m) / (2*h)

        print(H_i)
        input()

get_hessian()