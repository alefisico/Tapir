#!/bin/bash
for i in `seq 1 40`; do
    SGE_O_WORKDIR=`pwd` JOB_ID=$i ./worker.sh quick &
done
wait
