#!/bin/bash
#SBATCH -p hamsi
#SBATCH --account byaman
#SBATCH -J is-ismi
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=10:00:00   ## hour:minute:second

eval "$(conda shell.bash hook)"
conda activate fricsource

python3.8 main.py --calc_hessian --animate 1000

exit
