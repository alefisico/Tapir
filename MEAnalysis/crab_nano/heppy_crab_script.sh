#!/bin/bash
#dont kill on error
set +e
source env.sh
#manually copy the data configuration

python heppy_crab_script.py $@ --isMC &> log
EXITCODE=$?
./post.sh $EXITCODE
echo Finished_nano $EXITCODE
tail -n10 log

python mem_crab_script.py $@  --isMC >> log 2>&1
EXITCODE=$?
echo Finished_tthbb13 $EXITCODE
head -n 70 log
echo "=== SNIP ==="
tail -n 70 log
./post.sh $EXITCODE
