#!/bin/bash

expdir="no1_fast"

mkdir -p "${expdir}"
cp simulation.py ${expdir}


for temp in 0.1 1 2 4 8 16 32 64 128
do
  for dm in 0 0.1 0.5 1.5
  do
    for hz in 0.0 0.0005 0.001 0.002 0.004 0.01 0.02 0.03 0.1
    do
      hx=0
      subdir="${expdir}/${dm}_${hz}_${temp}"
      mkdir -p $subdir
      cp runjob.sh $subdir/
      pushd $subdir
      qsub -v DM=$dm,HX=$hx,HZ=$hz,TEMP=$temp runjob.sh
      popd
    done
  done
done