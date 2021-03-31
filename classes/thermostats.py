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
    """Calculates the temperatures of the atoms to whom the thermostat applied and the atoms to whom the thermostat is not applied, respectively

    'trap' stands for the region the thermostat is applied
    'nontrap' stands for the region the thermostat is not applied
    'T_trap' and 'T_nontrap' stand for the temperatures of these regions, respectively
    Returns 'T_trap', 'T_nontrap', and total temperature
    """
    globals.T_trap =  Subs.mass * np.sum(Subs.V[Subs.trap] ** 2) / (3 * globals.boltz * Subs.trap.size)
    globals.T_nontrap =  Subs.mass * np.sum(Subs.V[Subs.bound] ** 2) / (3 * globals.boltz * Subs.bound.size) - globals.T_trap
    return globals.T_trap, globals.T_nontrap, globals.T_trap + globals.T_nontrap


def VelRescale(F, T_target, trap):
    """Updates only the velocity multiplying it by the factor 'L' calculated by using the ratio of target and instantaneous temperatures

    Takes the parameters '(F, T_target, trap)'
    Indexes the velocity array with the array 'trap', and updates only that part of the velocity array
    Returns both velocity and force arrays
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
