import numpy as np
from scipy.spatial import distance

from agent import Agent
from substrate import Substrate
import globals
from tools import SafeDivision, NumericalDiff


dev_analyze = input("Want to see forces? y/n:    ")

"""
-> Calculates the total force present on the Agent.
-> Includes the lennard-jones force and the spring force.
"""
def AgentForce():
    ##print("AgentForce called.")
    ## Lennard-Jones Potential implementation in 3D.
    lj = []
    lj_pot = []

    dist = distance.cdist(Agent.pos, Substrate.R, 'euclidean')

    cutoff = (dist != 0) & (dist < globals.cutoff) * 1
    extract = np.where(cutoff == 1)
    idx = np.unique(extract[0], return_index=True)
    table = np.array_split(extract[1], idx[1])[1:]

    ##print(len(table))
    if (len(table) == 1):
        for i in range(len(table[0])):
            rr = dist[0][table[0][i]]
            dir = np.subtract(Agent.pos, Substrate.R[table[0][i]]) / rr
            lj_force_whole = (((48 * Agent.epsilon) * ((Agent.sigma ** 12) / (rr ** 13))) - ((24 * Agent.epsilon) * ((Agent.sigma ** 6) / (rr ** 7)))) * dir
            lj.append(lj_force_whole)
            """
            print("-------------------------------------------------------")
            print("This is force calculated directly:    " + str(((48 * Agent.epsilon) * ((Agent.sigma ** 12) / (rr ** 13))) - ((24 * Agent.epsilon) * ((Agent.sigma ** 6) / (rr ** 7)))))
            """
            if (globals.potential_switch == 1):
                lj_pot = np.sum((4 * Agent.epsilon) * (((Agent.sigma / rr) ** 12) - ((Agent.sigma / rr) ** 6)))
                """
                h = 0.000005
                print("This is force from potential, h = " + str(h) + ":    " + str(-(((4 * Agent.epsilon) * (((Agent.sigma / (rr + h)) ** 12) - ((Agent.sigma / (rr + h)) ** 6))) - ((4 * Agent.epsilon) * (((Agent.sigma / (rr - h)) ** 12) - ((Agent.sigma / (rr - h)) ** 6)))) / (2 * h)))
                """
            else:
                pass

        globals.lj_force = np.sum(lj, axis = 0)
    else:
        globals.lj_force = [[0, 0, 0]]


    ## Hooke's Law implementation. The equiliblium length taken as an input on the x-axis.
    spr_force = np.zeros((1, 3))
    spr_pot = []

    diff = np.subtract(Agent.pos, Agent.slider_pos)
    disp = np.linalg.norm(diff) - globals.eq_len
    normalized = diff / np.linalg.norm(diff)

    spr_force = -1 * globals.agent_k * disp * normalized
    """
    print("-------------------------------------------------------")
    print("This is force calculated directly: " + str(-1 * globals.agent_k * disp))
    """
    if (globals.potential_switch == 1):
        spr_pot = ((globals.agent_k * (disp ** 2)) / 2)
        """
        h = 1
        print("This is force from potential h =  " + str(h) + ": " + str(-(((globals.agent_k * ((disp + h) ** 2)) / 2) - ((globals.agent_k * ((disp - h) ** 2)) / 2)) / 2 * h))
        """
    else:
        pass


    if (dev_analyze == "y"):
        ## For debugging purposes.
        print("LJ:    " + str(globals.lj_force))
        print("SPR:    " + str(spr_force))
        print(np.shape(spr_force))
    elif (dev_analyze == "n"):
        pass


    agent_force = globals.lj_force + spr_force
    globals.agent_pot.append(lj_pot + spr_pot)


    ff = spr_force[0][0] - globals.lj_force[0][0]
    ##ff = spr_force[0][0]
    globals.fric.append(ff)

    ##print(globals.agent_pot)


    return agent_force


def SubstrateForce():
    subs_force = np.zeros(Substrate.R.shape)

    neighbor = Substrate.R[list(Substrate.N[Substrate.trap])]
    atom = Substrate.R[Substrate.trap].reshape((neighbor.shape[0], 1, 3))
    norm = np.linalg.norm(neighbor - atom, axis=2)[:, np.newaxis]

    subs_force[Substrate.trap] = np.squeeze(Substrate.k * (norm - Substrate.latt_const) / norm @ (neighbor - atom), axis=1)

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
