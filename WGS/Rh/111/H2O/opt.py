#!/bin/sh
from ase import Atoms, Atom
from ase.io.trajectory import Trajectory
from ase.optimize import BFGS
import numpy as np
from ase.constraints import FixAtoms, FixBondLength
from ase.visualize import view
import os
from ase.build import fcc111,fcc110,fcc100,hcp0001,add_adsorbate,molecule,rotate
from ase.spacegroup import crystal
from sys import path
from ase.io import read,write
from ase.vibrations import Vibrations

import glob

for filename in glob.iglob('*.traj'):
    syst=read(filename)

b=list([37,43,49,19,25,31,1,7,13,38,44,50,20,26,32,2,8,14])
for i in sorted(b, reverse=True):
    del syst[i]

from vasp_interactive import VaspInteractive

def run_vasp_interactive():
        """Relaxation using interactive VASP"""
        print("*" * 40)
        print("Running relaxation using VaspInteractive")
        print("*" * 40)

        calc = VaspInteractive(
                xc='pbe',
                encut=544.228, #40Ry
                kpts=(5,5,1),
                ismear=1,
                sigma=0.1,
                ibrion=-1,
                algo='Fast',
                lreal='Auto',
                ediff=1e-6,
                nelm=100,
                ncore=8,
                isym=0,
                )
        with calc:
                syst.calc = calc
                dyn = BFGS(syst, trajectory='final.traj')
                dyn.run(fmax=0.05)

if __name__=="__main__":
        run_vasp_interactive()
