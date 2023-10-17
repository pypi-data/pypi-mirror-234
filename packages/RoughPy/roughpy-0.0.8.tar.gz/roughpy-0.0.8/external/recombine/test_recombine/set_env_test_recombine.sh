#!/bin/bash -e
# $1: directory containing installed recombine library, relative to recombine installation folder
# (typically /lib or /lib64)

libpath="${PWD}/../$1"
if [ -d $libpath ]
then
   echo "Prefixing LD_LIBRARY_PATH with $libpath"
   export LD_LIBRARY_PATH=$libpath:$LD_LIBRARY_PATH
   export OMP_DISPLAY_ENV="FALSE"
   export OMP_DYNAMIC="TRUE"
   export OMP_MAX_ACTIVE_LEVELS="3"
   export OMP_NUM_THREADS="2"
else
    echo "Error: Directory $libpath does not exist."
fi
