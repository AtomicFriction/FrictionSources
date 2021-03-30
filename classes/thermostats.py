import numpy as np
import globals
from math import sqrt
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


def VelRescale(F, T_target, trap):
    """
    -> Velocity Rescaling Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    L = sqrt(T_target / globals.T_inst)
    Subs.V[trap] *= L
    F = F
    return Subs.V, F


def Berendsen(F, T_target, trap):
    """
    -> Berendsen Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Tau is taken as an input.
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    L = sqrt(1 + (globals.dt / globals.tau) * (T_target / globals.T_inst - 1))
    Subs.V[trap] *= L
    F = F
    return Subs.V, F


def NoseHoover(F, T_target, trap):
    N = F[trap].shape[0]
    gamma_deriv = 1/globals.Q * (np.sum(Subs.mass * Subs.V[trap]**2) - 3*N * globals.boltz * T_target)
    gamma = integrate(gamma_deriv)
    F[trap] -= gamma * Subs.V[trap]
    Subs.V = Subs.V
    return Subs.V, F 



def Langevin(F, T_target, trap):
    wiener = sqrt(globals.dt) * np.random.rand(*Subs.V[trap].shape)
    F[trap] += (-1) * Subs.mass * globals.gamma * Subs.V[trap] + \
        sqrt(2 * Subs.mass * globals.gamma * globals.boltz * T_target) * wiener
    Subs.V = Subs.V
    return Subs.V, F

ApplyThermo = eval(globals.thermotype)
