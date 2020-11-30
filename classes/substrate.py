from input_parser import parse
import numpy as np

"""
makes use of the function parse to
get parameters for specified block
then, creates classes for the blocks
with their own parameters
"""
# where to put try catch? here or into parser?

subs_parm = parse('input.txt', '&substrate')
class Substrate():
    def __init__(self):
        # parameters
        self.num_row = int(subs_parm['num_row'])
        self.latt_const = float(subs_parm['latt_const'])
        self.displace_type = subs_parm['displace_type']
        self.k = float(subs_parm['k'])
        self.mass = float(subs_parm['mass'])

        # atomic system
        Ry, Rx = np.mgrid[0:self.num_row, 0:self.num_row]
        Rx_points = np.vstack(Rx.ravel())
        Ry_points = np.vstack(Ry.ravel())
        self.R = np.hstack((Rx_points, Ry_points))
        self.R = np.column_stack((self.R, np.zeros(np.shape(self.R)[0]))) 
        # could be good to implement reshape(R, (num_row, num_row, 3))
        self.neighbortable = np.zeros(np.shape(self.R))

    def find_neighbor(self):
        """
        there may be a way to vectorize this function, such as:
            (i) row or column-wise operations on R with identity matrix
            (ii) usage of advanced matrix methods (to be searched)
        """
        for atom in enumerate(self.R):
            for neighbor in enumerate(self.R):
                # structure of atom and neighbor variables:
                # atom = (306, array([6., 6., 0.]))
                # atom[0] = 306
                # atom[1] = array([6, 6, 0])
                norm = np.linalg.norm(neighbor[1] - atom[1])
                if norm <= self.latt_const: # <== probably won't work except for initial condition
                    if atom[0] == neighbor[0]:
                        pass
                    else:
                        self.neighbortable[atom[0]] = self.R[neighbor[0]]