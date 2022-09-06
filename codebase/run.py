import numpy as np
import sys
from tqdm import tqdm
import globals
from agent import Agent
from substrate import Subs
from analysis import Temp, ProjectEigen, Analyze
from logger import InitLog, EigProjLogInit, WriteLog, EigProjLog
from hessian_vec import get_eigen, name_eigen
#from optimized_hessian import GetEigen, name_eigen
from thermostats import ApplyThermo
if (globals.agent_select == 'single'):
    from simulators_single import SimulateAgent, SimulateSubs
elif (globals.agent_select == 'wghost'):
    from simulators_ghost import SimulateAgent, SimulateSubs


def main(xyz_dir, log_dir, eig_dir):
    # Initialize the log files.
    InitLog(log_dir)
    EigProjLogInit(eig_dir)
    # Toggle for thermalization saving proccess.
    toggle = False

    # System state configurations checks.
    if (globals.from_progress == True and globals.calc_hessian == False and globals.load_eigs == True):
        print("Loading existing eigenvalues and continuing saved simulation.")
        # Load the previous state of the system.
        with np.load("system_state.npz") as system_state:
            Subs.R, Subs.V, Subs.A, i, step = \
                system_state["Subs_R"], system_state["Subs_V"], system_state["Subs_A"], \
                system_state["prot_i"], system_state["prot_j"]
            print("System state loaded.")
        # Load the eigenvalues and eigenvectors of the Hessian matrix from the previously saved files.
        try: globals.eigvec = np.load(name_eigen())
        except FileNotFoundError: exit('Cannot continue due to incongruity of the eigenvector file and input file.')

    # If the user wants a regular run, script goes on with the Hessian matrix calculation.
    elif (globals.from_progress == False and globals.calc_hessian == True and globals.load_eigs == False):
        print("Calculating Hessian matrix and starting a clean simulation.")
        GetEigen()
    elif (globals.from_progress == False and globals.calc_hessian == False and globals.load_eigs == True):
        print("Loading existing eigenvalues and starting a clean simulation.")
        try: globals.eigvec = np.load(name_eigen())
        except FileNotFoundError: exit('Cannot continue due to incongruity of the eigenvector file and input file.')

    else:
        print("You need to use a command line arguement to run the code. See command line options with 'python main.py --help'")
        sys.exit()


    tot_step = 0
    for i in range(len(globals.run)):
        # Write the outline for the log file.
        print("Executing protocol step " + str(i + 1) + " out of " + str(len(globals.run)))
        tot_step += int(globals.run[i][2])
        #print(globals.param['temp'])
        target_temp = globals.run[i][0]
        temp_inc = (((globals.run[i][1]) - (globals.run[i][0])) / (globals.run[i][2]))


        "Pull up the central atom on the surface"
        if (i == 1 and globals.pullup == True):
            Subs.pull_up()


        for step in tqdm(range(int(globals.run[i][2])), file=sys.stdout):
            # Triggers if the user wants to animate the system.
            if (globals.animate != False and globals.animate != None):
                if (step % int(globals.animate_step) == 0):
                    # Opens an xyz file with the setting 'ab', which stands for (a)ppend in (b)inary mode
                    with open(xyz_dir, 'ab') as coord:
                        # Save the Subs.R array to the file with the total atom number and time step as headers
                        np.savetxt(coord, Subs.R, header='{}\n{}'.format(Subs.tot_num + 2, tot_step), comments='')
                        # Save the positions of agent and slider atoms at the end of the time step
                        np.savetxt(coord, Agent.R)
                        np.savetxt(coord, Agent.slider_pos)

            # Temprature is always calculated because it is needed for the thermostats. Calculate the system temperature separately before the system updates.
            globals.log_param['temp'] = Temp()
            target_temp += temp_inc
            # Integration of the entire system here.
            (Subs.R, Subs.V, Subs.A) = SimulateSubs(target_temp, ApplyThermo, i, step)
            (Agent.R, Agent.V, Agent.A) = SimulateAgent(globals.apply_agent[i], i, step, eig_dir, log_dir)
            # Real time step counter for the plotter, implemented as a global variable now, may change it later on.
            globals.steps += 1

            # Hard coded eigenvector projection calculations for a baseline.
            project_last_steps = 10000 # Steps to calculate eigenvector projections before the protocols with the "Agent" starts.
            per_last_step = 1000
            if (step > project_last_steps + 1 and step % per_last_step):
                proj = ProjectEigen(globals.eigvec, Subs.R, Subs.bound, globals.initial_Subs_R, globals.eig_proj[0])
                EigProjLog(eig_dir, i, globals.steps, proj)
                # Write the calculated quatities to the log file.
                WriteLog(log_dir, i, globals.steps)

            # Calculate eigenvector projections and run analysis functions.
            if (step % globals.eig_proj[1] == 0):
                proj = ProjectEigen(globals.eigvec, Subs.R, Subs.bound, globals.initial_Subs_R, globals.eig_proj[0])
                EigProjLog(eig_dir, i, globals.steps, proj)
                # Run the necessary analysis functions.
                Analyze(i)
                # Write the calculated quantities to the log file.
                WriteLog(log_dir, i, globals.steps)
            # Triggers if the user wants to save the system state.
            if (globals.save_progress != False):
                '''
                FOR DEV USE - SAVE THE THERMALISATION PROTOCOLS
                '''
                if (i == 2 and toggle == False):
                    np.savez("system_state.npz", Subs_R = Subs.R, Subs_V = Subs.V, Subs_A = Subs.A, prot_i = i, prot_j = step)
                    print("System state saved at step " + str(step) + " of protocol run " + str(i + 1) + " out of " + str(len(globals.run)))
                    # toggle to run the thermalization saving process only once.
                    toggle = True
                """
                if (step % int(globals.save_progress) == 0):
                    # Save the whole state of the system.
                    np.savez("system_state.npz", Subs_R = Subs.R, Subs_V = Subs.V, Subs_A = Subs.A, Agent_R = Agent.R, Agent_V = Agent.V, Agent_A = Agent.A, Agent_slider_pos = Agent.slider_pos, Agent_slider_vel = Agent.slider_vel, prot_i = i, prot_j = step)
                    print("System state saved at step " + str(step) + " of protocol run " + str(i + 1) + " out of " + str(len(globals.run)))
                """
