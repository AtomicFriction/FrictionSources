import numpy as np
import globals
import matplotlib.pyplot as plt
from matplotlib import cm
from substrate import Subs
from mpl_toolkits.mplot3d import Axes3D

eigvec_all = np.load('eigtest_eigvec.npy')
eigval_all = np.load('eigtest_eigval.npy')


def eigtest(eigvec):

    eigvec_pl = eigvec[:, 0] ## 0, 1, 4, 5, 6, 7, 11, 15

    reshaped_eigvec = np.reshape(eigvec_pl, (Subs.bound.shape[0], 3))

    R_disp = []

    fig = plt.figure(figsize=(15,7))
    ax = fig.add_subplot(111, projection = "3d")
    for a in np.arange(-10, 10, 0.5):

        ax.set(zlim = (-0.3e1, 0.3e1))
        ax.set(xlim = (0, 20))
        ax.set(ylim = (0, 20))


        plt.ion()
        R_disp = Subs.R[Subs.bound] + ((reshaped_eigvec * a))

        ax.plot_trisurf(R_disp[:,0].real, R_disp[:,1].real, R_disp[:,2].real, cmap=cm.inferno)

        ax.scatter(R_disp[:,0], R_disp[:,1], R_disp[:,2], color = "red")

        plt.pause(0.05)

        plt.show()

        plt.cla()

eigtest(eigvec_all)
