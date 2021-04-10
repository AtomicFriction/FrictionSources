import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from tqdm import tqdm

import globals
from agent import Agent
from substrate import Subs
from analysis import Analysis, Temp
from logger import InitializeLog, LogProtocol, WriteLog
import hessian
from hessian import GetEigen, ProjectEigen
from simulators import SimulateAgent, SimulateSubs
from thermostats import ApplyThermo
from integrators import Integrate


"""
-> sigma is in Angstroms.
-> epsilon is in eV.
-> substrate spring constant is in eV/Angstroms^2.
-> substrate mass is in amu(atomic mass units).
-> latt_const for Argon is in Angstroms.
-> Coutoff constant taken as 2.5 * sigma.
"""

"""
-> If you are interested in using the plotting tools, use:
                DEV TOOLS SET 1 for regular 3D plots.
                DEV TOOLS SET 2 for real time animated 3D plots.

"""


def main():
    # Initialize the log file.
    InitializeLog()

    """
    # Initialize the hessian matrix.
    print('Hessian matrix calculations started...')

    hess_start = time.perf_counter()

    eigvec = GetEigen()

    hess_end = time.perf_counter()

    print(f"Hessian matrix calculations completed in {hess_end - hess_start:0.4f} seconds")
    # The eigenvectors of the hessian can be saved here in case you want to run tests on them. Comment this out otherwise.
    np.save('eigtest', eigvec)
    """
    # DEV TOOL SET 1: Empty arrays for plots.
    """
    time = []
    ag_x = []
    ag_y = []
    ag_z = []
    """

    # DEV TOOL SET 1: Set the axis to 3D projection mode for the 3D plots.
    #ax = plt.axes(projection='3d')
    # DEV TOOL SET 2: Initialize a figure for the animated plot.
    fig = plt.figure()

    for i in range(len(globals.run)):
        # Write the outline for the log file.
        LogProtocol(i)
        print("Executing protocol step " + str(i + 1) + " out of " + str(len(globals.run)))
        for j in tqdm(range(int(globals.run[i][2]))):
            # DEV TOOL SET 2:
            """
            if (j % 100 == 0):
                plt.ion()
                ax = fig.add_subplot(111, projection='3d')
                R = Subs.R
                ax.plot(R[:, 0], R[:, 1], R[:, 2], "o", markerfacecolor = "b", markersize = 3)
                ax.plot(Agent.pos[0][0], Agent.pos[0][1], Agent.pos[0][2], "s", markerfacecolor = "red", markersize = 8)
                ax.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], Agent.slider_pos[0][2], "s", markerfacecolor = "k", markersize = 16)
                ax.axis("tight")
                ax.set(zlim = (0, 7))
                ax.set(xlim = (0, 30))
                ax.set(ylim = (0, 30))
                plt.draw()
                plt.pause(0.1)
                ax.cla()
            """
            # Calculate the system temperature separately before the system updates.
            globals.temp, _, _ = Temp()
            # End of 3D animated plot here. Just end commenting out here.
            temp_inc = (((globals.run[i][1]) - (globals.run[i][0])) / (globals.run[i][2]))
            # Integration of the entire system here.
            (Subs.R, Subs.V, Subs.A) = SimulateSubs(globals.temp + temp_inc, ApplyThermo, Integrate)
            (Agent.pos, Agent.vel, Agent.acc) = SimulateAgent(globals.apply_agent[i], Integrate)
            # Run the necessary "analysis" functions.
            Analysis()
            # Write the wanted quatities to the log file.
            WriteLog(i, j)

            #proj = ProjectEigen(eigvec)


            # DEV TOOL SET 1:
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
