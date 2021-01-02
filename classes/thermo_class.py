import numpy as np

T = 300
boltz = 8.617333262 * 10**(-5)

def vel_scale(T_inst, mass, V, num_atom):
    num_bound = 4 * (num_atom - 1)
    T_inst =  mass * np.sum(V**2) / (3 * boltz * num_bound)
    L = (T / T_inst)**(1/2)
    return L

def berendsen(T_inst, dt):
    tau = 0.1
    L = (1 + dt / tau * (T/T_inst - 1))*(1/2)
    return L

def nosehoover(mass, R):
    s = None
    Q = None
    print("\n\nThis thermostat is not implementable yet.\n \
            If you want to proceed with another thermostat, \
            restart the program with another thermostat.\n\n")
    return quit()

def langevin(mass, V, F, f):
    gamma = None
    print("\n\nThis thermostat is not implementable yet.\n \
            If you want to proceed with another thermostat, \
            restart the program with another thermostat.\n\n")
    return quit()
