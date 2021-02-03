import numpy as np
import matplotlib.pyplot as plt

import globals
from agent import Agent
from substrate import Substrate
from integrators import Integrate
from tools import RunConf
from thermostats import vel_rescale, berendsen

"""
(force_select, ag_pos, subs_pos, slider_pos, slider_vel, neigh, mass, pos, vel, acc) are the parameters.
"""

time = []
ag_x = []

"""
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
"""

temperature_conf = RunConf()
##print(temperature_conf)

for i in range(len(temperature_conf)):
    for j in range(temperature_conf[i][2]):
        (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Substrate.R, Agent.slider_pos, Agent.slider_vel, Substrate.table, Agent.m, Agent.pos, Agent.vel, Agent.acc)
        (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Agent.pos, Substrate.R, Agent.slider_pos, Agent.slider_vel, Substrate.table, Substrate.mass, Substrate.R, Substrate.V, Substrate.A)

        L = berendsen(temperature_conf[i][1], 40, Substrate.V, (globals.dt *  temperature_conf[i][2]))
        Substrate.V = L * Substrate.V

        time.append(j)
        ag_x.append(Agent.pos[0][0])
        ##print(Substrate.R)

    plt.plot(time, ag_x)
    plt.show()
    time.clear()
    ag_x.clear()


"""
-> sigma is in Angstroms.
-> epsilon is in eV.
-> substrate spring constant is in eV/Angstroms^2.
-> substrate mass is in amu(atomic mass units).
-> latt_const for Argon is in Angstroms.
-> Coutoff constant taken as 2.5 * sigma.
"""
