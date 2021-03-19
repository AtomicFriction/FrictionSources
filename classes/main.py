import time
from run import main

print('Code execution started.')

tic = time.perf_counter()

if __name__ == "__main__":
    main()

toc = time.perf_counter()

print('Done!')
print(f"Code executed in {toc - tic:0.4f} seconds")
