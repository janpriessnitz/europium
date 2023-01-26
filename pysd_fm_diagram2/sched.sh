#!/bin/bash

expdir="no6_full"

mkdir -p "${expdir}"
cp simulation.py ${expdir}

for dm in 0 0.1 0.5 1 1.5 1.7 1.72 1.74 1.76 1.78 1.8 1.85 1.9 1.95 2 2.1 2.2 2.3 2.4 2.5
do
  for hx in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0
  do
    hz=0
    subdir="${expdir}/${dm}_${hx}_${hz}"
    mkdir -p $subdir
    cp runjob.sh $subdir/
    pushd $subdir
    qsub -v DM=$dm,HX=$hx,HZ=$hz runjob.sh
    popd
  done
done

for dm in 0 0.1 0.5 1 1.5 1.7 1.72 1.74 1.76 1.78 1.8 1.85 1.9 1.95 2 2.1 2.2 2.3 2.4 2.5
do
  for hz in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0
  do
    hx=0
    subdir="${expdir}/${dm}_${hx}_${hz}"
    mkdir -p $subdir
    cp runjob.sh $subdir/
    pushd $subdir
    qsub -v DM=$dm,HX=$hx,HZ=$hz runjob.sh
    popd
  done
done
