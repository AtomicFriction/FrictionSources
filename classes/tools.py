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
        conf_arr.append([float(globals.run.split(" ")[(3 * i) + 1]), float(globals.run.split(" ")[(3 * i) + 2]), float(globals.run.split(" ")[(3 * i) + 3])])

    conf_arr = np.array(conf_arr)

    return conf_arr


"""
Returns zero if there is a "RuntimeWarning: divide by zero encountered in true_divide" issue, which returns NaN.
Int and float inputs are fine, like the ordinary "/" operator.

"""
def SafeDivision(x, y):
    res = ( x / y ) if y.any() != 0 else 0
    return res


"""
Switcher for the output dump. Will be coded with care afterwards, just a structure for now.
For input: ndump, ff, etot, ke, pe
ndump: 1000
data: ndump ff etot ke pe
"""
def AnalysisSwitch(options_list):
    switcher = {
            "ff" in options_list : CalcFF(),
            "etot" in options_list : CalcEtot(),
            "ke" in options_list : CalcKE(),
            "pe" in options_list : CalcPE(),
            "e" in options_list : MethodE()
        }
    for i in range(0, len(options_list)):
        return switcher.get(options_list[i], "Invalid option.")


def AnalysisList():
    options_list = []
    for i in range(int(globals.data[0])):
        options_list.append(globals.data.split(" ")[i + 1])

    return options_list
