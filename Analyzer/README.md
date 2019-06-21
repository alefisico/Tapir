# Analyzer

This is a modified version of the [MEAnalysis](../MEAnalysis) and [Plotting](../Plotting) scripts. The scripts there can run directly from centrally produced nanoAOD, or one can create nanoAOD v04.
The next set of steps rely can be run after setting up the packages needed, as described in [here](../README.md)

## Create nanoAOD

For more information about nanoAOD, read the [twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD). *This step is not needed if you are using centrally produced nanoAOD samples.*

To test local the production of nanoAOD samples:
```
cd $CMSSW_BASE/src/TTH/Analyzer/test/   ## to go to the test folder
cmsenv                                  ## in case you haven't set the CMSSW environment
cmsRun simpleJob_nanoAOD.py
```

This script was done using the following cmsDriver command (for nanoAOD v4):
```
cmsDriver.py simpleJob_nanoAOD.py -s NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --no_exec --conditions 101X_upgrade2018_realistic_v7 --era Run2_2018,run2_nanoAOD_102Xv1
```

To submit several crab jobs to produce nanoAOD samples, you can run:
```
python multicrab_nanoAOD.py --sample ttHTobb --version v04 
```
where `--version` is just a label for your output datasets and `--sample` depends on the name of the sample inside the script in the `Samples` dictionary. To get a list of 2018 miniAOD samples you can use the `dasgoclient` command, for instance:
```
dasgoclient --query="/*/RunIIAutumn18MiniAOD*/MINIAODSIM"
```

## Create ntuples 

This step runs nanoAOD postprocessing (to calculate PU, btagging, JEC weights) and the analysis ntuples, both in one step, one after the other.
