#! /bin/bash
module purge
module load autoload python/3.5.0 numpy/1.10.1--python--3.5.0 mkl
module load autoload intelmpi/5.0.1--binary netcdff/4.4.2--intel--cs-xe-2015--binary
export LD_LIBRARY_PATH=/pico/scratch/userexternal/epascolo/scipy/lib/python3.5/site-packages/scipy/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/pico/scratch/userexternal/epascolo/scipy/lib/python3.5/site-packages/:$PYTHONPATH
source /pico/scratch/userexternal/epascolo/BFM_work/env_co2call/bin/activate
