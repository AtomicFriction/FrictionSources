import numpy as np
import globals
import matplotlib.pyplot as plt
from matplotlib import cm
from substrate import Subs
from mpl_toolkits.mplot3d import Axes3D


eigvec_all = np.load('eigtest.npy')

eigvec = eigvec_all[:, 240]

reshaped_eigvec = np.reshape(eigvec, (globals.num * globals.num, 3))

R_disp = []

fig = plt.figure(figsize=(15,7))
ax = fig.add_subplot(111, projection = "3d")
for a in np.arange(-10, 10, 1):

    ax.set(zlim = (-0.5e1, 0.5e1))
    ax.set(xlim = (0, 20))
    ax.set(ylim = (0, 20))


    plt.ion()
    R_disp = Subs.R + ((reshaped_eigvec * a))

    ax.plot_trisurf(R_disp[:,0].real, R_disp[:,1].real, R_disp[:,2].real, cmap=cm.inferno)

    #ax.scatter(R_disp[:,0], R_disp[:,1], R_disp[:,2], color = "red")

    plt.pause(0.2)

    plt.show()

    plt.cla()
