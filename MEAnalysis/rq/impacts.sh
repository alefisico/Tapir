#!/bin/bash
set +e
set -o xtrace

MASS=125

DCARD=`basename $1`
DCARD="${DCARD%.*}"
cd `dirname $1`

text2workspace.py $DCARD.txt -m $MASS
combineTool.py -M Impacts -d $DCARD.root --doInitialFit --robustFit=1 --minimizerStrategy 0 --minimizerTolerance 0.000001 -m $MASS
combineTool.py -M Impacts -d $DCARD.root --doFits --robustFit=1 --minimizerStrategy 0 --minimizerTolerance 0.000001 -m $MASS --parallel 10
combineTool.py -M Impacts -d $DCARD.root -m $MASS -o impacts.json
plotImpacts.py -i impacts.json -o impacts
