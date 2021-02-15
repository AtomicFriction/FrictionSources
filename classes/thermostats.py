import numpy as np
import globals
from tools import SafeDivision
from input_parser import parse



"""
Since the constants below will be used in the functions,
they must be defined in one of the files. For now, they
are defined here, so whenever one of the functions below
is called, the constants must be also called.
"""

def vel_rescale(T_aim, mass, V):
    """
    -> Velocity Rescaling Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    num_bound = 4 * (globals.num - 1)
    T_inst =  mass * np.sum(V ** 2) / (3 * globals.boltz * num_bound)
    L = (T_aim / T_inst) ** (1 / 2)
    return L

def berendsen(T_aim, mass, V, coup_param):
    """
    -> Berendsen Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Takes a coupling parameter (rise time?) "coup_param" as an input (Tau).
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    num_bound = 4 * (globals.num - 1)
    T_inst =  mass * np.sum(V ** 2) / (3 * globals.boltz * num_bound)
    L = (1 + (globals.dt / coup_param) * (SafeDivision(T_aim,T_inst) - 1)) * (1/2)
    return L

def nosehoover(mass, R):
    print("\n\nThis thermostat is not implementable yet.\n \
            If you want to proceed with another thermostat, \
            restart the program with another thermostat.\n\n")
    return quit()

def langevin(T_inst, mass, V_inst):
    comp1 = np.exp(-globals.gamma*globals.dt) * V_inst
    comp2 = np.random.normal(size=V_inst.shape) * np.sqrt(boltz*T_inst/mass*(1-np.exp(-2*globals.gamma*globals.dt)))
    print(comp1.shape, comp2.shape)
    V = comp1 + comp2
    return V

