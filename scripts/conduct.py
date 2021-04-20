import mdtools
from simtk.unit import *
from simtk.openmm.app import ForceField, Topology

import mdtraj
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use('Agg')

from scipy import stats

import re
import sys
import glob

from new_functions import *

#----------------------------------------------------------------#

# USAGE: sbatch cpu.sh HEWL_conduct.py -f FILENAME -o INPUT_DIR -axis 0/1/2

#----------------------------------------------------------------#


tags = sys.argv[1:]


flag = "0"
f = ""
o = ""
axis = 0

for i in tags:
    if flag == "0":
        if i[0] == "-":
            flag = i[1:]
    else:
        if flag == "f":
            f = i
            flag = "0"
        elif flag == "o":
            o = i
            flag = "0"
        elif flag == "axis":
            axis = int(i)
            flag = "0"

if o != "":
    o = "/" + o

axis_name = {0: 'x', 1: 'y', 2: 'z'}

ef = (1,1,float(f.split('-')[1]))
path = f'..{o}/{f}'


atoms = mdtraj.load_frame(path, 0)
ions = atoms.top.select('!protein and !water')
traj = mdtraj.load(path, atom_indices=ions, stride=3)
traj = fixWrapping(traj)

traj.xyz = traj.xyz[100:]

delays = np.arange(1, int(np.floor(traj.n_frames/2)))
storage = np.zeros(len(delays), dtype=float)


for t in delays:
    
    diff = traj.xyz[t:,:,:] - traj.xyz[:-t,:,:]    
    diff *= 1.60218e-19 
    for i in traj.top.select("name Cl"):
        diff[:,i,:] *= -1
    volume = np.mean(traj.unitcell_volumes)
    diff /= (volume * traj.timestep * t)
    currentdensity = np.sum(diff, axis=1)
    
    # j in units: coulombs/nanometers**2/picoseconds
    # ef in units: MV/cm
    # sigma in units: S/cm
    
    conductivity = np.divide(currentdensity, ef)
    conductivity *= 1e20
    conductivity = np.mean(conductivity, axis=0)
    storage[t-1] = conductivity[axis]

data = np.repeat(storage, np.flip(delays), axis=0)
result = np.mean(data, axis=0)        
    
with open(f'..{o}/{axis_name[axis]}_conductivity_results.txt', 'a+') as f:
    f.write(f"{path}, {result}, {ef}\n")
            