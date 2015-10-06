#!/bin/bash

set -e

DATACARD_DIR=./testhists
WD=$PWD
CODEDIR=$CMSSW_BASE/src/TTH

#make json job files for histogram projector
#python python/makeJobfiles.py
#
##run histograms
#ls *.json | parallel --gnu --results res ./melooper {}

#merge and move to output dir
#hadd -f ControlPlots.root ControlPlots_*.root
#rm ControlPlots_*.root
#
#mkdir -p $DATACARD_DIR
#mv ControlPlots.root $DATACARD_DIR/
#
##project out datacards
#python python/Datacards/makeDatacard.py $DATACARD_DIR

#Run combine in parallel jobs
cd $DATACARD_DIR
python $CODEDIR/Plotting/python/combine.py shapes*.txt
cd $WD

#Make limit plots
python python/joosep/limits.py $DATACARD_DIR
