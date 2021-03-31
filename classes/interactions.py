import numpy as np
from scipy.spatial import distance
import timeit
import sys
from numba import jit


from agent import Agent
from substrate import Subs
import globals
from tools import SafeDivision, NumericalDiff


# Lets the developer see big arrays.
np.set_printoptions(threshold=sys.maxsize)

"""
-> Calculates the total force present on the Agent.
-> Includes:
            3D Lennard-Jones force calculation between agent and substrate,
            3D spring force calculation between agent and slider.
"""
def AgentForce():
    ## Lennard-Jones Potential implementation in 3D.
    lj = []
    lj_pot = []
    # Evaluates all the distance values between the agent and the substrate atoms.
    dist = distance.cdist(Agent.pos, Subs.R, 'euclidean')

    cutoff = (dist != 0) & (dist < globals.cutoff) * 1
    extract = np.where(cutoff == 1)
    idx = np.unique(extract[0], return_index=True)
    table = np.array_split(extract[1], idx[1])[1:]

    if (len(table) == 1):
        for i in range(len(table[0])):
            rr = dist[0][table[0][i]]
            # We only calculate these once for efficiency.
            globals.rr = rr
            rr_12 = (rr ** 12)
            rr_6 = (rr ** 6)
            sig_12 = (Agent.sigma ** 12)
            sig_6 = (Agent.sigma ** 6)
            # Evaluate the direction of the force.
            dir = (Agent.pos - Subs.R[table[0][i]]) / rr
            lj_force_whole = (((48 * Agent.epsilon) * ((sig_12) / (rr_12 * rr))) - ((24 * Agent.epsilon) * ((sig_6) / (rr_6 * rr)))) * dir
            lj.append(lj_force_whole)
            globals.lj_force[table[0][i]] = lj[i][0]

        globals.lj_agent = np.sum(lj, axis = 0)
    else:
        globals.lj_agent = [[0, 0, 0]]

    lj.clear()

    ## Hooke's Law implementation in 3D.
    spr_pot = []
    diff = Agent.pos - Agent.slider_pos
    globals.disp = np.linalg.norm(diff) - globals.eq_len
    normalized = diff / np.linalg.norm(diff)
    globals.spr_force = -1 * globals.agent_k * globals.disp * normalized

    agent_force = globals.lj_agent + globals.spr_force

    return agent_force


def SubstrateForce():
    subs_force = np.zeros(Subs.R.shape)

    R_N = Subs.R[Subs.N]
    R_A = Subs.R[Subs.bound].reshape((R_N.shape[0], 1, 3))
    dist = R_N - R_A
    dist[dist > Subs.L/2] -= Subs.L
    dist[dist < -Subs.L/2] += Subs.L
    norm = np.linalg.norm(dist, axis=2)[:, np.newaxis]
    norm[norm[:, :, -1] == 0, -1] = Subs.latt_const

    dR = (norm - Subs.latt_const) / norm @ dist
    subs_force[Subs.trap] = np.squeeze(Subs.k * dR, axis=1)

    lj_force = globals.lj_force
    globals.subs_force_fin = subs_force - lj_force

    return globals.subs_force_fin
