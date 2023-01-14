#!/bin/bash

# for temp in 0.01 0.1 1 2 4
# do
temp=1
for dm in 1.7 1.8 1.9 2 2.1
do
	subdir="no3_d2/$dm"
	mkdir -p $subdir
	cp runjob.sh $subdir/
	pushd $subdir
	qsub -v TEMP=$temp,DM=$dm runjob.sh
	popd
done
# done
