from input_parser.input_parser import parse
from scipy.spatial import distance
from globals import run, boltz
import numpy as np
from dist import calc_dist
import timeit

"""
---------------------------------

For the sake of simulation to run well,
Call find_neighbor first, then init_disp.

---------------------------------
"""

_, _, _, subs_param, _, thermo_param = parse('./input_parser/input.txt')
class Substrate():
    def __init__(self):
        # define parameters
        self.k = subs_param['k']
        self.dim = subs_param['dim']
        self.num = subs_param['num']
        self.mass = subs_param['mass']
        layers = subs_param['layers']
        self.bound_cond = subs_param['bound_cond']
        self.displace_type = subs_param['displace_type']
        self.latt_const = subs_param['latt_const']
        self.cuto_const = subs_param['cuto_const']
        fix_layers = subs_param['fix_layers']
        self.L = self.num * self.latt_const
        mode = thermo_param['mode']
        thickness = thermo_param['thickness']
        
        # initialize position and set the boundary condition
        if self.dim == 1:
            zgrid, ygrid, xgrid = np.mgrid[0:layers, 0:1, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            if self.bound_cond == 'fixed':
                self.bound = np.where(\
                    (self.R[:, 0] != 0) & (self.R[:, 0] != (self.num-1)*self.latt_const))[0]
            elif self.bound_cond == 'periodic':
                self.bound = np.arange(self.R.shape[0])

        elif self.dim == 2:
            zgrid, ygrid, xgrid = np.mgrid[0:layers, 0:self.num, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            if self.bound_cond == 'fixed':
                self.bound = np.where(\
                    (self.R[:, 0] != 0) & (self.R[:, 0] != (self.num-1) * self.latt_const) & \
                    (self.R[:, 1] != 0) & (self.R[:, 1] != (self.num-1) * self.latt_const))[0]
            elif self.bound_cond == 'periodic':
                self.bound = np.arange(self.R.shape[0])

        elif self.dim == 3:
            zgrid, ygrid, xgrid = np.mgrid[0:layers, 0:self.num, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            self.bound = np.where(np.isin(self.R[:, 2], np.arange(fix_layers)*self.latt_const) == False)[0]
            self.numlayer = int(self.R.shape[0] / layers)

        # initialize velocity and acceleration
        self.V = np.random.normal(0, np.sqrt(boltz*run[0, 0]/self.mass), self.R.shape)
        self.V = np.sqrt(self.mass/(2*np.pi*boltz*run[0, 0])) * np.exp(-self.mass*self.V**2/(2*boltz*run[0, 0]))
        self.A = np.zeros(np.shape(self.R))

        # set the trap for thermostat
        if mode == 'full':
            self.trap = np.arange(self.R.shape[0])

        elif mode == 'partial': # unify dimensions if you can
            if self.dim == 2:
                self.trap = np.where((self.R-thickness >= 0).all(axis=1) & \
                    (self.R+thickness <= (self.num-1)*self.latt_const).all(axis=1))
                    
            elif self.dim == 3:
                self.trap = np.arange(self.numlayer * fix_layers, self.numlayer * (fix_layers + thickness))
        
    def find_neighbor(self):
        if self.bound_cond == 'fixed':
            dR = distance.cdist(self.R, self.R, 'euclidean')
            
        elif self.bound_cond == 'periodic':
            X = self.R[:, 0][np.newaxis]
            Y = self.R[:, 1][np.newaxis]
            Z = self.R[:, 2][np.newaxis]
            dX, dY, dZ = X - X.T, Y - Y.T, Z - Z.T
            Xbound, Ybound, Zbound = (abs(dX) > self.L/2), (abs(dY) > self.L/2), (abs(dZ) > self.L/2)
            Xcopy, Ycopy, Zcopy = dX * Xbound, dY * Ybound, dZ * Zbound
            dX += (-np.sign(Xcopy)) * self.L
            dY += (-np.sign(Ycopy)) * self.L
            dZ += (-np.sign(Zcopy)) * self.L
            dR = np.sqrt(dX**2 + dY**2 + dZ**2)

        cutoff = (dR[self.bound] != 0) & (dR[self.bound] < self.cuto_const)
        extract = np.where(cutoff == True)
        idx = np.unique(extract[0], return_index=True)
        self.N = np.array(np.split(extract[1], idx[1])[1:], dtype=object)
        if self.dim == 3:
            N = np.zeros((self.N.size, self.N[0].size))
            N[:-self.numlayer] = np.array(list(self.N[:-self.numlayer]))
            N[-self.numlayer:, :self.N[-1].size] = np.array(list(self.N[-self.numlayer:]))
            N[-self.numlayer:, -1] = np.arange(self.R.shape[0]-self.numlayer, self.R.shape[0])
            self.N = N.astype(np.int32, copy=False)
            
    def init_disp(self):
        if self.displace_type == 'random':
            if self.dim == 1:
                self.R[self.bound, 0:2] += (np.random.rand(*np.shape(self.R[self.bound, 0:2])) - 0.5) * 0.1

            elif self.dim != 1:
                self.R[self.bound] += (np.random.rand(*np.shape(self.R[self.bound])) - 0.5) * 0.1
            
        elif self.displace_type == 'sinusoidal':
            print('Sinusoidal displacement is not implemented yet.\n')
            choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
            if choice == "":
                self.R += (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            elif choice == "quit":
                return
            else:
                print('You either made an invalid request or the property you requested must be written differently.\n')
                choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
                if choice == "":
                    self.R += (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
                elif choice == "quit":
                    return
                else:
                    print('You either made an invalid request or the property you requested must be written differently.\n')
                    choice = input("If you want to continue with the feault displacement 'random', press enter.\nIf not, write 'quit'.")
        else:
            print('You either made an invalid request or the property you requested must be written differently.\n')
            choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")
            if choice == "":
                self.R += (np.random.rand(*np.shape(self.R)) - 0.5) * 0.1
            elif choice == "quit":
                return
            else:
                print('You either made an invalid request or the property you requested must be written differently.\n')
                choice = input("If you want to continue with the default displacement 'random', press enter.\nIf not, write 'quit'.")

Subs = Substrate()
Subs.find_neighbor()
#Subs.init_disp()
