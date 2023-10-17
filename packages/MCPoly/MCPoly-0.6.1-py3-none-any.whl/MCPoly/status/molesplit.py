import os
from ase.io import read
from ase import Atoms
import numpy as np
import sys

mydir = os.path.dirname( __file__ )
lmpdir = os.path.join(mydir, '..', 'lmpset')
sys.path.append(lmpdir)
from DataToXyz import DataToXyz

def near(atomnum, atoms, tolerance=2.000, Cfirst=True):
    atoms_not_H = []
    for i, atom in enumerate(atoms):
        if atom.symbol != 'H':
            atoms_not_H.append(i)
    mole = [atomnum]
    pre_distances = atoms.get_distances(atomnum, atoms_not_H)
    distances = np.delete(pre_distances, np.where(pre_distances >= tolerance))
    distances = np.delete(distances, np.where(distances == 0))
    distances.sort()
    length = len(distances)
    if length > 4:
        distances = distances[:4]
    for i, atom in enumerate(atoms_not_H):
        distance = atoms.get_distance(atom, atomnum)
        if distance in distances:
            mole.append(atom)
    mole_C = []
    mole_other = []
    for num in mole:
        if atoms[num].symbol == 'C':
            mole_C.append(num)
        else:
            mole_other.append(num)
    if Cfirst == True:
        return mole_C + mole_other
    else:
        return mole_other + mole_C

def molesplit(file, loc='./', atomnum=0, tolerance=2.000, withH=False,\
              form='XYZ', Cfirst=True):
    '''
        A method to find out the atoms belong to one molecule in a molecule system.
        You can also know the head and the tail of the moelcule if it's a polymer chain.
        molesplit(file, loc='./', atomnum=0, tolerance=2.000, withH=False,\
               form='XYZ')
        files: The name of ORCA output files already calculated.
        loc: File Location. The default is your current location.
        atomnum: The atom number on the molecule needed.
        tolerance: The best distance between atoms defined as a bond. The default is 2.000 Å.
        withH: Use it to include the atom of hydrogen in this molecule. The default is false.
        form: the format of the file, including 'XYZ' and 'LAMMPSDATA' (.data) file. The default is 'XYZ'.
        Example 1:
            Input:
                from MCPoly.status import molesplit
                molesplit('PolySystem1', atomnum=238)
            Output:
                [238, 235, 234, 213, 212, 216, 215, 210, 220, 219, 207, 203, 175, 176, 186, 172, 168, 184,\
                 169, 171, 173, 162, 167, 166, 164, 149, 163, 147, 145, 144, 142, 95, 94, 99, 101, 92, 91,\
                 55, 50, 46, 44, 47, 48, 49, 41, 40, 66, 38, 69, 37, 59, 62, 65, 14, 60, 15, 16, 12, 10, 4,\
                 9, 1, 19, 26, 28, 32] --> All non-H atom belong to the molecule with atom 238
        
        Example 2:
            Input:
                from MCPoly.status import molesplit
                molesplit('PolySystem1', atomnum=238, withH=True)
            Output:
                [238, 235, 234, 213, 212, 216, 215, 210, 220, 219, 207, 203, 175, 176, 186, 172, 168, 184,\
                 169, 171, 173, 162, 167, 166, 164, 149, 163, 147, 145, 144, 142, 95, 94, 99, 101, 92, 91,\
                 55, 50, 46, 44, 47, 48, 49, 41, 40, 66, 38, 69, 37, 59, 62, 65, 14, 60, 15, 16, 12, 10, 4,\
                 9, 1, 19, 26, 28, 32, 237, 262, 263, 236, 211, 217, 227, 258, 214, 223, 218, 224, 188, 208,\
                 196, 185, 170, 177, 187, 174, 103, 104, 165, 151, 146, 148, 137, 150, 140, 102, 138, 90,\
                 93, 98, 100, 96, 97, 89, 56, 88, 52, 53, 45, 51, 43, 54, 39, 42, 80, 35, 36, 61, 64, 68,\
                 13, 17, 11, 6, 0, 8, 18, 30, 27, 25, 31, 33] --> All atoms belong to the molecule with atom 238
                 
        Example 3:
            Input:
                from MCPoly.status import molesplit
                mole = molesplit('PolySystem1', atomnum=1, withH=True)
                print(mole)
                mole2 = molesplit('PolySystem1', atomnum=mole[-1])
                print(mole2)
                mole3 = molesplit('PolySystem1', atomnum=mole2[-1])
                print(mole3)
            Output:
                [1, 4, 19, 10, 26, 9, 12, 28, 16, 32, 15, 60, 14, 62, 65, 37, 59, 38, 66, 40, 69, 41, 49,\
                 48, 44, 46, 47, 50, 55, 91, 92, 101, 99, 94, 95, 142, 144, 145, 147, 149, 164, 163, 166,\
                 167, 162, 171, 169, 168, 173, 172, 184, 186, 175, 176, 203, 207, 219, 220, 215, 210, 216,\
                 212, 213, 234, 235, 238]
                [238, 235, 234, 213, 212, 216, 215, 210, 220, 219, 207, 203, 175, 176, 186, 172, 168, 184,\
                 169, 171, 173, 162, 167, 166, 164, 149, 163, 147, 145, 144, 142, 95, 94, 99, 101, 92, 91,\
                 55, 50, 46, 44, 47, 48, 49, 41, 40, 66, 38, 69, 37, 59, 62, 65, 14, 60, 15, 16, 12, 10,\
                 4, 9, 1, 19, 26, 28, 32]
                [32, 28, 26, 19, 1, 4, 10, 9, 12, 16, 15, 60, 14, 62, 65, 37, 59, 38, 66, 40, 69, 41, 49,\
                 48, 44, 46, 47, 50, 55, 91, 92, 101, 99, 94, 95, 142, 144, 145, 147, 149, 164, 163, 166,\
                 167, 162, 171, 169, 168, 173, 172, 184, 186, 175, 176, 203, 207, 219, 220, 215, 210, 216,\
                 212, 213, 234, 235, 238]
            ### In this way, we can know the head and the tail of the polymer is 32 and 238!
    '''
    opath = os.getcwd()
    os.chdir(loc)
    if form == 'XYZ':
        atoms = read(file+'.xyz')
    elif form == 'LAMMPSDATA':
        DataToXyz(file)
        atoms = read(file+'.xyz')
    atoms_not_H = []
    atoms_H = []
    for i, atom in enumerate(atoms):
        if atom.symbol != 'H':
            atoms_not_H.append(i)
        else:
            atoms_H.append(i)
    mole = near(atomnum, atoms, tolerance=tolerance, Cfirst=Cfirst)
    i = 1
    while 1:
        molefrag = near(mole[i], atoms, tolerance=tolerance, Cfirst=Cfirst)
        for num in molefrag:
            if num not in mole:
                mole.append(num)
        i = i + 1
        try:
            mole[i] == mole[-1]
        except:
            break
    if withH == True:
        mole_H = []
        for atom in mole:
            pre_distances = atoms.get_distances(atom, atoms_H)
            distances = np.delete(pre_distances, np.where(pre_distances >= 1.2))
            for H in atoms_H:
                distance = atoms.get_distance(H, atom)
                if distance in distances:
                    mole_H.append(H)
        mole = mole + mole_H
    if form == 'LAMMPSDATA':
        os.system('rm {0}.xyz'.format(file))
    os.chdir(opath)
    return mole