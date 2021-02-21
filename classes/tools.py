import numpy as np
import globals

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
-> Configures the "run" parameter as a (n x 3) array. The rows contain group of instructions.

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
-> Returns zero if there is a "RuntimeWarning: divide by zero encountered in true_divide" issue, which returns NaN.
-> Int and float inputs are fine, like the ordinary "/" operator.

"""
def SafeDivision(x, y):
    res = ( x / y ) if y.any() != 0 else 0
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
Reads the data row in the input file. Outputs it as a list.
For input: ff etot ke pe
Output: ['ff', 'etot', 'ke', 'pe']
"""
def AnalysisList():
    selection_list = (globals.data.split(" "))
    print(selection_list)
    if ("ke" in selection_list):
        globals.kinetic_switch = 1
        print("kin :" + str(globals.kinetic_switch))
    if ("pe" in selection_list):
        globals.potential_switch = 1
        print("pe: " + str(globals.potential_switch))
    if ("ff" in selection_list):
        globals.ff_switch = 1
        print("ff: " + str(globals.ff_switch))
    if ("temp" in selection_list):
        globals.temp_switch = 1
        print("temp: " + str(globals.temp_switch))


def LogFile():
    log = open('log.txt', 'w+')
    log.write()
    log.write()
    log.write()
    log.write()
