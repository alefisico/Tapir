#!/bin/bash
source common.sh
cd $GC_SCRATCH
OUTFILTER=@outfilter@ ANALYSIS_CONFIG=${CMSSW_BASE}/src/TTH/MEAnalysis/data/default.cfg python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/sparsinator.py
