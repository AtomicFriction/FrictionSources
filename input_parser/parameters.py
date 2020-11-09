from input_parser import parse_input

"""
Since the function 'parse_input' returns a dictionary, 'param' is a dictionary of inputs.
By calling param["keyname"], it returns its related item.
"""

# adjust parameters
param = parse_input("input.txt")
ptcl_type = param["ptcl_type"]
side_atom = int(param["side_atom"])
mass = float(param["mass"])
lattice_const = float(param["lattice_const"])
k = float(param["k"])
neighbor_step = int(param["neighbor_step"])
t_steps = int(param["t_steps"])
dt = float(param["dt"])

print("\n---\nThe {} atoms are separated by the lattice constant {} Angström.\n---\n".format(ptcl_type, lattice_const))
