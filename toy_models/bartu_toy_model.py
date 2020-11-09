## Used for array operations.
import numpy as np

## Used for the plots.
import matplotlib.pyplot as plt

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

lateral_chain_positions = [0]

vertical_chain_positions = [0]

number_of_steps = 2000

## A variable to hold the user choice for displacements.
displacement_choice = input("Choose displacement parameter, rand or sin?")


## User can choose between random and sinusoidal displacements.
if (displacement_choice == "rand"):
    for i in range(1, number_of_atoms - 1):
        lateral_chain_positions.append(i + (((random.randint(1, 48) - 0.5) * 0.1)))
        vertical_chain_positions.append((((random.randint(1, 48) - 0.5) * 0.1)))

elif (displacement_choice == "sin"):
    for i in range(1, number_of_atoms - 1):
        lateral_chain_positions.append(i + 0.05 * math.sin(6 * math.pi * (i) / (number_of_atoms - 1)))
        vertical_chain_positions.append(0.2 * math.sin(6 * math.pi * i / (number_of_atoms - 1)))

else:
    print("Invalid displacement parameter.")


def GetForces(R, k, a):

    forces_matrix = np.zeros(np.shape(R))
    N = R.shape[1]

    Rx = R[0, :]
    Ry = R[1, :]



    for n in range(1, N - 1):

        norm1 = np.linalg.norm(R[:, n + 1] - R[:, n])

        norm2 = np.linalg.norm(R[:, n - 1] - R[:, n])

        forces_matrix[0, n] = k * (norm1 - a) * (Rx[n + 1] - Rx[n]) / norm1 + k * (norm2 - a) * (Rx[n - 1] - Rx[n]) / norm2
        forces_matrix[1, n] = k * (norm1 - a) * (Ry[n + 1] - Ry[n]) / norm1 + k * (norm2 - a) * (Ry[n - 1] - Ry[n]) / norm2

    return forces_matrix


## In order to execute operations on the columns, the matrices have been transposed here.
Rx_transpose = np.transpose(lateral_chain_positions)
Ry_transpose = np.transpose(vertical_chain_positions)

## Transposed displacement matrices have been concatenated for simpler use.
R = np.concatenate(([Rx_transpose], [Ry_transpose]), axis = 0)

atom_velocity = np.zeros(np.shape(R))

## Turn the "interactive mode" on.
plt.ion()

x_axis = R[0, :]
y_axis = R[1, :]

## Initialize the plot.
figure, ax = plt.subplots(figsize = (10, 8))
line1, = ax.plot(x_axis, y_axis)

## Set the axis names.
plt.xlabel("Lateral Displacements",fontsize = 18)
plt.ylabel("Vertical Displacements",fontsize = 18)

## Set the title of the plot.
plt.title("1D Chain Toy Model", fontsize=25)

## This is the main loop that drives the code.
for i in range(0, number_of_steps + 1):

    if ((i % 10) == 0):
        ## Set the data that will be updated for each axis.
        line1.set_xdata(R[0, :])
        line1.set_ydata(R[1, :])
        ## Draw the data points.
        figure.canvas.draw()
        ## Clear the canvas for the upcoming data points.
        figure.canvas.flush_events()


    ## Compute forces for each instance.
    force = GetForces(R, spring_constant, lattice_constant)

    ## Update atom velocities with the forces.
    atom_velocity = atom_velocity + force * time_step / atomic_mass

    ## Update the displacement matrix with the updated atom velocities.
    R = R + atom_velocity * time_step


    ## Show the plot.
    plt.show()
