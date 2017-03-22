#!/bin/bash

source common.sh
cd $GC_SCRATCH
COUNTER=1
for fi in $FILE_NAMES; do
    rootcp root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat$fi:tree tree_$COUNTER.root
    COUNTER=$[$COUNTER +1]
done
hadd tree.root tree_*.root
