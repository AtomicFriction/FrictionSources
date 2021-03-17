import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import globals
from agent import Agent, AgentPeriodicity
from substrate import Subs
from integrators import Integrate
from thermostats import ApplyThermostat
from analysis import Analysis
from logger import InitializeLog, LogProtocol, WriteLog
import hessian
from hessian import Hessian

# Initialize the log file.
InitializeLog()


"""
-> sigma is in Angstroms.
-> epsilon is in eV.
-> substrate spring constant is in eV/Angstroms^2.
-> substrate mass is in amu(atomic mass units).
-> latt_const for Argon is in Angstroms.
-> Coutoff constant taken as 2.5 * sigma.
"""

## Empty arrays for the plots. These arrays won't make it to the final version.
time = []
ag_x = []
ag_y = []
ag_z = []


#ax = plt.axes(projection='3d') # For 3D plot.
fig = plt.figure() # For 3D animated plot.

for i in range(len(globals.run)):
    # Write the outline for the log file.
    LogProtocol(i)
    for j in range(int(globals.run[i][2])):

        # Start of 3D animated plot here. Just start commenting out here.
        if (j % 300 == 0):
            plt.ion()
            ax = fig.add_subplot(111, projection='3d')
            R = Subs.R
            ax.plot(R[:, 0], R[:, 1], R[:, 2], "o", markerfacecolor = "b", markersize = 3)
            ax.plot(Agent.pos[0][0], Agent.pos[0][1], Agent.pos[0][2], "s", markerfacecolor = "red", markersize = 8)
            ax.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], Agent.slider_pos[0][2], "s", markerfacecolor = "k", markersize = 16)
            ax.axis("tight")
            ax.set(zlim = (0, 7))
            ax.set(xlim = (0, 50))
            ax.set(ylim = (0, 50))
            plt.draw()
            plt.pause(0.5)
            ax.cla()
        # End of 3D animated plot here. Just end commenting out here.

        # Integration of the entire system here.
        (Agent.pos, Agent.vel, Agent.acc), Agent.slider_pos = Integrate("AGENT", Agent.pos, Agent.vel, Agent.acc, Agent.mass)
        (Subs.R, Subs.V, Subs.A), _ = Integrate("SUBSTRATE", Subs.R, Subs.V, Subs.A, Subs.mass)
        # Run the necessary "analysis" functions.
        Analysis()
        # Check for and apply periodicity to the agent atom.
        Agent.pos, Agent.slider_pos = AgentPeriodicity(Agent.pos, Agent.slider_pos)
        # Apply thermostat.
        temp_inc = ((float(globals.run[i][1]) - float(globals.run[i][0])) / int(globals.run[i][2]))
        Subs.V = ApplyThermostat(globals.temp + temp_inc)
        # Write the wanted quatities to the log file.
        WriteLog(i, j)
        # Not used plot stuff after here. Uncomment if you want them.
        """
        # For 3D scatter plot.
        time.append(j)
        ag_x.append(Agent.pos[0][0])
        ag_y.append(Agent.pos[0][1])
        ag_z.append(Agent.pos[0][2])

        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        ax.set_zlabel("Z Position")
        ax.scatter3D(ag_x, ag_y, ag_z)
        plt.show()
        time.clear()
        ag_x.clear()
        """
