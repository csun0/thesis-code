#!/bin/bash
#SBATCH -J mdconvert                 # A single job name for the array
#SBATCH -n 1                      # Number of cores
#SBATCH -N 1                      # All cores on one machine
#SBATCH -p shared          # Partition
#SBATCH --mem 100000               # Memory request (20 Gb)
#SBATCH -t 01-00:00               # time limit 3 days
#SBATCH -o openmm_%j.out          # Standard output
#SBATCH -e openmm_%j.err          # Standard error

hostname

conda activate md

# mdconvert $1.h5 -o $2.dcd

mdconvert $1.h5 -o $1.pdb -i -1