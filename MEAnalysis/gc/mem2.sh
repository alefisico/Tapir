#!/bin/bash

source common.sh
cd $GC_SCRATCH
python ${CMSSW_BASE}/src/TTH/MEIntegratorStandalone/python/run_csv.py
