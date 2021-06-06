import time
from run import main
import argparse
import globals
import tracemalloc


tic = time.perf_counter()
tracemalloc.start()

if __name__ == "__main__":
    # "-h" or "--help" arguement description.
    parser = argparse.ArgumentParser(description = """
    FrictionSources Software
    """)
    # Definitions of different command line arguements.
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
    print('Code execution started.')
    # Run the code.
    main()
    peak = tracemalloc.get_traced_memory()[1]
    print(f"Peak memory usage was {peak / 10**6}MB.")

tracemalloc.stop()
toc = time.perf_counter()

print('Done!')
print(f"Code executed in {toc - tic:0.4f} seconds")
