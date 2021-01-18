def parse(file):
    with open(file, 'r') as f:
        params = [param.split(' = ') for param in f.read().lower().splitlines()]

    gen_ind, agent_ind = params.index(['&general']), params.index(['&slider'])
    run_ind, subs_ind = params.index(['&run']),  params.index(['&substrate'])

    gen = dict(params[gen_ind+1:params.index(['/'], gen_ind)])
    run = dict(params[run_ind+1:params.index(['/'], run_ind)])
    subs = dict(params[subs_ind+1:params.index(['/'], subs_ind)])
    agent = dict(params[agent_ind+1:params.index(['/'], agent_ind)])

    # raise error in conditions below
    try:
        dim = int(subs['dim'])
        layers = int(subs['layers'])
    except:
        print("\n***\nEither number of dimensions or layers is not an integer.", \
        "\nPlease enter integer numbers for dimension and layer numbers.\n***\n")
    else:
        if (dim == 1 or dim == 2) and (layers != 1):
            print("\n***\nDimension and layer numbers are not matched.\nRecall that number", \
            "of layers must be equal to one where the system is one or two-dimensional.\n***\n")

    return gen, run, subs, agent
