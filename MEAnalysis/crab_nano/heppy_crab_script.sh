#!/bin/bash
#dont kill on error
set +e
source env.sh
#manually copy the data configuration

python heppy_crab_script.py $@ --isMC &> log
EXITCODE=$?
./post.sh $EXITCODE
echo Finished_vhbb $EXITCODE

python mem_crab_script.py $@ >> log 2>&1
EXITCODE=$?
echo ExitCode $EXITCODE
./post.sh $EXITCODE
