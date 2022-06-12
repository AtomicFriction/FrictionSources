# Library imports.
import numpy as np
import numpy.linalg as LA
from tqdm import tqdm
from math import sqrt
import time
import os
import sys


# File imports.
import globals
from substrate import Subs
from interactions import SubstrateForce
from input_parser.input_parser import parse


def name_eigen():
    # The eigenvectors of the hessian can be saved here in case you want to run tests on them.
    _, prot_param, _, subs_param, _, _ = parse('./input_parser/input.txt') # Parse the input file to save eigenvectors with the related parameters
    subs_param['bound_cond'] = subs_param['bound_cond'][0] # For naming convention of the file, take only the first letter of the boundary condition, 'fixed' -> 'f'
    del subs_param['displace_type'] # Since the displace type does not affect eigenvectors, remove it from the dictionary
    param = [prot_param['dt']] + list(subs_param.values()) # Make a list of the parameters to name the file
    eigvec_dir = './eigvecs/{}.npy'.format('-'.join(map(str, param)).replace('.', '-')) # Separate all the parameters by hyphen and replace the punctuation marks with it

    return eigvec_dir

def GetEigen():
    # Initialize the hessian matrix.
    print('Hessian matrix calculations started...')
    hess_start = time.perf_counter()
    h = 1e-3
    # Create an empty array of proper size.
    hessian = np.zeros([3 * Subs.bound.shape[0], 3 * Subs.bound.shape[0]])
    # Nested loop used for indexing.
    ctrl = np.zeros([3 * Subs.bound.shape[0], 3 * Subs.bound.shape[0]])
    for i in tqdm(range(3 * Subs.bound.shape[0]), file=sys.stdout):
        for j in range(i, 3 * Subs.bound.shape[0]):
            """
            Divider()
            print("Execution is at: i (outer loop) = " + str(i) + ", j (inner loop) = " + str(j))
            atom_num = FindEffectedComponent(j)
            ShowWhere((Subs.bound.shape[0]), atom_num)
            """
            full = np.copy(Subs.R)
            # Flatten the position array for easier indexing.
            subs_pos_flat = full[Subs.bound].flatten()
            pos_plus = subs_pos_flat[j] + h
            pos_minus = subs_pos_flat[j] - h

            # Calculate the "plus" force element for differentiation later on.
            subs_pos_flat[j] = pos_plus
            plus_pos_mat = np.reshape(subs_pos_flat, (Subs.bound.shape[0], 3))
            full[Subs.bound] = plus_pos_mat
            plus_force_calc = SubstrateForce(full, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound]
            plus_force_flat = plus_force_calc.flatten()
            plus_force = plus_force_flat[i]

            # Calculate the "minus" force element for differentiation later on.
            subs_pos_flat[j] = pos_minus
            min_pos_mat = np.reshape(subs_pos_flat, (Subs.bound.shape[0], 3))
            full[Subs.bound] = min_pos_mat
            minus_force_calc = SubstrateForce(full, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound]
            minus_force_flat = minus_force_calc.flatten()
            minus_force = minus_force_flat[i]

            # Perform the actual differentiation here.
            ij_val = (plus_force - minus_force) / (2 * h)
            #print("This is the second derivative ij: " + str(ij_val))

            # Insert the calculated value to its place inside the Hessian matrix.
            hessian[i][j] = -ij_val

    diag = hessian.diagonal()
    diag_mat = np.zeros(np.shape(hessian))
    np.fill_diagonal(diag_mat, diag)
    hessian = (hessian + np.transpose(hessian)) - diag_mat

    # Calculate the eigenvalues and eigenvectors.
    eigval, eigvec = LA.eig(hessian)

    # Ascending sort.
    idx = np.argsort(eigval)
    eigvecn = eigvec[:,idx]

    globals.eigvec = eigvecn

    hess_end = time.perf_counter()
    print(f"Hessian matrix calculations completed in {hess_end - hess_start:0.4f} seconds")

    eigvec_dir = name_eigen()
    os.makedirs(os.path.dirname(eigvec_dir), exist_ok=True)
    np.save(eigvec_dir, globals.eigvec)
