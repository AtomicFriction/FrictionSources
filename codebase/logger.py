import globals
import csv

"""
-> Copies the contents of "input.txt" file to "log.txt".
-> Needs to run only once, at the beginning of the code.
"""
def InitLog():
    # Copy the contents of "input.txt" to "log.txt"
    with open("log.csv", "w") as file_1, open('./input_parser/input.txt', 'r') as file_2:
        for line in file_2:
            file_1.write(line)
        file_1.write("\n")
        file_1.write("\n")


"""
-> Writes the protocol step and the analyzed quantities.
-> Needs to run "counter_i" times.
"""
def ProtLog(counter_i):
    with open("log.csv", "a") as file_1:
        file_1.write("Protocol Step " + str(globals.run[counter_i]) + "\n")
        file_1.write("\n")
        file_1.write("Step")
        if ("ff" in globals.data):
            globals.ff_switch = 1
            file_1.write("," + "ff_x")
            file_1.write("," + "ff_y")
            file_1.write("," + "ff_z")
        if ("pe" in globals.data):
            globals.potential_switch = 1
            file_1.write("," + "pe")
        if ("ke" in globals.data):
            globals.kinetic_switch = 1
            file_1.write("," + "ke")
        if ("etot" in globals.data):
            globals.etot_switch = 1
            file_1.write("," + "etot")
        if ("temp" in globals.data):
            globals.temp_switch = 1
            file_1.write("," + "temp")
        file_1.write("\n")


"""
-> Logs the desired analysis parameters each step.
"""
def WriteLog(counter_i, counter_j):
    log = open('log.csv', 'a')
    if (counter_j <= globals.run[counter_i][2]):
        log.write(str(counter_j) + ",")
        if (globals.ff_switch == 1):
            log.write(str(list(globals.ff)) + ",")
        if (globals.potential_switch == 1):
            log.write(str(globals.pe) + ",")
        if (globals.kinetic_switch == 1):
            log.write(str(globals.ke) + ",")
        if (globals.etot_switch == 1):
            log.write(str(globals.etot) + ",")
        if (globals.temp_switch == 1):
            log.write(str(globals.temp) + ",")

        log.write("\n")


"""
-> 
"""
def EigProjLogInit():
    with open('eig_proj_log.csv', 'w') as proj_log:
        proj_log.write("Eigenvector Projection Log")
        proj_log.write("\n")


"""
-> 
"""
def EigProjLog(counter_i, counter_j, proj):
    with open('eig_proj_log.csv', 'a') as proj_log:
        proj_log.write("Protocol: " + str(counter_i) + " step: " + str(counter_j) + "  ")
        proj_log.write(str(list(proj)))
        proj_log.write("\n")
