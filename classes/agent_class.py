import numpy as np
import random

slider_param = parse('input.txt', '&slider')

""""
Class description goes here.

""""

## Agent is the parent class.
class Agent:

    ## Spring constant between slider and agent.
    k = slider_param['k']
    ## Mass of the agent.
    m = slider_param['mass']
    ## Shape of the agent.
    shape = slider_param['shape']
    ## The constant sigma for The Lennard Jones interaction.
    sigma = slider_param['sigma']
    ## The constant epsilon for The Lennard Jones interaction.
    epsilon = slider_param['epsilon']
    ## Initial position of the agent. Input is taken as a list for now.
    init_pos = [int(slider_param["agent_initial_x"]), int(slider_param["agent_initial_x"]), int(slider_param["agent_initial_x"])]


    def __init__(self):
        self.mass = m
        self.spring_constant = k
        self.hooking_point = hooking_point_slider_agent
        self.sigma = sigma
        self.epsilon = epsilon
        self.agent = Make_Agent(shape)


    def LJ_Interaction(displacement_matrix, sigma, epsilon):

        ## Matrix that contains the forces due to the Lennard Jones interaction.
        lj_interaction_matrix = np.zeros(np.shape(R))
        ## "N" is needed for the iteration later in the loop.
        N = displacement_matrix.shape[1]
        ## "Rx" holds the x-axis displacements here.
        Rx = displacement_matrix[0, :]
        ## "Ry" holds the y-axis displacements here.
        Ry = displacement_matrix[1, :]
        ## "Ry" holds the z-axis displacements here.
        Rz = displacement_matrix[2, :]

        ## Loop that computes the Lennard Jones interaction forces.
        for n in range(1, N - 1):

            norm1 = np.linalg.norm(displacement_matrix[:, n + 1] - displacement_matrix[:, n])
            norm2 = np.linalg.norm(displacement_matrix[:, n - 1] - displacement_matrix[:, n])

            lj_interaction_matrix[0, n] = (((48 / (Rx[n + 1] - Rx[n])) * ((1 / ((Rx[n + 1] - Rx[n]) ** 6)) ** 2) - ((1 / ((Rx[n + 1] - Rx[n]) ** 6)) / 2)) * (Rx[n + 1] - Rx[n]) / norm1) + (((48 / (Rx[n - 1] - Rx[n])) * ((1 / ((Rx[n - 1] - Rx[n]) ** 6)) ** 2) - ((1 / ((Rx[n - 1] - Rx[n]) ** 6)) / 2)) * (Rx[n - 1] - Rx[n]) / norm2)
            lj_interaction_matrix[1, n] = (((48 / (Ry[n + 1] - Ry[n])) * ((1 / ((Ry[n + 1] - Ry[n]) ** 6)) ** 2) - ((1 / ((Ry[n + 1] - Ry[n]) ** 6)) / 2)) * (Ry[n + 1] - Ry[n]) / norm1) + (((48 / (Ry[n - 1] - Ry[n])) * ((1 / ((Ry[n - 1] - Ry[n]) ** 6)) ** 2) - ((1 / ((Ry[n - 1] - Ry[n]) ** 6)) / 2)) * (Ry[n - 1] - Ry[n]) / norm2)
            lj_interaction_matrix[2, n] = (((48 / (Rz[n + 1] - Rz[n])) * ((1 / ((Rz[n + 1] - Rz[n]) ** 6)) ** 2) - ((1 / ((Rz[n + 1] - Rz[n]) ** 6)) / 2)) * (Rz[n + 1] - Rz[n]) / norm1) + (((48 / (Rz[n - 1] - Rz[n])) * ((1 / ((Rz[n - 1] - Rz[n]) ** 6)) ** 2) - ((1 / ((Rz[n - 1] - Rz[n]) ** 6)) / 2)) * (Rz[n - 1] - Rz[n]) / norm2)


        return lj_interaction_matrix


    def Single_Shape():
        single_disp = [init_pos[0], init_pos[1], init_pos[2]]

        return single_disp


    def Hemisphere_Shape():
        ## Hemisphere shape will not be used for now.
        pass


    def Shape_Select(shape):
        if (shape == "single"):
            Single_Shape()

        ## Hemisphere shape will not be used for now.
        elif (shape == "hemisphere"):
            ##Hemisphere_Shape()
            print("Hemisphere shape is not available right now. Default shape 'single' will be used.")
            Single_Shape()

        else:
            print("An invalid shape was specified in the input. Default shape 'single' will be used.")
            Single_Shape()


        return agent_disp


## Slider is initialized as a child class of the parent class Agent.
class Slider(Agent):

    def __init__(self):

        self.velocity = slider_velocity

        pass
