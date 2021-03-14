## Global definitions here.
from input_parser import parse
import numpy as np
from substrate import Subs

##################################################
##################################################
gen_param, _, _, _, _, _ = parse('input.txt')

cutoff = gen_param['cutoff']
##################################################
##################################################
_, prot_param, _, _, _, _ = parse('input.txt')

dt = prot_param['dt']
integrator = prot_param['integ']
run = np.array(prot_param['run']).reshape(len(prot_param['run'])/3, 3)
##################################################
##################################################
_, _, analysis_param, _, _, _ = parse('input.txt')
data = analysis_param['data']
##################################################
##################################################
_, _, _, subs_param, _, _ = parse('input.txt')

num = subs_param['num']
subs_k = subs_param['k']
latt_const = subs_param['latt_const']
##################################################
##################################################
_, _, _, _, agent_param, _ = parse('input.txt')

constrain = agent_param['constrain']
eq_len = agent_param['eq_len']
agent_k = agent_param['k']
##################################################
##################################################
_, _, _, _, _, thermo_param = parse('input.txt')

thermo = thermo_param['thermo']
tau = thermo_param['tau']
s, Q = thermo_param['s'], thermo_param['q']
gamma = thermo_param['gamma']
boltz = 8.617333262e-5
##################################################
##################################################
potential_switch = 0
kinetic_switch = 0
ff_switch = 0
temp_switch = 0
etot_switch = 0
spr_force = np.zeros((1, 3))
lj_force = np.zeros((num * num, 3))
lj_agent = []
L = Subs.num * Subs.latt_const
subs_force_fin = 0

rr = 0
disp = 0
subs_dR = 0
T_inst = 0

"""
agent_pot = subs_pot = fric = lj_force = np.zeros(np.sum(run[:, 2]))
"""

agent_pot = []
subs_pot = []
