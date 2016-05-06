#!/bin/bash

#uncomment these to test the script
#these are all the input parameters that MEAnalysis_heppy_gc.py reads
#export SKIP_EVENTS=0
#export MAX_EVENTS=200
#export DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8
#export FILE_NAMES=/store/user/jpata/VHBBHeppyV20/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V20_ttHTobb_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160209_170826/0000/tree_1.root
#export MY_SCRATCH=./

source common.sh

#here we use @...@ to give grid-control the possibility to substitute the configuration file name
#comment this line when testing locally
#export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/cfg_withME.py
export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/@me_conf@

#go to work directory
cd $GC_SCRATCH

# Make sure we process all events (as currently using file based splitting)
# Change back if we go to event bases
export MAX_EVENTS=9999999999

#print out the environment
env

python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py
echo "MEAnalysis is done"

#copy output
ME_CONF_NAME=$(basename "$ME_CONF")

#OUTDIR=${TASK_ID}/${ME_CONF_NAME%.*}/${DATASETPATH}/
OUTDIR=~/tth/gc/${GC_TASK_ID}/${ME_CONF_NAME%.*}/${DATASETPATH}/

echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root

#export SRMBASE=srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/$USER/tth
#mkdir -p $SRMBASE/$OUTDIR || true
#gfal-copy file://$MY_SCRATCH/Loop/tree.root $SRMBASE/$OFNAME

mkdir -p $OUTDIR
cp $GC_SCRATCH/Loop/tree.root $OUTDIR/tree_$MY_JOBID.root

echo $OFNAME > output.txt

