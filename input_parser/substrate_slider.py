from input_parser import parse

"""
makes use of the function parse to
get parameters for specified block
then, creates classes for the blocks
with their own parameters
"""
# where to put try catch for the possible wrong inputs?
# here or into parser?

subs_parm = parse('input.txt', '&substrate')
class Substrate():
    def __init__(self):
        self.num_row = subs_parm['num_row']
        self.latt_const = subs_parm['latt_const']
        self.displace_type = subs_parm['displace_type']
        self.k = subs_parm['k']
        self.mass = subs_parm['mass']
        
slider_parm = parse('input.txt', '&slider')
class Slider():
    def __init__(self):
        self.mass = slider_parm['mass']
        self.spacing = slider_parm['spacing']
        self.k = slider_parm['k']
