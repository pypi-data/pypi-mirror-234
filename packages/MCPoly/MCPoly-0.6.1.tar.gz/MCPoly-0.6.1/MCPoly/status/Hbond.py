from ase.io import read
from ase import Atoms
import numpy as np
import os
import sys

mydir = os.path.dirname( __file__ )
stadir = os.path.join(mydir, '..', 'status')
sys.path.append(stadir)
from molesplit import molesplit

def Hbond(file, loc='./', HBond=2.0, angle=150, mode='all'):
    """
    A method to see all hydrogen bonds of the single status XYZ file.
    
    HBond(file, loc='./', HBond=2.0, angle=150, mode='all')
    file: File Name.
    loc: File Location. The default is your current location.
    Hbond: The distance defined as hydrogen bond. The default is 2.0 Å, or, non-bonded atom couples whose distance is less than 2 Å will be defined as hydrogen bond.
    angle: The degree of angle X1HX2 defined as hydrogen bond. The default is 150 degrees.
    mode: The pattern of hydrogen bonds, includes 'all', 'intra' (molecule within one molecule) and 'inter' (molecule between molecules)
    Example:
        Input:
            from MCPoly.status import Hbond
            a = Hbond('Poly1')
        
        Output:
            [[149, 150, 195], [146, 152, 191], [159, 238, 240]]
            --> The middle number (150, 152, 238) is the hydrogen atom number.
    """
    path = os.getcwd()
    os.chdir(loc)
    atoms = read(file+'.xyz')
    atoms_H_bond = []
    atoms_H = []
    angle_group = []
    
    for i, atom in enumerate(atoms):
        if atom.symbol == 'O':
            atoms_H_bond.append(i)
        elif atom.symbol == 'F':
            atoms_H_bond.append(i)
        elif atom.symbol == 'N':
            atoms_H_bond.append(i)
        if atom.symbol == 'H':
            atoms_H.append(i)

    for atom2 in atoms_H:
        distances = atoms.get_distances(atom2, atoms_H_bond)
        targets = np.delete(distances, np.where(distances >= HBond))
        targets.sort()
        pre_angle_group = []
        
        if len(targets) == 2:
            if targets[0] >= 1.2:
                continue
            for i, atom in enumerate(atoms_H_bond):
                distance = atoms.get_distance(atom, atom2)
                if distance in targets:
                    if atom not in angle_group:
                        pre_angle_group.append(atom)
                    pre_angle_group.append(atom2)
            if atoms.get_angle(pre_angle_group[0], pre_angle_group[1],\
                               pre_angle_group[2]) >= angle:
                if mode == 'inter' or mode == 'intra':
                    part1 = molesplit(file, atomnum=pre_angle_group[0], Cfirst=False)
                    if pre_angle_group[2] in part1 and mode == 'inter':
                        continue
                    elif pre_angle_group[2] not in part1 and mode == 'intra':
                        continue
                angle_group.append(pre_angle_group[:3])
    
    os.chdir(path)
    return angle_group