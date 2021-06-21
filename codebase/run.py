import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import sys
from tqdm import tqdm
import globals
from agent import Agent
from substrate import Subs
from analysis import Analysis, Temp
from logger import InitLog, ProtLog, WriteLog, EigProjLogInit, EigProjLog
from hessian import GetEigen
from simulators import SimulateAgent, SimulateSubs
from thermostats import ApplyThermo
from integrators import Integrate

"""
import mplcyberpunk
plt.style.use("cyberpunk")
"""


def main():
    # Initialize the log file.
    InitLog()
    EigProjLogInit()
    
    # System state configurations checks.
    if (globals.from_progress == True and globals.calc_hessian == False and globals.load_eigs == False):
        # Load the previous state of the system.
        with np.load("system_state.npz") as system_state:
            Subs.R, Subs.V, Subs.A, Agent.R, Agent.V, Agent.A, Agent.slider_pos, Agent.slider_vel, i, j = system_state["Subs_R"], system_state["Subs_V"], system_state["Subs_A"], system_state["Agent_R"], system_state["Agent_V"], system_state["Agent_A"], system_state["Agent_slider_pos"], system_state["Agent_slider_vel"], system_state["prot_i"], system_state["prot_j"]
        # Load the eigenvalues and eigenvectors of the Hessian matrix from the previously saved files.
        globals.eigval, globals.eigvec = np.load('eigtest_eigval.npy'), np.load('eigtest_eigvec.npy')
    # If the user wants a regular run, script goes on with the Hessian matrix calculation.
    elif (globals.from_progress == False and globals.calc_hessian == True and globals.load_eigs == False):
        # Initialize the hessian matrix.
        print('Hessian matrix calculations started...')
        hess_start = time.perf_counter()
        globals.eigval, globals.eigvec = GetEigen()
        hess_end = time.perf_counter()
        print(f"Hessian matrix calculations completed in {hess_end - hess_start:0.4f} seconds")
    
        # The eigenvectors of the hessian can be saved here in case you want to run tests on them.
        np.save('eigtest_eigvec', globals.eigvec)
        np.save('eigtest_eigval', globals.eigval)
        print("Hessian matrix eigenvalues and eigenfunctions are saved.")
    elif (globals.from_progress == False and globals.calc_hessian == False and globals.load_eigs == True):
        globals.eigvec = np.load("eigtest_eigvec.npy")
        globals.eigval = np.load("eigtest_eigval.npy")
    else:
        print("You need to use a command line arguement to run the code. See command line options with 'python main.py --help'")
        sys.exit()

    
    # Initialize a figure in case the user wants to animate the system.
    fig = plt.figure()

    for i in range(len(globals.run)):
        # Write the outline for the log file.
        ProtLog(i)
        print("Executing protocol step " + str(i + 1) + " out of " + str(len(globals.run)))
        #print(globals.temp)
        for j in tqdm(range(int(globals.run[i][2]))):
            # Triggers if the user wants to animate the system.
            if (globals.animate != False and j % int(globals.animate_step) == 0):
                plt.ion()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(Subs.R[:, 0], Subs.R[:, 1], Subs.R[:, 2], "o", markerfacecolor = "b", markersize = 5)
                ax.plot(Agent.R[0][0], Agent.R[0][1], Agent.R[0][2], "8", markerfacecolor = "red", markersize = 16)
                ax.plot(Agent.slider_pos[0][0], Agent.slider_pos[0][1], Agent.slider_pos[0][2], "s", markerfacecolor = "k", markersize = 8)
                ax.axis("tight")
                ax.set(zlim = (0, 7))
                ax.set(xlim = (0, Subs.L))
                ax.set(ylim = (0, Subs.L))
                plt.draw()
                plt.pause(0.1)
                ax.cla()
            # Temprature is always calculated because it is needed for the thermostats. Calculate the system temperature separately before the system updates.
            globals.temp = Temp()
            #print(globals.temp)
            #temp_inc = (((globals.run[i][1]) - globals.temp) / (globals.run[i][2]))
            # Integration of the entire system here.
            (Subs.R, Subs.V, Subs.A) = SimulateSubs(100000, ApplyThermo, Integrate, i, j)
            (Agent.R, Agent.V, Agent.A) = SimulateAgent(globals.apply_agent[i], Integrate, i, j)

            # Triggers if the user wants to save the system state.
            if (globals.save_progress != False and j % int(globals.save_progress_step) == 0):
                # Save the whole state of the system.
                np.savez("system_state.npz", Subs_R = Subs.R, Subs_V = Subs.V, Subs_A = Subs.A, Agent_R = Agent.R, Agent_V = Agent.V, Agent_A = Agent.A, Agent_slider_pos = Agent.slider_pos, Agent_slider_vel = Agent.slider_vel, prot_i = i, prot_j = j)
                print("System state saved at step " + str(j) + " of protocol run " + str(i + 1) + " out of " + str(len(globals.run)))
            
            
