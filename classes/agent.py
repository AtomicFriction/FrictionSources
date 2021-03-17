import numpy as np
from input_parser import parse
import globals


"""
Uses the input data given by the user to initialize an agent and a slider.
"""

_, _, _, _, agent_param, _ = parse('input.txt')

## Agent class.
class AgentSlider:

    def __init__(self):
        ## Mass of the agent.
        self.mass = (agent_param['mass'])
        ## Spring constant between slider and agent.
        self.k = (agent_param['k'])
        ## The constant sigma for The Lennard Jones interaction.
        self.sigma = (agent_param['sigma'])
        ## The constant epsilon for The Lennard Jones interaction.
        self.epsilon = (agent_param['epsilon'])
        ## Shape of the agent.
        self.shape = agent_param['shape']
        ## The position of the slider.
        self.slider_pos = np.array(agent_param["slider_pos"]).reshape(1, 3)
        ## The velocity of the slider.
        self.slider_vel = np.array(agent_param["slider_vel"]).reshape(1, 3)

        ## Initialize agent position, velocity and acceleration as (1 x 3) arrays depending on the user selected shape.
        if (self.shape == "single"):
            self.pos = np.array(agent_param["agent_pos"]).reshape(1, 3)
            self.vel = np.zeros((1, 3))
            self.acc = np.zeros((1, 3))

        elif (self.shape == "hemisphere"):
            ## Not in use right now.
            pass


def AgentPeriodicity(agent_pos, slider_pos):
    if (agent_pos[0][0] > globals.L):
        agent_pos[0][0] = agent_pos[0][0] - globals.L
        slider_pos[0][0] = slider_pos[0][0] - globals.L

    if (agent_pos[0][0] < 0):
        agent_pos[0][0] = agent_pos[0][0] + globals.L
        slider_pos[0][0] = slider_pos[0][0] + globals.L

    if (agent_pos[0][1] > globals.L):
        agent_pos[0][1] = agent_pos[0][1] - globals.L
        slider_pos[0][1] = slider_pos[0][1] - globals.L

    if (agent_pos[0][1] < 0):
        agent_pos[0][1] = agent_pos[0][1] + globals.L
        slider_pos[0][1] = slider_pos[0][1] + globals.L

    return agent_pos, slider_pos


Agent = AgentSlider()
