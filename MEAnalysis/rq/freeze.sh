#!/bin/bash

combine -M MultiDimFit --saveWorkspace -n _step1 --minimizerStrategy 0 --minimizerTolerance 0.00001 --rMin -10 --rMax 10 shapes_group_group_sldl.txt
CMD="combine higgsCombine_step1.MultiDimFit.mH120.root -w w --snapshotName "MultiDimFit"  -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.00001 --rMin -10 --rMax 10 --minos all"
$CMD > freeze_none.log
$CMD --freezeNuisanceGroups exp,theory > freeze_all.log
$CMD --freezeNuisanceGroups exp > freeze_exp.log
$CMD --freezeNuisanceGroups theory > freeze_theory.log
$CMD --freezeNuisanceGroups jec > freeze_jec.log
$CMD --freezeNuisanceGroups btag > freeze_btag.log
$CMD --freezeNuisanceGroups mcstat > freeze_mcstat.log
