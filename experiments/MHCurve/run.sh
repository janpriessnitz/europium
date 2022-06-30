#!/bin/bash


BASEDIR=$(realpath ../../)
RUNDIR=runs/
Hzs=(0 0.5 1 1.5 2 3)
DMs=(0 0.1 0.2 0.4 0.8 1.6 3.2)

for hz in ${Hzs[@]}; do
  for dm in ${DMs[@]}; do
    echo "running sim for Hz $hz and DM $dm"
    curdir=$RUNDIR/$dm/$hz
    mkdir -p $curdir
    echo $hz > $curdir/hz
    echo $dm > $curdir/dm

    export H_Z=$hz
    export DM=$dm
    export MODE=M
    export N_ENS=10
    $BASEDIR/uppasd_configs/fillconf.sh $BASEDIR/uppasd_configs/basic/ $curdir
    pushd $curdir
    $BASEDIR/uppasd > stdout.txt
    popd
  done
done
