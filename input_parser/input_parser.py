from input_parser.dtypes import typeof
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

    for key, val in gen.items():
        try: gen[key] = typeof[key](val)
        except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()
    for key, val in prot.items():
        if key != 'run':
            try: prot[key] = typeof[key](val)
            except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()
        elif key == 'run':
            try:
                prot[key] = list(map(float, prot[key].split())); prot[key][2::3] = map(int, prot[key][2::3])
                prot[key] = np.array(prot[key]).reshape(int(len(prot[key])/3), 3)
            except ValueError: print('The input run must consist of types (float, float, int), respectively.'); exit()
    for key, val in anal.items():
        if key != 'data':
            try: anal[key] = typeof[key](val)
            except ValueError: print('The input {} must be of type {}'.format(key, typeof[key])); exit()
        elif key == 'data':
            try: anal[key] = list(map(str, anal[key].split()))
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

    dim = subs['dim']
    if not dim >= 1 and dim <= 3: exit('Unexpected dimension')
    elif dim == 1 or dim == 2:
        subs['layers'] = 1
        subs['fix_layers'] = 0
    elif dim == 3 and subs['bound_cond'] == 'fixed':
        subs['bound_cond'] = 'periodic'

    return gen, prot, anal, subs, slid, thermo
