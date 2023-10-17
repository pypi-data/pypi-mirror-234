from MCPoly.lmpset import mould
import re
import os
import pytest

@pytest.fixture
def atoms():
    return mould('Poly1', loc='./data_lmpset/')

def test_cube(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.cube(6, 5, 6, 5, 3, 5)
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly1_663.data', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    i8 = 0
    i9 = 0
    for line in fl:
        a = re.search('972 atoms', line)
        if a:
            i1 = 1
        b = re.search('1404 angles', line)
        if b:
            i2 = 1
        c = re.search('432 impropers', line)
        if c:
            i3 = 1
        d = re.search('4 atom types', line)
        if d:
            i4 = 1
        e = re.search('4 bond types', line)
        if e:
            i5 = 1
        f = re.search('4 dihedral types', line)
        if f:
            i6 = 1
        g = re.search('0.00000 53.32948 xlo xhi', line)
        if g:
            i7 = 1
        h = re.search('0.00000 54.87382 ylo yhi', line)
        if h:
            i8 = 1
        i = re.search('0.00000 26.46613 zlo zhi', line)
        if i:
            i9 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 * i7 * i8 * i9 != 0

@pytest.fixture
def atoms():
    return mould('Poly1', loc='./data_lmpset/')

def test_brick_xy(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.brick(6, 5, 6, 5, 4, 5, xpattern='y')
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly1_664_brickxy.data', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    i8 = 0
    i9 = 0
    for line in fl:
        a = re.search('1188 atoms', line)
        if a:
            i1 = 1
        b = re.search('1056 bonds', line)
        if b:
            i2 = 1
        c = re.search('1584 dihedrals', line)
        if c:
            i3 = 1
        d = re.search('4 atom types', line)
        if d:
            i4 = 1
        e = re.search('5 angle types', line)
        if e:
            i5 = 1
        f = re.search('1 improper types', line)
        if f:
            i6 = 1
        g = re.search('0.00000 53.32948 xlo xhi', line)
        if g:
            i7 = 1
        h = re.search('0.00000 54.87382 ylo yhi', line)
        if h:
            i8 = 1
        i = re.search('0.00000 36.95484 zlo zhi', line)
        if i:
            i9 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 * i7 * i8 * i9 != 0

@pytest.fixture
def atoms():
    return mould('Poly1',loc='./data_lmpset/')

def test_brick_yz(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.brick(6, 5, 6, 5, 4, 5, ypattern='z')
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly1_664_brickyz.data', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    i8 = 0
    i9 = 0
    for line in fl:
        a = re.search('1134 atoms', line)
        if a:
            i1 = 1
        b = re.search('1008 bonds', line)
        if b:
            i2 = 1
        c = re.search('1512 dihedrals', line)
        if c:
            i3 = 1
        d = re.search('4 atom types', line)
        if d:
            i4 = 1
        e = re.search('5 angle types', line)
        if e:
            i5 = 1
        f = re.search('1 improper types', line)
        if f:
            i6 = 1
        g = re.search('0.00000 53.32948 xlo xhi', line)
        if g:
            i7 = 1
        h = re.search('0.00000 54.87382 ylo yhi', line)
        if h:
            i8 = 1
        i = re.search('0.00000 36.95484 zlo zhi', line)
        if i:
            i9 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 * i7 * i8 * i9 != 0

@pytest.fixture
def atoms():
    return mould('Poly1', loc='./data_lmpset/')

def test_brick_zx(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.brick(6, 5, 6, 5, 4, 5, zpattern='x')
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly1_664_brickzx.data', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    i8 = 0
    i9 = 0
    for line in fl:
        a = re.search('1188 atoms', line)
        if a:
            i1 = 1
        b = re.search('1056 bonds', line)
        if b:
            i2 = 1
        c = re.search('1584 dihedrals', line)
        if c:
            i3 = 1
        d = re.search('4 atom types', line)
        if d:
            i4 = 1
        e = re.search('5 angle types', line)
        if e:
            i5 = 1
        f = re.search('1 improper types', line)
        if f:
            i6 = 1
        g = re.search('0.00000 53.32948 xlo xhi', line)
        if g:
            i7 = 1
        h = re.search('0.00000 54.87382 ylo yhi', line)
        if h:
            i8 = 1
        i = re.search('0.00000 36.95484 zlo zhi', line)
        if i:
            i9 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 * i7 * i8 * i9 != 0

@pytest.fixture
def atoms():
    return mould('Poly2', loc='./data_lmpset/')

def test_DataToXyz(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.DataToXyz()
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly2.xyz', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    for line in fl:
        a = re.match('9', line)
        if a:
            i1 = 1
        b = re.search('C       -6.94821584       1.31130517      -1.06055707', line)
        if b:
            i2 = 1
        c = re.search('H       -7.85312000       0.69751000      -1.04387000', line)
        if c:
            i3 = 1
        d = re.search('O       -4.55939129       1.28068339      -1.05975265', line)
        if d:
            i4 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 != 0

@pytest.fixture
def atoms():
    return mould('Poly1', loc='./data_lmpset/')

def test1_DataToMolTxt(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.DataToMolTxt(savename='Poly1_1')
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly1_1.txt', 'r')
    i1 = 0
    i2 = 0
    i3 = 1
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    i8 = 0
    i9 = 0
    i10 = 0
    for line in fl:
        a = re.search('9 atoms', line)
        if a:
            i1 = 1
        b = re.search('12 dihedrals', line)
        if b:
            i2 = 1
        c = re.search('5 angle types', line)
        if c:
            i3 = 0
        d = re.search('Coords', line)
        if d:
            i4 = 1
        e = re.search('Types', line)
        if e:
            i5 = 1
        f = re.search('Charges', line)
        if f:
            i6 = 1
        g = re.search('Bonds', line)
        if g:
            i7 = 1
        h = re.search('Angles', line)
        if h:
            i8 = 1
        i = re.search('Dihedrals', line)
        if i:
            i9 = 1
        j = re.search('Impropers', line)
        if j:
            i10 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 * i7 * i8 * i9 * i10 != 0

def test2_DataToMolTxt(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.DataToMolTxt(types={1:11}, savename='Poly1_3')
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly1_3.txt', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    for line in fl:
        a = re.match('2 11', line)
        if a:
            i1 = 1
        b = re.match('5 2', line)
        if b:
            i2 = 1
        c = re.match('9 4', line)
        if c:
            i3 = 1
    fl.close()
    assert i1 * i2 * i3 != 0

@pytest.fixture
def atoms():
    return mould('Poly2', loc='./data_lmpset/')

def test_infchain(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.infchain(3)
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly2_Chain.data', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    for line in fl:
        a = re.search('7 atoms', line)
        if a:
            i1 = 1
        b = re.search('9 angles', line)
        if b:
            i2 = 1
        c = re.search('2 impropers', line)
        if c:
            i3 = 1
        d = re.search('4 bond types', line)
        if d:
            i4 = 1
        e = re.search('4 dihedral types', line)
        if e:
            i5 = 1
        f = re.search('7 3 5 1', line)
        if f:
            i6 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 != 0

def test_chain(atoms):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.chain(3, 5)
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly2_5x.data', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    for line in fl:
        a = re.search('37 atoms', line)
        if a:
            i1 = 1
        b = re.search('36 bonds', line)
        if b:
            i2 = 1
        c = re.search('49 angles', line)
        if c:
            i3 = 1
        d = re.search('5 angle types', line)
        if d:
            i4 = 1
        e = re.search('4 dihedral types', line)
        if e:
            i5 = 1
        f = re.match('12 2 14 10', line)
        if f:
            i6 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 != 0

@pytest.fixture
def atoms3():
    return mould('Poly3', loc='./data_lmpset/')

def test_rebuild(atoms3):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms3.rebuild('Poly3_re', x=[-50, 50], y=[-50, 50], z=[-50, 50],\
                   subloc='./data_lmpset/')
    os.chdir(opath)
    fl = open('./MCPoly/tests/data_lmpset/Poly3.data', 'r')
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    for line in fl:
        a = re.search('-50.00000   50.00000 xlo xhi', line)
        if a:
            i1 = 1
        b = re.search('-50.00000   50.00000 ylo yhi', line)
        if b:
            i2 = 1
        c = re.search('-50.00000   50.00000 zlo zhi', line)
        if c:
            i3 = 1
        d = re.search('2 1 2  0.7694    9.97863    4.59047    2.66070', line)
        if d:
            i4 = 1
        e = re.search('10 1 7  0.1191   11.55624    6.78551    3.42033', line)
        if e:
            i5 = 1
        f = re.search('73 1 8 -0.4064   19.29389    5.70762    2.26849', line)
        if f:
            i6 = 1
            break
    fl.close()
    assert i1 * i2 * i3 * i4 * i5 * i6 != 0