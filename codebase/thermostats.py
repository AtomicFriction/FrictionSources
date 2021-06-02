import numpy as np
import globals
from substrate import Subs
import math

"""
Since the constants below will be used in the functions,
they must be defined in one of the files. For now, they
are defined here, so whenever one of the functions below
is called, the constants must be also called.
"""


def VelRescale(F, T_target, frame):
    """
    Updates only the velocity multiplying it by the factor 'L' calculated by using the ratio of target and instantaneous temperatures
    Takes the parameters '(F, T_target, frame)'
    Indexes the velocity array with the array 'frame', and updates only that part of the velocity array
    Returns both velocity and force arrays
    """
    L = (T_target / globals.temp) ** (1/2)
    Subs.V[frame] *= L
    F = F
    return Subs.V, F


def Berendsen(F, T_target, frame):
    """
    -> Berendsen Thermostat.
    -> Calculates the instantaneous temperature of the system using the equipartition theorem, T_inst.
    -> T (taken as an input), is the target temperature.
    -> Tau is taken as an input.
    -> Returns a constant L to multiply with velocity of the particles in the system.
    """
    L = sqrt(1 + (globals.dt / globals.tau) * (T_target / globals.temp - 1))
    Subs.V[frame] *= L
    F = F
    return Subs.V, F


def NoseHoover(F, T_target, frame):
    N = F[frame].shape[0]
    gamma_deriv = 1/globals.Q * (np.sum(Subs.mass * Subs.V[frame]**2) - 3*N * globals.boltz * T_target)
    gamma = integrate(gamma_deriv)
    F[frame] -= gamma * Subs.V[frame]
    Subs.V = Subs.V
    return Subs.V, F



def Langevin(F, T_target, frame):
    wiener = sqrt(globals.dt) * np.random.rand(*Subs.V[frame].shape)
    F[frame] += (-1) * Subs.mass * globals.gamma * Subs.V[frame] + \
        sqrt(2 * Subs.mass * globals.gamma * globals.boltz * T_target) * wiener
    Subs.V = Subs.V
    return Subs.V, F

ApplyThermo = eval(globals.thermotype)
