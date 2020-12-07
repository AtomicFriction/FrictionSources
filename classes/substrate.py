from input_parser import parse
import numpy as np

"""
Makes use of the parser to get
parameter for substrate class
then, creates the substrate class
"""
# where to put try catch? here or into parser?

subs_param, _ = parse('input.txt')
class Substrate():
    def __init__(self):
        # parameters
        self.num = int(subs_param['num'])
        self.k = float(subs_param['subs_k'])
        self.mass = float(subs_param['subs_m'])
        self.z_layers = int(subs_param['z_layers'])
        self.displace_type = subs_param['displace_type']
        self.latt_const = float(subs_param['latt_const'])
        
        # atomic system
        Ry, Rx = np.mgrid[0:self.num, 0:self.num]
        Rx_points = np.vstack(Rx.ravel())
        Ry_points = np.vstack(Ry.ravel())
        self.R = np.hstack((Rx_points, Ry_points))
        self.R = np.column_stack((self.R, np.zeros(np.shape(self.R)[0]))) # add z-layer
        self.neighbortable = np.zeros((self.num**2, 4), dtype=int)

    def find_neighbor(self):
        for atom, _ in enumerate(self.R):
            self.neighbortable[atom] = [atom-self.num, atom-1, atom+1, atom+self.num]
    
    def displace(self):
        if self.displace_type == 'random':
            self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1

        elif self.displace_type == 'sinusoidal':
            print('This property is not implemented yet.\n')
            default = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
            if default == "":
                self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            elif default == "quit":
                return
            else:
                print('You either made an invalid request or the property you requested must be written differently.\n')
                default = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")

        else:
            print('You either made an invalid request or the property you requested must be written differently.\n')
            default = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
            if default == "":
                self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            elif default == "quit":
                return
            else:
                print('You either made an invalid request or the property you requested must be written differently.\n')
                default = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
