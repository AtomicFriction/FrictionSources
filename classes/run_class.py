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
    (agent.pos, agent.vel, agent.acc) = Integrate("AGENT", subs.R, agent.pos, agent.vel, agent.acc, agent.m, agent.slider_pos, agent.k)

    ##print(agent_pos)
    time.append(t)
    ag_x.append(agent.pos[0][0])


plt.plot(time, ag_x)
plt.show()
