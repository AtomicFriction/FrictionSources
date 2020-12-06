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
defines two dictionaries, sub_params and agent_params,
by indexing from related block names till end sign '/'
--------------------------------------------------
(!) block order is of importance (see Ln 31, Col 80)
--------------------------------------------------
CALLING
*******
when creating a class, parser should be called with a placeholder
so that only related parameters are assigned. examples as follows:
subs_params, _ = parse('input.txt')
_ , agent_params = parse('input.txt')
"""

def parse(file):
    with open(file, 'r') as f:
        params = [param.split(' = ') for param in f.read().lower().splitlines()]
        
    sub_param = dict(params[params.index(['&substrate'])+1:params.index(['/'])])
    agent_param = dict(params[params.index(['&slider'])+1:params.index(['/'], 9)])
    return sub_param, agent_param
