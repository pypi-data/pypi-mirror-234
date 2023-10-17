# MCPoly
Some methods to deal with some manipulation of computational chemistry, mostly about mechanical properties of polymers.
![](./reference/function.png)

## Overview
`MCPoly` is a Python library to make some steps of computational chemistry easier. It includes some functions of drawing molecule structures, creating proper .xyz , .inp , .mol and .data file, which specialised for using ORCA and LAMMPS, and some functions for researching the mechanical property of some polymers.

## Updated in v0.6.1(11.10.23)
1. Add molesplit function in 'status' package to judge the location of the atom.
2. Add Hbond function in 'status' package to count the number of hydrogen bonds.

## Updated in v0.6.0(08.08.23)
1. Standardise the package to fit PEP 8 style, so 'DATAtoXYZ' is changed into 'DataToXyz', 'DATAtomolTXT' is changed into 'DataToMolTxt', 'XYZtoINP' is changed into 'XyzToInp'.
2. Add special functions about Molecular Dynamic functions in ORCA.
3. Fix some bugs about ORCA Calculations Settings.
4. Fix some bugs about ORCA GUI display.
5. Fix some bugs about judging the maximum iteration of atoms.
6. Fix some bugs about save .xyz file in ORCA GUI.
7. Fix some bugs about selecting files in ComboBox by file location.
8. Add special functions 'untie' to tidy up your molecule number.

## Updated in v0.5.1.3(29.06.23)
1. Add 'rebuild' in 'lmpset' package. You can now use it to rebuild geometry structure of LAMMPS input data now.
2. Add 'DATAtoXYZ' in 'lmpset' package to convert LAMMPS Data File into XYZ File
3. Add 'DATAtomolTXT' to convert LAMMPS Data File into LAMMPS Molecule Text File.
4. All these functions can be used by lmpset.mould().XXX() now.
5. Fix some bugs about ORCA Calculations Settings.
6. Fix some bugs about ORCA GUI display.
7. Fix some bugs about judging the maximum iteration of atoms.

## Updated in v0.4.2.3(12.06.23)
1. BIG UPDATE: Molecule Designer GUI is included in this package. You can now use it to draw molecule with 3D view at the same time.
<img src="https://github.com/Omicron-Fluor/MCPoly/blob/main/reference/moldraw_gui.png">
2. Add 'chain' in 'lmpset' package. You can now use it to convert periodic polymer structure input data now.
3. Fix some bugs about ORCA Calculations.
4. Fix some bugs about calculating stress-strain curve.

## Functions for ORCA
<img src="https://github.com/Omicron-Fluor/MCPoly/blob/main/reference/ORCA.png" width="400" height="263" >

### orcaset
Used to create ORCA input files and run it on ORCA. It's especially handy for researching mechanical property of polymers.

### status
Because we can't use ORCA to visualize the geometry structure, this command can be used to see the optimisation status and the trait of geometry structure.

### view3d
See the 3D structure of a normal .xyz file.

### sscurve
With calculated .xyz file, we can draw the stress-strain curve of each polymer, and we can also calculate the Young's modulus of relevant polymers.

### moldraws (Under Construction)
Used to build a simple molecule and save it under .xyz form.

## Functions for LAMMPS
<img src="https://github.com/Omicron-Fluor/MCPoly/blob/main/reference/LAMMPS.png" width="395" height="100" >

### lmpset
Used to draw special patterns of polymers. Mostly in grids.

## Installation
To get `MCPoly`, you can install it with pip:
    `$ pip install MCPoly`

If you want to get the latest version of `MCPoly`, you can see the latest release here:

<https://github.com/Omicron-Fluor/MCPoly/release> 

There will be a corresponding release on `pip` for each release on GitHub, and you can update your `MCPoly` with:

`$ pip install MCPoly --upgrade`

## How to cite
<https://github.com/Omicron-Fluor/MCPoly>

## Outlook
We will add some new function about polymers based on ReaxFF.
