#!/bin/bash

# for dm in 0 0.5 1 1.5 1.7 1.75 1.8 1.9 2 2.1 2.2 2.3 2.5
for dm in 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.2 2.4
do
	subdir="t_0.0001_no1/$dm"
	mkdir -p $subdir
	cp runjob.sh $subdir/
	pushd $subdir
	qsub -v DM=$dm runjob.sh
	popd
done
