import numpy as np
from numba import jit


@jit(nopython = True)
def EulerCromer(pos, vel, acc, delt):
    """
    -> Takes force values from another function "GetForces()", uses that to obtain acceleration values.
    -> Detailed tests will be carried out and documented.
    """
    vel = vel + (acc * delt)
    pos = pos + (vel * delt)
    acc = acc = GetForces() / mass

    return pos, vel


@jit(nopython = True)
def VelocityVerlet(pos, vel, acc, delt):
    """
    -> Takes force values from another function "GetForces()", uses that to obtain acceleration values.
    -> Detailed tests will be carried out and documented.
    """
    pos = pos + (delt * vel) + (0.5 * (time_step ** 2.0) * acc)
    vel = vel + (0.5 * acc * delt)
    acc = GetForces() / mass
    vel = vel + (0.5 * acc * deltat)

    return pos, vel


@jit(nopython = True)
def RK4(t, dt, y, f):
    """
    -> 4th Order Runge Kutta will need the function to be defined differently.
    -> Work in progress for now.
    -> Detailed tests will be carried out and documented.
    """
    k1 = dt * f(t, y)
    k2 = dt * f(t + 0.5 * dt, y + 0.5 * k1)
    k3 = dt * f(t + 0.5 * dt, y + 0.5 * k2)
    k4 = dt * f(t + dt, y + k3)

    y_new = y + (1/6.) * (k1+ 2 * k2 + 2 * k3 + k4)
    return y_new
