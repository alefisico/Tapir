#!/bin/bash
for i in `seq 1 20`; do
    qsub -N rq_worker -wd `pwd` -o `pwd`/logs/ -e `pwd`/logs/ worker.sh
done
