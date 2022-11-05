#!/bin/bash

DMs=(0 0.002 0.005 0.01 0.02 0.04 0.07 0.1 0.2 0.4 0.5 0.6 0.63 0.64 0.65)

RUNDIR=runs/

for dm in ${DMs[@]}; do
    curdir=$RUNDIR/$dm
    mkdir -p $curdir
    cp -R job/* $curdir
    echo DM=$dm > $curdir/params.sh
done