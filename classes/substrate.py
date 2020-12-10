from input_parser import parse
import numpy as np

"""
Makes use of the parser to get
parameter for substrate class
then, creates the substrate class
"""
# put try catch into parser

subs_param, _ , _ = parse('input.txt')
class Substrate():
    def __init__(self):
        # parameters
        self.dim = int(subs_param['dim'])
        self.num = int(subs_param['num'])
        self.k = float(subs_param['k'])
        self.mass = float(subs_param['mass'])
        self.bound_cond = subs_param['bound_cond']
        self.layers = int(subs_param['layers'])
        self.displace_type = subs_param['displace_type']
        self.latt_const = float(subs_param['latt_const'])
        
        if self.dim == 1:
            self.R = np.arange(self.num)

        elif self.dim == 2:
            Ry, Rx = np.mgrid[0:self.num, 0:self.num]
            Rx_points = np.vstack(Rx.ravel())
            Ry_points = np.vstack(Ry.ravel())
            self.R = np.hstack((Rx_points, Ry_points))
            self.R = np.column_stack((self.R, np.zeros(np.shape(self.R)[0]))) # add z-layer

        elif self.dim == 3:
            Ry, Rx = np.mgrid[0:self.num, 0:self.num]
            Rx_points = np.vstack(Rx.ravel())
            Ry_points = np.vstack(Ry.ravel())
            self.R = np.hstack((Rx_points, Ry_points))
            self.R = np.expand_dims(self.R, axis=0)
            self.R = np.repeat(self.R, self.layers, axis=0)
            Rz = [[z] for z in list(range(self.layers))] # you can vectorize!
            self.R = np.insert(self.R, 2, Rz, axis=2)

    def find_neighbor(self): # to be updated for distance-wise computation
        if self.dim == 1: # CHECK
            if self.bound_cond == 'fixed':
                R_min = self.R[0:len(self.R)-1]
                R_plus = self.R[1:len(self.R)]
                self.neighbortable = np.hstack((np.vstack(R_min), np.vstack(R_plus)))

            elif self.bound_cond == 'periodic': # replace np.tile with np.pad
                R_min = np.tile(self.R, 2)[len(self.R)-1:2*len(self.R)-1]
                R_plus = np.tile(self.R, 2)[1:len(self.R)+1]
                self.neighbortable = np.hstack((np.vstack(R_min), np.vstack(R_plus))) # naming convention for neighbortable (??)

        elif self.dim == 2:
            if self.bound_cond == 'fixed':
                print("\n---------\nProgram is not applicable for fixed boundary conditions yet.\n")
                print("Please change the condition to 'periodic' and restart the program with periodic condition.\n---------")
                return

            elif self.bound_cond == 'periodic':
                Nx = np.vstack(np.pad(np.arange(len(self.R)), (1, 1), 'constant', constant_values=(self.num-1, len(self.R)-self.num)))
                Ny = np.vstack(np.pad(np.arange(len(self.R)), (self.num, self.num), 'wrap')) # unpacked array of neighbor indices
                self.neighbortable = np.hstack((Ny[:-2*(self.num)], Nx[:-2], Nx[2:], Ny[2*(self.num):]))
                

        elif self.dim == 3: # add boundary check
            print("\n---------\nProgram is not applicable for 3-dimensional atomic systems yet.\n")
            print("Please change the dimension and restart the program to either 1D or 2D.\n---------")
            return

    def get_disp(self): # it should be working for all dimensions
        if self.displace_type == 'random':
            self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1

        elif self.displace_type == 'sinusoidal':
            print('Sinusoidal displacement is not implemented yet.\n')
            choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
            if choice == "":
                self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            elif choice == "quit":
                return
            else:
                print('You either made an invalid request or the property you requested must be written differently.\n')
                choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")

        else:
            print('You either made an invalid request or the property you requested must be written differently.\n')
            choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
            if choice == "":
                self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            elif choice == "quit":
                return
            else:
                print('You either made an invalid request or the property you requested must be written differently.\n')
                choice = input("If you want to continue with the feault displacement 'random', press enter.\nIf not, write 'quit'.")
