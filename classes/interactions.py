import numpy as np
from scipy.spatial import distance

from agent import Agent
from substrate import Substrate
import globals
from tools import SafeDivision


dev_analyze = input("Want to see forces? y/n:    ")

"""
-> Calculates the total force present on the Agent.
-> Includes the lennard-jones force and the spring force.
"""
def AgentForce():
    lj = []

    dist = distance.cdist(Agent.pos, Substrate.R, 'euclidean')

    cutoff = (dist != 0) & (dist < globals.cutoff) * 1
    extract = np.where(cutoff == 1)
    idx = np.unique(extract[0], return_index=True)
    table = np.array_split(extract[1], idx[1])[1:]

    for i in range(0, len(table[0])):
        rr = dist[0][table[0][i]]
        dir = np.subtract(Agent.pos, Substrate.R[table[0][i]]) / rr
        lj_force_comp = (48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr, 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr, 7)) * dir
        lj.append(lj_force_comp)

    lj_force = np.sum(lj, axis = 0)

    ## Hooke's Law implementation. The equiliblium length taken as an input on the x-axis.
    spr_force = np.zeros((1, 3))
    diff = np.subtract(Agent.pos, Agent.slider_pos)
    disp = np.linalg.norm(diff) - globals.eq_len
    normalized = diff / np.linalg.norm(diff)

    spr_force = -1 * globals.agent_k * disp * normalized


    if (dev_analyze == "y"):
        ## For debugging purposes.
        print("LJ:    " + str(lj_force))
        print("SPR:    " + str(spr_force))
        print(np.shape(spr_force))
    elif (dev_analyze == "n"):
        pass

    agent_force = lj_force + spr_force
    ##print(agent_force)

    return (agent_force, lj_force)


def SubstrateForce():
    subs_force = np.zeros(Subs.R.shape)
    
    neighbor = Subs.R[list(Subs.N[Subs.trap])]
    atom = Subs.R[Subs.trap].reshape((neighbor.shape[0], 1, 3))
    norm = LA.norm(neighbor - atom, axis=2)[:, np.newaxis]

    subs_force[Subs.trap] = np.squeeze(Subs.k * (norm - Subs.latt_const) / norm @ (neighbor - atom), axis=1)

    lj_force = AgentForce()[1]
    subs_force = np.subtract(subs_force, lj_force)

    return subs_force


## A method to unify all of the force calculator functions in one. This is needed for later use in the integrators.
def GetForces(force_select):
    if (force_select == "AGENT"):
        return AgentForce()[0]
    elif (force_select == "SUBSTRATE"):
        return SubstrateForce()
