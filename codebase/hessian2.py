import numpy as np
import numpy.linalg as LA

import globals
import sys
import os
from tqdm import tqdm
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

def get_eigen():
    h = 1e-3
    bound_num = Subs.bound.shape[0]
    # Create an empty array of proper size.
    H = np.zeros([3 * bound_num, 3 * bound_num])

    # Define an array for increment/discrement step
    S = h * np.eye(3*bound_num, 3*bound_num).reshape(3*bound_num, bound_num, 3)

    R_plus = np.repeat(Subs.R[np.newaxis], 3*bound_num, axis=0)
    R_minus = np.repeat(Subs.R[np.newaxis], 3*bound_num, axis=0)

    R_plus[:, Subs.bound, :] = Subs.R[Subs.bound] + S
    R_minus[:, Subs.bound, :] = Subs.R[Subs.bound] - S

    for i in tqdm(range(H.shape[0]), file=sys.stdout):
        F_p = SubstrateForce(R_plus[i], Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound].flatten()
        F_m = SubstrateForce(R_minus[i], Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)[Subs.bound].flatten()

        H[:, i] = (F_m - F_p) / (2*h) # the difference (F_p - F_m) multiplied by (-1)

    # Symmetrize the matrix
    H = 0.5 * (H + np.transpose(H))
    # Calculate the eigenvalues and eigenvectors
    eigval, eigvec = LA.eig(H)

    # Ascending sort
    idx = np.argsort(eigval)
    globals.eigvec = eigvec[:, idx]

    eigvec_dir = name_eigen()
    os.makedirs(os.path.dirname(eigvec_dir), exist_ok=True)
    np.save(eigvec_dir, globals.eigvec)
    
get_eigen()
