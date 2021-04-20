import mdtools
from simtk.unit import *
from simtk.openmm.app import ForceField, Topology
import mdtraj
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import *
import pandas as pd
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter
import seaborn as sns
import itertools
import glob
import re
import seaborn as sns
import matplotlib
matplotlib.use("Agg")

# h5s = glob.glob(f"../md_out/water/*.h5")

# store = []

# for i in h5s:
#     itertraj = mdtraj.iterload(i, 300)
#     traj = next(itertools.islice(itertraj, 30))
#     t = traj.atom_slice(traj.top.select("water"))
#     # average positions of H1 and H2
#     ok = (t.xyz[:,1::3,:] + t.xyz[:,2::3,:]) / 2
#     huh = t.xyz[:,0::3] - ok
#     ui = np.mean(huh, axis=1)
#     params = re.findall("\d+M-\d+", i)[0].split("-")
#     # params[0][:-1]
#     store.append([np.mean(ui[:,0]), int(params[1])/1000000])
    
# sns.pointplot(x='MV/cm', y='Alignment', data=pd.DataFrame(store, columns=["Alignment", 'MV/cm']))
# plt.savefig("alignment.png")


tags = sys.argv[1:]

flag = "0"

for i in tags:
    if flag == "0":
        if i[0] == "-":
            flag = i[1:]
    else:
        if flag == "file":
            file = i
            flag = "0"
            
            
itertraj = mdtraj.iterload(f'../md_out/water/{file}', 300)
traj = next(itertools.islice(itertraj, 30))
t = traj.atom_slice(traj.top.select("water"))

# average positions of H1 and H2
h_pos = (t.xyz[:,1::3,:] + t.xyz[:,2::3,:]) / 2
dipole_direction = t.xyz[:,0::3] - h_pos

frame_average_dipole = np.mean(dipole_direction, axis=0)
ef = file.split("-")[1]

output = np.append(frame_average_dipole, file)
output = np.append(output, ef)


with open(f'../md_out/water/alignment_results.txt', 'a+') as f:
    f.write(f"{output}\n")


            
            
            