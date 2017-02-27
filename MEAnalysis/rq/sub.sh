#!/bin/bash
WD=`pwd`
for i in `seq 1 100`; do
    qsub -q all.q -l h_vmem=3G -N rq_worker -wd $WD -o $WD/logs/ -e $WD/logs/ worker.sh
done
