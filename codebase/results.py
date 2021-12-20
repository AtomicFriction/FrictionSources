from shutil import copyfile, make_archive
import time
import os
from zipfile import ZipFile

# Create a folder for results (log and xyz files).
def fold_results():
    # To name the results folder, define a string consisting of the current date and time
    # In the fashion 'month, day, year, hour, minute, and second'
    timestr = time.strftime('%m-%d-%Y-%H-%M-%S')
    # Create directory name for coord.xyz file
    xyz_dir = './results/{}/coord.xyz'.format(timestr)
    # Create directory name for log.csv file
    log_dir = './results/{}/log.csv'.format(timestr)
    # Create directory name for eig_proj_log.csv file
    eig_dir = './results/{}/eig_proj.csv'.format(timestr)
    # If the directory does not exist, then create it. If it exists, pass.
    for file in (xyz_dir, log_dir, eig_dir):
        os.makedirs(os.path.dirname(file), exist_ok=True)
    # Copy the input.txt file into the related result folder.
    copyfile('./input_parser/input.txt', './results/{}/input.txt'.format(timestr))

    return xyz_dir, log_dir, eig_dir, timestr


# Compress the results folder for easier relocation.
def zip_results(timestr):
    res_dir ='./results/{}/'.format(timestr)
    zip_dir = res_dir + timestr
    make_archive(zip_dir, 'zip', res_dir)

    print('Results are compressed.')
