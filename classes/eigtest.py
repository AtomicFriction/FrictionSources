import numpy as np
import globals
import matplotlib.pyplot as plt
from substrate import Subs

#plt.style.use('ggplot')

eigvec_all = np.loadtxt('eigtest.txt')
print(np.shape(eigvec_all))

eigvec = eigvec_all[:, 0]

reshaped_eigvec = np.reshape(eigvec, (globals.num * globals.num, 3))
print(np.shape(reshaped_eigvec))


R_disp = []
t = []

fig = plt.figure(figsize=(15,7))
ax = fig.add_subplot(111)

for a in np.arange(-10, 10, 1):
    plt.ion()
    R_disp = (Subs.R + (reshaped_eigvec * a))

    ax.plot(R_disp[:,0], color = "blue", label = "0")
    ax.plot(R_disp[:,1], color = "red", label = "1")
    ax.plot(R_disp[:,2], color = "cyan", label = "2")
    plt.pause(0.5)

    plt.show()

    plt.cla()
