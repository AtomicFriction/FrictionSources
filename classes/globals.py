## Global definitions here.
from input_parser import parse

# General
gen_param, _, _, _, _, _ = parse('input.txt')

cutoff = float(gen_param['cutoff'])

# Protocol
_, prot_param, _, _, _, _ = parse('input.txt')

dt = float(prot_param['dt'])
integrator = (prot_param['integ'])
run = (prot_param['run'])

# Substrate
_, _, _, subs_param, _, _= parse('input.txt')

num = int(subs_param['num'])
subs_k = float(subs_param['k'])
latt_const = float(subs_param['latt_const'])

# Slider
_, _, _, _, slid_param, _ = parse('input.txt')

constrain = str(slid_param['constrain'])
eq_len = float(slid_param['eq_len'])
slid_k = float(slid_param['k'])

# Thermostats

_, _, _, _, _, thermo_param = parse('input.txt')

tau = float(thermo_param['tau'])
s, Q = float(thermo_param['s']), float(thermo_param['q'])
gamma = float(thermo_param['gamma'])
boltz = 8.617333262 * 10**(-5)
