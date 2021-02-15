from input_parser import parse
from scipy.spatial import distance
import numpy as np

"""
---------------------------------

For the sake of simulation to run well,
Call find_neighbor first, then init_disp.

---------------------------------
"""
## it's to be modified for periodic conditions.

_, _, _, subs_param, _, _ = parse('input.txt')
class Substrate():
    def __init__(self):
        # define parameters
        self.k = float(subs_param['k'])
        self.dim = int(subs_param['dim'])
        self.num = int(subs_param['num'])
        self.mass = float(subs_param['mass'])
        self.layers = int(subs_param['layers'])
        self.bound_cond = subs_param['bound_cond']
        self.displace_type = subs_param['displace_type']
        self.latt_const = float(subs_param['latt_const'])
        self.cuto_const = float(subs_param['cuto_const'])
        
        # initialize position and trap
        if self.dim == 1:
            zgrid, ygrid, xgrid = np.mgrid[0:self.layers, 0:1, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            if self.bound_cond == 'fixed':
                self.trap = np.where(\
                    (self.R[:, 0] != 0) & (self.R[:, 0] != (self.num-1)*self.latt_const))
                    
            elif self.bound_cond == 'periodic':
                print("Periodic boundary condition is not implented yet.\n")
                quit()

        elif self.dim == 2:
            zgrid, ygrid, xgrid = np.mgrid[0:self.layers, 0:self.num, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            if self.bound_cond == 'fixed':
                self.trap = np.where(\
                    (self.R[:, 0] != 0) & (self.R[:, 0] != (self.num-1) * self.latt_const) & \
                    (self.R[:, 1] != 0) & (self.R[:, 1] != (self.num-1) * self.latt_const))
                    
            elif self.bound_cond == 'periodic':
                print("Periodic boundary condition is not implented yet.\n")
                quit()

        elif self.dim == 3:
            zgrid, ygrid, xgrid = np.mgrid[0:self.layers, 0:self.num, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            if self.bound_cond == 'fixed':
                self.trap = np.where(\
                    (self.R[:, 0] != 0) & (self.R[:, 0] != (self.num-1) * self.latt_const) & \
                    (self.R[:, 1] != 0) & (self.R[:, 1] != (self.num-1) * self.latt_const) & \
                    (self.R[:, 2] != 0) & (self.R[:, 2] != (self.layers-1) * self.latt_const))
            elif self.bound_cond == 'periodic':
                print("Periodic boundary condition is not implented yet.\n")
                quit()

        # initialize velocity and acceleration
        self.V = np.zeros(np.shape(self.R))
        self.A = np.zeros(np.shape(self.R))
        
    def find_neighbor(self):
        if self.bound_cond == 'fixed':
            dist = distance.cdist(self.R, self.R, 'euclidean')
            cutoff = (dist != 0) & (dist < self.cuto_const) * 1
            extract = np.where(cutoff == 1)
            idx = np.unique(extract[0], return_index=True)
            self.N = np.array(np.split(extract[1], idx[1])[1:])
                
        elif self.bound_cond == 'periodic': 
            print('Neighbor table is not implemented for periodic boundary condition yet.\n')
            quit()

    def init_disp(self):
        if self.displace_type == 'random':
            if self.dim == 1:
                if self.bound_cond == 'fixed':
                    self.R[self.trap, 0:2] += (np.random.rand(*np.shape(self.R[self.trap, 0:2])) - 0.5) * 0.1

                elif self.bound_cond == 'periodic':
                    self.R[:, 0:2] += (np.random.rand(*np.shape(self.R[:, 0:2])) - 0.5) * 0.1

            elif self.dim != 1:
                if self.bound_cond == 'fixed':
                    self.R[self.trap] += (np.random.rand(*np.shape(self.R[self.trap])) - 0.5) * 0.1

                elif self.bound_cond == 'periodic':
                    self.R += (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            
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
                if choice == "":
                    self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
                elif choice == "quit":
                    return
                else:
                    print('You either made an invalid request or the property you requested must be written differently.\n')
                    choice = input("If you want to continue with the feault displacement 'random', press enter.\nIf not, write 'quit'.")
        else:
            print('You either made an invalid request or the property you requested must be written differently.\n')
            choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
            if choice == "":
                self.R = self.R + (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            elif choice == "quit":
                return
            else:
                print('You either made an invalid request or the property you requested must be written differently.\n')
                choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
