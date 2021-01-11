import numpy as np
from agent import agent

cutoff = 4

def AgentForce(pos, subs_pos, slider_pos, k):
    """
    -> The name "pos" is used for the position of the agent. This name is chosen to enable the usage of the RK4 integrator.
    -> Calculates the total force present on the agent. Includes the lennard-jones force and the spring force.
    -> Working as expected so far, no detailed tests have been carried out.
    -> Needs the loop to be vectorized, work in progress.
    -> Needs a careful dimensional analysis to make sure this is the correct implementation.
    """
    lj_force = np.zeros((1, 3))
    spr_force = np.zeros((1, 3))

    ##print(pos)

    disp = np.subtract(pos, slider_pos)
    r = np.subtract(pos, subs_pos)
    r = r.tolist()

    ##print(r)

    rr = [[], [], []]

    for i in range(3):
        for j in range(50):
            if (r[j][i] <= cutoff and r[j][i] >= -cutoff and r[j][i] != 0):
                rr[i].append(r[j][i])

    ##print(rr)



    lj_force[0][0] = np.sum(48 * agent.epsilon * np.power(agent.sigma, 12) / np.power(rr[0], 13) - 24 * agent.epsilon * np.power(agent.sigma, 6) / np.power(rr[0], 7))
    lj_force[0][1] = np.sum(48 * agent.epsilon * np.power(agent.sigma, 12) / np.power(rr[1], 13) - 24 * agent.epsilon * np.power(agent.sigma, 6) / np.power(rr[1], 7))
    lj_force[0][2] = np.sum(48 * agent.epsilon * np.power(agent.sigma, 12) / np.power(rr[2], 13) - 24 * agent.epsilon * np.power(agent.sigma, 6) / np.power(rr[2], 7))

    ##print(spr_force)

    spr_force[0][0] = - k * disp[0][0]
    spr_force[0][1] = - k * disp[0][1]
    spr_force[0][2] = - k * disp[0][2]

    return lj_force + spr_force


## A method to unify all of the force calculator functions in one. This is needed for later use in the integrators.
def GetForces(force_select, pos, subs_pos, slider_pos, k):
    if (force_select == "AGENT"):
        return AgentForce(pos, subs_pos, slider_pos, k)
