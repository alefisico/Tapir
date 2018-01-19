#!/bin/bash

#crash in case of error
set -e
#print out
#set -x

#SRC=srm://storm-se-01.ba.infn.it:8444/srm/managerv2?SFN=/cms
SRC=root://cms-xrd-global.cern.ch
DST=srm://t3se01.psi.ch:8443/srm/managerv2\?SFN=/pnfs/psi.ch/cms/trivcat

source common.sh
cd $GC_SCRATCH
for fi in $FILE_NAMES; do
    echo $fi
    newfi="${fi/arizzi/$USER}"
    LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH gfal-copy -n1 --force $SRC/$fi $DST/$newfi
    python $CMSSW_BASE/src/TTH/MEAnalysis/test/getBranches.py root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat/$newfi Events | grep " = " >> out.txt 
done
