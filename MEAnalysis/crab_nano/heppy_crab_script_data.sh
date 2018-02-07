#!/bin/bash
#dont kill on error
set +e
source env.sh
#manually copy the data configuration
#cp heppy_config_data.py heppy_config.py

python heppy_crab_script.py $@ --isData &> log
EXITCODE=$?
./post.sh $EXITCODE
echo Finished_vhbb $EXITCODE

python mem_crab_script.py $@ --isData >> log 2>&1
EXITCODE=$?
echo ExitCode $EXITCODE
./post.sh $EXITCODE
