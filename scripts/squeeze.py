from simtk.openmm.app import PDBFile, ForceField
from simtk.unit import *
import mdtools
import glob
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("notebook", font_scale=1.3)
import mdtraj
forcefield = ForceField('amber14/protein.ff14SB.xml',
                        'amber14/tip3p.xml')
# Load and solvate PDB                                                                                                                                                                                    
pdb = PDBFile("../pdb/HEWL_NA.pdb")
mdsystem = mdtools.LatticeMDSystem(pdb.topology, pdb.positions, forcefield, "P 43 21 2")

# pdb = PDBFile("../pdb/5E21_prepped.pdb")
# mdsystem = mdtools.LatticeMDSystem(pdb.topology, pdb.positions, forcefield, "C 2")

mdsystem.buildSuperCell(1, 1, 2)
# mdsystem.buildSuperCell(2, 2, 2)

mdsystem.addSolvent(neutralize=True)
mdsystem.calmdown(posre=True)
# Squeeze                                                                                                                                                                                                 
mdsystem.squeeze(tolerance=0.001, maxIterations=20)


# Plot squeeze run                                                                                                                                                                                        
h5trajs = sorted(glob.glob("iter*.h5"))
sns.set_palette(sns.cubehelix_palette(len(h5trajs), start=.5, rot=-.75))
plt.figure(figsize=(9, 6))

for h5traj in h5trajs:
    traj = mdtraj.load(h5traj)
    n = int(len(traj.topology.select("water")) / 3)
    plt.plot(traj.time, traj.unitcell_volumes, label=f"{n} waters")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel("Time (ps)")
plt.ylabel(r"Box Volume (nm$^3$)")
plt.xlim(0, traj.time[-1])
plt.tight_layout()
plt.savefig("HEWL_squeeze.png")
