import numpy as np
from ocpapi import find_adsorbate_binding_sites, keep_slabs_with_miller_indices
import ase
import asyncio
from ase import Atoms, Atom
from ase.io.trajectory import Trajectory
import os


species_list = ['*H', '*CO', '*OH2', '*OH', '*O', '*COOH', '*OCHO', '*C', 
                '*CH', '*CH2', '*CH3', '*CHO']
name_list = ['H', 'CO', 'H2O', 'OH', 'O', 'COOH', 'HCOO', 'C',
              'CH', 'CH2', 'CH3', 'CHO']
keep_n = 4

for name, species in enumerate(species_list):
    results = asyncio.run(find_adsorbate_binding_sites(
        adsorbate=species,
        bulk="mp-74",
        adslab_filter=keep_slabs_with_miller_indices([(1, 1, 0)]),
    ))
    E_list = []
    atoms_list = []
    for i in range(len(results.slabs[0].configs)):
        ase_atoms = results.slabs[0].configs[i].to_ase_atoms()
        E_list.append(ase_atoms.get_potential_energy())
        atoms_list.append(ase_atoms)
    indx = sorted(range(len(E_list)), key=lambda sub: E_list[sub])[:keep_n]
    os.mkdir(name_list[name])
    for i in indx:
            traj = Trajectory(name_list[name] + '/' + str(i) + '.traj','w')
            traj.write(atoms_list[i])
