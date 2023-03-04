#!/bin/bash


expdir="no1"


for dm in 0 0.1 0.2 0.5 1
do
    for T in 1 10 32 100
    do
        for Hz in 0.005 0.01 0.02 0.05
        do
            d=$expdir/${dm}_${T}_${Hz}
            mkdir -p $d
            pushd $d
            ../../simulation.py $dm $T $Hz
            popd
        done
    done
done