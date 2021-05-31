import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from tqdm import tqdm

import globals
from agent import Agent
from substrate import Subs
from analysis import Analysis, Temp
from logger import InitLog, ProtLog, WriteLog, EigProjLogInit, EigProjLog
import hessian
from hessian import GetEigen, ProjectEigen
from simulators import SimulateAgent, SimulateSubs
from thermostats import ApplyThermo
from integrators import Integrate


"""
-> distance is in Angstroms.
-> time is in picoseconds.
-> sigma is in Angstroms.
-> epsilon is in eV.
-> substrate spring constant is in eV/Angstroms^2.
-> substrate mass is in amu(atomic mass units).
-> latt_const for Argon is in Angstroms.
-> Coutoff constant taken as 2.5 * sigma.
"""


def main():
    # Initialize the log file.
    InitLog()
    EigProjLogInit()

    # Triggers if the user wants to run the previous system state.
    if (globals.from_progress == True):
        # Load the previous state of the system.
        with np.load("system_state.npz") as system_state:
            Subs.R, Subs.V, Subs.A, Agent.R, Agent.V, Agent.A, Agent.slider_pos, Agent.slider_vel, i, j = system_state["Subs_R"], system_state["Subs_V"], system_state["Subs_A"], system_state["Agent_R"], system_state["Agent_V"], system_state["Agent_A"], system_state["Agent_slider_pos"], system_state["Agent_slider_vel"], system_state["prot_i"], system_state["prot_j"]
        # Load the eigenvalues and eigenvectors of the Hessian matrix from the previously saved files.
        eigval, eigvec = np.load('eigtest_eigval.npy'), np.load('eigtest_eigvec.npy')
    # If the user wants a regular run, script goes on with the Hessian matrix calculation.
    else:
        # Initialize the hessian matrix.

        print('Hessian matrix calculations started...')

        hess_start = time.perf_counter()

        eigval, eigvec = GetEigen()

        hess_end = time.perf_counter()

        print(f"Hessian matrix calculations completed in {hess_end - hess_start:0.4f} seconds")


    # The eigenvectors of the hessian can be saved here in case you want to run tests on them.
    np.save('eigtest_eigvec', eigvec)
    np.save('eigtest_eigval', eigval)
    print("Hessian matrix eigenvalues and eigenfunctions are saved.")

    # ınitialize a figure in case the user wants to animate the system.
    fig = plt.figure()

    for i in range(len(globals.run)):
        # Write the outline for the log file.
        ProtLog(i)
        print("Executing protocol step " + str(i + 1) + " out of " + str(len(globals.run)))
        for j in tqdm(range(int(globals.run[i][2]))):
            # Triggers if the user wants to animate the system.
            if (globals.animate != None and j % int(globals.animate) == 0):
                plt.ion()
                ax = fig.add_subplot(111, projection='3d')
                R = Subs.R
                ax.plot(R[:, 0], R[:, 1], R[:, 2], "o", markerfacecolor = "b", markersize = 3)
                ax.plot(Agent.R[0][0], Agent.R[0][1], Agent.R[0][2], "s", markerfacecolor = "red", markersize = 8)
                ax.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], Agent.slider_pos[0][2], "s", markerfacecolor = "k", markersize = 16)
                ax.axis("tight")
                ax.set(zlim = (0, 7))
                ax.set(xlim = (0, 30))
                ax.set(ylim = (0, 30))
                plt.draw()
                plt.pause(0.1)
                ax.cla()
            # Calculate the system temperature separately before the system updates.
            globals.temp, _, _ = Temp()
            # End of 3D animated plot here. Just end commenting out here.
            temp_inc = (((globals.run[i][1]) - (globals.run[i][0])) / (globals.run[i][2]))
            # Integration of the entire system here.
            (Subs.R, Subs.V, Subs.A) = SimulateSubs(globals.temp + temp_inc, ApplyThermo, Integrate)
            (Agent.R, Agent.V, Agent.A) = SimulateAgent(globals.apply_agent[i], Integrate)
            # Run the necessary "analysis" functions.
            Analysis()
            # Write the wanted quatities to the log file.
            WriteLog(i, j)

            # Calculate eigenvector projections.
            if (j % globals.eig_proj[1] == 0):
                proj = ProjectEigen(eigvec, Subs.R, Subs.bound, globals.initial_Subs_R, globals.eig_proj[0])
                EigProjLog(i, j, proj)

            # Triggers if the user wants to save the system state.
            if (globals.save_progress != None and j % int(globals.save_progress) == 0):
                # Save the whole state of the system.
                np.savez("system_state.npz", Subs_R = Subs.R, Subs_V = Subs.V, Subs_A = Subs.A, Agent_R = Agent.R, Agent_V = Agent.V, Agent_A = Agent.A, Agent_slider_pos = Agent.slider_pos, Agent_slider_vel = Agent.slider_vel, prot_i = i, prot_j = j)
                print("System state saved at step " + str(j) + " of protocol run " + str(i + 1) + " out of " + str(len(globals.run)))
