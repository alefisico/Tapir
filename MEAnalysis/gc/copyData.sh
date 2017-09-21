#!/bin/bash

#crash in case of error
set -e

source common.sh
cd $GC_SCRATCH
COUNTER=1
for fi in $FILE_NAMES; do
    echo $f

    #in case file was blacklisted, don't try to copy it
    if [ ! -z $(grep $fi blacklist.txt) ]; then
        echo "Found file $fi in blacklist, skipping";
        continue;
    fi
    gfal-copy -n1 gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat$fi tmp.root || echo "could not copy $fi"
    rootcp tmp.root:tree tree_$COUNTER.root || echo "could not copy tree"
    rootcp tmp.root:vhbb/Count count_$COUNTER.root || echo "could not copy count"
    rm tmp.root
    COUNTER=$[$COUNTER +1]
done
hadd tree.root tree_*.root count_*.root
