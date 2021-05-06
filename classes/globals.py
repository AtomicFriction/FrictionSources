from input_parser.input_parser import parse
import numpy as np


# "general" parameters from the input file.
gen_param, _, _, _, _, _ = parse('./input_parser/input.txt') # Parse the parameters.

cutoff = gen_param['cutoff']


# "protocol" parameters from the input file.
_, prot_param, _, _, _, _ = parse('./input_parser/input.txt') # Parse the parameters.

dt = prot_param['dt']
integtype = prot_param['integ']
run = prot_param['run']
eig_proj = prot_param['eig_proj']
apply_agent = prot_param['apply_agent']


# "analysis" parameters from the input file.
_, _, analysis_param, _, _, _ = parse('./input_parser/input.txt') # Parse the parameters.
data = analysis_param['data']


# "substrate" parameters from the input file.
_, _, _, subs_param, _, _ = parse('./input_parser/input.txt') # Parse the parameters.

num = subs_param['num']
subs_k = subs_param['k']
latt_const = subs_param['latt_const']


# "agent" parameters from the input file.
_, _, _, _, agent_param, _ = parse('./input_parser/input.txt') # Parse the parameters.

constrain = agent_param['constrain']
eq_len = agent_param['eq_len']
agent_k = agent_param['k'] #
sigma = (agent_param['sigma']) # The constant sigma for The Lennard Jones interaction.
epsilon = (agent_param['epsilon']) # The constant epsilon for The Lennard Jones interaction.


# "thermo" parameters from the input file.
_, _, _, _, _, thermo_param = parse('./input_parser/input.txt') # Parse the parameters.

thermotype = thermo_param['thermo']
tau = thermo_param['tau']
s, Q = thermo_param['s'], thermo_param['q']
gamma = thermo_param['gamma'],
mode = thermo_param['mode']
thickness = thermo_param['thickness']
boltz = 8.617333262e-5


# Switches for logging.
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
vec_proj = 0


# Potential energy calculation variables.
rr_12 = []
rr_6 = []
disp = 0
subs_dR = 0


# Agent force calculation variables.
sig_12 = (sigma ** 12)
sig_6 = (sigma ** 6)
spr_force = np.zeros((1, 3))
lj_force = np.zeros((num * num, 3))

"""
agent_pot = subs_pot = fric = lj_force = np.zeros(np.sum(run[:, 2]))
"""

agent_pot = []
subs_pot = []

# Initial substrate position for evctor projection calculations.
initial_Subs_R = 0

# Command line arguement switches.
save_progress = 0
from_progress = False
save_hess_eig = False
animate = 0
