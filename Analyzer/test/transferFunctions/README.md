# Evaluate transfer functions

Transfer functions map the measured properties of jets by the detector to the underlying generated particles. These are needed for the computation of the MEM.

## Create root files with quark-jet matched information

To calculate transfer functions first we need to match the quarks from generator information with reconstructed jets. This is done by running the script `runSkimmerTF.py`. This is a nanoAOD postprocessing-like python script which applies some basic selection and then runs `TTH/Analyzer/python/skimTF.py` for the matching part.

To run local:
```
cd $CMSSW_BASE/src/TTH/Analyzer/test/transferFunctions/
python runSkimmerTF.py --sample ttHTobb_ttToSemiLep
```
There is a crab script to submit several samples at the time: `multicrab_nanoAODPostproc_TF.py`. To run it:
```
python multicrab_nanoAODPostproc_TF.py -d ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8 -v v02
```
where `-d` is the name of the samples in the `dictSamples` dictionary inside the multicrab file and `-v` is a tag. 

## Calculation of transfer functions
