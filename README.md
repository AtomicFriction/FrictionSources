# 0.1.0 Development Release Is Now Live!
![System Visualization](https://media.giphy.com/media/uixLzupbeZH3X5mTk2/giphy.gif)

Friction Sources is ....

The units used for the system are:  
-> distance is in Angstroms.  
-> time is in picoseconds.  
-> sigma is in Angstroms.  
-> epsilon is in eV.  
-> substrate spring constant is in eV/Angstroms^2.  
-> substrate mass is in amu(atomic mass units).  
-> latt_const for Argon is in Angstroms.  
-> Cutoff constant taken as 2.5 * sigma.  

## For Users


### Quick Start

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



### Execution Modes

Assuming that you are operating in the ``` codebase ```directory, use the following command to see possible command line arguements
```
python main.py --help
```
##### The ```--save_progress``` Mode
This mode can be used by the following command, replace ```save_per_steps``` with the step interval you prefer for the saving proccess.
```
python main.py --save_progress save_per_steps
```
Saves the state of the system to a ".npz" file every ```save_per_steps``` steps. This option is implemented to prevent progress loss, may be preferred for longer runs. The save file is a compressed NumPy file, the size of the file is relatively small.

##### The ```--from_progress``` Mode
This mode can be used by the following command, does not require additional arguements.
```
python main.py --from_progress
```
Finds the saved ".npz" file and resumes the interrupted run. Keep in mind that this mode requires the same "input.txt" file that you used to save the previous state, changing the "input.txt" file may result in unwanted consequences.

##### The ```--animate``` Mode
```
python main.py --animate animate_per_steps
```
Animates the system per ```animate_per_steps``` steps. This is a very basic visualization, may be used to get a rough understanding of the system.



## For Developers


### Benchmarking

##### Keep in mind that the software will already show the elapsed time and maximum memory used at the end of execution.

1) Locate to the repository, assuming that you have the repo at ./Desktop.
```
cd Desktop/FrictionSources/codebase
```
2) Use cProfile to profile the software and print them on the terminal in decreasing total time taken to execute.
```
python -m cProfile -s tottime main.py
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
