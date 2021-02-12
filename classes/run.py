import numpy as np
import matplotlib.pyplot as plt

import globals
from agent import Agent
from substrate import Substrate
from integrators import Integrate
from tools import RunConf, AnalysisList
from thermostats import ApplyThermostat

"""
-> sigma is in Angstroms.
-> epsilon is in eV.
-> substrate spring constant is in eV/Angstroms^2.
-> substrate mass is in amu(atomic mass units).
-> latt_const for Argon is in Angstroms.
-> Coutoff constant taken as 2.5 * sigma.
"""

dev_select = input("Select visualization style. anim/x/y/3d:    ")

## Empty arrays for the plots.
time = []
ag_x = []
ag_y = []

temperature_conf = RunConf()

if (dev_select == "anim"):
    plt.figure()
    for i in range(len(temperature_conf)):
        for j in range(int(temperature_conf[i][2])):
            with plt.style.context(('dark_background')):
                R = Substrate.R
                plt.xlabel("X Position")
                plt.ylabel("Y Position")
                plt.plot(R[:, 0], R[:, 1], "o", markerfacecolor = "b", markersize = 8)
                plt.axis([0, globals.latt_const * (globals.num), -10, 10])
                plt.plot(Agent.pos[0][0], Agent.pos[0][1], "s", markerfacecolor = "red", markersize = 8)
                plt.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], "|", markerfacecolor = "k", markersize = 16)
                plt.pause(0.01)
                plt.clf()

            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            L = ApplyThermostat(temperature_conf[i][1], 40, Substrate.V)
            Substrate.V = L * Substrate.V

elif (dev_select == "x"):
    for i in range(len(temperature_conf)):
        for j in range(int(temperature_conf[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            L = ApplyThermostat(temperature_conf[i][1], 40, Substrate.V)
            Substrate.V = L * Substrate.V

            time.append(j)
            ag_x.append(Agent.pos[0][0])

        plt.xlabel("Time")
        plt.ylabel("X Position")
        plt.plot(time, ag_x);
        plt.show()
        time.clear()
        ag_x.clear()

elif(dev_select == "y"):
    for i in range(len(temperature_conf)):
        for j in range(int(temperature_conf[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            L = ApplyThermostat(temperature_conf[i][1], 40, Substrate.V)
            Substrate.V = L * Substrate.V

            time.append(j)
            ag_y.append(Agent.pos[0][1])

        plt.xlabel("Time")
        plt.ylabel("Y Position")
        plt.plot(time, ag_y);
        plt.show()
        time.clear()
        ag_x.clear()

elif (dev_select == "3d"):
    ax = plt.axes(projection='3d')
    for i in range(len(temperature_conf)):
        for j in range(int(temperature_conf[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            L = ApplyThermostat(temperature_conf[i][1], 40, Substrate.V)
            Substrate.V = L * Substrate.V

            time.append(j)
            ag_x.append(Agent.pos[0][0])
            ag_y.append(Agent.pos[0][1])

        ax.set_xlabel("X Position")
        ax.set_ylabel("Time")
        ax.set_zlabel("Y Position")
        ax.scatter3D(ag_x, time, ag_y);
        plt.show()
        time.clear()
        ag_x.clear()

else:
    print("Invalid visualization selection.")
