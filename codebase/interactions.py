import numpy as np
from scipy.spatial import distance, cKDTree
import timeit
import sys
from numba import jit


import globals
from substrate import Subs


# Lets the developer see big arrays.
np.set_printoptions(threshold=sys.maxsize)

"""
-> Calculates the total force present on the Agent.
-> Includes:
            3D Lennard-Jones force calculation between agent and substrate,
            3D spring force calculation between agent and slider.
"""
def AgentForce(agent_pos, slider_pos, substrate_pos, box):
    """
    Lennard-Jones Potential implementation in 3D.
    """
    lj = []
    # Evaluates all the distance values between the agent and the substrate atoms.
    dist = distance.cdist(agent_pos, substrate_pos, 'euclidean')

    cutoff = (dist != 0) & (dist < globals.cutoff) * 1
    extract = np.where(cutoff == 1)
    idx = np.unique(extract[0], return_index=True)
    table = np.array_split(extract[1], idx[1])[1:]
            
    """ Create cKDTree, and query for the neighbors in the cut off region.

    If the system is fixed, box=None.
    If it is periodic, then box=[Subs.L, Subs.L, Subs.L], where L is the boxsize along i-th dimension.
    """
    trie = cKDTree(substrate_pos, box=box)
    N = trie.query_ball_point(agent_pos, globals.cutoff)

    if (len(table) == 1):
        for i in range(len(table[0])):
            rr = dist[0][table[0][i]]
            """
            -> "rr" is the distance between the agent and the substrate atom that lies inside the cutoff region.
            -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for substrate force calculation at /analysis.py/PE()).
            """
            # The following four variables are calculated for the Lennard-Jones potential.
            globals.rr_12.append(rr ** 12)
            globals.rr_6.append(rr ** 6)
            # Evaluation of the direction of the Lennard-Jones force.
            dir = (agent_pos - substrate_pos[table[0][i]]) / rr
            # Evaluation of the Lennard-Jones force.
            lj_force_whole = (((48 * globals.epsilon) * ((globals.sig_12) / (globals.rr_12[i] * rr))) - ((24 * globals.epsilon) * ((globals.sig_6) / (globals.rr_6[i] * rr)))) * dir
            # Append the calculated force to the "lj" array to sum it all up later.
            lj.append(lj_force_whole)
            """
            -> The Lennard-Jones force on each substrate atom with their index is calculated here and needed for the substrate force calculation.
            -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for substrate force calculation at /interactions.py/SubstrateForce()).
            """
            globals.lj_force[table[0][i]] = lj[i][0]
        # Sum the Lennord-Jones forces for every agent-susbtrate pair.
        lj_agent = np.sum(lj, axis = 0)
    else:
        # This is to avoid "division by zero" errors if there are no substrate atoms lying inside the cutoff region.
        lj_agent = [[0, 0, 0]]


    """
    Hooke's Law implementation in 3D.
    """
    # Individual distance between the 3D components of the agent and the slider.
    diff = agent_pos - slider_pos
    """
    -> The total displacement evaluated for the spring.
    -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for potential energy calculation at /analysis.py/PE()).
    """
    globals.disp = np.linalg.norm(diff) - globals.eq_len
    # Normalization of the distance vector.
    normalized = diff / np.linalg.norm(diff)
    """
    -> Evaluation of the spring force.
    -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for potential energy calculation at /analysis.py/FF()).
    """
    globals.spr_force = -1 * globals.agent_k * globals.disp * normalized

    # Evaluate the total force on the agent.
    agent_force = lj_agent + globals.spr_force

    # Return the total force on the agent.
    return agent_force


def SubstrateForce(subs_pos, subs_bound, subs_N, latt_const, subs_k, subs_L):
    # Define a zero array for force with the shape Nx3
    subs_force = np.zeros(subs_pos.shape)

    # Define a position array of neighboring atoms with the shape Nx1x3
    R_N = subs_pos[subs_N]
    # Define a position array of atoms themselves with the shape Nx1x3
    R_A = subs_pos[subs_bound].reshape((R_N.shape[0], 1, 3))
    # Calculate distance between atoms and their neighbors in xyz directions separately
    dist = R_N - R_A
    # If the substrate is periodic, recompute the distance array for boundary atoms
    dist[dist > subs_L/2] -= subs_L
    dist[dist < -subs_L/2] += subs_L
    # Compute the norm using distance array, and increase the dimension by one
    norm = np.linalg.norm(dist, axis=2)[:, np.newaxis]
    # For 3D system, eliminate the contribution of the imaginary neighbors to the force
    norm[norm == 0] = latt_const

    # Define an array for the distance from equilibrium
    dR = (norm - latt_const) / norm @ dist
    # Update the force array for free atoms in terms of Hooke's Law
    subs_force[subs_bound] = np.squeeze(subs_k * dR, axis=1)

    # Adds the contribution of Lennard-Jones to the force
    subs_force_fin = subs_force - globals.lj_force

    return subs_force_fin
