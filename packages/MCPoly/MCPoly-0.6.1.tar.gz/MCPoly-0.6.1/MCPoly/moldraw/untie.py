import os
import sys
import numpy as np
from ase.io import read
from ase import Atoms
import math as m

mydir = os.path.dirname( __file__ )
statusdir = os.path.join(mydir, '..', 'status')
sys.path.append(statusdir)
from status import status

def untie(file1, file2, tolerance=0.015, loc='./', savefile=''):
    """
    A method to see the relative element number of the same conformer after being disordered, and you can also save the relevent file into .xyz format.
    untie(file1, file2, tolerance=0.015, num=-1, loc='./', savefile='')
    file1, file2: File Name.
    tolerance: If some bonds, angles or dihedrals has small changes, you can change it to get better results. The default is 0.015 Å.
    loc: File Location. The default is your current location.
    savefile: The name of the saved file.
    TIPS: Pay attention to tolerance. If it's too small, the result will not show the full result. If it's too big, the result will be inaccurate.
    
    Example:
        Input:
            from MCPoly.moldraw import untie
            result = untie(file1, file2, tolerance=0.015, num=-1, loc='./', savefile='')
            print(result)
        
        Output:
            {0: 0, 1: 15, 2: 16, 3: 17, 4: 18, 5: 19, 6: 20, 7: 21, 8: 22,\
             9: 23, 10: 24, 11: 1, 12: 2, 13: 3, 14: 4, 15: 5, 16: 6, 17: 7,\
             18: 8, 19: 9, 20: 10, 21: 11, 22: 12, 23: 13, 24: 14}
    """
    
    path = os.getcwd()
    os.chdir(loc)
    
    atoms1 = read(file1 + '.xyz')
    atoms2 = read(file2 + '.xyz')
    
    targeted_distances = atoms1.get_distances(0,range(len(atoms1)))
    targeted_distances = np.delete(targeted_distances,\
                                   np.where(targeted_distances <= 1.2))
    elements = atoms1.get_chemical_symbols()
    elements_not_H1 = []
    edge1 = 0
    max_element1 = 0
    max_distances1 = []
    max_all_distances = 0
    
    for i, element in enumerate(elements):
        if element != 'H':
            elements_not_H1.append(i)
    for i in elements_not_H1:
        distances_not_H1 = atoms1.get_distances(i, elements_not_H1)
        all_distances_not_H1 = np.sum(distances_not_H1)
        if all_distances_not_H1 > max_all_distances:
            max_element1 = i
            max_distances1 = distances_not_H1
            max_all_distances = all_distances_not_H1
    for i, distance in enumerate(max_distances1):
        if distance == np.max(max_distances1):
            max_num1 = elements_not_H1[i]
            break
    targeted_distances1 = atoms1.get_distances(max_element1, range(len(atoms1)))

    targeted_distances = atoms2.get_distances(0, range(len(atoms2)))
    targeted_distances = np.delete(targeted_distances,\
                                   np.where(targeted_distances <= 1.2))
    elements = atoms2.get_chemical_symbols()
    elements_not_H2 = []
    edge2 = 0
    max_element2 = 0
    max_distances2 = []
    max_all_distances = 0
    
    for i, element in enumerate(elements):
        if element != 'H':
            elements_not_H2.append(i)
    for i in elements_not_H2:
        distances_not_H2 = atoms2.get_distances(i, elements_not_H2)
        all_distances_not_H2 = np.sum(distances_not_H2)
        if all_distances_not_H2 > max_all_distances:
            max_element2 = i
            max_distances2 = distances_not_H2
            max_all_distances = all_distances_not_H2
    for i, distance in enumerate(max_distances2):
        if distance == np.max(max_distances2):
            max_num2 = elements_not_H2[i]
            break
    targeted_distances2 = atoms2.get_distances(max_element2, range(len(atoms2)))

    result = {}
    for i, distance1 in enumerate(targeted_distances1):
        for j, distance2 in enumerate(targeted_distances2):
            if abs(distance1 - distance2) <= tolerance:
                if j in result.values():
                    continue
                result[i] = j
                break
            result[i] = None
    
    status2 = status(file2).atom()
    
    try:
        if savefile == '':
            f = open('{0}_untied.xyz'.format(file2), 'x')
        else:
            f = open('{0}.xyz'.format(savefile), 'x')
    except:
        if savefile == '':
            f = open('{0}_untied.xyz'.format(file2), 'w')
        else:
            f = open('{0}.xyz'.format(savefile), 'w')
    f.write('{0}\n\n'.format(len(status2)))
    for i in range(len(status2)):
        j = result[i]
        f.write('{0} {1:.5f} {2:.5f} {3:.5f}\n'.format(*status2[j]))
    f.close()
    
    os.chdir(path)
    
    return result