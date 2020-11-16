## Used for array operations.
import numpy as np

## Used for the plots.
import matplotlib.pyplot as plt

## Style library for the plots.
import mplcyberpunk

## Used to obtain the sin and pi functions.
import math

## Used for the random displacement values.
import random

## May be used to artificially slow down the animated plots without changing the other parameters.
import time


time_step = 0.1

number_of_atoms = 50

spring_constant = 10

atomic_mass = 1

lattice_constant = 1

lateral_chain_displacements = [0]

vertical_chain_displacements = [0]

number_of_steps = 200000

damping_coefficent = 0.02

## This loops generates the lateral and vertical displacements for the atoms.
for i in range(1, number_of_atoms - 1):
    lateral_chain_displacements.append(i + 0.05 * math.sin(6 * math.pi * i / (number_of_atoms - 1)))
    vertical_chain_displacements.append(0.2 * math.sin(6 * math.pi * i / (number_of_atoms - 1)))


def ComputeForces(R, k, a):

    force_matrix = np.zeros(np.shape(R))
    ## "N" is needed for the iteration later in the loop.
    N = displacement_matrix.shape[1]

    ## "Rx" holds the lateral displacements here.
    Rx = displacement_matrix[0, :]
    ## "Ry" holds the vertical displacements here.
    Ry = displacement_matrix[1, :]

    for n in range(1, N - 1):

        norm1 = np.linalg.norm(displacement_matrix[:, n + 1] - displacement_matrix[:, n])
        norm2 = np.linalg.norm(displacement_matrix[:, n - 1] - displacement_matrix[:, n])

        force_matrix[0, n] = (k * (norm1 - a) * (Rx[n + 1] - Rx[n]) / norm1) + (k * (norm2 - a) * (Rx[n - 1] - Rx[n]) / norm2)
        force_matrix[1, n] = (k * (norm1 - a) * (Ry[n + 1] - Ry[n]) / norm1) + (k * (norm2 - a) * (Ry[n - 1] - Ry[n]) / norm2)

    return force_matrix


## In order to execute operations on the columns, the matrices have been transposed here.
lateral_displacements_transpose = np.transpose(lateral_chain_displacements)
vertical_displacements_transpose = np.transpose(vertical_chain_displacements)

## Transposed displacement matrices have been concatenated for simpler use.
displacement_matrix = np.concatenate(([lateral_displacements_transpose], [vertical_displacements_transpose]), axis = 0)

velocity_matrix = np.zeros(np.shape(displacement_matrix))

## Turn the "interactive mode" on.
plt.ion()

## Set plot style.
plt.style.use("cyberpunk")

x_axis = displacement_matrix[0, :]
y_axis = displacement_matrix[1, :]

## Initialize the plot.
figure, ax = plt.subplots(figsize = (10, 8))
line1, = ax.plot(x_axis, y_axis)

## Set the axis names.
plt.xlabel("Lateral Displacements",fontsize = 18)
plt.ylabel("Vertical Displacements",fontsize = 18)

## Set the title of the plot.
plt.title("1D Chain Toy Model", fontsize = 25)

## This is the main loop that drives the code.
for i in range(0, number_of_steps + 1):

    if ((i % 10) == 0):
        ## Set the data that will be updated for each axis.
        line1.set_xdata(displacement_matrix[0, :])
        line1.set_ydata(displacement_matrix[1, :])
        ## Draw the data points.
        figure.canvas.draw()
        ## Clear the canvas for the upcoming data points.
        figure.canvas.flush_events()

    ## Compute forces for each instance.
    force_matrix = ComputeForces(displacement_matrix, spring_constant, lattice_constant)

    ## Update atom velocities with the forces.
    velocity_matrix = velocity_matrix + force_matrix - (damping_coefficent * velocity_matrix) * time_step / atomic_mass

    ## Update the displacement matrix with the updated atom velocities.
    displacement_matrix = displacement_matrix + velocity_matrix * time_step

    ## Show the plot.
    plt.show()
