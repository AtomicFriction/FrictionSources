import numpy as np
from input_parser.input_parser import parse
import globals
from numba import njit


"""
Uses the input data given by the user to initial size an agent and a slider.
"""

_, _, _, _, agent_param, _ = parse('./input_parser/input.txt')
## Agent class.
class AgentSlider:

    def __init__(self):
        ## Mass of the agent.
        self.mass = (agent_param['mass'])
        ## Spring constant between slider and agent.
        self.k = (agent_param['k'])
        ## Shape of the agent.
        self.shape = agent_param['shape']
        ## The position of the slider.
        self.slider_pos = np.array(agent_param["slider_pos"]).reshape(1, 3)
        ## The velocity of the slider.
        self.slider_vel = np.array(agent_param["slider_vel"]).reshape(1, 3)
        self.F = 0

        ## Initialize agent position, velocity and acceleration as (1 x 3) arrays depending on the user selected shape.
        if (self.shape == "single"):
            self.pos = np.array(agent_param["agent_pos"]).reshape(1, 3)
            self.vel = np.zeros((1, 3))
            self.acc = np.zeros((1, 3))

        elif (self.shape == "hemisphere"):
            ## Not in use right now.
            pass


    def AgentPeriodicity(self, box_len):
        if (self.pos[0][0] > box_len):
            self.pos[0][0] -= box_len
            self.slider_pos[0][0] -= box_len

        if (self.pos[0][0] < 0):
            self.pos[0][0] += box_len
            self.slider_pos[0][0] += box_len

        if (self.pos[0][1] > box_len):
            self.pos[0][1] -= box_len
            self.slider_pos[0][1] -= box_len

        if (self.pos[0][1] < 0):
            self.pos[0][1] += box_len
            self.slider_pos[0][1] += box_len

Agent = AgentSlider()
