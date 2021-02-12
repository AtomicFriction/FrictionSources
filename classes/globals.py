## Global definitions here.
from input_parser import parse


gen_param, _, _, _, _, _ = parse('input.txt')

cutoff = float(gen_param['cutoff'])
##################################################
##################################################
_, prot_param, _, _, _, _ = parse('input.txt')

dt = float(prot_param['dt'])
integrator = (prot_param['integ'])
run = (prot_param['run'])
##################################################
##################################################
_, _, analysis_param, _, _, _ = parse('input.txt')
data = (analysis_param['data'])
##################################################
##################################################
_, _, _, subs_param, _, _ = parse('input.txt')

num = int(subs_param['num'])
subs_k = float(subs_param['k'])
latt_const = float(subs_param['latt_const'])
##################################################
##################################################
_, _, _, _, agent_param, _ = parse('input.txt')

constrain = str(agent_param['constrain'])
eq_len = [float(agent_param['eq_len']), 0, 0]
agent_k = float(agent_param['k'])
##################################################
##################################################
_, _, _, _, _, thermo_param = parse('input.txt')
tau = float(thermo_param['tau'])
thermo = str(thermo_param['thermo'])

##################################################
##################################################
boltz = 8.617333262 * 10**(-5)
