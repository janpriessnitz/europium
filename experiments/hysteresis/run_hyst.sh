#!/bin/bash

EXP_NAME="EuAlOBas"
BASE_DIR=$(realpath ../../)
RUN_DIR="run_10reps4/"

INIT_H="-1"
HS=(-0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.25 -0.2 -0.15 -0.1 -0.05 0 0.05 0.1 0.15 0.2 0.25 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.25 0.2 0.15 0.1 0.05 0 -0.05 -0.1 -0.15 -0.2 -0.25 -0.3 -0.4 -0.5 -0.6 -0.7 -0.8 -0.9 -1)

# HS=(-0.08 -0.07 -0.06 -0.05 -0.04 -0.03 -0.02 -0.015 -0.01 -0.005 0 0.005 0.01 0.015 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.1 0.08 0.07 0.06 0.05 0.04 0.03 0.02 0.015 0.01 0.005 0 -0.005 -0.01 -0.015 -0.02 -0.03 -0.04 -0.05 -0.06 -0.07 -0.08 -0.1)
# INIT_H="-0.1"

# INIT_H=-1
# HS=(-0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1 0 -0.1 -0.2 -0.3 -0.4 -0.5 -0.6 -0.7 -0.8 -0.9 -1)


# INIT_H=-0.2
# HS=(-0.1 -0.05 0 0.002 0.004 0.006 0.008 0.01 0.013 0.017 0.02 0.025 0.03 0.035 0.04 0.045 0.05 0.06 0.07 0.08 0.09 0.1 0.2)

# INIT_H=-1
# HS=(0 1 2 4 8 16 32)

# INIT_H=-1
# HS=(0 0.002 0.004 0.006)

REPS=5

fillconf="$BASE_DIR/uppasd_configs/fillconf.sh"
uppasd="/home/jp/UppASD/bin/sd.gfortran"

mkdir -p $RUN_DIR

export N_ENS=1
export H_Z=$INIT_H
# export DM=0.64336
export DM=0
# export DM=0.65
$fillconf config_initial/ $RUN_DIR/0/
pushd $RUN_DIR/0
echo $H_Z > hz
$uppasd > stdout.txt
popd


i=0
for r in `seq $REPS`; do
    for hz in ${HS[@]}; do
        oldi=$i
        i=$((i+1))
        mkdir -p $RUN_DIR/$i
        cp $RUN_DIR/$oldi/restart.EuAlOBas.out $RUN_DIR/$i/prev_restart.EuAlOBas.out
        export H_Z=$hz  
        $fillconf config_step/ $RUN_DIR/$i
        pushd $RUN_DIR/$i
        echo $H_Z > hz
        $uppasd > stdout.txt
        popd

    done
done