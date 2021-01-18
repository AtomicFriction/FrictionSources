import numpy as np
import matplotlib.pyplot as plt

from agent import agent
from substrate import Substrate
from integrators import Integrate


subs = Substrate()
#####


time = []
ag_x = []

for t in range(1000):
    (Agent.pos, Agent.vel, Agent.acc) = Integrate("AGENT", subs.R, Agent.pos, Agent.vel, Agent.acc, Agent.m, Agent.slider_pos, Agent.k)

    ##print(agent_pos)
    time.append(t)
    ag_x.append(agent.pos[0][0])


plt.plot(time, ag_x)
plt.show()
