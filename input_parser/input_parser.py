def parse_input(file):
    with open(file, 'r') as f:
        inputs = [param.split(": ") for param in f.read().split("\n")]
    inputs = dict(inputs)
    return inputs
