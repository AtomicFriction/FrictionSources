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
    except:
        print("\n***\nEither number of dimensions or layers is not an integer.", \
        "\nPlease enter integer numbers for dimension and layer numbers.\n***\n")
    else:
        if not (dim >= 1 and dim <= 3):
            print("\n***\nUnexpected dimension.", \
            "\nPlease confirm that the dimension is an integer from one to three.\n***\n")
        elif (dim == 1 or dim == 2) and (layers != 1):
            print("\n***\nDimension and layer numbers are not matched.\nRecall that number", \
            "of layers must be equal to one where the system is one or two-dimensional.\n***\n")

    return gen, prot, anal, subs, slid, thermo
