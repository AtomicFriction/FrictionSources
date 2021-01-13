## Global definitions here.
from input_parser import parse


_, run_param, _, _ = parse('input.txt')
gen_param, _, _, _ = parse('input.txt')


dt = float(run_param['dt'])
integrator = (run_param['integ'])
cutoff = float(gen_param['cutoff'])
