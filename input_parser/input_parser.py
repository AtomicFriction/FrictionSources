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

    # raise error in case of the conditions below
    try:
        dim = int(subs['dim'])
        layers = int(subs['layers'])
        fix_layers = int(subs['fix_layers'])
    except:
        print("\n***\nEither number of dimensions or layers is not an integer.", \
        "\nPlease enter integer numbers for dimension and layer numbers.\n***\n")
    else:
        try:
            prot['run'] = list(map(int, prot['run'].split()))
            anal['data'] = list(map(str, anal['data'].split()))
            slid['agent_pos'] = list(map(float, slid['agent_pos'].split()))
            slid['slider_pos'] = list(map(float, slid['slider_pos'].split()))
            slid['slider_vel'] = list(map(float, slid['slider_vel'].split()))
        except:
            print("\n***\nPlease check if data consists of strings,", \
            "and if run, agent_pos, slider_pos, and slider_vel consist of integers and floats.\n***\n")

        if not (dim >= 1 and dim <= 3):
            print("\n***\nUnexpected dimension.", \
            "\nPlease confirm that the dimension is an integer from one to three.\n***\n")
        elif (dim == 1 or dim == 2) and ((layers != 1) or (fix_layers != 0)):
            subs['layers'] = 1
            subs['fix_layers'] = 0
        elif dim == 3:
            subs['bound_cond'] = 'periodic'

    return gen, prot, anal, subs, slid, thermo
