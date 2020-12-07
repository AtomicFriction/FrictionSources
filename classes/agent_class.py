import numpy as np
from input_parser import parse

""""
Uses the input data given by the user to initialize a sliding agent.
""""


## _ , agent_params = parse('input.txt') ## Does not belong here. Kept for testing purposes.


## Agent is the parent class.
class Agent:

    def __init__(self):
        ## Mass of the agent.
        self.m = agent_params['mass']
        ## Spring constant between slider and agent.
        self.k = agent_params['k']
        self.hooking_point = hooking_point_slider_agent
        ## The constant sigma for The Lennard Jones interaction.
        self.sigma = agent_params['sigma']
        ## The constant epsilon for The Lennard Jones interaction.
        self.epsilon = agent_params['epsilon']
        ## Shape of the agent.
        self.shape = agent_params['shape']


    def LJ_Interaction(disp, sigma, epsilon):

        ## Matrix that contains the forces due to the Lennard Jones interaction.
        lj_force = np.zeros(np.shape(R))
        ## "N" is needed for the iteration later in the loop.
        N = disp.shape[1]
        ## "Rx" holds the x-axis displacements here.
        Rx = disp[0, :]
        ## "Ry" holds the y-axis displacements here.
        Ry = disp[1, :]
        ## "Ry" holds the z-axis displacements here.
        Rz = disp[2, :]

        ## Loop that computes the Lennard Jones interaction forces.
        for n in range(1, N - 1):

            norm1 = np.linalg.norm(disp[:, n + 1] - disp[:, n])
            norm2 = np.linalg.norm(disp[:, n - 1] - disp[:, n])

            lj_force[0, n] = (((48 / (Rx[n + 1] - Rx[n])) * ((1 / ((Rx[n + 1] - Rx[n]) ** 6)) ** 2) - ((1 / ((Rx[n + 1] - Rx[n]) ** 6)) / 2)) * (Rx[n + 1] - Rx[n]) / norm1) + (((48 / (Rx[n - 1] - Rx[n])) * ((1 / ((Rx[n - 1] - Rx[n]) ** 6)) ** 2) - ((1 / ((Rx[n - 1] - Rx[n]) ** 6)) / 2)) * (Rx[n - 1] - Rx[n]) / norm2)
            lj_force[1, n] = (((48 / (Ry[n + 1] - Ry[n])) * ((1 / ((Ry[n + 1] - Ry[n]) ** 6)) ** 2) - ((1 / ((Ry[n + 1] - Ry[n]) ** 6)) / 2)) * (Ry[n + 1] - Ry[n]) / norm1) + (((48 / (Ry[n - 1] - Ry[n])) * ((1 / ((Ry[n - 1] - Ry[n]) ** 6)) ** 2) - ((1 / ((Ry[n - 1] - Ry[n]) ** 6)) / 2)) * (Ry[n - 1] - Ry[n]) / norm2)
            lj_force[2, n] = (((48 / (Rz[n + 1] - Rz[n])) * ((1 / ((Rz[n + 1] - Rz[n]) ** 6)) ** 2) - ((1 / ((Rz[n + 1] - Rz[n]) ** 6)) / 2)) * (Rz[n + 1] - Rz[n]) / norm1) + (((48 / (Rz[n - 1] - Rz[n])) * ((1 / ((Rz[n - 1] - Rz[n]) ** 6)) ** 2) - ((1 / ((Rz[n - 1] - Rz[n]) ** 6)) / 2)) * (Rz[n - 1] - Rz[n]) / norm2)


        return lj_force


    def SingleAtom():
        ## Position of the single atom from the user.
        pos_single = [float(agent_params["agent_pos"].split(" ")[0]), float(agent_params["agent_pos"].split(" ")[1]), float(agent_params["agent_pos"].split(" ")[2])]

        return single_disp


    def Hemisphere():
        ## Hemisphere shape will not be used for now.
        pass


    def Shape_Select(shape):
        if (shape == "single"):
            SingleAtom()
        ## Hemisphere shape will not be used for now.
        elif (shape == "hemisphere"):
            ##Hemisphere_Shape()
            print("Hemisphere shape is not available right now. Default shape 'single' will be used.")
            SingleAtom()
        else:
            ## Raise an error and use a predefined default shape for the agent.
            print("An invalid shape was specified in the input. Default shape 'single' will be used.")
            SingleAtom()
        return agent_disp


## Slider is initialized as a child class of the parent class Agent.
class Slider(Agent):

    def __init__(self):

        self.velocity = slider_velocity

        pass
