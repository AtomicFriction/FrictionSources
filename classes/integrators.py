import numpy as np
from numba import jit
from interactions import GetForces
from tools import constrain
import globals


def EulerCromer(force_select, subs_pos, pos, vel, acc, mass, slider_pos, slider_vel, ag_k, subs_k, neigh, latt_const):
    """
    -> Takes force values from the unified "GetForces()" function, uses that to obtain acceleration values.
    -> Uses a standard Euler-Cromer integration algorithm.
    -> Working as expected.
    """
    vel = vel + (acc * globals.dt)
    pos = pos + (vel * globals.dt)
    acc = (GetForces(force_select, pos, subs_pos, slider_pos, ag_k, subs_k, neigh, latt_const) / mass)
    slider_pos = slider_pos + (slider_vel * globals.dt)
    ## Perform a quick array multiplication to constrain the movement. Takes inputs "x", "y" and "none".
    (vel, acc) = constrain(globals.constrain, vel, acc)
    ##print(type(vel))

    return (pos, vel, acc), slider_pos


def VelocityVerlet(force_select, subs_pos, pos, vel, acc, mass, slider_pos, slider_vel, ag_k, subs_k, neigh, latt_const):
    """
    -> Takes force values from the unified "GetForces()" function, uses that to obtain acceleration values.
    -> Uses a standard Velocity-Verlet integration algorithm.
    -> Working as expected so far.
    """
    pos = (pos + ((vel * globals.dt) + (0.5 * acc * (globals.dt ** 2))))
    vel = (vel + (0.5 * acc * globals.dt))
    acc = (GetForces(force_select, pos, subs_pos, slider_pos, ag_k, subs_k, neigh, latt_const) / mass)
    vel = (vel + (0.5 * acc * globals.dt))
    slider_pos = slider_pos + (slider_vel * globals.dt)
    ## Perform a quick array multiplication to constrain the movement. Takes inputs "x", "y" and "none".
    (vel, acc) = constrain(globals.constrain, vel, acc)

    return (pos, vel, acc), slider_pos


def RK4(force_select, subs_pos, pos, vel, acc, mass, slider_pos, slider_vel, ag_k, subs_k, neigh, latt_const):
    """
    -> Takes force values from the unified "GetForces()" function, uses that to obtain acceleration values.
    -> Uses a standard 4th Order Runge Kutta integration algorithm.
    -> Not sure if it is working as expected.
    """
    k1y = vel * globals.dt
    k1v = GetForces(force_select, pos, subs_pos, slider_pos, ag_k, subs_k, neigh, latt_const) * globals.dt

    k2y = (vel + 0.5 * k1v) * globals.dt
    k2v = GetForces(force_select, pos + 0.5 * k1y, subs_pos, slider_pos, ag_k, subs_k, neigh, latt_const) * globals.dt

    k3y = (vel + 0.5 * k2v) * globals.dt
    k3v = GetForces(force_select, pos + 0.5 * k2y, subs_pos, slider_pos, ag_k, subs_k, neigh, latt_const) * globals.dt

    k4y = (vel + k3v) * globals.dt
    k4v = GetForces(force_select, pos + k3y, subs_pos, slider_pos, ag_k, subs_k, neigh, latt_const) * globals.dt

    # Update next value of y
    pos = pos + (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0
    vel = vel + (k1v + 2 * k2v + 2 * k3v + k4v) / 6.0

    slider_pos = slider_pos + (slider_vel * globals.dt)

    ## Perform a quick array multiplication to constrain the movement. Takes inputs "x", "y" and "none".
    (vel, acc) = constrain(globals.constrain, vel, acc)

    return (pos, vel, acc), slider_pos


def Integrate(force_select, subs_pos, pos, vel, acc, mass, slider_pos, slider_vel, ag_k, subs_k, neigh, latt_const):
    if (globals.integrator == "ec"):
        return EulerCromer(force_select, subs_pos, pos, vel, acc, mass, slider_pos, slider_vel, ag_k, subs_k, neigh, latt_const)
    elif (globals.integrator == "vv"):
        return VelocityVerlet(force_select, subs_pos, pos, vel, acc, mass, slider_pos, slider_vel, ag_k, subs_k, neigh, latt_const)
    elif (globals.integrator == "rk4"):
        return RK4(force_select, subs_pos, pos, vel, acc, mass, slider_pos, slider_vel, ag_k, subs_k, neigh, latt_const)
