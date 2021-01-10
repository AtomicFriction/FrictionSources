import numpy as np
from input_parser import parse

"""
Uses the input data given by the user to initialize a sliding agent.
"""

_ , agent_param, _ = parse('input.txt') ## Use the parser either here of inside the Run class.

## Agent class.
class Agent:

    def __init__(self):
        ## Mass of the agent.
        self.m = float(agent_param['mass'])
        ## Spring constant between slider and agent.
        self.k = float(agent_param['k'])
        ## The constant sigma for The Lennard Jones interaction.
        self.sigma = float(agent_param['sigma'])
        ## The constant epsilon for The Lennard Jones interaction.
        self.epsilon = float(agent_param['epsilon'])
        ## Shape of the agent.
        self.shape = agent_param['shape']


        ## Do we need inputs from the user for the slider?
        self.slider_pos = [[float(agent_param["slider_pos"].split(" ")[0]), float(agent_param["slider_pos"].split(" ")[1]), float(agent_param["slider_pos"].split(" ")[2])]]

        self.slider_vel = [[float(agent_param["slider_vel"].split(" ")[0]), float(agent_param["slider_vel"].split(" ")[1]), float(agent_param["slider_vel"].split(" ")[2])]]

        ## Initialize agent position, velocity and acceleration as (1 x 3) arrays depending on the user selected shape.
        if (self.shape == "single"):
            ## There is an error here. Probably related to the parser.
            ## Do we need velocity and acceleration inputs from the user?
            self.pos = [[float(agent_param["agent_pos"].split(" ")[0]), float(agent_param["agent_pos"].split(" ")[1]), float(agent_param["agent_pos"].split(" ")[2])]]

            self.vel = [[float(agent_param["agent_vel"].split(" ")[0]), float(agent_param["agent_vel"].split(" ")[1]), float(agent_param["agent_vel"].split(" ")[2])]]

            self.acc = [[float(agent_param["agent_acc"].split(" ")[0]), float(agent_param["agent_acc"].split(" ")[1]), float(agent_param["agent_acc"].split(" ")[2])]]


        elif (self.shape == "hemisphere"):
            ## Not in use right now.
            pass