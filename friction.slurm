#!/bin/bash                                                                     
#SBATCH -p single                                                               
#SBATCH --account proj9                                                         
#SBATCH -J is-ismi                                                              
#SBATCH -N 1                                                                    
#SBATCH -n 28                                                                   
#SBATCH --time=10:00:00   ## hour:minute:second                                 


python3.6 main.py

exit

