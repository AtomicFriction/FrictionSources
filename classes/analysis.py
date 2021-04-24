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
    # globals.rr list olarak al, her rr değeri için ayrı pe hesabı yapıp topla.
    if (globals.potential_switch == 1 or globals.etot_switch == 1):
        lj_pot_arr = []
        for i in range(len(globals.rr_12)):
            lj_pot_arr.append(np.sum((4 * globals.epsilon) * ((globals.sig_12 / globals.rr_12[i]) - (globals.sig_6 / globals.rr_6[i]))))
        lj_pot = np.sum(lj_pot_arr, axis = 0)
        ag_pot = ((globals.agent_k * (globals.disp ** 2)) / 2)
        subs_pot = np.sum(1/2 * Subs.k * globals.subs_dR**2)
        globals.pe = lj_pot + ag_pot + subs_pot
        return globals.pe


"""
-> Kinetic energy calculation of agent and susbtrate atoms.
-> Not evaluated if (globals.kinetic_switch == 0).
"""
def KE():
    if (globals.kinetic_switch == 1 or globals.etot_switch == 1):
        subs_kin = (Subs.mass * np.sum(Subs.V ** 2)) / 2
        agent_kin = (Agent.mass * np.sum(Agent.V ** 2)) / 2
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
    """Calculates the temperatures of the atoms to whom the thermostat applied and the atoms to whom the thermostat is not applied, respectively
    'trap' stands for the region the thermostat is applied
    'nontrap' stands for the region the thermostat is not applied
    'T_trap' and 'T_nontrap' stand for the temperatures of these regions, respectively
    Returns 'T_trap', 'T_nontrap', and total temperature
    """
    globals.T_trap =  Subs.mass * np.sum(Subs.V[Subs.trap] ** 2) / (3 * globals.boltz * Subs.trap.size)
    globals.T_nontrap =  Subs.mass * np.sum(Subs.V[Subs.bound] ** 2) / (3 * globals.boltz * Subs.bound.size) - globals.T_trap
    return globals.T_trap, globals.T_nontrap, globals.T_trap + globals.T_nontrap


"""
-> Group all the "analysis" funcitons together and call them all at once,
there will be just one line for "analysis" in the main function thanks to this approach.
"""
def Analysis():
    FF()
    PE()
    KE()
    Etot()
