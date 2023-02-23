#!/bin/bash


for steps in 100000
do
for temp in 0.01 1 4 16 32 64 128
do
	for dm in 0 0.1 0.5 1 1.5
	do
		subdir="no10/$steps/$temp/$dm"
		mkdir -p $subdir
		cp runjob.sh $subdir/
		pushd $subdir
		qsub -v TEMP=$temp,DM=$dm,STEPS=$steps runjob.sh
		popd
	done
done
done