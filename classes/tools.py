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
