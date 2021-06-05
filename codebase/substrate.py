from input_parser.input_parser import parse
from scipy.spatial import distance, cKDTree
import numpy as np
import globals
import warnings

"""
---------------------------------
For the sake of simulation to run well,
Call find_neighbor first, then init_disp.
---------------------------------
"""

_, _, _, subs_param, _, _ = parse('./input_parser/input.txt')
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
        self.fix_layers = int(subs_param['fix_layers'])
        self.L = self.num * self.latt_const

        # initialize position and set the boundary condition
        if self.dim == 1:
            zgrid, ygrid, xgrid = np.mgrid[0:self.layers, 0:1, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            if self.bound_cond == 'fixed':
                self.bound = np.where(\
                    (self.R[:, 0] != 0) & (self.R[:, 0] != (self.num-1)*self.latt_const))[0]
            elif self.bound_cond == 'periodic':
                self.bound = np.arange(self.R.shape[0])

        elif self.dim == 2:
            zgrid, ygrid, xgrid = np.mgrid[0:self.layers, 0:self.num, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            if self.bound_cond == 'fixed':
                self.bound = np.where(\
                    (self.R[:, 0] != 0) & (self.R[:, 0] != (self.num-1) * self.latt_const) & \
                    (self.R[:, 1] != 0) & (self.R[:, 1] != (self.num-1) * self.latt_const))[0]
            elif self.bound_cond == 'periodic':
                self.bound = np.arange(self.R.shape[0])

        elif self.dim == 3:
            zgrid, ygrid, xgrid = np.mgrid[0:self.layers, 0:self.num, 0:self.num] * self.latt_const
            Rx, Ry, Rz = np.vstack(xgrid.ravel()), np.vstack(ygrid.ravel()), np.vstack(zgrid.ravel())
            self.R = np.hstack((Rx, Ry, Rz))

            self.bound = np.where(np.isin(self.R[:, 2], np.arange(self.fix_layers)*self.latt_const) == False)[0]
            self.numlayer = int(self.R.shape[0] / self.layers)

        # initialize velocity and acceleration
        self.V = np.zeros(self.R.shape)
        self.V[self.bound] = np.random.normal(0, np.sqrt(globals.boltz*globals.run[0, 0]/self.mass), size=self.V[self.bound].shape)
        self.A = np.zeros(np.shape(self.R))

        # set the frame and the trap for thermostat
        if globals.mode == 'full':
            self.trap = np.arange(self.R.shape[0])
            self.trap = np.array([])

        elif globals.mode == 'partial':
            if self.dim == 2:
                self.frame = np.where(\
                    (self.R[:, 0] - globals.thickness < 0) | \
                    (self.R[:, 1] - globals.thickness < 0) | \
                    (self.R[:, 0] + globals.thickness > self.L - self.latt_const) | \
                    (self.R[:, 1] + globals.thickness > self.L - self.latt_const))[0]

                self.trap = np.setdiff1d(np.arange(self.R.shape[0]), self.frame) 
                
            elif self.dim == 3: # add trap
                self.trap = np.arange(self.numlayer * self.fix_layers, self.numlayer * (self.fix_layers + globals.thickness))

    def neighbor_def(self):
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
        self.N_def = np.array(np.split(extract[1], idx[1])[1:])
        if self.dim == 3:
            N = np.zeros((self.N.size, self.N[0].size))
            N[:-self.numlayer] = np.array(list(self.N_def[:-self.numlayer]))
            N[-self.numlayer:, :self.N_def[-1].size] = np.array(list(self.N_def[-self.numlayer:]))
            N[-self.numlayer:, -1] = np.arange(self.R.shape[0]-self.numlayer, self.R.shape[0])
            self.N_def = N.astype(np.int32, copy=False)
        print(self.N_def)

    def neighbor_tree(self):
        # Box size might be increased to prevent atoms to exceed the box if the function is to be called for multiple times.

        if self.bound_cond == 'fixed':
            trie = cKDTree(self.R, boxsize=None)
            self.N = np.vstack(trie.query_ball_point(self.R, self.latt_const)[self.bound])

        elif self.bound_cond == 'periodic':
            trie = cKDTree(self.R, boxsize=[self.L, self.L, self.L])

            if self.dim != 3:
                self.N = np.vstack(trie.query_ball_point(self.R, self.latt_const))

            if self.dim == 3:
                '''Queries the tree to construct neighbor table for 3D system
                Removes the fixed layer from the table
                Counts the last layer atoms as neighbors to themselves for all the arrays to have compatible sizes
                '''

                N_list = trie.query_ball_point(self.R, self.latt_const)
                upplayer = np.array(list(N_list[-self.numlayer:]))
                self_neigh = self.bound[-self.numlayer:]
                N_upper = np.hstack((upplayer, self_neigh[:, np.newaxis]))
                N_lower = np.array(list(N_list[self.fix_layers*self.numlayer:-self.numlayer]))
                self.N = np.vstack((N_lower, N_upper))

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
#Subs.neighbor_def()
Subs.neighbor_tree()
globals.initial_Subs_R = Subs.R
#Subs.init_disp()
