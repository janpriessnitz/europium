#!/bin/bash

# all template parameters + defaults
export LATTICE_SIZE=${LATTICE_SIZE:-'20'}
export N_ENS=${N_ENS:-'1'}
export MODE=${MODE:-'H'}
export H_X=${H_X:-'0'}
export H_Y=${H_Y:-'0'}
export H_Z=${H_Z:-'0'}

export J=${J:-'1'}
export DELTAJ=${DELTAJ:-'1'}

export DM=${DM:-'0'}

SRC_DIR=$1
DST_DIR=$2

mkdir -p $DST_DIR

for f in $(ls $SRC_DIR); do
  echo $f
  src_path=$SRC_DIR/$f
  dst_path=$DST_DIR/$f
  envsubst < $src_path > $dst_path
done