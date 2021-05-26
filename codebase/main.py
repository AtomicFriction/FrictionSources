import time
from run import main
import argparse
import globals


tic = time.perf_counter()

if __name__ == "__main__":
    # "-h" or "--help" arguement description.
    parser = argparse.ArgumentParser(description = """
    FrictionSources Software
    """)
    # Definitions of different command line arguements.
    parser.add_argument("--save_progress", help = "Saves the state of the system every given step interval in case it gets interrupt somehow. For example, '-save_progress 10000' means that the state of the system will be saved every 10000 steps.")
    parser.add_argument("--from_progress", help = "Loads the state of the system from a saved file and continues to run the saved configuration. ", action="store_true")
    parser.add_argument("--animate", help = "Animates the system every given step interval. For example, '--animate 100' animates the system every 100 steps.")
    # Parse the arguements from the command line.
    args = parser.parse_args()
    # Save the parsed arguements into global variables.
    globals.save_progress = args.save_progress
    globals.from_progress = args.from_progress
    globals.animate = args.animate
    print('Code execution started.')
    # Run the code.
    main()

toc = time.perf_counter()

print('Done!')
print(f"Code executed in {toc - tic:0.4f} seconds")
