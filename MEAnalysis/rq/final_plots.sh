#!/bin/bash

workdir=results/2017-11-03T09-56-19-945288_e78ed59f-6ac6-4e04-b05c-b89ec07bcf2d

#Make the pull plots, produces mlfitshapes file
python ../Plotting/python/Datacards/MakeLimits.py --jobtype pulls --config rq/results/2017-10-30T20-03-26-609041_dde7d311-e1ca-4842-a91a-b960119b7e3d/analysis.pickle --group all

#Based on the pull plot results, do the best fit plot based on the mlfitshapes
python ../../Plotting/python/joosep/fit_results.py $workdir

#Prefit and postfit plots
python ../../Plotting/python/joosep/prefit_postfit.py $workdir

#Nuisance correlation plot
python corrs.py $workdir
