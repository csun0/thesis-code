import mdtools
from simtk.unit import *
from simtk.openmm.app import ForceField, Topology

import mdtraj
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
# matplotlib.use('Agg')

from scipy import stats

import re
import sys
import glob
import ast

from new_functions import *


atoms = mdtraj.load_frame('../crystalmd/run1/NVT-1.0-a.h5', 0)
lys = atoms.top.select('protein or backbone')
lys_traj = mdtraj.load('../crystalmd/run1/NVT-1.0-a.h5', stride=50)

side = np.mean(lys_traj.unitcell_lengths, axis=0)[2]


x_index = pd.DataFrame(lys_traj.xyz[:,:,0])
y_index = pd.DataFrame(lys_traj.xyz[:,:,1])
z_index = pd.DataFrame(lys_traj.xyz[:,:,2])


diff = x_index.diff()
diff[diff > .95*side] -= side
diff[diff < -.95*side] += side
for col in diff:
    x_index[col] = pd.DataFrame(np.r_[x_index[col].iloc[0], diff[col].iloc[1:]].cumsum())
    
x_index = x_index.dropna()



diff = y_index.diff()
diff[diff > .95*side] -= side
diff[diff < -.95*side] += side
for col in diff:
    y_index[col] = pd.DataFrame(np.r_[y_index[col].iloc[0], diff[col].iloc[1:]].cumsum())
    
y_index = y_index.dropna()

fig, axes = plt.subplots(1,1)

diff = z_index.diff()
diff[diff > .95*side] -= side
diff[diff < -.95*side] += side
for col in diff:
    z_index[col] = pd.DataFrame(np.r_[z_index[col].iloc[0], diff[col].iloc[1:]].cumsum())

z_index = z_index.dropna()

lys_traj.xyz[:,:,0] = x_index.to_numpy()
lys_traj.xyz[:,:,1] = y_index.to_numpy()
lys_traj.xyz[:,:,2] = z_index.to_numpy()



lys_traj.superpose(lys_traj, ref_atoms_indicies=lys)