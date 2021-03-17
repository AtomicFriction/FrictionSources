import numpy as np
from numba import jit
from interactions import GetForces
from tools import constrain
import globals
from agent import Agent

"""
Euler-Cromer integration scheme implementation.
Uses the unified GetForces() function for the force/acceleration calculations.
"""
def EulerCromer(force_select, pos, vel, acc, mass):
    ## Updates of the target.
    vel += (acc * globals.dt)
    pos += (vel * globals.dt)
    acc = (GetForces(force_select) / mass)
    ## Updates of the slider, happens regardless of the target choice.
    slider_pos = Agent.slider_pos + (Agent.slider_vel * globals.dt)
    ## Operation to constrain the target, depends on the user input.
    (vel, acc) = constrain(globals.constrain, vel, acc)

    return (pos, vel, acc), slider_pos


"""
Velocity-Verlet integration scheme implementation.
Uses the unified GetForces() function for the force/acceleration calculations.
"""
def VelocityVerlet(force_select, pos, vel, acc, mass):
    ## Updates of the target.
    pos += ((vel * globals.dt) + (0.5 * acc * (globals.dt ** 2)))
    vel += (0.5 * acc * globals.dt)
    acc = (GetForces(force_select) / mass)
    vel += (0.5 * acc * globals.dt)
    ## Updates of the slider, happens regardless of the target choice.
    slider_pos = Agent.slider_pos + (Agent.slider_vel * globals.dt)
    ## Operation to constrain the target, depends on the user input.
    (vel, acc) = constrain(globals.constrain, vel, acc)

    return (pos, vel, acc), slider_pos


"""
4th Order Runge-Kutta integration scheme implementation. Uses the unified GetForces() function for the force/acceleration calculations.
-> Problematic right now. Needs substrate-agent control.
-> I don't want to fix it for a while, before eveything settles down.
"""
def RK4(force_select, ag_pos, subs_pos, slider_pos, slider_vel, neigh, mass, pos, vel, acc):
    ## Preliminary calculations for the updates of the target.
    k1y = vel * globals.dt
    k1v = GetForces(force_select, ag_pos, subs_pos, slider_pos, neigh) * globals.dt

    k2y = (vel + 0.5 * k1v) * globals.dt
    k2v = GetForces(force_select, pos + 0.5 * k1y, subs_pos, slider_pos, neigh) * globals.dt

    k3y = (vel + 0.5 * k2v) * globals.dt
    k3v = GetForces(force_select, pos + 0.5 * k2y, subs_pos, slider_pos, neigh) * globals.dt

    k4y = (vel + k3v) * globals.dt
    k4v = GetForces(force_select, pos + k3y, subs_pos, slider_pos, neigh) * globals.dt

    ## Updates of the target.
    pos = pos + (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0
    vel = vel + (k1v + 2 * k2v + 2 * k3v + k4v) / 6.0

    ## Updates of the slider, happens regardless of the target choice.
    slider_pos = slider_pos + (slider_vel * globals.dt)

    ## Operation to constrain the target, depends on the user input.
    (vel, acc) = constrain(globals.constrain, vel, acc)

    return (pos, vel, acc), slider_pos

## A method to unify all of the integration functions in one. This is needed for later use in the main function.
def Integrate(force_select, pos, vel, acc, mass):
    ##print("Integrator called.")
    if (globals.integrator == "ec"):
        return EulerCromer(force_select, pos, vel, acc, mass)
    elif (globals.integrator == "vv"):
        return VelocityVerlet(force_select, pos, vel, acc, mass)
    elif (globals.integrator == "rk4"):
        return RK4(force_select, ag_pos, subs_pos, slider_pos, slider_vel, neigh, mass, pos, vel, acc)
