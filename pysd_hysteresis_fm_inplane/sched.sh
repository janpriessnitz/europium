#!/bin/bash

for temp in 0.01 0.1 1 2 4
do
	for dm in 0 0.05 0.1 0.2 0.4 1 1.7 2
	do
		subdir="no0_fast/$temp/$dm"
		mkdir -p $subdir
		cp runjob.sh $subdir/
		pushd $subdir
		qsub -v TEMP=$temp,DM=$dm runjob.sh
		popd
	done
done
