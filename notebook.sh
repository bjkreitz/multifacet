#!/usr/bin/env bash
#SBATCH --job-name=tunel
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem=60GB
##SBATCH --account=cfgoldsm-condo
#SBATCH --output jupyter-log-%J.txt

## get tunneling info
XDG_RUNTIME_DIR=""
ipnport=$(shuf -i8000-9999 -n1)
ipnip=$(hostname -i)
## print tunneling instructions to jupyter-log-{jobid}.txt
echo -e "
    Copy/Paste this in your local terminal to ssh tunnel with remote
    -----------------------------------------------------------------
    ssh -N -L $ipnport:$ipnip:$ipnport $USER@sshcampus.ccv.brown.edu
    -----------------------------------------------------------------
    Then open a browser on your local machine to the following address
    ------------------------------------------------------------------
    localhost:$ipnport  (prefix w/ https:// if using password)
    ------------------------------------------------------------------
    "
## start an ipcluster instance and launch jupyter server

unset PYTHONPATH
export PYTHONPATH=/users/bkreitz1/.conda/envs/ct-env/lib/python3.10/site-packages:$PYTHONPATH


module load miniconda3/23.11.0s
source /oscar/runtime/software/external/miniconda3/23.11.0/etc/profile.d/conda.sh
conda activate ct-env

/users/bkreitz1/.conda/envs/ct-env/bin/jupyter-notebook --no-browser --port=$ipnport --ip=$ipnip
