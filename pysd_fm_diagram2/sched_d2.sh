#!/bin/bash

expdir="no5_d2"

mkdir -p "${expdir}"
cp simulation.py ${expdir}

hz=0

dm=2
for hx in 1 1.02 1.04 1.06 1.08 1.1 1.12 1.14 1.16 1.18 1.2 1.22 1.24 1.26 1.28 1.3
do
  subdir="${expdir}/${dm}_${hx}_${hz}"
  mkdir -p $subdir
  cp runjob.sh $subdir/
  pushd $subdir
  qsub -v DM=$dm,HX=$hx,HZ=$hz runjob.sh
  popd
done

# dm=3
# for hx in 0 0.1 0.2 0.4 0.6 0.8 1 1.1 1.2 1.3 1.4 1.5 1.6 1.8 2 2.5
# do
#   subdir="${expdir}/${dm}_${hx}_${hz}"
#   mkdir -p $subdir
#   cp runjob.sh $subdir/
#   pushd $subdir
#   qsub -v DM=$dm,HX=$hx,HZ=$hz runjob.sh
#   popd
# done
