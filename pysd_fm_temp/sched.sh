#!/bin/bash

expdir="no7_init3"

mkdir -p "${expdir}"
cp simulation.py ${expdir}


for temp in 0.01 1 16 64 128
# for temp in 0.01 64
do
  for dm in 0 0.1 0.2 0.5 1.5
  # for dm in 0 1.5
  do
    for hz in 0.0 0.0001 0.0002 0.0003 0.0004 0.0005 0.0006 0.0007 0.0008 0.0009 0.001 0.0012 0.0014 0.0016 0.0018 0.002 0.003 0.004 0.005 0.006 0.008 0.01
    # for hz in 0.0 0.0001 0.0002 0.0003 0.0004 0.0005 0.0007 0.001 0.0012 0.0016  0.002 0.004
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