#!/bin/bash

for temp in 0.01 2
do
	for dm in 0 0.02 0.04 0.06 0.08 0.1 0.2 0.4 0.6 1 1.4 1.7 1.75 1.8 2 2.5
	do
		for deltaJ in 0.5 0.8 0.9 1 1.1 1.2 1.5
		do
			subdir="no6/$temp/$dm/$deltaJ"
			mkdir -p $subdir
			cp runjob.sh $subdir/
			pushd $subdir
			qsub -v TEMP=$temp,DM=$dm,DELTAJ=$deltaJ runjob.sh
			popd
		done
	done
done
