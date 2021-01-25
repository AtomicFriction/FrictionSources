import numpy as np
import matplotlib.pyplot as plt

import globals
from agent import Agent
from substrate import Substrate
from integrators import Integrate

"""
(force_select, subs_pos, pos, vel, acc, mass, slider_pos, ag_k, subs_k, neigh, latt_const) are the parameters.
"""

time = []
ag_x = []

plt.figure()
for t in range(1000):
    with plt.style.context(('dark_background')): ## This is arbitrary, I found the white background just too bright to look at :D
        R = Substrate.R
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.plot(R[:, 0], R[:, 1], "o", markerfacecolor = "b", markersize = 8)
        plt.axis([0, globals.num, -5, 5])
        plt.plot(Agent.pos[0][0], Agent.pos[0][1], "s", markerfacecolor = "red", markersize = 8)
        plt.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], "|", markerfacecolor = "k", markersize = 16)
        plt.pause(0.01)
        plt.clf()

        (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Substrate.R, Agent.pos, Agent.vel, Agent.acc, Agent.m, Agent.slider_pos, Agent.slider_vel, Agent.k, Substrate.k, Substrate.table, Substrate.latt_const)
        (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.R, Substrate.V, Substrate.A, Agent.m, Agent.slider_pos, Agent.slider_vel, Agent.k, Substrate.k, Substrate.table, Substrate.latt_const)

        ##time.append(t)
        ##ag_x.append(Agent.pos[0][0])


##plt.plot(time, ag_x)
##plt.show()
