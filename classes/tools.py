import numpy as np
import globals


"""
Constrains the motion to the desired axis by simple matrix multiplications.

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
Configures the "run" parameter as a (n x 3) array. The rows contain group of instructions.

For input n x y z k l m :
    n = the number of groups of three
    configured_array (output) = [[x, y, z],
                                [k, l, m]]
    x, k = Starting temperatures.
    y, l = Target temperatures.
    z, m = Number of steps to reach the target temperature.

"""
def RunConf():
    conf_arr = []
    for i in range(int(globals.run[0])):
        conf_arr.append([int(globals.run.split(" ")[(3 * i) + 1]), int(globals.run.split(" ")[(3 * i) + 2]), int(globals.run.split(" ")[(3 * i) + 3])])

    conf_arr = np.array(conf_arr)

    return conf_arr


"""
Returns zero if there is a "RuntimeWarning: divide by zero encountered in true_divide" issue, which returns NaN.
Int and float inputs are fine, like the ordinary "/" operator.

"""
def SafeDivision(x, y):
    res = ( x / y ) if y != 0 else 0
    return res


"""
Switcher for the output dump. Will be coded with care afterwards, just a structure for now.
"""
def AnalysisSwitch(options):
    switcher = {
            Ndump : 0,
            Ff : 0,
            Etot : 0,
            KE : 0,
            PE : 0
        }
    return switcher.get(options, "Invalid option.")
