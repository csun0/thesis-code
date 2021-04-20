import mdtools
from simtk.unit import *
from simtk.openmm.app import ForceField, Topology
import mdtraj
import numpy as np
import matplotlib.pyplot as plt
# from scipy.constants import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter

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

#----------------------------------------------------------------#

def fixWrapping(traj):
    """
    Account for crossing of periodic boundary conditions in traj position array.
    """
    diff = np.diff(traj.xyz, axis=0)
    for frame, atom, dim in zip(*np.where(diff > .95*traj.unitcell_lengths[0,0])):
        traj.xyz[frame+1:, atom, dim] -= traj.unitcell_lengths[frame+1, dim]
    for frame, atom, dim in zip(*np.where(diff < .95*-1*traj.unitcell_lengths[0,0])):
        traj.xyz[frame+1:, atom, dim] += traj.unitcell_lengths[frame+1, dim]
    return traj  

def removeWater(traj):
    """
    Remove all water molecules from trajectory
    """
    nowater = traj.atom_slice(traj.top.select("!water"))
    nowater = fixWrapping(nowater)
    
    return nowater

#----------------------------------------------------------------#

def currentDensityCalc(traj, t):
    """
    Calculate current density    
    traj[frame,atom,xyz] position -> [frame-1,xyz] current density
    """
    diff = traj.xyz[t:,:,:] - traj.xyz[:-t,:,:]    
    diff *= elementary_charge
    # manual fix; unsure how to do better
    for i in traj.top.select("name Cl"):
        diff[:,i,:] *= -1
    # could account for variable unit cell lengths; best way to do it? average of two points / average over timespan
    volume = np.product(np.mean(traj.unitcell_lengths, axis=0))
    diff /= volume * traj.timestep * t
    diff = np.sum(diff, axis=1)
    
    return diff
    
def conductivityCalc(currentdens, ef=(5,1,1)):
    """
    Calculate conductivity from current density and EF
    """
    conductivity = np.divide(currentdens, ef)
    conductivity *= coulombs/nanometers**2/picoseconds / (kilojoules/moles/nanometers/elementary_charges)
    conductivity = conductivity.value_in_unit(seconds*coulombs**2*item/kilogram/meters**3) * 10
    conductivity = np.mean(conductivity, axis=0)
    
    return conductivity[0]

def loadTraj(path):
    traj = mdtraj.load(path)
    nowater = traj.atom_slice(traj.top.select("!water"))
    nowater = fixWrapping(nowater)
    
    return nowater

#----------------------------------------------------------------#

def slicedConductivityCalc(traj, slices=5, ef=(5,1,1)):
    trajs = [traj.slice(tslice.astype(int)-1) for tslice in np.array_split(traj.time, slices)]
    delays = np.arange(1, int(np.floor(traj.n_frames/slices/2)))
    conductivity = np.zeros((len(delays), len(trajs)), dtype=object)
    for i, traj in enumerate(trajs):
        for j, t in enumerate(delays):
            conductivity[j, i] = currentDensityCalc(traj, t)
            conductivity[j, i] = conductivityCalc(conductivity[j, i], ef=ef)
    
    return conductivity
