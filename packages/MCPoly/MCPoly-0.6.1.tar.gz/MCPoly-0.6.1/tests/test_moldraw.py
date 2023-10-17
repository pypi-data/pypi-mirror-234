from MCPoly.moldraw import molecule
import pytest
import os
import re

@pytest.fixture
def object_moldraw1():
    return molecule('Bu', loc='./MCPoly/tests/data_moldraw/')

def test_rectify1(object_moldraw1):
    return object_moldraw1.sub('Cl', 6)

def test_rectify3(object_moldraw1):
    return object_moldraw1.bind(6, [2,3])

def test_rectify3(object_moldraw1):
    return object_moldraw1.C('CO', 2)

#def test_geoview(object_moldraw):
#    return object_moldraw.geoview()

def test_conformer1(object_moldraw1):
    return object_moldraw1.conformer(must=True)

def test_conformer2(object_moldraw1):
    object_moldraw1.conformer(lowenergy=1.2, must=True)
    assert object_moldraw1.energy < 1.2

def test_conformer3(object_moldraw1):
    object_moldraw1.conformer(highenergy=1.2, must=True)
    assert object_moldraw1.energy > 1.2

@pytest.fixture
def object_moldraw2():
    return molecule('test1', loc='./MCPoly/tests/data_moldraw/')

def test1_untie(object_moldraw2):
    result = object_moldraw2.untie('test2', tolerance=0.012, savefile='test3')
    assert result[0] == 0

def test2_untie(object_moldraw2):
    result = object_moldraw2.untie('test2', tolerance=0.012, savefile='test3')
    assert result[6] == 20
    
def test3_untie(object_moldraw2):
    result = object_moldraw2.untie('test2', tolerance=0.012, savefile='test3')
    assert result[20] == 10

def test4_untie(object_moldraw2):
    f = open('./MCPoly/tests/data_moldraw/test3.xyz', 'r')
    x1 = 0
    x2 = 0
    x3 = 0
    for line in f:
        a1 = re.search('25\n', line)
        if a1:
            x1 = 1
        a2 = re.search('C 0.38700 1.09300 2.23900', line)
        if a2:
            x2 = 1
        a3 = re.search('O 5.07300 1.80600 1.39600', line)
        if a3:
            x3 = 1
    f.close()
    assert x1 * x2 * x3 == 1