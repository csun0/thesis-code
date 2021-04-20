#!/bin/bash
#SBATCH -J gpu                 # A single job name for the array
#SBATCH -n 1                      # Number of cores
#SBATCH -N 1                      # All cores on one machine
#SBATCH -p seas_gpu,gpu,gpu_requeue          # Partition
#SBATCH --gres=gpu:1              # Request 1 GPU
#SBATCH --mem 32G               # Memory request (32 Gb)
#SBATCH -t 03-00:00               # time limit 3 days
#SBATCH -o openmm_%j.out          # Standard output
#SBATCH -e openmm_%j.err          # Standard error
#SBATCH --constraint=v100

hostname
nvidia-smi

conda activate md
python3 $1 "${@:2}" 

# seas_dgx1
