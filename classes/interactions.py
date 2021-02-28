import numpy as np
from scipy.spatial import distance
import timeit

from agent import Agent
from substrate import Subs
import globals
from tools import SafeDivision, NumericalDiff


#dev_analyze = input("Want to see forces? y/n:    ")
dev_analyze = "n"

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

        globals.lj_force = np.sum(lj, axis = 0)
    else:
        globals.lj_force = [[0, 0, 0]]


    ## Hooke's Law implementation. The equiliblium length taken as an input on the x-axis.
    spr_pot = []

    diff = Agent.pos - Agent.slider_pos
    disp = np.linalg.norm(diff) - globals.eq_len
    normalized = diff / np.linalg.norm(diff)

    globals.spr_force = -1 * globals.agent_k * disp * normalized

    if (dev_analyze == "y"):
        ## For debugging purposes.
        print("LJ:    " + str(globals.lj_force))
        print("SPR:    " + str(globals.spr_force))
        print(np.shape(globals.spr_force))
    elif (dev_analyze == "n"):
        pass

    agent_force = globals.lj_force + globals.spr_force

    return agent_force


def SubstrateForce():
    subs_force = np.zeros(Subs.R.shape)

    neighbor = Subs.R[list(Subs.N[Subs.trap])]
    atom = Subs.R[Subs.trap].reshape((neighbor.shape[0], 1, 3))
    dist = (neighbor - atom)
    dist[dist > globals.L/2] -= globals.L
    dist[dist < -globals.L/2] += globals.L
    norm = np.linalg.norm(dist, axis=2)[:, np.newaxis]

    dR = (norm - Subs.latt_const) / norm @ dist
    subs_force[Subs.trap] = np.squeeze(Subs.k * dR, axis=1)

    subs_force[Subs.trap] = np.squeeze(Subs.k * dR, axis=1)

    lj_force = globals.lj_force
    subs_force_fin = subs_force - lj_force

    return subs_force_fin


## A method to unify all of the force calculator functions in one. This is needed for later use in the integrators.
def GetForces(force_select):
    ##print("GetForces called.")
    if (force_select == "AGENT"):
        return AgentForce()
    elif (force_select == "SUBSTRATE"):
        return SubstrateForce()
