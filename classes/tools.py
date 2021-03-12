import numpy as np
import globals
from agent import Agent
from substrate import Subs

"""
-> Constrains the motion to the desired axis by simple matrix multiplications.
Input x: Constrains the motion on the x-axis. Nullifies the components of other axes.
Input y: Constrains the motion on the y-axis. Nullifies the components of other axes.
Else: Does nothing.
"""
def constrain(direction, vel, acc):
    if (direction == "x"):
        vel = vel * np.array([1, 0, 0])
        acc = acc * np.array([1, 0, 0])
        return (vel, acc)

    elif (direction == "y"):
        vel = vel * np.array([0, 1, 0])
        acc = acc * np.array([0, 1, 0])
        return (vel, acc)

    else:
        return (vel, acc)


"""
-> Returns zero if there is a "RuntimeWarning: divide by zero encountered in true_divide" issue, which returns NaN.
-> Int and float inputs are fine, like the ordinary "/" operator.
"""
def SafeDivision(x, y):
    res = ( x / y ) if y != 0 else 1
    return res


"""
-> Numerical differentiation carried out by the central difference method.
For inputs: f = the function to be differentiated.
            a = the point we want to find the differentiation for.
            h = step size (must be virtually zero because of the definition of this method).
Output: The value of f'(a).
"""
def NumericalDiff(f, a, h):
    return (f(a + h) - f(a - h)) / (2 * h)


"""
-> Returns "None" if (globals.kinetic_switch == 0).
"""
def KE():
    if (globals.kinetic_switch == 1):
        subs_kin = (Subs.mass * np.sum(Subs.V ** 2)) / 2
        agent_kin = (Agent.mass * np.sum(Agent.vel ** 2)) / 2
        return subs_kin + agent_kin

"""
-> Returns "None" if (globals.potential_switch == 0).
"""
def PE():
    if (globals.potential_switch == 1):
        rr_12 = (globals.rr ** 12)
        rr_6 = (globals.rr ** 6)
        sig_12 = (Agent.sigma ** 12)
        sig_6 = (Agent.sigma ** 6)
        lj_pot = np.sum((4 * Agent.epsilon) * ((sig_12 / rr_12) - (sig_6 / rr_6)))
        spr_pot = ((globals.agent_k * (globals.disp ** 2)) / 2)
        return lj_pot + spr_pot


"""
-> Projection of the spring force vector on the slider velocity vector calculated for the friction force.
-> Returns "None" if (globals.ff_switch == 0).
"""
def Friction():
    if (globals.ff_switch == 1):
        slid_vel_norm = np.sqrt(sum(Agent.slider_vel[0] ** 2))
        ff = (np.dot(globals.spr_force[0], Agent.slider_vel[0]) / slid_vel_norm ** 2) * Agent.slider_vel[0]
        return ff
