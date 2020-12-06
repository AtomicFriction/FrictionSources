import numpy as np
from input_parser import parse

""""
Uses the input data given by the user to initialize a sliding agent.
""""

## Agent is the parent class.
class Agent:
    ## Use the parser for the input values.
    _ , agent_params = parse('input.txt')
    ## Spring constant between slider and agent.
    k = agent_params['k']
    ## Mass of the agent.
    m = agent_params['mass']
    ## Shape of the agent.
    shape = agent_params['shape']
    ## The constant sigma for The Lennard Jones interaction.
    sigma = agent_params['sigma']
    ## The constant epsilon for The Lennard Jones interaction.
    epsilon = agent_params['epsilon']


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
        ## Position of the single atom from the user.
        pos_single = [float(agent_params["agent_pos"].split(" ")[0]), float(agent_params["agent_pos"].split(" ")[1]), float(agent_params["agent_pos"].split(" ")[2])]

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
            ## Raise an error and use a predefined default shape for the agent.
            print("An invalid shape was specified in the input. Default shape 'single' will be used.")
            Single_Shape()
        return agent_disp


## Slider is initialized as a child class of the parent class Agent.
class Slider(Agent):

    def __init__(self):

        self.velocity = slider_velocity

        pass
