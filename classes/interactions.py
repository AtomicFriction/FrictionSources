def AgentForce(agent_pos, slider_pos, subs_pos, k):

    lj_force = np.zeros((1, 3))

    r = np.subtract(agent_pos, subs_pos)
    r = r.tolist()

    rr = [[], [], []]

    for i in range(3):
        for j in range(10):
            if (r[j][i] <= cutoff and r[j][i] >= -cutoff and r[j][i] != 0):
                rr[i].append(r[j][i])


    lj_force[0][0] = np.sum(48 * epsilon * np.power(sigma, 12) / np.power(rr[0], 13) - 24 * epsilon * np.power(sigma, 6) / np.power(rr[0], 7))
    lj_force[0][1] = np.sum(48 * epsilon * np.power(sigma, 12) / np.power(rr[1], 13) - 24 * epsilon * np.power(sigma, 6) / np.power(rr[1], 7))
    lj_force[0][2] = np.sum(48 * epsilon * np.power(sigma, 12) / np.power(rr[2], 13) - 24 * epsilon * np.power(sigma, 6) / np.power(rr[2], 7))


    spr_force = np.zeros((1, 3))

    disp = np.subtract(agent_pos, slider_pos)

    spr_force = - k * disp

    total_force = lj_force + spr_force


    return total_force, lj_force, spr_force


def GetForces(force_select, agent_pos, subs_pos, slider_pos, k):
    if (force_select == "AGENT"):
        return AgentForce(agent_pos, subs_pos, subs_pos, k)
