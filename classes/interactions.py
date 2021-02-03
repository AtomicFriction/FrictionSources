import numpy as np
from agent import Agent
import globals
from tools import SafeDivision


"""
-> Calculates the total force present on the Agent.
-> Includes the lennard-jones force and the spring force.
"""
def AgentForce(ag_pos, subs_pos, slider_pos):
    ## Empty arrays for the forces to fill in later on.
    lj_force = np.zeros((1, 3))
    spr_force = np.zeros((1, 3))

    disp = ag_pos - slider_pos
    r = np.subtract(ag_pos, subs_pos)
    r = r.tolist()

    rr = [[], [], []]
    for i in range(3):
        for j in range(globals.num):
            if (r[j][i] <= globals.cutoff and r[j][i] >= -globals.cutoff and r[j][i] != 0):
                rr[i].append(r[j][i])

    ## Lennard-Jones Force implementation in 3D.
    lj_force[0][0] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[0][0], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[0][0], 7))
    lj_force[0][1] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[0][1], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[0][1], 7))
    lj_force[0][2] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[0][2], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[0][2], 7))

    ## Hooke's Law implementation. The equiliblium length taken as an input on the x-axis.
    spr_force[0][0] = - globals.agent_k * (disp[0][0] - globals.eq_len)
    spr_force[0][1] = - globals.agent_k * disp[0][1]
    spr_force[0][2] = - globals.agent_k * disp[0][2]

    """
    ## For debugging purposes.
    print("LJ:    " + str(lj_force))
    print("SPR:    " + str(spr_force))
    print(np.shape(lj_force))
    """

    return (lj_force + spr_force, lj_force)


def SubstrateForce(ag_pos, subs_pos, slider_pos, neigh):
    subs_force = np.zeros(np.shape(subs_pos))
    # index R, such that R[1:-1], to ignore boundaries
    # (at least for now, but it may be generalized to non-boundary conditions)
    norm1 = np.linalg.norm(subs_pos[neigh[1:-1]][:, 1] - subs_pos[1:-1])
    norm2 = np.linalg.norm(subs_pos[neigh[1:-1]][:, 0] - subs_pos[1:-1])

    a = (globals.subs_k * (norm1 - globals.latt_const) * (subs_pos[neigh[1:-1]][:, 1] - subs_pos[1:-1]))
    b = (globals.subs_k * (norm2 - globals.latt_const) * (subs_pos[neigh[1:-1]][:, 0] - subs_pos[1:-1]))

    subs_force[1:-1] = SafeDivision(a, norm1) + SafeDivision(b, norm2)

    lj_force = AgentForce(ag_pos, subs_pos, slider_pos)[1]
    subs_force = np.subtract(subs_force, lj_force)

    return subs_force


## A method to unify all of the force calculator functions in one. This is needed for later use in the integrators.
def GetForces(force_select, ag_pos, subs_pos, slider_pos, neigh):
    if (force_select == "AGENT"):
        return AgentForce(ag_pos, subs_pos, slider_pos)[0]
    elif (force_select == "SUBSTRATE"):
        return SubstrateForce(ag_pos, subs_pos, slider_pos, neigh)
