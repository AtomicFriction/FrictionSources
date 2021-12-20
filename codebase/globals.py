# Library imports.
import numpy as np


# File imports.
from input_parser.input_parser import parse



# "general" parameters from the input file.
gen_param, _, _, _, _, _ = parse('./input_parser/input.txt') # Parse the parameters.

cutoff = gen_param['cutoff']

# "protocol" parameters from the input file.
_, prot_param, _, _, _, _ = parse('./input_parser/input.txt') # Parse the parameters.

dt = prot_param['dt']
integtype_agent = prot_param['integ_agent']
integtype_subs = prot_param['integ_subs']
run = prot_param['run']
eig_proj = prot_param['eig_proj']
apply_agent = prot_param['apply_agent']
apply_thermo = prot_param['apply_thermo']
apply_damping = prot_param['apply_damping']


# "analysis" parameters from the input file.
_, _, analysis_param, _, _, _ = parse('./input_parser/input.txt') # Parse the parameters.
data = analysis_param['data']


# "substrate" parameters from the input file.
_, _, _, subs_param, _, _ = parse('./input_parser/input.txt') # Parse the parameters.

num = subs_param['num']
subs_k = np.array([subs_param['k1'], subs_param['k2'], subs_param['k3']])
latt_const = subs_param['latt_const']
subs_eta = subs_param['eta']


# "agent" parameters from the input file.
_, _, _, _, agent_param, _ = parse('./input_parser/input.txt') # Parse the parameters.

constrain = agent_param['constrain']
eq_len = agent_param['eq_len']
agent_k = agent_param['k'] #
sigma = (agent_param['sigma']) # The constant sigma for The Lennard Jones interaction.
epsilon = (agent_param['epsilon']) # The constant epsilon for The Lennard Jones interaction.
agent_eta = agent_param['eta']


# "thermo" parameters from the input file.
_, _, _, _, _, thermo_param = parse('./input_parser/input.txt') # Parse the parameters.

thermotype = thermo_param['thermo']
tau = thermo_param['tau']
s, Q = thermo_param['s'], thermo_param['q']
gamma = thermo_param['gamma']
mode = thermo_param['mode']
thickness = thermo_param['thickness']
boltz = 8.617333262e-5

for prot, step in enumerate(run):
    print(prot, step)
# Values for logging.
log_param = {key: 0 for key in data}

eigvec = 0
eigval = 0


# Potential energy calculation variables.
rr_12 = []
rr_6 = []
disp = 0
subs_dR = 0

agent_zcomp = 0


# Agent force calculation variables.
sig_12 = (sigma ** 12)
sig_6 = (sigma ** 6)
spr_force = np.zeros((1, 3))
lj_force = 0
agent_force = 0

"""
agent_pot = subs_pot = fric = lj_force = np.zeros(np.sum(run[:, 2]))
"""

agent_pot = []
subs_pot = []

# Initial substrate position for evctor projection calculations.
initial_Subs_R = 0

# Command line argument switches.
save_progress = False # This argument needs an integer input form the user.
from_progress = False
calc_hessian = False
load_eigs = False
animate = False # This arguement needs an integer input form the user.
save_progress_step = 0
animate_step = 0
pullup = False 
