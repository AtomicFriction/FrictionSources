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
    #print("This is trie: " + str(trie))
    N = (trie.query_ball_point(agent_pos, globals.cutoff))
    #print("First N " + str(N))
    N = np.array([N[0]])
    #print("This is N: " + str(N))
    # Added custom exception when the distance between the agent and the substrate atom is larger than the cutoff distance.
    try:
        dist = distance.cdist(agent_pos, substrate_pos[N[0]], 'euclidean')
        #print("This is dist: " + str(dist))
    except IndexError:
        print("Agent out of bounds.")
        sys.exit()


    for i in range(len(N[0])):
        #print(i)
        rr = dist[0][i]
        #print("This is rr: " + str(rr))
        """
        -> "rr" is the distance between the agent and the substrate atom that lies inside the cutoff region.
        -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for substrate force calculation at /analysis.py/PE()).
        """
        # The following two variables are calculated for later use for the Lennard-Jones potential in analysis.
        globals.rr_6.append(rr ** 6)
        globals.rr_12.append(rr ** 12) # This is faster than (globals.rr_6[i] ** 2).
        # Evaluation of the direction of the Lennard-Jones force.
        dir = (agent_pos - substrate_pos[N[0][i]]) / rr
        #print("This is dir: " + str(dir))
        # Evaluation of the Lennard-Jones force.
        lj_force_whole = (((48 * globals.epsilon) * ((globals.sig_12) / (globals.rr_12[i] * rr))) - ((24 * globals.epsilon) * ((globals.sig_6) / (globals.rr_6[i] * rr)))) * dir
        """
        if (-0.00001< lj_force_whole[0][2] < 0.00001):
            print("Force is zero now!\n")
            print(rr)
            sys.exit()
        """
        #print("This is lj_force_whole " + str(lj_force_whole))
        # Append the calculated force to the "lj" array to sum it all up later.
        lj.append(lj_force_whole)
        """
        -> The Lennard-Jones force on each substrate atom with their index is calculated here and needed for the substrate force calculation.
        -> This is chosen to be global so that it will only be calculated once and will be used outside this function as well (for substrate force calculation at /interactions.py/SubstrateForce()).
        """
        globals.lj_force[N[0][i]] = lj[i][0]
        #print("This is globals.lj_force: " + str(globals.lj_force))
    # Sum the Lennard-Jones forces for every agent-susbtrate pair.
    lj_agent = np.sum(lj[0], axis = 0)
    #print("This is lj_agent " + str(lj_agent))

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
    globals.agent_force = lj_agent + globals.spr_force


    # Return the total force on the agent.
    return globals.agent_force


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
    subs_force[subs_bound] = np.squeeze(subs_k[0] * dR + subs_k[1] * dR**2 + subs_k[2] * dR**3, axis=1)

    # Adds the contribution of Lennard-Jones to the force
    subs_force_fin = subs_force - globals.lj_force

    return subs_force_fin
