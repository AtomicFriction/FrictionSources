import numpy as np
import globals


"""
-> Constrains the motion to the desired axis by simple matrix multiplications.
Input x: Constrains the motion on the x-axis. Nullifies the components of other axes.
Input y: Constrains the motion on the y-axis. Nullifies the components of other axes.
Input y: Constrains the motion on the z-axis. Nullifies the components of other axes.
Else: Does nothing.
"""
def constrain(direction, vel, acc):
    if (direction == "x"):
        vel *= np.array([1, 0, 0])
        acc *= np.array([1, 0, 0])
        return (vel, acc)

    elif (direction == "y"):
        vel *= np.array([0, 1, 0])
        acc *= np.array([0, 1, 0])
        return (vel, acc)
    elif (direction == "z"):
        vel *= np.array([0, 0, 1])
        acc *= np.array([0, 0, 1])
        return (vel, acc)
    else:
        return (vel, acc)


"""
Euler-Cromer integration scheme implementation.
Uses the unified GetForces() function for the force/acceleration calculations.
JIT compilation makes the function slower.
"""
def EulerCromer(force, pos, vel, acc, mass):
    ## Updates of the target.
    vel += (acc * globals.dt)
    pos += (vel * globals.dt)
    acc = (force / mass)
    ## Operation to constrain the target, depends on the user input.
    #(vel, acc) = constrain(globals.constrain, vel, acc)

    return pos, vel, acc


"""
Velocity-Verlet integration scheme implementation.
Uses the unified GetForces() function for the force/acceleration calculations.
"""
def VelocityVerlet(force, pos, vel, acc, mass):
    ## Updates of the target.
    vel += (0.5 * acc * globals.dt)
    pos += ((vel * globals.dt) + (0.5 * acc * (globals.dt ** 2)))
    acc = (force / mass)
    vel += (0.5 * acc * globals.dt)
    ## Operation to constrain the target, depends on the user input.
    #(vel, acc) = constrain(globals.constrain, vel, acc)

    return pos, vel, acc

'''
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
'''

# Evaluates the proper function depending on the user choice, the dictionary used is at ./input_parser/input_profile.py
Integrate = eval(globals.integtype)
