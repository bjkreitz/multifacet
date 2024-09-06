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

syst = read('initial.traj')
syst.set_initial_magnetic_moments([1.5]*len(syst))

from vasp_interactive import VaspInteractive

def run_vasp_interactive():
        """Relaxation using interactive VASP"""
        print("*" * 40)
        print("Running relaxation using VaspInteractive")
        print("*" * 40)

        calc = VaspInteractive(
                xc='beef-vdw',
                luse_vdw = True,
                zab_vdw = -1.8867,
                encut=544.228, #40Ry
                kpts=(5,5,1),
                ismear=1,
                sigma=0.1,
                ibrion=-1,
                ispin=2,
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
                dyn.run(fmax=0.01)


if __name__=="__main__":
        run_vasp_interactive()

