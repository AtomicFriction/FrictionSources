import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import globals
from agent import Agent
from substrate import Subs
from integrators import Integrate
from tools import PE, KE, Friction
from thermostats import ApplyThermostat, CalcTemp
from logger import InitializeLog, LogProtocol, WriteLog
import hessian
from hessian import Hessian

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
        LogProtocol(i)
        for j in range(int(globals.run[i][2])):
            if (j % 1000 == 0):
                with plt.style.context(('dark_background')):
                    R = Subs.R
                    plt.xlabel("X Position")
                    plt.ylabel("Y Position")
                    plt.plot(R[:, 0], R[:, 1], "o", markerfacecolor = "b", markersize = 8)
                    plt.axis([0, globals.latt_const * (globals.num), -10, 10])
                    plt.plot(Agent.pos[0][0], Agent.pos[0][1], "s", markerfacecolor = "red", markersize = 8)
                    plt.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], "|", markerfacecolor = "k", markersize = 16)
                    plt.pause(0.01)
                    plt.clf()

            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Subs.R, Subs.V, Subs.A), _ = Integrate("SUBSTRATE", Subs.R, Subs.V, Subs.A, Subs.mass)

            pe = PE()
            ff = Friction()
            ke = KE()
            temp = CalcTemp()

            if (Agent.pos[0][0] > globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] - globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] - globals.L

            if (Agent.pos[0][0] < globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] + globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] + globals.L

            if (Agent.pos[0][1] > globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] - globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] - globals.L

            if (Agent.pos[0][1] < globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] + globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] + globals.L

            ## Target temperature / Step.
            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Subs.V = ApplyThermostat(temp_inc, 40, Subs.V)

            WriteLog(i, j, ff, pe, ke, 0, temp)

            ##print((globals.agent_pot))
            globals.agent_pot.clear()


elif (dev_select == "x"):
    for i in range(len(globals.run)):
        LogProtocol(i)
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Subs.R, Subs.V, Subs.A), _ = Integrate("SUBSTRATE", Subs.R, Subs.V, Subs.A, Subs.mass)

            pe = PE()
            ff = Friction()
            ke = KE()
            temp = CalcTemp()


            if (Agent.pos[0][0] > globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] - globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] - globals.L

            if (Agent.pos[0][0] < globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] + globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] + globals.L

            if (Agent.pos[0][1] > globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] - globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] - globals.L

            if (Agent.pos[0][1] < globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] + globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] + globals.L


            # Possible porblem fix temp_inc --> temp + temp_inc, discuss.
            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Subs.V = ApplyThermostat(temp + temp_inc)

            WriteLog(i, j, ff, pe, ke, 0, temp)

            #print(Hessian())
        """
            time.append(j)
            ag_x.append(Agent.pos[0][0])


        plt.xlabel("Time")
        plt.ylabel("X Position")
        plt.plot(time, ag_x)
        plt.show()
        time.clear()
        ag_x.clear()
        """

elif(dev_select == "y"):
    for i in range(len(globals.run)):
        LogProtocol(i)
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Subs.R, Subs.V, Subs.A), _ = Integrate("SUBSTRATE", Subs.R, Subs.V, Subs.A, Subs.mass)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Subs.V = ApplyThermostat(temp_inc, 40, Subs.V)

            pe = PE()
            ff = Friction()
            ke = KE()
            temp = CalcTemp()

            if (Agent.pos[0][0] > globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] - globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] - globals.L

            if (Agent.pos[0][0] < globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] + globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] + globals.L

            if (Agent.pos[0][1] > globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] - globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] - globals.L

            if (Agent.pos[0][1] < globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] + globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] + globals.L

            WriteLog(i, j, ff, pe, ke, 0, temp)

            time.append(j)
            ag_y.append(Agent.pos[0][1])

        plt.xlabel("Time")
        plt.ylabel("Y Position")
        plt.plot(time, ag_y)
        plt.show()
        time.clear()
        ag_x.clear()


