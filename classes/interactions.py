import numpy as np
from agent import Agent
import globals

def AgentForce(pos, subs_pos, slider_pos, ag_k):
    """
    -> The name "pos" is used for the position of the Agent. This name is chosen to enable the usage of the RK4 integrator.
    -> Calculates the total force present on the Agent. Includes the lennard-jones force and the spring force.
    -> Working as expected so far, no detailed tests have been carried out.
    -> Needs the loop to be vectorized, work in progress.
    -> Needs a careful dimensional analysis to make sure this is the correct implementation.
    """
    lj_force = np.zeros((1, 3))
    spr_force = np.zeros((1, 3))

    disp = np.subtract(pos, slider_pos)
    r = np.subtract(pos, subs_pos)
    r = r.tolist()

    rr = [[], [], []]

    for i in range(3):
        for j in range(50):
            if (r[j][i] <= globals.cutoff and r[j][i] >= -globals.cutoff and r[j][i] != 0):
                rr[i].append(r[j][i])

    lj_force[0][0] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[0], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[0], 7))
    lj_force[0][1] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[1], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[1], 7))
    lj_force[0][2] = np.sum(48 * Agent.epsilon * np.power(Agent.sigma, 12) / np.power(rr[2], 13) - 24 * Agent.epsilon * np.power(Agent.sigma, 6) / np.power(rr[2], 7))

    spr_force[0][0] = - ag_k * disp[0][0]
    spr_force[0][1] = - ag_k * disp[0][1]
    spr_force[0][2] = - ag_k * disp[0][2]

    ##print("LJ:    " + str(lj_force))
    ##print("SPR:    " + str(spr_force))
    ##print(np.shape(lj_force))

    return (lj_force + spr_force, lj_force)


def SubstrateForce(pos, subs_pos, slider_pos, ag_k, neigh, subs_k, latt_const):
    subs_force = np.zeros(np.shape(pos))
    # index R, such that R[1:-1], to ignore boundaries
    # (at least for now, but it may be generalized to non-boundary conditions)
    norm1 = np.linalg.norm(pos[neigh[1:-1]][:, 1] - pos[1:-1])
    norm2 = np.linalg.norm(pos[neigh[1:-1]][:, 0] - pos[1:-1])

    subs_force[1:-1] = subs_k * (norm1 - latt_const) * (pos[neigh[1:-1]][:, 1] - pos[1:-1]) / norm1 \
        +  subs_k * (norm2 - latt_const) * (pos[neigh[1:-1]][:, 0] - pos[1:-1]) / norm2

    lj_force = AgentForce(pos, subs_pos, slider_pos, ag_k)[1]

    return np.subtract(subs_force, lj_force)


## A method to unify all of the force calculator functions in one. This is needed for later use in the integrators.
def GetForces(force_select, pos, subs_pos, slider_pos, ag_k, subs_k, neigh, latt_const):
    if (force_select == "AGENT"):
        return AgentForce(pos, subs_pos, slider_pos, ag_k)[0]
    elif (force_select == "SUBSTRATE"):
        return SubstrateForce(pos, subs_pos, slider_pos, ag_k, neigh, subs_k, latt_const)
