import numpy as np
import globals
from agent import Agent, AgentPeriodicity
from substrate import Subs
from interactions import AgentForce, SubstrateForce
from integrators import Integrate
from thermostats import ApplyThermo


def SimulateAgent(Integrate):
    agent_force = AgentForce(Agent.pos, Agent.slider_pos, Subs.R, Agent.sigma, Agent.epsilon)
    Agent.pos, Agent.slider_pos = AgentPeriodicity(Agent.pos, Agent.slider_pos, Subs.L)
    return Integrate(agent_force, Agent.pos, Agent.vel, Agent.acc, Agent.mass)


def SimulateSubs(T_target, ApplyThermo, Integrate):
    """Simulates substrate for that time step using thermostat and integrator

    Takes the parameters '(T_target, ApplyThermo, Integrate)'
    Calls the function 'ApplyThermo' providing it with the function 'SubstrateForce',
    so that no requirement to define a variable for force
    Returns the result of the function 'Integrate'
    """

    Subs.V, subs_force = ApplyThermo(SubstrateForce(Subs.R, Subs.bound, Subs.N, Subs.latt_const, Subs.k, Subs.L), T_target, Subs.trap)

    return Integrate(subs_force, Subs.R, Subs.V, Subs.A, Subs.mass)
