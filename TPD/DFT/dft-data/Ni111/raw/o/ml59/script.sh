#!/usr/bin/env bash
#SBATCH --job-name=Ni111_o59
#SBATCH --time=100:00:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=48
#SBATCH --partition=batch
#SBATCH --mem=80G
##SBATCH --account=cfgoldsm-condo
#SBATCH --cpus-per-task=1
#SBATCH --exclude=node1832
#SBATCH --constraint=48core

#############################################################################
unset PYTHONPATH
export PYTHONPATH=/users/bkreitz1/anaconda/finetuna/lib/python3.9/site-packages:$PYTHONPATH

module load miniconda3/23.11.0s
source /oscar/runtime/software/external/miniconda3/23.11.0/etc/profile.d/conda.sh

module load vasp-mpi/6.4.2_cfgoldsm-7krhcss
conda activate /users/bkreitz1/anaconda/finetuna

export ASE_VASP_VDW=/oscar/runtime/software/external/vasp/6.4.2_cfgoldsm/source/
export VASP_PP_PATH=$HOME/vasp/mypps_5.4/

export OMP_PROC_BIND=close
export OMP_PLACES=cores
export OMP_STACKSIZE=512m
export OMP_NUM_THREADS=1

export ASE_VASP_COMMAND="mpirun -np 32 --bind-to core --report-bindings vasp_std"

python3 vib.py
