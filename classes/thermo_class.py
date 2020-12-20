import numpy as np

class Thermo:
    def __init__(self):
        self.T = 300
        self.boltz = 8.617333262 * 10**(-5)

    def vel_scale(self, T_inst, mass, V, num_atom):
        num_bound = 4 * (num_atom - 1)
        T_inst =  mass * np.sum(V**2) / (3 * self.boltz * num_bound)
        L = (self.T / T_inst)**(1/2)
        return L

    def berendsen(self, T_inst, dt):
        self.tau = 0.1
        L = (1 + dt / self.tau * (self.T/T_inst - 1))*(1/2)
        return L

    def nosehoover(self, mass, R):
        self.s = None
        self.Q = None
        print("\n\nThis thermostat is not implementable yet.\n \
                If you want to proceed with another thermostat, \
                restart the program with another thermostat.\n\n")
        return quit()

    def langevin(self, mass, V, F, f):
        self.gamma = None
        print("\n\nThis thermostat is not implementable yet.\n \
                If you want to proceed with another thermostat, \
                restart the program with another thermostat.\n\n")
        return quit()