elif (dev_select == "3d"):
    ax = plt.axes(projection='3d')
    for i in range(len(globals.run)):
        LogProtocol(i)
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Subs.R, Subs.V, Subs.A), _ = Integrate("SUBSTRATE", Subs.R, Subs.V, Subs.A, Subs.mass)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Subs.V = ApplyThermostat(temp_inc, 40, Subs.V)

            pe = PE()
            ff = Friction()
            ke = KE()
            temp = CalcTemp()

            if (Agent.pos[0][0] > globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] - globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] - globals.L

            if (Agent.pos[0][0] < globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] + globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] + globals.L

            if (Agent.pos[0][1] > globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] - globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] - globals.L

            if (Agent.pos[0][1] < globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] + globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] + globals.L

            WriteLog(i, j, ff, pe, ke, 0, temp)

            time.append(j)
            ag_x.append(Agent.pos[0][0])
            ag_y.append(Agent.pos[0][1])
            ag_z.append(Agent.pos[0][2])

        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        ax.set_zlabel("z Position")
        ax.scatter3D(ag_x, ag_y, ag_z)
        plt.show()
        time.clear()
        ag_x.clear()


elif (dev_select == "ff"):
    for i in range(len(globals.run)):
        LogProtocol(i)
        for j in range(int(globals.run[i][2])):
            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Subs.R, Subs.V, Subs.A), _ = Integrate("SUBSTRATE", Subs.R, Subs.V, Subs.A, Subs.mass)

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) + float(globals.run[i][0]) / int(globals.run[i][2]))
            Subs.V = ApplyThermostat(temp_inc, 40, Subs.V)

            pe = PE()
            ff = Friction()
            ke = KE()
            temp = CalcTemp()

            if (Agent.pos[0][0] > globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] - globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] - globals.L

            if (Agent.pos[0][0] < globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] + globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] + globals.L

            if (Agent.pos[0][1] > globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] - globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] - globals.L

            if (Agent.pos[0][1] < globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] + globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] + globals.L

            WriteLog(i, j, ff, pe, ke, 0, temp)

            time.append(j)

        plt.xlabel("Time")
        plt.ylabel("Lateral Force")
        plt.plot(time, globals.fric)
        plt.show()
        time.clear()
        globals.fric.clear()


elif (dev_select == "an3d"):
    fig = plt.figure()
    for i in range(len(globals.run)):
        LogProtocol(i)
        for j in range(int(globals.run[i][2])):
            if (j % 300 == 0):
                plt.ion()
                ax = fig.add_subplot(111, projection='3d')
                R = Subs.R

                ax.plot(R[:, 0], R[:, 1], R[:, 2], "o", markerfacecolor = "b", markersize = 3)
                ax.plot(Agent.pos[0][0], Agent.pos[0][1], Agent.pos[0][2], "s", markerfacecolor = "red", markersize = 8)
                ax.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], Agent.slider_pos[0][2], "|", markerfacecolor = "k", markersize = 16)
                ax.axis("tight")
                ax.set(zlim = (0, 7))
                plt.draw()
                plt.pause(0.5)
                ax.cla()

            (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
            (Subs.R, Subs.V, Subs.A), _ = Integrate("SUBSTRATE", Subs.R, Subs.V, Subs.A, Subs.mass)


            pe = PE()
            ff = Friction()
            ke = KE()
            temp = CalcTemp()

            if (Agent.pos[0][0] > globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] - globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] - globals.L

            if (Agent.pos[0][0] < globals.L):
                Agent.pos[0][0] = Agent.pos[0][0] + globals.L
                Agent.slider_pos[0][0] = Agent.slider_pos[0][0] + globals.L

            if (Agent.pos[0][1] > globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] - globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] - globals.L

            if (Agent.pos[0][1] < globals.L):
                Agent.pos[0][1] = Agent.pos[0][1] + globals.L
                Agent.slider_pos[0][1] = Agent.slider_pos[0][1] + globals.L

            temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
            Subs.V = ApplyThermostat(temp_inc, 40, Subs.V)

            WriteLog(i, j, ff, pe, ke, 0, temp)

            time.append(j)

else:
    print("Invalid visualization selection.")
