import numpy as np
import globals
from agent import Agent
from substrate import Subs
from interactions import AgentForce, SubstrateForce
from integrators import Integrate
from thermostats import ApplyThermo
from hessian import GetEigen
from logger import InitLog, WriteLog, EigProjLogInit, EigProjLog
from analysis import Analyze, Temp, ProjectEigen


"""
Simulates the agent and slider atoms for every time step.
Performs a "status check" to see if the user wants to apply the agent on the substrate atoms.
"""
def SimulateAgent(status, Integrate, prot, step):
    # "on" choice simulates the agent normally.
    if (status == 1):
        agent_force = AgentForce(Agent.R, Agent.slider_pos, Subs.R, None)
        Agent.AgentPeriodicity(Subs.L)
        Agent.slider_pos += Agent.slider_vel * globals.dt
        # Calculate eigenvector projections.
        if (step % globals.eig_proj[1] == 0):
            proj = ProjectEigen(globals.eigvec, Subs.R, Subs.bound, globals.initial_Subs_R, globals.eig_proj[0])
            #print("a")
            EigProjLog(prot, step, proj)
            # Run the necessary "analysis" functions.
            Analyze()
            # Write the wanted quatities to the log file.
            WriteLog(prot, step)
        return Integrate(agent_force, Agent.R, Agent.V, Agent.A, Agent.mass)

    # "off" choice virtually "lifts up" the agent from the substrate atoms, removing it from the system.
    elif (status == 0):
        # The global variable containing the Lennard-Jones force needs to be nullified, so that it won't effect the substrate force calculations.
        globals.lj_force = np.zeros(np.shape(globals.initial_Subs_R))
        return (Agent.R, Agent.V, Agent.A)


def SimulateSubs(T_target, ApplyThermo, Integrate, i, step):
    """Simulates substrate atoms for that time step using thermostat and integrator
    Takes the parameters '(T_target, ApplyThermo, Integrate)'
    Calls the function 'ApplyThermo' providing it with the function 'SubstrateForce',
    so that no requirement to define a variable for force
    Returns the result of the function 'Integrate'
    """

    if (step % globals.apply_thermo[i] == 0):
        Subs.V, subs_force = ApplyThermo(SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L), T_target, Subs.frame)
    else:
        subs_force = SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)

    return Integrate(subs_force, Subs.R, Subs.V, Subs.A, Subs.mass)
