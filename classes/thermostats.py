import numpy as np
import globals
from tools import SafeDivision
from substrate import Subs

"""
Since the constants below will be used in the functions,
they must be defined in one of the files. For now, they
are defined here, so whenever one of the functions below
is called, the constants must be also called.
"""

# Possible problem with "T" and increment here. Needs a discussion.
# Possible take the T_inst calculation out of the thermostats and make it a seperate function.

def CalcTemp():
    num_bound = 4 * (globals.num - 1)
    globals.T_inst =  Subs.mass * np.sum(Subs.V ** 2) / (3 * globals.boltz * num_bound)
    return globals.T_inst


def VelRescale(TargetTemp):
    """
    -> Velocity Rescaling Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    L = SafeDivision(TargetTemp, globals.T_inst) ** (1 / 2)
    ##L = T / T_inst ** (1 / 2)
    V = Subs.V * L
    return V


def Berendsen(TargetTemp):
    """
    -> Berendsen Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Tau is taken as an input.
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    L = (1 + (globals.dt / globals.tau) * (SafeDivision(TargetTemp, globals.T_inst) - 1)) * (1/2)
    V = Subs.V * L
    return V


def nosehoover(mass, R):
    s = None
    Q = None
    print("\n\nThis thermostat is not implementable yet.\n \
            If you want to proceed with another thermostat, \
            restart the program with another thermostat.\n\n")
    return quit()


# What is T_inst? Target temp or calculated temp?
def langevin():
    comp1 = np.exp(-globals.gamma * globals.dt) * Subs.V
    comp2 = np.random.normal(size = Subs.V.shape) * np.sqrt(boltz * globals.T_inst / mass * (1 - np.exp(-2 * globals.gamma * globals.dt)))
    print(comp1.shape, comp2.shape)
    V = comp1 + comp2
    return V


def ApplyThermostat(TargetTemp):
    if (globals.thermo == "velrescale"):
        return VelRescale(TargetTemp)
    elif (globals.thermo == "berendsen"):
        return Berendsen(TargetTemp)
