import numpy as np
import scipy.linalg as la
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
            plus_force_calc = SubstrateForce() # The force function needs to take the altered position element as an input here.
            plus_force_flat = plus_force_calc.flatten()
            plus_force = plus_force_flat[i]

            # Calculate the "minus" force element for differentiation later on.
            subs_pos_flat[j] = pos_minus
            minus_force_calc = SubstrateForce() # The force function needs to take the altered position element as an input here.
            minus_force_flat = minus_force_calc.flatten()
            minus_force = minus_force_flat[i]

            # Perform the actual differentiation here.
            ij_val = (plus_force - minus_force) / (2 * h)

            # Insert the calculated value to its place inside the Hessian matrix.
            hessian[i][j] = ij_val

    return hessian
