# Analyzer

This is a modified version of the [MEAnalysis](../MEAnalysis) and [Plotting](../Plotting) scripts. The scripts there can run directly from centrally produced nanoAOD, or one can create nanoAOD v04.
The next set of steps rely can be run after setting up the packages needed, as described in [here](../README.md)

## Create nanoAOD

Instructions on how to create private nanoAOD samples are in this [README](../nanoAODTools/README.md)

## Create ntuples 

This step runs nanoAOD postprocessing (to calculate PU, btagging, JEC weights) and the analysis ntuples, both in one step, one after the other.
