# 9-23 pointplot
import mdtools
from simtk.unit import *
from simtk.openmm.app import ForceField, Topology
import mdtraj
import numpy as np
from scipy.constants import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter

import glob
from functions import *
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

from scipy import stats
import seaborn as sns
import re
import sys

# USAGE: sbatch cpu.sh efielderror prefix

suffix = sys.argv[1]

h5s = glob.glob(f"../md_out/efield/*-{suffix}.h5")
a = [float(i[0][:-1]) for i in [re.findall("[0-9.]+-", i) for i in h5s]]

pathway = [(i, j) for i,j in zip(h5s, a)]
pathway.sort(key=lambda x: x[1])

storage = np.zeros((int(len(a)), 2))



for i in range(len(storage)):
    
    path = pathway[i][0]
    traj = loadTraj(f"{path}")
    traj = traj[50:]

    delays = np.arange(1, int(np.floor(traj.n_frames/2)))
    conductivity = np.zeros(len(delays), dtype=float)

    for j, t in enumerate(delays):
        conductivity[j] = conductivityCalc(currentDensityCalc(traj, t), ef=(pathway[i][1]))

    data = np.repeat(conductivity, np.flip(delays), axis=0)
    
    storage[i, 0] = np.mean(data, axis=0)
    storage[i, 1] = pathway[i][1]                  
    
    with open(f'../txt_out/efield_{suffix}.txt', 'a+') as f:
        f.write(f"{path}, {storage[i][0]}, {storage[i][1]}\n")
            
# plt.rcParams["figure.dpi"] = 300
# ax = sns.pointplot(x=unique[:, 1], y=unique[:, 0], dodge=True, join=False, ci='sd')
# ax.set(xlabel="Molarity", ylabel = "Conductivity (mS/cm)")
# plt.savefig("molarity-errorbars.png")
