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

#----------------------------------------------------------------#

# MV/cm to abt
def converter_abt(x):
    x *= 1e6
    ef = x*(volts/centimeter/mole)
    ef = ef.in_units_of(kilojoule_per_mole/nanometer/elementary_charge)*AVOGADRO_CONSTANT_NA
    return float(ef.__str__().split(' ')[0])

# abt to MV/cm
def converter_mvcm(x):
    ef = x*(kilojoule_per_mole/nanometer/elementary_charge)
    ef = ef.in_units_of(volts/centimeter/mole)/AVOGADRO_CONSTANT_NA
    ef /= 1e6
    return float(ef.__str__().split(' ')[0])

# abt to slanted abt vector
def converter_slant(abt):
    slant = [0.88773502, 0., 0.46035479]
    n = slant[0] / slant[2]
    A = np.sqrt(n**2 + 1)
    
    x = abt / A
    z = n * x
    
    return (x, 0, z)

#----------------------------------------------------------------#

def fixWrapping(traj):
    """
    Account for crossing of periodic boundary conditions in traj position array.
    """
    diff = np.diff(traj.xyz, axis=0)
    for frame, atom, dim in zip(*np.where(diff > .5*traj.unitcell_lengths[3,0])):
        traj.xyz[frame+1:, atom, dim] -= traj.unitcell_lengths[frame+1, dim]
    for frame, atom, dim in zip(*np.where(diff < .5*-1*traj.unitcell_lengths[3,0])):
        traj.xyz[frame+1:, atom, dim] += traj.unitcell_lengths[frame+1, dim]
    return traj

#----------------------------------------------------------------#

def buildSolventBox(boxSize=[75]*3*angstroms, ionicStrength=0.2*molar, ef=(0,0,0), temperature=298.15):
    """Build solventbox of desired size"""

    ff = ForceField("amber99sbildn.xml", "tip3p.xml")
    top = Topology()
    system = mdtools.SolvatedMDSystem(top, []*nanometers, ff)
    system.addSolvent(boxSize=boxSize, ionicStrength=ionicStrength)
    system.buildSimulation(efx=True, ef=ef, temperature=temperature*kelvin, ensemble='NPT')
    return system

def runSimulation(solventbox, ef=(0,0,0), etime=100*picoseconds, ptime=1*nanoseconds, filePrefix="file", temperature=298.15, atomSubset=None):
    """Run simulation of solventbox"""

    # Minimization and Equilibration
    solventbox.minimize()
    solventbox.simulate(etime)
    
    # Production run
    solventbox.buildSimulation(efx=True, ef=ef, temperature=temperature*kelvin, filePrefix=filePrefix, saveTrajectory=True, 
                             saveStateData=True, trajInterval=250, atomSubset=atomSubset)
    solventbox.simulate(ptime)
    solventbox.buildSimulation() # close reporters