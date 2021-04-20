from simtk.unit import *
from simtk.openmm.app import ForceField, Topology
import mdtools
import mdtraj
import sys
import datetime
import ast

from new_functions import *

'''
mol: molarity (M), 0.2
ef: efield strength MV/cm, 1
box: box length (angstroms), 75
etime: runtime (ps), 120
ptime: primetime (ns), 20
o: output directory
'''

tags = sys.argv[1:]

flag = "0"
mol = 0.2
ef = 1
box = 75
etime = 120
ptime = 20
o = ""
desc = 'z'
temperature = 298.15*kelvin
atomSubset = None

for i in tags:
    if flag == "0":
        if i[0] == "-":
            flag = i[1:]
    else:
        if flag == "mol":
            mol = ast.literal_eval(i)
            flag = "0"
        elif flag == "ef":
            ef = ast.literal_eval(i)
            flag = "0"
        elif flag == "box":
            box = float(i)
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
        elif flag == "temperature":
            temperature = ast.literal_eval(i)
            flag = "0"
        elif flag == 'subset':
            atomSubset = True
            flag = '0'

if o != "":
    o = "/" + o

tag = str(mol) + "M-" + str(ef) + "-" + str(desc)
solventbox = buildSolventBox(boxSize=[box]*3*angstroms, ionicStrength=mol*molar, ef=(converter_abt(ef), 0, 0), temperature=temperature)

if atomSubset == True:
    h20 = ["O", "H1", "H2"]
    atomSubset = []
    for i in solventbox.topology.atoms():
        temp = str(i).split()    
        if temp[2][1:-1] not in h20:
            atomSubset.append(int(temp[1]))

runSimulation(solventbox, ef=(converter_abt(ef), 0, 0), 
              etime=etime*picoseconds, ptime=ptime*nanoseconds, filePrefix=f"../md_out{o}/{tag}", temperature=temperature, atomSubset=atomSubset)
