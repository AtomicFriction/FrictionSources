import globals
import numpy as np
from agent import Agent
from substrate import Subs


"""
-> Projection of the spring force vector on the slider velocity vector, calculated to obtain the friction force.
-> Not evaluated if (globals.ff_switch == 0).
"""
def FF():
    if (globals.ff_switch == 1):
        slid_vel_norm = np.sqrt(np.sum(Agent.slider_vel[0] ** 2))
        globals.ff = (np.dot(globals.spr_force[0], Agent.slider_vel[0]) / slid_vel_norm ** 2) * Agent.slider_vel[0]
        return globals.ff


"""
-> Potential energy calculation that consists of agent-substrate Lennard Jones Potential, agent-slider spring potential and substrate spring potentials.
-> Not evaluated if (globals.potential_switch == 0).
"""
def PE():
    if (globals.potential_switch == 1):
        rr_12 = (globals.rr ** 12)
        rr_6 = (globals.rr ** 6)
        sig_12 = (Agent.sigma ** 12)
        sig_6 = (Agent.sigma ** 6)
        lj_pot = np.sum((4 * Agent.epsilon) * ((sig_12 / rr_12) - (sig_6 / rr_6)))
        ag_pot = ((globals.agent_k * (globals.disp ** 2)) / 2)
        subs_pot = np.sum(1/2 * Subs.k * globals.subs_dR**2)
        globals.pe = lj_pot + ag_pot + subs_pot
        return globals.pe


"""
-> Kinetic energy calculation of agent and susbtrate atoms.
-> Not evaluated if (globals.kinetic_switch == 0).
"""
def KE():
    if (globals.kinetic_switch == 1):
        subs_kin = (Subs.mass * np.sum(Subs.V ** 2)) / 2
        agent_kin = (Agent.mass * np.sum(Agent.vel ** 2)) / 2
        globals.ke = subs_kin + agent_kin
        return globals.ke

"""
-> Adds the already calculated potential and kinetic energies.
-> Not evaluated if (globals.etot_switch == 0).
"""
def Etot():
    if (globals.etot_switch == 1):
        globals.etot = globals.pe + globals.ke
        return globals.etot

"""
-> Temprature is always calculated, because it is needed for the thermostats.
"""
def Temp():
    num_bound = 4 * (globals.num - 1)
    globals.temp =  Subs.mass * np.sum(Subs.V ** 2) / (3 * globals.boltz * num_bound)
    return globals.temp


"""
-> Group all the "analysis" funcitons together and call them all at once,
there will be just one line for "analysis" in the main function thanks to this approach.
"""
def Analysis():
    FF()
    PE()
    KE()
    Etot()
    Temp()