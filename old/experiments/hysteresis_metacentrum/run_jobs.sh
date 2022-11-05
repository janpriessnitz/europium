#!/bin/bash


for dm in $(ls runs/); do
	curdir=runs/$dm
	echo queuing $curdir
	pushd $curdir
	qsub runjob.sh
	popd
done
