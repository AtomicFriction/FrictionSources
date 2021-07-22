import pandas as pd
from input_parser.input_parser import parse
import matplotlib.pyplot as plt

_, prot_param, anal_param, _, _, _ = parse('./input_parser/input.txt')
t_steps = prot_param['run'][:, 2]
apply_agent = prot_param['apply_agent']
cols = ['Step', *anal_param['data']]

# this functions is not ready
def plot_anal_log():
    with open('./input_parser/input.txt', 'r') as file: 
        len_input = len(file.readlines()) 

    data = pd.read_csv('log.csv', skiprows=len_input, usecols=cols)
    print(data)

def plot_proj_log(Y):
    df = pd.read_csv('eig_proj_log.csv', skiprows=1) # skip the first row where the title of the file is written
    df.plot(x='step', y=Y, xlabel='Step', ylabel='Projection(s)', title='Eigenvector Projection of {}'.format(', and '.join(Y)))
    plt.show()

plot_proj_log(['proj0', 'proj1'])