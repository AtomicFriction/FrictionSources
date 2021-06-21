import time
from run import main
import globals
import tracemalloc
from pyfiglet import Figlet
from PyInquirer import prompt
from examples import custom_style_2, custom_style_1, custom_style_3
import argparse

# Start of the maximum memory allocation calculation process.
tic = time.perf_counter()
tracemalloc.start()

if __name__ == "__main__":
    print("\n")
    f = Figlet(font='basic')
    print(f.renderText('Friction Sources'))


    # This part is for the command line arguements.
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_progress", help = "Saves the state of the system every given step interval in case it gets interrupt somehow. For example, '-save_progress 10000' means that the state of the system will be saved every 10000 steps.")
    parser.add_argument("--from_progress", help = "Loads the state of the system from a saved file and continues to run the saved configuration. ", action="store_true")
    parser.add_argument("--animate", help = "Animates the system every given step interval. For example, '--animate 100' animates the system every 100 steps.")
    parser.add_argument("--calc_hessian", help = "First calculates the Hessian and then goes on with the protocols.", action="store_true")
    parser.add_argument("--load_eigs", help = "Skips the Hessian calculation and loads a pre-calculated set of eigenvectors and eigenvalues. This mode requires the Hessian to be calculated beforehand with the same input parameters.", action="store_true")
    # Parse the arguements from the command line.
    args = parser.parse_args()
    # Save the parsed arguements into global variables.
    globals.save_progress = args.save_progress
    globals.from_progress = args.from_progress
    globals.calc_hessian = args.calc_hessian
    globals.load_eigs = args.load_eigs
    globals.animate = args.animate
    print(args.load_eigs)

    if (args.save_progress == None and args.from_progress == None and args.calc_hessian == None and args.load_eigs == None and args.animate == None):
        # This part is for the CLI menu.
        questions = [
            {
                'type': 'list',
                'name': 'ExecutionMode',
                'message': 'Which execution mode do you want to use?',
                'choices': [
                    'Calculate hessian matrix eigenvectors first, then run protocols.',
                    'Load pre-calculated eigenvectors, then run protocols.',
                    'Load a saved system state and run the rest of the protocols.'
                ]
            },
            {
                'type': 'confirm',
                'message': 'Do you want to save the state of your system?',
                'name': 'Save',
            },
            {
                'type': 'input',
                'message': 'Enter the system save interval, in "per steps".',
                'name': 'SaveInterval',
                'when': lambda answers: answers['Save'] != False
            },
            {
                'type': 'confirm',
                'message': 'Do you want to animate the system? (The progress will slow down significantly!)',
                'name': 'Animate',
            },
            {
                'type': 'input',
                'message': 'Enter the animation interval, in "per steps".',
                'name': 'AnimationInterval',
                'when': lambda answers: answers['Animate'] != False
            }
        ]

        answers = prompt(questions,  style=custom_style_3)

        globals.save_progress = answers["Save"]

        if (answers["Save"] == True):
            globals.save_progress_step = answers["SaveInterval"]

        if (answers["ExecutionMode"] == 'Calculate hessian matrix eigenvectors first, then run protocols.'):
            globals.calc_hessian = True
        elif (answers["ExecutionMode"] == 'Load pre-calculated eigenvectors, then run protocols.'):
            globals.load_eigs = True
        elif (answers["ExecutionMode"] == 'Load a saved system state and run the rest of the protocols.'):
            globals.from_progress = True

        globals.animate = answers["Animate"]

        if (answers["Animate"] == True):
            globals.animate_step = answers["AnimationInterval"]

    print('Code execution started.')
    # Run the code.
    main()
    peak = tracemalloc.get_traced_memory()[1]
    print(f"Peak memory usage was {peak / 10**6}MB.")

# End of the maximum memory allocation calculation process.
tracemalloc.stop()
toc = time.perf_counter()

print('Done!')
print(f"Code executed in {toc - tic:0.4f} seconds")
