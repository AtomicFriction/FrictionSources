import pandas as pd
from input_parser.input_parser import parse
import matplotlib.pyplot as plt

""" _, prot_param, anal_param, _, _, _ = parse('./input_parser/input.txt')
t_steps = prot_param['run'][:, 2]
apply_agent = prot_param['apply_agent']
cols = ['prot', 'step', *anal_param['data']]  """

def plot_anal_log(anal, result_folder):
    # Define directories for the input file and the log file
    inp_dir = './results/{}/input.txt'.format(result_folder)
    log_dir = './results/{}/log.csv'.format(result_folder)

    # Define a variable equal to the number of rows in the input file
    with open(inp_dir, 'r') as file: len_input = len(file.readlines())

    # Read the log file as a dataframe starting from where the input file ends
    anal_df = pd.read_csv(log_dir, skiprows=len_input)

    # Plot the dataframe
    anal_df.plot(x='step', y=anal, xlabel='Step', ylabel='Analyzed Quantities', title='Analyses of the Data')
    plt.show()

#plot_anal_log(['ff_x', 'ff_y', 'ff_z', 'vf', 'temp'], '10-02-2021-19-31-34')

def plot_proj_log(proj, result_folder):
    # Define directories for the input file and the log file
    eig_dir = './results/{}/eig_proj.csv'.format(result_folder)

    # Read the eigen vector projection file as a dataframe excluding the title
    proj_df = pd.read_csv(eig_dir, skiprows=1)

    # Plot the dataframe
    proj_df.plot(x='step', y=proj, xlabel='Step', ylabel='Projection(s)', title='Eigenvector Projection')
    plt.show()

plot_proj_log(['mod5', 'mod6'], '10-02-2021-19-31-34')
