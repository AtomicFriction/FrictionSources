from input_parser.input_parser import parse
import numpy as np
from substrate import Subs

##################################################
##################################################
gen_param, _, _, _, _, _ = parse('./input_parser/input.txt')

cutoff = gen_param['cutoff']
##################################################
##################################################
_, prot_param, _, _, _, _ = parse('./input_parser/input.txt')

dt = prot_param['dt']
subs_integ = prot_param['integ'] + '(Subs.F, Subs.R, Subs.V, Subs.A, Subs.mass)'
agent_integ = prot_param['integ'] + '(Agent.F, Agent.R, Agent.V, Agent.A, Agent.mass)'
print(subs_integ)
run = np.array(prot_param['run']).reshape(int(len(prot_param['run'])/3), 3)
##################################################
##################################################
_, _, analysis_param, _, _, _ = parse('./input_parser/input.txt')
data = analysis_param['data']
##################################################
##################################################
_, _, _, subs_param, _, _ = parse('./input_parser/input.txt')

num = subs_param['num']
subs_k = subs_param['k']
latt_const = subs_param['latt_const']
##################################################
##################################################
_, _, _, _, agent_param, _ = parse('./input_parser/input.txt')

constrain = agent_param['constrain']
eq_len = agent_param['eq_len']
agent_k = agent_param['k']
##################################################
##################################################
_, _, _, _, _, thermo_param = parse('./input_parser/input.txt')

thermotype = thermo_param['thermo']
tau = thermo_param['tau']
s, Q = thermo_param['s'], thermo_param['q']
gamma = thermo_param['gamma']
boltz = 8.617333262e-5
##################################################
##################################################
pe_switch = 0
pe = 0
ke_switch = 0
ke = 0
ff_switch = 0
ff = 0
temp_switch = 0
temp = 0
etot_switch = 0
etot = 0


spr_force = np.zeros((1, 3))
lj_force = np.zeros((num * num, 3))
lj_agent = []
L = Subs.num * Subs.latt_const
subs_force_fin = 0

rr = 0
disp = 0
subs_dR = 0

"""
agent_pot = subs_pot = fric = lj_force = np.zeros(np.sum(run[:, 2]))
"""

agent_pot = []
subs_pot = []
