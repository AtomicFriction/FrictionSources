import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import globals
from agent import Agent
from substrate import Substrate
from integrators import Integrate
from tools import AnalysisList, PE, Friction
from thermostats import ApplyThermostat
from logger import InitializeLog, LogProtocol, WriteLog

AnalysisList()
InitializeLog()


"""
-> sigma is in Angstroms.
-> epsilon is in eV.
-> substrate spring constant is in eV/Angstroms^2.
-> substrate mass is in amu(atomic mass units).
-> latt_const for Argon is in Angstroms.
-> Coutoff constant taken as 2.5 * sigma.
"""

#dev_select = input("Select visualization style. an2d/an3d/x/y/3d/ff:    ")
dev_select = "x"

## Empty arrays for the plots.
time = []
ag_x = []
ag_y = []
ag_z = []

if (dev_select == "an2d"):
    plt.figure()
    for i in range(len(globals.run)):
        for j in range(int(globals.run[i][2])):
            if (j % 1 == 0):
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
            pe = PE()
            ff = Friction()
            ##ke = KE()
            #Agent.pos[Agent.pos > L] = 0
            #Agent.pos[Agent.pos < 0] = L
            Agent.pos = np.mod(Agent.pos, L)

            ## Target temperature / Step.
            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Substrate.V = ApplyThermostat(temp_inc, 40, Substrate.V)

            ##print((globals.agent_pot))
            globals.agent_pot.clear()


elif (dev_select == "x"):
    for i in range(len(globals.run)):
        LogProtocol(i)
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)
            pe = PE()
            ff = Friction()
            ##ke = KE()
            """
            Agent.pos[Agent.pos > L] = 0
            Agent.pos[Agent.pos < 0] = L
            """
            #Agent.pos = np.mod(L, Agent.pos)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Substrate.V = ApplyThermostat(temp_inc, 40, Substrate.V)

            WriteLog(i, j, pe, ff)

            time.append(j)
            ag_x.append(Agent.pos[0][0])

        """
        plt.xlabel("Time")
        plt.ylabel("X Position")
        plt.plot(time, ag_x);
        plt.show()
        time.clear()
        ag_x.clear()
        """


elif(dev_select == "y"):
    for i in range(len(globals.run)):
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Substrate.V = ApplyThermostat(temp_inc, 40, Substrate.V)

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
    for i in range(len(globals.run)):
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Substrate.V = ApplyThermostat(temp_inc, 40, Substrate.V)

            time.append(j)
            ag_x.append(Agent.pos[0][0])
            ag_y.append(Agent.pos[0][1])
            ag_z.append(Agent.pos[0][2])

        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        ax.set_zlabel("z Position")
        ax.scatter3D(ag_x, ag_y, ag_z);
        plt.show()
        time.clear()
        ag_x.clear()


elif (dev_select == "ff"):
    for i in range(len(globals.run)):
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) + float(globals.run[i][0]) / int(globals.run[i][2]))
            Substrate.V = ApplyThermostat(temp_inc, 40, Substrate.V)

            time.append(j)

        plt.xlabel("Time")
        plt.ylabel("Lateral Force")
        plt.plot(time, globals.fric);
        plt.show()
        time.clear()
        globals.fric.clear()


elif (dev_select == "an3d"):
    fig = plt.figure()
    for i in range(len(globals.run)):
        for j in range(int(globals.run[i][2])):
            if (j % 300 == 0):
                plt.ion()
                ax = fig.add_subplot(111, projection='3d')
                R = Substrate.R

                ax.plot(R[:, 0], R[:, 1], R[:, 2], "o", markerfacecolor = "b", markersize = 3)
                ax.plot(Agent.pos[0][0], Agent.pos[0][1], Agent.pos[0][2], "s", markerfacecolor = "red", markersize = 8)
                ax.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], Agent.slider_pos[0][2], "|", markerfacecolor = "k", markersize = 16)
                ax.axis("tight")
                ax.set(zlim = (0, 7))
                plt.draw()
                plt.pause(0.5)
                ax.cla()

            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Substrate.R, Substrate.V, Substrate.A), _ = Integrate("SUBSTRATE", Substrate.R, Substrate.V, Substrate.A, Substrate.mass)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Substrate.V = ApplyThermostat(temp_inc, 40, Substrate.V)

            time.append(j)

else:
    print("Invalid visualization selection.")
