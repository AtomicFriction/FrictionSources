#!/bin/bash                                                                     
#SBATCH -p mid1                                                               
#SBATCH --account proj9                                                         
#SBATCH -J is-ismi                                                              
#SBATCH -N 1                                                                    
#SBATCH -n 28                                                                   
#SBATCH --time=10:00:00   ## hour:minute:second                                 

module load centos7.3/comp/python/3.8.12-openmpi-4.1.1-oneapi-2021.2

python3.8 main.py

exit

