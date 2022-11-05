#!/bin/bash

for dm in 0 0.05 0.1 0.2 0.3 0.4
do
  for hx in 0 0.5 1 1.5 2 2.5
  do
    subdir="no1/$dm/$hx"
    mkdir -p $subdir
    cp runjob.sh $subdir/
    pushd $subdir
    qsub -v DM=$dm,HX=$hx runjob.sh
    popd
  done
done
