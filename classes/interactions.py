import numpy as np
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
    lj_force = np.zeros((1, 3))

    r = np.subtract(Agent.pos, Substrate.R)
    r = r.tolist()

    ##print(np.shape(r))

    rr = [[0, 0, 0]]

    for j in range(globals.num):
        dist_r = np.sqrt((r[j][0] ** 2) + (r[j][1] ** 2) + (r[j][2] ** 2))
        if ((dist_r) <= globals.cutoff):
            rr = np.concatenate((rr, [r[j]]))

    rr = np.delete(rr, 0, 0)

    ##print(rr)

    ## Lennard-Jones Force implementation in 3D.
    lj_force[0][0] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[:, 0], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[:, 0], 7))
    lj_force[0][1] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[:, 1], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[:, 1], 7))
    lj_force[0][2] = np.sum(48 * Agent.epsilon * SafeDivision(np.power(Agent.sigma, 12), np.power(rr[:, 2], 13)) - 24 * Agent.epsilon * SafeDivision(np.power(Agent.sigma, 6), np.power(rr[:, 2], 7)))

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
    subs_force = np.zeros(np.shape(Substrate.R))
    # index R, such that R[1:-1], to ignore boundaries
    # (at least for now, but it may be generalized to non-boundary conditions)
    norm1 = np.linalg.norm(Substrate.R[Substrate.table[1:-1]][:, 1] - Substrate.R[1:-1])
    norm2 = np.linalg.norm(Substrate.R[Substrate.table[1:-1]][:, 0] - Substrate.R[1:-1])

    a = (globals.subs_k * (norm1 - globals.latt_const) * (Substrate.R[Substrate.table[1:-1]][:, 1] - Substrate.R[1:-1]))
    b = (globals.subs_k * (norm2 - globals.latt_const) * (Substrate.R[Substrate.table[1:-1]][:, 0] - Substrate.R[1:-1]))

    subs_force[1:-1] = SafeDivision(a, norm1) + SafeDivision(b, norm2)

    lj_force = AgentForce()[1]
    ##lj_force = 0
    subs_force = np.subtract(subs_force, lj_force)

    return subs_force


## A method to unify all of the force calculator functions in one. This is needed for later use in the integrators.
def GetForces(force_select):
    if (force_select == "AGENT"):
        return AgentForce()[0]
    elif (force_select == "SUBSTRATE"):
        return SubstrateForce()
