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
python3 main.py
```
