import time
from run import main
import globals
import tracemalloc
from pyfiglet import Figlet
from PyInquirer import prompt
from examples import custom_style_2, custom_style_1, custom_style_3

# Start of the maximum memory allocation calculation process.
tic = time.perf_counter()
tracemalloc.start()

if __name__ == "__main__":
    print("\n")
    f = Figlet(font='basic')
    print(f.renderText('Friction Sources'))

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
