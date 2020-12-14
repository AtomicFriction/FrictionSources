"""
PARSING
*******
takes file as a parameter with quotes
then, reads file and parses it in a manner that:
- all the characters are lowered by lower()
- all the lines are splitted into a list by splitlines()
- all the items of the list are also splitted into lists by
        split(' = ') if they have ' = ' sign in them 
--------------------------------------------------
DICTIONARY
*******
defines two dictionaries, sub_params and slider_params,
by indexing from related block names till end sign '/'
--------------------------------------------------
(!) block order is 'not' of importance in the input file
(!) however, it is vital to call parser in the order:
            substrate - agent - numba 
(see paragraph below for detailed explanation)
--------------------------------------------------
CALLING
*******
when creating a class, parser should be called with a placeholder
so that only related parameters are assigned. examples as follows:
        subs_param, _ , _ = parse('input.txt')
        _ , agent_param, _ = parse('input.txt')
"""

def parse(file):
    with open(file, 'r') as f:
        params = [param.split(' = ') for param in f.read().lower().splitlines()]
        # add error catcher
    subs_ind, slid_ind, numba_ind = params.index(['&substrate']), params.index(['&slider']), params.index(['&numba'])
    subs_param = dict(params[subs_ind+1:params.index(['/'], subs_ind)])
    agent_param = dict(params[slid_ind+1:params.index(['/'], agent_ind)])
    use_numba = dict(params[numba_ind+1:params.index(['/'], numba_ind)])
    return subs_param, agent_param, use_numba
