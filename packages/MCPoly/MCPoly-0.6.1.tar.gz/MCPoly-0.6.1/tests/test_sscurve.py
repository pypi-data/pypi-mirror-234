from MCPoly.sscurve import single
from MCPoly.sscurve import multiple
from MCPoly.sscurve import multiple2
from MCPoly.sscurve import YModulus
import os
import re
import pytest

opath = os.getcwd()
os.chdir('./MCPoly/tests/data_sscurve')
try:
    os.system('rm Polymer1.png')
except:
    pass
try:
    os.system('rm Polymer1_Result.txt')
except:
    pass
try:
    os.system('rm Polymer3.png')
except:
    pass
try:
    os.system('rm Polymer3_Result.txt')
except:
    pass
try:
    os.system('rm Result.csv')
except:
    pass
try:
    os.system('rm Result.png')
except:
    pass
os.chdir(opath)

@pytest.fixture
def single1():
    return single(polymer='Polymer1', loc='./data_sscurve/')

def test_curve1(single1):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    single1.curve(2, 13, savefig=False, savedata=False, saveloc='./data_sscurve/', xx=True)
    i = 1
    for path in os.listdir(single1.loc):
        if os.path.isfile(os.path.join(single1.loc, path)):
            b = re.search('Polymer1_Result.txt', path)
            if b:
                i = 0
            c = re.search('Polymer1.png', path)
            if c:
                i = 0
    os.chdir(opath)
    assert i == 1

def test_autocurve1(single1):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    single1.autocurve(savefig=False, savedata=True, saveloc='./data_sscurve/', xx=True)
    i = 0
    j = 1
    for path in os.listdir(single1.loc):
        if os.path.isfile(os.path.join(single1.loc, path)):
            b = re.search('Polymer1_Result.txt', path)
            if b:
                i = 1
            c = re.search('Polymer1.png',path)
            if c:
                j = 0
    os.chdir(opath)
    assert i * j == 1
    
@pytest.fixture
def single3():
    return single(polymer='Polymer3', loc='./data_sscurve/')

def test_autocurve2(single3):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    single3.autocurve(savefig=False, saveloc='./data_sscurve/', xx=True)
    i = 0
    j = 1
    for path in os.listdir(single3.loc):
        if os.path.isfile(os.path.join(single3.loc, path)):
            b = re.search('Polymer3_Result.txt', path)
            if b:
                i = 1
#            c = re.search('Polymer3.png',path)
#            if c:
#                j = 1
    os.chdir(opath)
    assert i * j == 1
    
def test_multiple1():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    multiple(polymers=['Polymer1', 'Polymer2', 'Polymer3'],\
             loc='./data_sscurve/', savefig=False, savedata=False, xx=True)
    i = 1
    for path in os.listdir('./data_sscurve/'):
        if os.path.isfile(os.path.join('./data_sscurve/', path)):
#            b = re.search('Result.png', path)
#            if b:
#                i = 0
            c = re.search('Result.csv', path)
            if c:
                i = 0
    os.chdir(opath)
    assert i == 1

def test1_multiple2():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    multiple(loc='./data_sscurve/', savefig=False, needYM=False, xx=True)
    i = 1
    j = 0
    k = 1
    for path in os.listdir('./data_sscurve/'):
        if os.path.isfile(os.path.join('./data_sscurve/', path)):
            b = re.search('Result.png', path)
            if b:
                i = 0
            c = re.search('Result.csv', path)
            if c:
                j = 1
            d = re.search('ot.txt', path)
            if d:
                k = 0
    os.chdir(opath)
    assert i * j * k == 1

def test2_multiple2():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/data_sscurve/')
    f = open('Result.csv','r')
    i = 0
    for line in f:
        i = i + 1
    f.close()
    os.chdir(opath)
    assert i == 8

@pytest.fixture
def test_YModulus():
    os.system('rm ./MCPoly/tests/data_sscurve/Polymer1_Result.txt')
    return YModulus('./MCPoly/tests/data_sscurve/Polymer3_Result.txt') + 1

@pytest.fixture
def single1():
    return single(polymer='Polymer1', loc='./data_sscurve/')

def test_curve2(single1):
    os.system('rm ./MCPoly/tests/data_sscurve/Polymer1_Result.txt')
    os.system('rm ./MCPoly/tests/data_sscurve/Polymer1_Result.png')
    os.system('rm ./MCPoly/tests/data_sscurve/Polymer3_Result.txt')
    os.system('rm ./MCPoly/tests/data_sscurve/Result.csv')
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    single1.curve2(2, 13, savefig=False, savedata=False, saveloc='./data_sscurve/', xx=True)
    i = 1
    for path in os.listdir(single1.loc):
        if os.path.isfile(os.path.join(single1.loc, path)):
            b = re.search('Polymer1_Result.txt', path)
            if b:
                i = 0
            c = re.search('Polymer1.png', path)
            if c:
                i = 0
    os.chdir(opath)
    assert i == 1

def test_autocurve3(single1):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    single1.autocurve2(savefig=False, savedata=True, saveloc='./data_sscurve/', xx=True)
    i = 0
    j = 1
    for path in os.listdir(single1.loc):
        if os.path.isfile(os.path.join(single1.loc, path)):
            b = re.search('Polymer1_Result.txt', path)
            if b:
                i = 1
            c = re.search('Polymer1.png',path)
            if c:
                j = 0
    os.chdir(opath)
    assert i * j == 1

@pytest.fixture
def single3():
    return single(polymer='Polymer3', loc='./data_sscurve/')

def test_autocurve4(single3):
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    single3.autocurve2(savefig=False, saveloc='./data_sscurve/', xx=True)
    i = 0
    j = 1
    for path in os.listdir(single3.loc):
        if os.path.isfile(os.path.join(single3.loc, path)):
            b = re.search('Polymer3_Result.txt', path)
            if b:
                i = 1
#            c = re.search('Polymer3.png',path)
#            if c:
#                j = 1
    os.chdir(opath)
    assert i * j == 1
    
def test_multiple5():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    multiple2(polymers=['Polymer1', 'Polymer2', 'Polymer3'],\
              loc='./data_sscurve/', savefig=False, savedata=False, xx=True)
    i = 1
    for path in os.listdir('./data_sscurve/'):
        if os.path.isfile(os.path.join('./data_sscurve/', path)):
#            b = re.search('Result.png', path)
#            if b:
#                i = 0
            c = re.search('Result.csv', path)
            if c:
                i = 0
    os.chdir(opath)
    assert i == 1

def test1_multiple6():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/')
    multiple2(loc='./data_sscurve/', savefig=False, xx=True)
    i = 1
    j = 0
    k = 1
    for path in os.listdir('./data_sscurve/'):
        if os.path.isfile(os.path.join('./data_sscurve/', path)):
            b = re.search('Result.png', path)
            if b:
                i = 0
            c = re.search('Result.csv', path)
            if c:
                j = 1
            d = re.search('ot.txt', path)
            if d:
                k = 0
    os.chdir(opath)
    assert i * j * k == 1

def test2_multiple6():
    opath = os.getcwd()
    os.chdir('./MCPoly/tests/data_sscurve/')
    f = open('Result.csv','r')
    i = 0
    for line in f:
        i = i + 1
    f.close()
    os.chdir(opath)
    assert i == 8