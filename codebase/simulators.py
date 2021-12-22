import numpy as np
import globals
from agent import Agent
from substrate import Subs
from interactions import AgentForce, SubstrateForce
from logger import WriteLog, EigProjLog
from analysis import Analyze, ProjectEigen


"""
-> Constrains the motion to the desired axis by simple matrix multiplications.
Input x: Constrains the motion on the x-axis. Nullifies the components of other axes.
Input y: Constrains the motion on the y-axis. Nullifies the components of other axes.
Input y: Constrains the motion on the z-axis. Nullifies the components of other axes.
Else: Does nothing.
"""
def constrain(direction, vel, acc):
    if (direction == "z"):
        vel *= np.array([1, 1, 0])
        acc *= np.array([1, 1, 0])
        return (vel, acc)
    else:
        return (vel, acc)


"""
Simulates the agent and slider atoms for every time step.
Performs a "status check" to see if the user wants to apply the agent on the substrate atoms.
"""
def SimulateAgentEC(status, prot, step, eig_dir, log_dir):
    # "on" choice simulates the agent normally.
    if (status == 1):
        ## Updates of the target.
        Agent.V += (Agent.A * globals.dt)
        Agent.R += (Agent.R * globals.dt)
        AgentForce(Agent.R, Agent.slider_pos, Subs.R, None)
        Agent.A = (globals.agent_force - (globals.agent_eta * Agent.V) / Agent.mass)
        ## Operation to constrain the target, depends on the user input.
        (Agent.V, Agent.A) = constrain(globals.constrain, Agent.V, Agent.A)
        Agent.AgentPeriodicity(Subs.L)
        Agent.slider_pos += Agent.slider_vel * globals.dt

        return (Agent.R, Agent.V, Agent.A)

    # "off" choice virtually "lifts up" the agent from the substrate atoms, removing it from the system.
    elif (status == 0):
        # The global variable containing the Lennard-Jones force needs to be nullified, so that it won't effect the substrate force calculations.
        globals.lj_force = np.zeros(np.shape(globals.initial_Subs_R))
        return (Agent.R, Agent.V, Agent.A)


def SimulateAgentVV(status, prot, step, eig_dir, log_dir):
    # "on" choice simulates the agent normally.
    if (status == 1):

        ## Updates of the target.
        Agent.V += (0.5 * Agent.A * globals.dt)
        Agent.R += ((Agent.V * globals.dt) + (0.5 * Agent.A * (globals.dt ** 2)))
        AgentForce(Agent.R, Agent.slider_pos, Subs.R, None)
        Agent.A = (globals.agent_force - (globals.agent_eta * Agent.V) / Agent.mass)
        Agent.V += (0.5 * Agent.A * globals.dt)
        ## Operation to constrain the target, depends on the user input.
        (Agent.V, Agent.A) = constrain(globals.constrain, Agent.V, Agent.A)
        Agent.AgentPeriodicity(Subs.L)
        Agent.slider_pos += Agent.slider_vel * globals.dt

        return (Agent.R, Agent.V, Agent.A)

    # "off" choice virtually "lifts up" the agent from the substrate atoms, removing it from the system.
    elif (status == 0):
        # The global variable containing the Lennard-Jones force needs to be nullified, so that it won't effect the substrate force calculations.
        globals.lj_force = np.zeros(np.shape(globals.initial_Subs_R))
        return (Agent.R, Agent.V, Agent.A)

"""
def SimulateAgentRK4(status, prot, step, eig_dir, log_dir):
    # "on" choice simulates the agent normally.
    if (status == 1):
        ## Updates of the target.

        ## Operation to constrain the target, depends on the user input.
        (Agent.V, Agent.A) = constrain(globals.constrain, Agent.V, Agent.A)
        Agent.AgentPeriodicity(Subs.L)
        Agent.slider_pos += Agent.slider_vel * globals.dt

        return (Agent.R, Agent.V, Agent.A)

    # "off" choice virtually "lifts up" the agent from the substrate atoms, removing it from the system.
    elif (status == 0):
        # The global variable containing the Lennard-Jones force needs to be nullified, so that it won't effect the substrate force calculations.
        globals.lj_force = np.zeros(np.shape(globals.initial_Subs_R))
        return (Agent.R, Agent.V, Agent.A)
"""

"""
Simulates substrate atoms for that time step using thermostat and integrator
Takes the parameters '(T_target, ApplyThermo, Integrate)'
Calls the function 'ApplyThermo' providing it with the function 'SubstrateForce',
so that no requirement to define a variable for force
Returns the result of the function 'Integrate'
"""
def SimulateSubsEC(T_target, ApplyThermo, i, step):
    Subs.V += (Subs.A * globals.dt)
    Subs.R += (Subs.R * globals.dt)

    if (step % globals.apply_thermo[i] == 0):
        Subs.V, subs_force = ApplyThermo(\
            SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L), T_target, Subs.frame)
    else:
        subs_force = SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)

    Subs.A = (subs_force - (globals.subs_eta * Subs.V) / Subs.mass)
    ## Operation to constrain the target, depends on the user input.
    (Subs.V, Subs.A) = constrain(globals.constrain, Subs.V, Subs.A)

    return (Subs.R, Subs.V, Subs.A)


def SimulateSubsVV(T_target, ApplyThermo, i, step):
    Subs.V += (0.5 * Subs.A * globals.dt)
    Subs.R += ((Subs.V * globals.dt) + (0.5 * Subs.A * (globals.dt ** 2)))

    if (step % globals.apply_thermo[i] == 0):
        Subs.V, subs_force = ApplyThermo(\
            SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L), T_target, Subs.frame)
    else:
        subs_force = SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)

    Subs.A = (subs_force - (globals.subs_eta * Subs.V) / Subs.mass)
    Subs.V += (0.5 * Subs.A * globals.dt)
    ## Operation to constrain the target, depends on the user input.
    (Subs.V, Subs.A) = constrain(globals.constrain, Subs.V, Subs.A)

    return (Subs.R, Subs.V, Subs.A)

"""
def SimulateSubsRK4(T_target, ApplyThermo, i, step):
    Subs.V += (0.5 * Subs.A * globals.dt)
    Subs.R += ((Subs.V * globals.dt) + (0.5 * Subs.A * (globals.dt ** 2)))

    if (step % globals.apply_thermo[i] == 0):
        Subs.V, subs_force = ApplyThermo(\
            SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L), T_target, Subs.frame)
    else:
        subs_force = SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L)

    Subs.A = (subs_force - (globals.subs_eta * Subs.V) / Subs.mass)
    Subs.V += (0.5 * Subs.A * globals.dt)
    ## Operation to constrain the target, depends on the user input.
    (Subs.V, Subs.A) = constrain(globals.constrain, Subs.V, Subs.A)

    return (Subs.R, Subs.V, Subs.A)
"""


SimulateAgent = eval(globals.integtype_agent)
SimulateSubs = eval(globals.integtype_subs)
