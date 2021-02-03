## Global definitions here.
from input_parser import parse


gen_param, _, _, _ = parse('input.txt')

cutoff = float(gen_param['cutoff'])
##################################################
##################################################
_, run_param, _, _ = parse('input.txt')

dt = float(run_param['dt'])
integrator = (run_param['integ'])
run = (run_param['run'])
##################################################
##################################################
_, _, subs_param, _ = parse('input.txt')

num = int(subs_param['num'])
subs_k = float(subs_param['k'])
latt_const = float(subs_param['latt_const'])
##################################################
##################################################
_, _, _, agent_param = parse('input.txt')

constrain = str(agent_param['constrain'])
eq_len = float(agent_param['eq_len'])
agent_k = float(agent_param['k'])
##################################################
##################################################

boltz = 8.617333262 * 10**(-5)
