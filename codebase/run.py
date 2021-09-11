import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import sys
from tqdm import tqdm
import globals
from agent import Agent
from substrate import Subs
from analysis import Analyze, Temp
from logger import InitLog, WriteLog, EigProjLogInit, EigProjLog
from hessian import GetEigen
from simulators import SimulateAgent, SimulateSubs
from thermostats import ApplyThermo
from integrators import Integrate


def main():
    # Initialize the log files.
    InitLog()
    EigProjLogInit()
    
    # System state configurations checks.
    if (globals.from_progress == True and globals.calc_hessian == False and globals.load_eigs == False):
        # Load the previous state of the system.
        with np.load("system_state.npz") as system_state:
            Subs.R, Subs.V, Subs.A, Agent.R, Agent.V, Agent.A, Agent.slider_pos, Agent.slider_vel, i, step = system_state["Subs_R"], system_state["Subs_V"], system_state["Subs_A"], system_state["Agent_R"], system_state["Agent_V"], system_state["Agent_A"], system_state["Agent_slider_pos"], system_state["Agent_slider_vel"], system_state["prot_i"], system_state["prot_j"]
        # Load the eigenvalues and eigenvectors of the Hessian matrix from the previously saved files.
        globals.eigvec = np.load("./eigvecs/eigvecs.npy")
    # If the user wants a regular run, script goes on with the Hessian matrix calculation.
    elif (globals.from_progress == False and globals.calc_hessian == True and globals.load_eigs == False):
        GetEigen()
    elif (globals.from_progress == False and globals.calc_hessian == False and globals.load_eigs == True):
        globals.eigvec = np.load("./eigvecs/eigvecs.npy")
    else:
        print("You need to use a command line arguement to run the code. See command line options with 'python main.py --help'")
        sys.exit()

    
    # Initialize a figure in case the user wants to animate the system.
    fig = plt.figure()

    tot_step = 0
    for i in range(len(globals.run)): 
        # Write the outline for the log file.
        print("Executing protocol step " + str(i + 1) + " out of " + str(len(globals.run)))
        tot_step += int(globals.run[i][2])
        #print(globals.param['temp'])
        for step in tqdm(range(int(globals.run[i][2]))):
            # Triggers if the user wants to animate the system.
            if (globals.animate != False and globals.animate != None):
                if (step % int(globals.animate_step) == 0):
                    # Opens an xyz file with the setting 'ab', which stands for (a)ppend in (b)inary mode
                    with open('coord.xyz', 'ab') as coord:
                        # Save the Subs.R array to the file with the total atom number and time step as headers
                        np.savetxt(coord, Subs.R, header='{}\n{}'.format(Subs.tot_num + 2, tot_step), comments='')
                        # Save the positions of agent and slider atoms at the end of the time step
                        np.savetxt(coord, Agent.R)
                        np.savetxt(coord, Agent.slider_pos)

            # Temprature is always calculated because it is needed for the thermostats. Calculate the system temperature separately before the system updates.
            globals.log_param['temp'] = Temp() # why isn't this done in analysis.py?
            temp_inc = (((globals.run[i][1]) - globals.log_param['temp']) / (globals.run[i][2]))
            # Integration of the entire system here.
            (Subs.R, Subs.V, Subs.A) = SimulateSubs((globals.run[i][1]), ApplyThermo, Integrate, i, step)
            (Agent.R, Agent.V, Agent.A) = SimulateAgent(globals.apply_agent[i], Integrate, i, step)
            # Triggers if the user wants to save the system state.
            if (globals.save_progress != False and globals.save_progress != None):
                if (step % int(globals.save_progress_step) == 0):
                    # Save the whole state of the system.
                    np.savez("system_state.npz", Subs_R = Subs.R, Subs_V = Subs.V, Subs_A = Subs.A, Agent_R = Agent.R, Agent_V = Agent.V, Agent_A = Agent.A, Agent_slider_pos = Agent.slider_pos, Agent_slider_vel = Agent.slider_vel, prot_i = i, prot_j = step)
                    print("System state saved at step " + str(step) + " of protocol run " + str(i + 1) + " out of " + str(len(globals.run)))
