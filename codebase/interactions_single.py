import numpy as np
from scipy.spatial import distance, KDTree
import timeit
import sys


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
    #dist = distance.cdist(agent_pos, substrate_pos, 'euclidean')
    """ Create cKDTree, and query for the neighbors in the cut off region.
    If the system is fixed, box=None.
    If it is periodic, then box=[Subs.L, Subs.L, Subs.L], where L is the boxsize along i-th dimension.
    """

    trie = KDTree(substrate_pos, boxsize = box)
    N = (trie.query_ball_point(agent_pos, globals.cutoff))
    N = np.array([N[0]])
    try:
        dist = distance.cdist(agent_pos, substrate_pos[N[0]], 'euclidean')
    # Custom exception when the distance between the agent and the substrate atom is larger than the cutoff distance.
    except IndexError:
        print("Agent out of bounds.")
        sys.exit()

    # Create empty arrays to store these values.
    globals.rr_6 = np.zeros(shape = (1, len(N[0])))
    globals.rr_12 = np.zeros(shape = (1, len(N[0])))

    rr = dist[0][:len(N[0])]
    """
    -> "rr" is the distance between the agent and the substrate atom that lies inside the cutoff region.
    -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for substrate force calculation at /analysis.py/PE()).
    """
    # The following two variables are calculated for later use for the Lennard-Jones potential in analysis.
    globals.rr_6[0] = rr ** 6
    globals.rr_12[0] = rr ** 12
    rr = np.reshape(rr, (len(N[0]), 1))
    # Evaluation of the direction of the Lennard-Jones force.
    dir = (agent_pos - substrate_pos[N[0][:len(N[0])]]) / rr
    rr = dist[0][:len(N[0])]
    # Evaluation of the Lennard-Jones force.
    lj = np.multiply(np.reshape(((48 * globals.epsilon) * ((globals.sig_12) / (globals.rr_12[0] * rr))) - ((24 * globals.epsilon) * ((globals.sig_6) / (globals.rr_6[0] * rr))), (len(N[0]), 1)), dir)
    """
    -> The Lennard-Jones force on each substrate atom with their index is calculated here and needed for the substrate force calculation.
    -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for substrate force calculation at /interactions.py/SubstrateForce()).
    """
    #print(np.sum(lj, axis = 0))
    globals.lj_force[N[0][:len(N[0])]] = lj

    # Sum the Lennard-Jones forces for every agent-susbtrate pair.
    lj_agent = np.sum(lj, axis = 0)


    """
    Hooke's Law implementation in 3D.
    """
    # Individual distance between the 3D components of the agent and the slider.
    diff = agent_pos - slider_pos
    """
    -> The total displacement evaluated for the spring.
    -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for potential energy calculation at /analysis.py/PE()).
    """
    norm = np.linalg.norm(diff)
    dR = ((norm - globals.eq_len) / norm) * np.transpose(diff)
    """
    -> Evaluation of the spring force.
    -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for potential energy calculation at /analysis.py/FF()).
    """
    spr_force_whole = -1 * globals.agent_k * dR
    globals.spr_force = np.reshape(spr_force_whole, (1, 3))

    normal = np.array([0, 0, -1 * globals.normal_force])
    # Evaluate the total force on the agent. This is where we add the normal force as well.
    globals.agent_force = lj_agent + globals.spr_force + normal


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

    # Update the force array for free atoms in terms of the Hooke's Law
    subs_force[subs_bound] = np.squeeze(subs_k[0] * dR + subs_k[1] * dR**2 + subs_k[2] * dR**3, axis=1) \
        - globals.lj_force[subs_bound] # Adds the contribution of Lennard-Jones to the force

    return subs_force
