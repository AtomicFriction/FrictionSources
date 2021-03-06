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
        file_1.write("    ".join(globals.data) + "        " + "\n")

"""
-> Logs the each step.
"""
def WriteLog(counter_i, counter_j, ff, pe, ke, etot, temp):
    log = open('log.txt', 'a')
    if (counter_j <= globals.run[counter_i][2]):
        log.write("Step " + str(counter_j) + ":    ")
        if (globals.ff_switch == 1):
            log.write("ff:  " + str(ff) + "   ")
        if (globals.potential_switch == 1):
            log.write("pe:  " + str(pe) + "   ")
        if (globals.kinetic_switch == 1):
            log.write("ke:  " + str(ke) + "   ")
        if (globals.etot_switch == 1):
            log.write("etot:    " + str(etot) + "   ")
        if (globals.temp_switch == 1):
            log.write("temp:    " + str(temp) + "   ")

        log.write("\n")