# Analyzer

## Histograms and selection
This is the main part of the analyzer, which is based on [nanoAODTools](https://github.com/cms-nanoAOD/nanoAOD-tools) and uses the [nanoAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD) format.

This step runs nanoAOD postprocessing (to calculate PU, btagging, JEC weights) and the analysis ntuples, both in one step, one after the other. Two python files are essential: [simpleAnalyzer.py](test/simpleAnalyzer.py) and [boostedAnalyzer.py](python/boostedAnalyzer.py). To run it locally, after setting the main environment described [here](../README.md):

```bash
python simpleAnalyzer.py --sample TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8  --oFile _ttHTobb --local --process boosted
```
where the input root file is specified in [PSet.py](test/PSet.py).

To run many jobs, in the HTCondor system, the script [submitCondorJobsAnalyzer.sh](test/submitCondorJobsAnalyzer.sh) can be used. For instance:
```bash
source submitCondorJobsAnalyzer.sh Muon 2017_boosted v10
```
The output of these jobs needs to be merged, for that we can use the script [massiveHadd.sh](test/massiveHadd.sh):
```bash
source massiveHadd.sh simple 
```

## Background estimation

For this step, the Combine environment described [here](../README.md) *needs to be set up*. The script [Rhalphabet.py](test/Rhalphabet.py) creates the workspaces and datacards needed for the next steps. To run it:
```bash
python Rhalphabet.py -v v09
```

To run simple fit of the workspaces and datacards created in the previous step:
```bash
combine -M FitDiagnostics datacard.txt  --robustFit 1 --setRobustFitAlgo Minuit2,Migrad --saveNormalizations --plot --saveShapes --saveWorkspace 
```
