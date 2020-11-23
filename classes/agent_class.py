import numpy as np
import random

## Just a dummy function for now. This will be replaced by the input parser.
def ReadFile(file_name):

    f = open(filename, "r")

    necessary_inputs = f.readline()

    return necessary_inputs



## Agent is the parent class.
class Agent:

    agent_velocity = random.random()
    spring_constant_between_slider_and_agent = 10
    hooking_point_slider_agent = 0
    ## Zero is placed as a placeholder for the type of the sliding entity that will be read from the input file.
    sliding_entity_select = 0




    def __init__(self):
        self.velocity = agent_velocity
        self.spring_constant = spring_constant_between_slider_and_agent
        self.hooking_point = hooking_point_slider_agent
        self.sliding_entity = sliding_entity_select


    def LJ_Interaction(displacement_matrix):

        lj_interaction_matrix = np.zeros(np.shape(R))
        ## "N" is needed for the iteration later in the loop.
        N = displacement_matrix.shape[1]
        ## "Rx" holds the lateral displacements here.
        Rx = displacement_matrix[0, :]
        ## "Ry" holds the vertical displacements here.
        Ry = displacement_matrix[1, :]

        Rz = displacement_matrix[2, :]

        for n in range(1, N - 1):

            norm1 = np.linalg.norm(displacement_matrix[:, n + 1] - displacement_matrix[:, n])
            norm2 = np.linalg.norm(displacement_matrix[:, n - 1] - displacement_matrix[:, n])

            lj_interaction_matrix[0, n] = (((48 / (Rx[n + 1] - Rx[n])) * ((1 / ((Rx[n + 1] - Rx[n]) ** 6)) ** 2) - ((1 / ((Rx[n + 1] - Rx[n]) ** 6)) / 2)) * (Rx[n + 1] - Rx[n]) / norm1) + (((48 / (Rx[n - 1] - Rx[n])) * ((1 / ((Rx[n - 1] - Rx[n]) ** 6)) ** 2) - ((1 / ((Rx[n - 1] - Rx[n]) ** 6)) / 2)) * (Rx[n - 1] - Rx[n]) / norm2)
            lj_interaction_matrix[1, n] = (((48 / (Ry[n + 1] - Ry[n])) * ((1 / ((Ry[n + 1] - Ry[n]) ** 6)) ** 2) - ((1 / ((Ry[n + 1] - Ry[n]) ** 6)) / 2)) * (Ry[n + 1] - Ry[n]) / norm1) + (((48 / (Ry[n - 1] - Ry[n])) * ((1 / ((Ry[n - 1] - Ry[n]) ** 6)) ** 2) - ((1 / ((Ry[n - 1] - Ry[n]) ** 6)) / 2)) * (Ry[n - 1] - Ry[n]) / norm2)
            lj_interaction_matrix[2, n] = (((48 / (Rz[n + 1] - Rz[n])) * ((1 / ((Rz[n + 1] - Rz[n]) ** 6)) ** 2) - ((1 / ((Rz[n + 1] - Rz[n]) ** 6)) / 2)) * (Rz[n + 1] - Rz[n]) / norm1) + (((48 / (Rz[n - 1] - Rz[n])) * ((1 / ((Rz[n - 1] - Rz[n]) ** 6)) ** 2) - ((1 / ((Rz[n - 1] - Rz[n]) ** 6)) / 2)) * (Rz[n - 1] - Rz[n]) / norm2)

        return lj_interaction_matrix


## Slider is initialized as a child class of the parent class Agent.
class Slider(Agent):

    def __init__(self):

        pass
