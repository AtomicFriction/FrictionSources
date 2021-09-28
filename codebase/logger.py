import numpy as np
import globals

"""
-> Copies the contents of "input.txt" file to "log.txt".
-> Needs to run only once, at the beginning of the code.
"""
def InitLog(log_dir):
    with open(log_dir, 'w') as log, open('./input_parser/input.txt', 'r') as input:
        # Copy the contents of "input.txt" to "log.txt"
        log.write(input.read() + '\n\n')
        # Write the header for the analysis part
        log.write('prot,step,' + ','.join(globals.log_param.keys()) + '\n')

"""
-> Logs the desired analysis parameters each step.
"""
def WriteLog(log_dir, prot, step):
    with open(log_dir, 'a') as log:
        np.savetxt(log, \
            np.array([prot, step, *globals.log_param.values()])[np.newaxis], delimiter=',')

"""
-> 
"""
proj_pref = globals.eig_proj[0]
# create a list of same headers
proj_col = ['mod_'] * proj_pref
# modify the headers to have sequential indices
for idx, _ in enumerate(proj_col):
    proj_col[idx] = proj_col[idx].replace('_', str(idx))
# unify the list of strings into one single string with commas as delimiters
proj_col = ','.join(proj_col)

def EigProjLogInit(eig_dir):
    with open(eig_dir, 'w') as proj_log:
        proj_log.write("Eigenvector Projection Log\n")
        proj_log.write('protocol,step,{}\n'.format(proj_col)) 
 

"""
-> 
"""
def EigProjLog(eig_dir, prot, step, proj):
    with open(eig_dir, 'a') as proj_log:
        counter = np.array([prot, step])[np.newaxis]
        np.savetxt(proj_log, \
            np.hstack((counter, proj[:proj_pref][np.newaxis])), delimiter=',')
