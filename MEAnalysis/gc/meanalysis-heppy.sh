#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

#print out the environment
env

python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/@me_conf@.cfg

mv $GC_SCRATCH/Loop/tree.root out.root

echo $OFNAME > output.txt

