from shutil import copyfile
import time
import os
from zipfile import ZipFile
import globals

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
    res_dir = './results/{}/'.format(timestr)
    zip_dir = res_dir + timestr
    with ZipFile(res_dir + timestr + '.zip', 'w') as zipObj:
        os.chdir(res_dir)
        if (os.path.exists("./coord.xyz") == True):
            zipObj.write('coord.xyz')
        if (os.path.exists("log.csv") == True):
            zipObj.write('log.csv')
        if (os.path.exists("eig_proj.csv") == True):
            zipObj.write('eig_proj.csv')
        os.chdir("..")
        os.chdir("..")
    globals.compression_control = 1
    print("Files are compressed.")


# Delete the files if the compression is succesfull to save space.
def delete_files(xyz_dir, log_dir, eig_dir):
    if (globals.compression_control == 1):
        try:
            os.remove(xyz_dir)
            os.remove(log_dir)
            os.remove(eig_dir)
        except:
            print("Compression succesfull, file deletion failed.")
    elif (globals.compression_control == 0):
        print("Compression function failed, files are not deleted.")
    else:
        print("Compression switch can only take 0 or 1.")
