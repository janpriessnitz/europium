#!/bin/bash

expdir="no1"

mkdir -p "${expdir}"
cp simulation.py ${expdir}

# for dm in 0 0.1 0.5 1 1.5 2
# do
#   for hx in 0 0.5 1 1.5 2 2.5
#   do
#     hz=0
#     subdir="${expdir}/${dm}_${hx}_${hz}"
#     mkdir -p $subdir
#     cp runjob.sh $subdir/
#     pushd $subdir
#     qsub -v DM=$dm,HX=$hx,HZ=$hz runjob.sh
#     popd
#   done
# done

# for dm in 0 0.1 0.5 1 1.5 2
# do
#   for hz in 0.5 1 1.5 2 2.5
#   do
#     hx=0
#     subdir="${expdir}/${dm}_${hx}_${hz}"
#     mkdir -p $subdir
#     cp runjob.sh $subdir/
#     pushd $subdir
#     qsub -v DM=$dm,HX=$hx,HZ=$hz runjob.sh
#     popd
#   done
# done

for dm in 0 0.1 0.5 1 1.5 2
do
  for hz in 0.5 1 1.5 2 2.5
  do
    hx=$hz
    subdir="${expdir}/${dm}_${hx}_${hz}"
    mkdir -p $subdir
    cp runjob.sh $subdir/
    pushd $subdir
    qsub -v DM=$dm,HX=$hx,HZ=$hz runjob.sh
    popd
  done
done
