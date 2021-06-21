import globals
import numpy as np
import numpy.linalg as LA
from agent import Agent
from substrate import Subs
import sys

"""
-> Projection of the spring force vector on the slider velocity vector calculated to obtain the friction force.
-> Not evaluated if (globals.ff_switch == 0).
"""
def FF():
    if (globals.ff_switch == 1):
        slid_vel_norm = np.sqrt(np.sum(Agent.slider_vel[0] ** 2))
        globals.ff = (np.dot(globals.spr_force[0], Agent.slider_vel[0]) / slid_vel_norm ** 2) * Agent.slider_vel[0]
        return globals.ff

"""
-> Vertical force on the agent defined as the force on the "z-axis".
"""
def VF():
    if (globals.vf_switch == 1):
        globals.vf = globals.agent_force[0][2]
        return globals.vf


"""
-> Potential energy calculation that consists of agent-substrate Lennard Jones Potential, agent-slider spring potential and substrate-substrate spring potentials.
-> Not evaluated if (globals.potential_switch == 0).
"""
def PE():
    if (globals.pe_switch == 1 or globals.etot_switch == 1):
        # Lennard-Jones potential calculation between agent-substrate.
        lj_pot = (np.sum((4 * globals.epsilon) * ((globals.sig_12 / np.array(globals.rr_12)) - (globals.sig_6 / np.array(globals.rr_6)))))
        # Spring potential calculation between agent-slider.
        ag_pot = ((globals.agent_k * (globals.disp ** 2)) / 2)
        # Spring potential calculation between substrate-substrate.
        subs_pot = np.sum(1/2 * Subs.k * globals.subs_dR**2)
        globals.pe = lj_pot + ag_pot + subs_pot
        return globals.pe
        

"""
-> Kinetic energy calculation of agent and susbtrate atoms.
-> Not evaluated if (globals.kinetic_switch == 0).
"""
def KE():
    if (globals.ke_switch == 1 or globals.etot_switch == 1):
        # Kinetic energy calculation for frame atoms.
        frame_kin = (Subs.mass * np.sum(Subs.V[Subs.frame] ** 2)) / 2
        # Kinetic energy calculation for trap atoms.
        trap_kin = (Subs.mass * np.sum(Subs.V[Subs.trap] ** 2)) / 2
        # Kinetic energy calculation for substrate atoms.
        subs_kin = frame_kin + trap_kin
        # Kinetic energy calculation for the agent atom.
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
-> Calculates the temperatures of the atoms to whom the thermostat is applied and the atoms to whom the thermostat is not applied separately.
-> 'trap' stands for the region the thermostat is applied
-> 'nontrap' stands for the region the thermostat is not applied
-> 'T_trap' and 'T_nontrap' stand for the temperatures of these regions, respectively
-> Returns 'T_trap', 'T_nontrap', and total temperature
"""
def Temp():
    t_bound =  (Subs.mass * np.sum(Subs.V[Subs.bound] ** 2)) / (3 * globals.boltz * Subs.bound.shape[0])
    if(np.isnan(t_bound) == True):
        print("NaN at temperature calc.")
        sys.exit()
    return t_bound


def ProjectEigen(eigvec, subs_pos, subs_bound, initial_pos, eigvec_num):
    eigvec_select = eigvec[:, 0:(eigvec_num)]
    vec_proj = abs(np.dot((subs_pos[subs_bound] - initial_pos[subs_bound]).ravel(), eigvec_select)) / (LA.norm(subs_pos[subs_bound] - initial_pos[subs_bound]))
    print(LA.norm(subs_pos[subs_bound] - initial_pos[subs_bound]))
    print(vec_proj)
    if(np.isnan(vec_proj[0]) == True):
        print("NaN at eigenvector projections.")
        sys.exit()
    return vec_proj

"""
-> Group all the "analysis" funcitons together and call them all at once,
-> There will be just one line for "analysis" in the main function thanks to this approach.
"""
def Analysis():
    FF()
    VF()
    PE()
    KE()
    Etot()
