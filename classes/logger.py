import globals

"""
-> Copies the contents of "input.txt" file to "log.txt".
-> Needs to run only once, at the beginning of the code.
"""
def InitializeLog():
    # Copy the contents of "input.txt" to "log.txt"
    with open("log.txt", "w") as file_1, open("input.txt", 'r') as file_2:
        for line in file_2:
            file_1.write(line)
        file_1.write("\n")
        file_1.write("\n")

"""
-> Writes the protocol step and the analyzed quantities.
-> Needs to run "counter_i" times.
"""
def LogProtocol(counter_i):
    with open("log.txt", "a") as file_1:
        file_1.write("Protocol Step " + str(globals.run[counter_i]) + "\n")
        file_1.write("Step")
        if ("ff" in globals.data):
            globals.ff_switch = 1
            file_1.write("              " + "ff")
        if ("pe" in globals.data):
            globals.potential_switch = 1
            file_1.write("              " + "pe")
        if ("ke" in globals.data):
            globals.kinetic_switch = 1
            file_1.write("              " + "ke")
        if ("etot" in globals.data):
            globals.etot_switch = 1
            file_1.write("              " + "etot")
        if ("temp" in globals.data):
            globals.temp_switch = 1
            file_1.write("              " + "temp")
        file_1.write("\n")

"""
-> Logs the each step.
"""
def WriteLog(counter_i, counter_j):
    log = open('log.txt', 'a')
    if (counter_j <= globals.run[counter_i][2]):
        log.write(str(counter_j) + "    ")
        if (globals.ff_switch == 1):
            log.write(str(globals.ff) + "   ")
        if (globals.potential_switch == 1):
            log.write(str(globals.pe) + "   ")
        if (globals.kinetic_switch == 1):
            log.write(str(globals.ke) + "   ")
        if (globals.etot_switch == 1):
            log.write(str(globals.etot) + "   ")
        if (globals.temp_switch == 1):
            log.write(str(globals.temp) + "   ")

        log.write("\n")
