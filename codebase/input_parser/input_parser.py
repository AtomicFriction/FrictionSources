from input_parser.input_profile import *
import numpy as np

def parse(file):
    with open(file, 'r') as f:
        params = [param.split(' = ') for param in f.read().lower().splitlines()]

    gen_ind, prot_ind = params.index(['&general']), params.index(['&protocol'])
    anal_ind, subs_ind = params.index(['&analysis']), params.index(['&substrate'])
    slid_ind, thermo_ind = params.index(['&slider']), params.index(['&thermostat'])

    gen = dict(params[gen_ind+1:params.index(['/'], gen_ind)])
    prot = dict(params[prot_ind+1:params.index(['/'], prot_ind)])
    anal = dict(params[anal_ind+1:params.index(['/'], anal_ind)])
    subs = dict(params[subs_ind+1:params.index(['/'], subs_ind)])
    slid = dict(params[slid_ind+1:params.index(['/'], slid_ind)])
    thermo = dict(params[thermo_ind+1:params.index(['/'], thermo_ind)])

    ### VALUE ERROR MUST BE TYPE ERROR

    for key, val in gen.items():
        try: gen[key] = typeof[key](val)
        except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()

    for key, val in prot.items():
        if key != 'run' and key != 'integ_agent' and key != 'integ_subs' and key != 'apply_agent' and key != 'apply_thermo' and key != 'apply_damping' and key != 'eig_proj':
            try: prot[key] = typeof[key](val)
            except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()
        elif key == 'run':
            try:
                prot[key] = list(map(float, prot[key].split())); prot[key][2::3] = map(int, prot[key][2::3])
                prot[key] = np.array(prot[key]).reshape(int(len(prot[key])/3), 3)
            except ValueError: print('The input run must consist of types (float, float, int), respectively.'); exit()
        elif key == 'integ_agent':
            for integrator in list(integtype_agent.keys()):
                if val in integrator:
                    try: prot[key] = integtype_agent.get(integrator)
                    except: print('Undefined integrator') # error type is to be specified
        elif key == 'integ_subs':
            for integrator in list(integtype_subs.keys()):
                if val in integrator:
                    try: prot[key] = integtype_subs.get(integrator)
                    except: print('Undefined integrator') # error type is to be specified
        elif key == 'apply_agent':
            try:
                prot[key] = list(map(int, prot[key].split()))
            except: print('Agent application combination must consist of "0" and "1" values.')
        elif key == 'apply_thermo':
            try:
                prot[key] = list(map(int, prot[key].split()))
            except: print('Thermostat application combination must consist of integer.')
        elif key == 'apply_damping':
            try:
                prot[key] = list(map(int, prot[key].split()))
            except: print('Damping application combination must consist of "0" and "1" values.')
        elif key == 'eig_proj':
            try:
                prot[key] = list(map(int, prot[key].split()))
            except: print('Eigenvector projection selection combination error.')


    for key, val in anal.items():
        if key != 'data':
            try: anal[key] = typeof[key](val)
            except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()
        elif key == 'data':
            try:
                if 'ff' in anal[key]: anal[key] = anal[key].replace('ff', 'ff_x ff_y ff_z')
                anal[key] = list(map(str, anal[key].split()))
            except ValueError: print('The input {} must consist of type {}'.format(key, typeof[key])); exit()
 
    for key, val in subs.items():
        try: subs[key] = typeof[key](val)
        except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()

    for key, val in slid.items():
        if key != 'agent_pos' and key != 'slider_pos' and key != 'slider_vel':
            try: slid[key] = typeof[key](val)
            except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()
        elif key == 'agent_pos' or key == 'slider_pos' or key == 'slider_vel':
            try: slid[key] = np.array(list(map(float, slid[key].split())))
            except ValueError: print('The input {} must consist of type {}'.format(key, typeof[key])); exit()

    for key, val in thermo.items():
        try: thermo[key] = typeof[key](val)
        except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()
        else:
            if key == 'thermo':
                for thermostat in list(thermotype.keys()):
                    if val in thermostat:
                        try: thermo[key] = thermotype.get(thermostat)
                        except: print('Undefined thermostat') # error type is to be specified

    dim = subs['dim']
    free_layers = subs['layers'] - subs['fix_layers']

    if not dim >= 1 and dim <= 3: raise ValueError('Unexpected dimension')

    elif dim == 1 or dim == 2: subs['layers'] = 1; subs['fix_layers'] = 0

    elif free_layers < 1: raise ValueError('The input "layers" must be greater than "fix_layers"')

    elif dim == 3 and free_layers != 1: subs['bound_cond'] = 'periodic'

    if thermo['mode'] == 'partial' and not thermo['thickness'] > 0:
        raise ValueError('Thickness must be a positive integer')

    return gen, prot, anal, subs, slid, thermo
