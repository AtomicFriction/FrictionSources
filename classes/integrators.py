import numpy as np
from numba import jit
import agent
from interactions import GetForces

dt = 0.01
integ = "EC"


def EulerCromer(force_select, subs_pos, pos, vel, acc, mass, slider_pos, k):
    """
    -> Takes force values from the unified "GetForces()" function, uses that to obtain acceleration values.
    -> Uses a standard Euler-Cromer integration algorithm.
    -> Working as expected so far, no detailed tests have been carried out.
    """

    vel = vel + (acc * dt)
    pos = pos + (vel * dt)
    acc = (GetForces(force_select, pos, subs_pos, slider_pos, k) / mass)

    return (pos, vel, acc)


def VelocityVerlet(force_select, subs_pos, pos, vel, acc, mass, slider_pos, k):
    """
    -> Takes force values from the unified "GetForces()" function, uses that to obtain acceleration values.
    -> Uses a standard Velocity-Verlet integration algorithm.
    -> Working as expected so far, no detailed tests have been carried out.
    """
    pos = (pos + ((vel * dt) + (0.5 * acc * (dt ** 2))))
    vel = (vel + (0.5 * acc * dt))
    acc = (GetForces(force_select, pos, subs_pos, slider_pos, k) / mass)
    vel = (vel + (0.5 * acc * dt))

    return (pos, vel, acc)


def RK4(force_select, subs_pos, pos, vel, acc, mass, slider_pos, k):
    """
    -> Takes force values from the unified "GetForces()" function, uses that to obtain acceleration values.
    -> Uses a standard 4th Order Runge Kutta integration algorithm.
    -> Not sure if it is working as expected so far, no detailed tests have been carried out.
    """
    k1y = dt * vel
    k1v = dt * GetForces(force_select, pos, subs_pos, slider_pos, k)

    k2y = dt * (vel + 0.5 * k1v)
    k2v = dt * GetForces(force_select, pos + 0.5 * k1y, subs_pos, slider_pos, k)

    k3y = dt * (vel + 0.5 * k2v)
    k3v = dt * GetForces(force_select, pos + 0.5 * k2y, subs_pos, slider_pos, k)

    k4y = dt * (vel + k3v)
    k4v = dt * GetForces(force_select, pos + k3y, subs_pos, slider_pos, k)

    # Update next value of y
    pos = pos + (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0
    vel = vel + (k1v + 2 * k2v + 2 * k3v + k4v) / 6.0

    return (pos, vel, acc)


def Integrate(force_select, subs_pos, pos, vel, acc, mass, slider_pos, k):
    if (integ == "EC"):
        return EulerCromer(force_select, subs_pos, pos, vel, acc, mass, slider_pos, k)
    elif (integ == "VV"):
        return VelocityVerlet(force_select, subs_pos, pos, vel, acc, mass, slider_pos, k)
    elif (integ == "RK4"):
        return RK4(force_select, subs_pos, pos, vel, acc, mass, slider_pos, k)
