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
    acc = acc + GetForces() / mass

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
def RK4(pos, vel, delt):
    """
    -> 4th Order Runge Kutta will need the function to be defined differently.
    -> Work in progress for now.
    -> Detailed tests will be carried out and documented.
    """
    k1y = delt * vel
    k1v = delt * GetForces(pos)

    k2y = delt * (vel + 0.5 * k1v)
    k2v = delt * GetForces(pos + 0.5 * k1y)

    k3y = delt * (vel + 0.5 * k2v)
    k3v = delt * GetForces(pos + 0.5 * k2y)

    k4y = delt * (vel + k3v)
    k4v = delt * GetForces(pos + k3y)

    # Update next value of y
    pos = pos + (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0
    vel = vel + (k1v + 2 * k2v + 2 * k3v + k4v) / 6.0
    return pos, vel
