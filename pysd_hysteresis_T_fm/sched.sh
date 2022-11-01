#!/bin/bash

for temp in 0.01 0.1 1 2 4
do
	for dm in 0 0.1 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.7 1.75 1.8 2 2.5
	do
		subdir="no3/$temp/$dm"
		mkdir -p $subdir
		cp runjob.sh $subdir/
		pushd $subdir
		qsub -v TEMP=$temp,DM=$dm runjob.sh
		popd
	done
done
