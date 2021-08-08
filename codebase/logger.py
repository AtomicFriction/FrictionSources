import pandas as pd
import numpy as np
import globals
import csv

"""
-> Copies the contents of "input.txt" file to "log.txt".
-> Needs to run only once, at the beginning of the code.
"""
def InitLog():
    with open('log.csv', 'w') as log, open('./input_parser/input.txt', 'r') as input:
        # Copy the contents of "input.txt" to "log.txt"
        log.write(input.read() + '\n\n')
        # Write the header for the analysis part
        log.write('prot,step,' + ','.join(globals.log_param.keys()) + '\n')

"""
-> Logs the desired analysis parameters each step.
"""
def WriteLog(prot, step):
    with open('log.csv', 'a') as log:
        np.savetxt(log, \
            np.array([prot, step, *globals.log_param.values()])[np.newaxis], delimiter=',')

"""
-> 
"""
proj_pref = globals.eig_proj[1]
# create a list of same headers
proj_col = ['proj_'] * proj_pref
# modify the headers to have sequential indices
for idx, _ in enumerate(proj_col):
    proj_col[idx] = proj_col[idx].replace('_', str(idx))
# unify the list of strings into one single string with commas as delimiters
proj_col = ','.join(proj_col)

def EigProjLogInit():
    with open('eig_proj_log.csv', 'w') as proj_log:
        proj_log.write("Eigenvector Projection Log\n")
        proj_log.write('protocol,step,{}\n'.format(proj_col))


"""
-> 
"""
def EigProjLog(counter_i, step, proj):
    with open('eig_proj_log.csv', 'a') as proj_log:
        counter = np.array([counter_i, step])[np.newaxis]
        np.savetxt(proj_log, \
            np.hstack((counter, proj[:proj_pref][np.newaxis])), delimiter=',')
