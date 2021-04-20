from simtk.unit import *
from simtk.openmm.app import ForceField, Topology
import mdtools
import mdtraj
import sys

def buildSolventBox(boxSize=[75]*3*angstroms, ionicStrength=0.2*molar, ef=(0,0,0)):
    """Build solventbox of desired size"""

    ff = ForceField("amber99sbildn.xml", "tip3p.xml")
    top = Topology()
    system = mdtools.SolvatedMDSystem(top, []*nanometers, ff)
    system.addSolvent(boxSize=boxSize, ionicStrength=ionicStrength)
    system.buildSimulation(efx=True, ef=ef, temperature=293.15*kelvin, ensemble='NPT')
    return system

def runSimulation(solventbox, ef=(0,0,0), etime=100*picoseconds, ptime=1*nanoseconds, filePrefix="file"):
    """Run simulation of solventbox"""

    # Minimization and Equilibration
    solventbox.minimize()
    solventbox.simulate(etime)
    
    # Production run
    solventbox.buildSimulation(efx=True, ef=ef, temperature=293.15*kelvin, filePrefix=filePrefix, saveTrajectory=True, 
                             saveStateData=True, trajInterval=250)
    solventbox.simulate(ptime)
    solventbox.buildSimulation() # close reporters

suffix = 'b'

if sys.argv[1] == 'molarity':
    if sys.argv[2] == 'lower':
        molarity = [[0.086,0.173,0.349,0.901,1.901,4.278],[.5,1,2,5,10,20]]
    if sys.argv[2] == 'higher':
        molarity = [[1.901,4.278],[10,20]]
    for i,j in zip(molarity[0], molarity[1]):
        solventbox = buildSolventBox(boxSize=[75]*3*angstroms, ionicStrength=i*molar, ef=(5, 0, 0))
        runSimulation(solventbox, ef=(5, 0, 0), etime=120*picoseconds, ptime=20*nanoseconds, filePrefix=f"../md_out/molarity/{j}-{suffix}")

if sys.argv[1] == 'efield':
#     efield = [0, 1, 2, 5, 10, 15, 20, 40, 80]
    efield = []
    for i in sys.argv[2:]:
        efield.append(int(i))
    print(efield)
    for i in efield:
        solventbox = buildSolventBox(boxSize=[75]*3*angstroms, ionicStrength=0.2*molar, ef=(i, 0, 0))
        runSimulation(solventbox, ef=(i, 0, 0), etime=120*picoseconds, ptime=20*nanoseconds, filePrefix=f"../md_out/efield/{i}-{suffix}")
