import mdtools
from simtk.unit import *
from simtk.openmm.app import ForceField, Topology
import mdtraj
import numpy as np
# from scipy.constants import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter
import ast

import glob
from new_functions import *
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

from scipy import stats
import seaborn as sns
import re
import sys

mdtools.printVersions()


# USAGE: sbatch gpu.sh loadin -ef EF -path ../PATH/*.h5
desc = 'empty'
tags = sys.argv[1:]
flag = "0"
slant = False



for i in tags:
    if flag == "0":
        if i[0] == "-":
            flag = i[1:]
    else:
        if flag == "ef":
            ef = ast.literal_eval(i)
            flag = "0"
        elif flag == "etime":
            etime = float(i)
            flag = "0"
        elif flag == "ptime":
            ptime = float(i)
            flag = "0"
        elif flag == "o":
            o = i
            flag = "0"
        elif flag == "desc":
            desc = i
            flag = "0"
        elif flag == "path":
            path = i
            flag = "0"
        elif flag == "slant":
            slant = True
            flag = "0"

            
            
            
abt = converter_abt(ef)

if slant == True:
    abt = converter_slant(abt)
else:
    abt = (0,abt,0)


files = glob.glob(f"../{path}/*.h5")
index = []
for i in files:
    index.append(float(re.findall('iter\w+', i)[0][-2:]))
    
# Load and solvate PDB
t = mdtraj.load(files[np.argmax(index)])
ff = forcefield = ForceField('amber14/protein.ff14SB.xml',
                        'amber14/tip3p.xml')
mdsystem = mdtools.LatticeMDSystem(t.topology.to_openmm(), t.openmm_positions(-1), ff, "P 1")
mdsystem.topology.setPeriodicBoxVectors(t.openmm_boxes(-1))

mdsystem.buildSimulation(efx=True, ef=abt, temperature=293.15*kelvin, 
                         ensemble='NPT', saveStateData=False, trajInterval=250, filePrefix=f'NPT-{ef}')
mdsystem.simulate(2*nanosecond)

mdsystem.buildSimulation(efx=True, ef=abt, temperature=293.15*kelvin, filePrefix=f'NVT-{ef}-{desc}', saveTrajectory=True, 
                             saveStateData=True, trajInterval=250, ensemble='NVT', thermalize=True)

mdsystem.simulate(10*nanosecond)

    
