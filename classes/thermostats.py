import numpy as np
import globals
from tools import SafeDivision

"""
Since the constants below will be used in the functions,
they must be defined in one of the files. For now, they
are defined here, so whenever one of the functions below
is called, the constants must be also called.
"""

def vel_rescale(T, mass, V):
    """
    -> Velocity Rescaling Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    num_bound = 4 * (globals.num - 1)
    T_inst =  mass * np.sum(V ** 2) / (3 * globals.boltz * num_bound)
    L = (T / T_inst) ** (1 / 2)
    return L

def berendsen(T, mass, V, coup_param):
    """
    -> Berendsen Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Takes a coupling parameter (rise time?) "coup_param" as an input (Tau).
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    num_bound = 4 * (globals.num - 1)
    T_inst =  mass * np.sum(V ** 2) / (3 * globals.boltz * num_bound)
    L = (1 + (globals.dt / coup_param) * (SafeDivision(T,T_inst) - 1)) * (1/2)
    return L

def nosehoover(mass, R):
    s = None
    Q = None
    print("\n\nThis thermostat is not implementable yet.\n \
            If you want to proceed with another thermostat, \
            restart the program with another thermostat.\n\n")
    return quit()

def langevin(mass, V, F, f):
    gamma = None
    print("\n\nThis thermostat is not implementable yet.\n \
            If you want to proceed with another thermostat, \
            restart the program with another thermostat.\n\n")
    return quit()
