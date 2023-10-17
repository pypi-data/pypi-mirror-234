from MCPoly.orcaset import XyzToInp
from MCPoly.orcaset import orca
from MCPoly.orcaset import ssorca
from MCPoly.orcaset import multiorca
import os
import re
import pytest

def test_XyzToInp2():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    loc = './data_orcaset/'
    file = 'Atoms1'
    XyzToInp(file, fileloc=loc, saveloc=loc, method='B3LYP', basis_set='def2-TZVP', freq=True,\
            external_force=True, aim=[0, 3], strain=1.5, maxcore=4096, corenum=7)
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    f = open(loc+file+'.inp', 'r')
    for line in f:
        a = re.search(r'B3LYP def2-TZVP OPT FREQ', line)
        if a:
            i1 = 1
        b = re.search(r'maxcore 4096', line)
        if b:
            i2 = 1
        c = re.search('%PAL NPROCS 7 END', line)
        if c:
            i3 = 1
        d1 = re.search(r'POTENTIALS', line)
        if d1:
            i4 = 1
        d2 = re.search('{C 0 3 1.500}', line)
        if d2:
            i5 = 1
            break
    f.close()
    os.chdir(opath)
    assert i1 * i2 * i3 * i4 * i5 != 0

def test_XyzToInp3():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    file = 'Atoms1'
    loc = './data_orcaset/'
    XyzToInp(file, fileloc=loc, saveloc=loc, method='B3LYP', basis_set='def2-TZVP', scan = True, \
            aim=[0, 3], stretch=0.8, scanstep=8, maxcore=4096, corenum=8)
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    f = open(loc+file+'.inp', 'r')
    for line in f:
        a = re.search(r'B3LYP def2-TZVP', line)
        if a:
            i1 = 1
        b = re.search(r'maxcore 4096', line)
        if b:
            i2 = 1
        c = re.search('%PAL NPROCS 8 END', line)
        if c:
            i3 = 1
        d1 = re.search(r'geom Scan', line)
        if d1:
            i4 = 1
        d2 = re.search('B 0 3 = 3.804,  4.604,  8', line)
        if d2:
            i5 = 1
            break
    f.close()
    os.chdir(opath)
    assert i1 * i2 * i3 * i4 * i5 != 0

def test_XyzToInp4():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    file = 'Atoms1'
    loc = './data_orcaset/'
    XyzToInp(file, fileloc=loc, saveloc=loc, method='B3LYP D3BJ', basis_set='def2-TZVP',\
                     MD=True, freq=True, md_timestep=1.0, initvel=350,\
             tsNHC=350, dumpcon=25, runstep=2500, maxcore=4096, corenum=8)
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    f = open(loc+file+'.inp', 'r')
    for line in f:
        print(line)
        a = re.search(r'MD B3LYP D3BJ def2-TZVP', line)
        if a:
            i1 = 1
        b = re.search(r'maxcore 4096', line)
        if b:
            i2 = 1
        c = re.search('%PAL NPROCS 8 END', line)
        if c:
            i3 = 1
        d1 = re.search(r'Timestep 1.0_fs', line)
        if d1:
            i4 = 1
        d2 = re.search('Dump Position Stride 25 Filename "Atoms1_dump.xyz"', line)
        if d2:
            i5 = 1
        d3 = re.search('Run 2500', line)
        if d3:
            i6 = 1
    f.close()
    os.chdir(opath)
    assert i1 * i2 * i3 * i4 * i5 * i6 != 0

def test_XyzToInp1():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    file = 'Atoms1'
    loc = './data_orcaset/'
    XyzToInp(file, fileloc = loc, saveloc = loc)
    i = 0
    j = 0
    f = open(loc+file+'.inp', 'r')
    for line in f:
        a = re.search(r'B3LYP def2-SVP', line)
        if a:
            i = 1
        b = re.search(r'xyz 0 1', line)
        if b:
            j = 1
            break
    f.close()
    os.chdir(opath)
    assert i * j != 0

def test_ORCA():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    file = 'Atoms1'
    loc = './data_orcaset/'
    orca(file, fileloc=loc, saveloc=loc)
    os.chdir(opath)
    return 0

@pytest.fixture
def suite():
    return multiorca(['Atoms1', 'Atoms2'], loc = './data_orcaset/')

def test_multiorca(suite):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    suite.run()
    os.chdir(opath)
    return 0

def object_ssorca():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    ssorca('Atoms3', loc = './data_orcaset/')
    os.chdir(opath)
    return 0

#def test_ssORCA(object_ssorca):
#    return ssorca(file3, loc=loc)