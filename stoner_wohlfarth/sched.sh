#!/bin/bash

expdir="no2"

mkdir -p "${expdir}"
cp simulation.py ${expdir}

for dm in 0.1 0.2 0.3 0.5 0.7 1 1.5
do
    for T in 1 4 16 32 64 128
    do
        expected_H=$(echo "$dm * $dm * $T / 1250 + 0.001" | bc -l | awk '{ printf("%.4f\n",$1) '})
        halfH=$(echo "$expected_H/2" | bc -l | awk '{ printf("%.4f\n",$1) '})
        twoH=$(echo "$expected_H*2" | bc -l | awk '{ printf("%.4f\n",$1) '})
        for Hz in $expected_H $halfH $twoh
        do
            subdir="$expdir/${dm}_${T}_${Hz}"
            echo $subdir
            mkdir -p $subdir
            cp runjob.sh $subdir/
            pushd $subdir
            qsub -v DM=$dm,HZ=$Hz,TEMP=$T runjob.sh
            popd
        done
    done
done