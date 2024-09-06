#!/bin/sh
from ase import Atoms, Atom
from ase.io.trajectory import Trajectory
from ase.calculators.vasp import Vasp
import numpy as np
from ase.constraints import FixAtoms, FixBondLength
from ase.visualize import view
import os
from ase.build import hcp0001,add_adsorbate,molecule,rotate
from ase.spacegroup import crystal
from sys import path
from ase.io import read,write
from ase.vibrations import Vibrations

syst=read('final.traj',index=-1)

from vasp_interactive import VaspInteractive

calc = VaspInteractive(
		xc='beef-vdw',
     		encut=544, #40Ry
     		luse_vdw=True,
     		zab_vdw=-1.8867,
     		kpts=(5,5,1),
     		ismear=1,
     		sigma=0.1,
     		ibrion=-1,
     		algo='Fast',
     		lreal='Auto',
     		ediff=1e-7,
     		isym=0,
                ncore=8,
                nelm=100,
)
syst.calc = calc

from ase.vibrations import Vibrations

no_slab=36
total=syst.get_global_number_of_atoms()

adsorbate=list(np.arange(no_slab,total,1))

vib = Vibrations(syst,indices=adsorbate)
vib.run()
vib.summary(log='vib.log')
vib.write_mode() #write modes to traj file
vib.clean()
