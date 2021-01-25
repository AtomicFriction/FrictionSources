## Global definitions here.
from input_parser import parse


gen_param, _, _, _ = parse('input.txt')

cutoff = float(gen_param['cutoff'])
##################################################
##################################################
_, run_param, _, _ = parse('input.txt')

dt = float(run_param['dt'])
integrator = (run_param['integ'])
##################################################
##################################################
_, _, subs_param, _ = parse('input.txt')

num = int(subs_param['num'])
##################################################
##################################################
_, _, _, agent_param = parse('input.txt')

constrain = str(agent_param['constrain'])
##################################################
##################################################
