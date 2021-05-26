# 0.1.0 Development Release Is Now Live!

### How To Run The Software:

1) Go to the directory you want to download the code at.
```
cd my/directory
```
2) Download the source code.
```
git clone https://github.com/AtomicFriction/FrictionSources.git
```
3) Locate and access the ``` input.txt``` file which will allow you to change the parameters of the simulation to your liking.
```
cd FrictionSources/codebase/input_parser
```
For UNIX based systems:
```
nano input.txt
```
For Windows:
```
start notepad input.txt
```
4) Once you configure the parameters at step 3, the software is ready to run. Go back to the previous directory and run the software.
```
cd -
python main.py
```
### How To Benchmark The Software:

##### Keep in mind that the software will already show the elapsed time and maximum memory used at the end of execution.

1) Locate to the repository, assuming that you have the repo at ./Desktop.
```
cd Desktop/FrictionSources/codebase
```
2) Use cProfile to profile the software and print them on the terminal in decreasing total time taken to execute.
```
python -m cProfile -tottime main.py
```
##### If you prefer to visualize the cProfile results, here is how you do it:

3) Install the snakeviz package.
```
pip install snakeviz
```
4) Use cProfile to profile the software and save the results to a ".dat" file
```
python -m cProfile -0 temp.dat main.py
```
5) Use the snakeviz package to visualize the result.
```
snakeviz temp.dat
```
