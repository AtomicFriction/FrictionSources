# Library imports.
import numpy as np

# File imports.
from input_parser.input_parser import parse
import globals

# Get the input parameters from the parser to initialize the agent atom.
_, _, _, _, agent_param, _ = parse('./input_parser/input.txt')

# Define the "Agent" class for the initialization of the system.
class AgentSlider:

    def __init__(self):
        # Mass of the agent.
        self.mass = (agent_param['mass'])
        # Spring constant between slider and agent.
        self.k = (agent_param['k'])
        # Shape of the agent.
        self.shape = agent_param['shape']
        # The position of the slider.
        self.slider_pos = np.array(agent_param["slider_pos"]).reshape(1, 3)
        # The velocity of the slider.
        self.slider_vel = np.array(agent_param["slider_vel"]).reshape(1, 3)
        # The force on the agent.
        self.F = 0

        ## Initialize agent position, velocity and acceleration as (1 x 3) arrays depending on the user selected shape.
        if (self.shape == "single"):
            self.R = np.array(agent_param["agent_pos"]).reshape(1, 3)
            self.V = np.zeros((1, 3))
            self.A = np.zeros((1, 3))

        elif (self.shape == "hemisphere"):
            ## Not in use right now.
            pass

    # Periodicity function for the Agent that prevents it from going outside of the system.
    def AgentPeriodicity(self, box_len):
        if (self.R[0][0] > box_len):
            self.R[0][0] -= box_len
            self.slider_pos[0][0] -= box_len

        if (self.R[0][0] < 0):
            self.R[0][0] += box_len
            self.slider_pos[0][0] += box_len

        if (self.R[0][1] > box_len):
            self.R[0][1] -= box_len
            self.slider_pos[0][1] -= box_len

        if (self.R[0][1] < 0):
            self.R[0][1] += box_len
            self.slider_pos[0][1] += box_len

# Call the class to initialize the Agent. The Agent is initalized when the file is read by the interpreter.
Agent = AgentSlider()
