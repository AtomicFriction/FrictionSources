import pandas as pd
from input_parser.input_parser import parse
import matplotlib.pyplot as plt

_, prot_param, anal_param, _, _, _ = parse('./input_parser/input.txt')
t_steps = prot_param['run'][:, 2]
apply_agent = prot_param['apply_agent']
cols = ['prot', 'step', *anal_param['data']]

# this function is not ready
def plot_anal_log(anal):
    with open('./input_parser/input.txt', 'r') as file: 
        len_input = len(file.readlines()) 

    anal_df = pd.read_csv('log.csv', skiprows=len_input)
    anal_df.plot(x='step', y=anal, xlabel='Step', ylabel='Analyzed Quantities', title='Analyses of the Data')
    plt.show()

plot_anal_log(['ff_x', 'ff_y', 'ff_z', 'vf', 'temp'])

def plot_proj_log(proj):
    proj_df = pd.read_csv('eig_proj_log.csv', skiprows=1) # read the file excluding the title
    proj_df.plot(x='step', y=proj, xlabel='Step', ylabel='Projection(s)', title='Eigenvector Projection')
    plt.show()
    #print(df.get(df['protocol']==2))

plot_proj_log(['mod5', 'mod6', 'mod97', 'mod89'])
