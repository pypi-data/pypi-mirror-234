from ase.io import read
from ase import Atoms
import math as m

def straight(atoms, start, end):
    pos = atoms.get_positions()
    Apos = pos[start]
    Bpos = pos[end]
    atoms.rotate(m.atan((Bpos[-1]-Apos[-1])/(Bpos[1]-Apos[1]))/m.pi*180,\
                      'x', Apos)
    pos = atoms.get_positions()
    Apos = pos[start]
    Bpos = pos[end]
    atoms.rotate(m.atan((Bpos[-1]-Apos[-1])/(Bpos[0]-Apos[0]))/m.pi*180,\
                      'y', Apos)
    pos = atoms.get_positions()
    Apos = pos[start]
    Bpos = pos[end]
    atoms.rotate(m.atan(-(Bpos[1]-Apos[1])/(Bpos[0]-Apos[0]))/m.pi*180+180,\
                      'z', Apos)
    pos = atoms.get_positions()
    return atoms