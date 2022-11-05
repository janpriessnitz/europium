#!/bin/bash


for dm in $(ls $1/); do
  for hz in $(ls $1/$dm); do
    curdir=$1/$dm/$hz/
    pushd $curdir
    tar xf results.tar.gz
    popd
  done
done
