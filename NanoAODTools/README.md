# ttHbb13 nanoAODTools

## To produce modified nanoAOD

For more information about nanoAOD, please look at the (nanoAOD twiki)[https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD].

For the nominal analysis, the centrally produced nanoAOD samples are sufficient. 
The following recipe is to include a different jet collection (ak4 puppi jets) in the nanoAOD samples. 
For that, the recommendation from JMAR is to use the (jetToolbox)[https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetToolbox]. If you have not clone it before, just run:

~~~
cd $CMSSW_BASE/src
git clone git@github.com:cms-jet/JetToolbox.git JMEAnalysis/JetToolbox -b jetToolbox_102X_v2
scram b -j 4
~~~

In this version of the jetToolbox, a python file is needed to run a different jet collection and produced an output in nanoAOD format. 
An example of this file is (nanoAOD_jetToolbox_cff.py)[../python/nanoAOD_jetToolbox_cff.py]

~~~
cmsDriver.py myNanoProdMc2017 -s NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM   --conditions 102X_mc2017_realistic_v6 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))" --filein=/store/mc/RunIIFall17MiniAODv2/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/E40C4367-E4AE-E811-B96D-FA163E4CF25C.root --customise TTH/NanoAODTools/nanoAOD_jetToolbox_cff.nanoJTB_customizeMC -n 10
~~~


## Training samples

To create numpy arrays directly from nanoAOD files there is an script called `TTH/NanoAODTools/test/makeNumpyarrays.py`. It is fairly simple to run and instructions are included inside the file. 

For instance, to run locally with a test root file:
```bash
python makeNumpyarrays.py -s -v v00 -d TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8
```
The `-s` option is included to run a singleFile, the option `-v` is to include a version of the output file, and `-d` is for the name of the dataset input (this name will be use to format the outputfile). If you want to specify another input file, you can use `-i /store/blahblah`. 

In addition to run a condor job with several files from a dataset, you can use the file `TTH/NanoAODTools/test/submitCondorJobs.sh`. To run it, first create a `test/condorlogs/` directory and run:

```bash
source submitCondorJobs.sh ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8
```
where the first input is the name of a txt file with the list of input files. This script will create two files (`_condorJob.sh`, `_condorJob.sub`) and it wil submit a job per input file. To transfer the output file directly to the T3_CH_PSI you need to modify the variables `myproxy` and `t3Dir` inside the `submitCondorJobs.sh` script.

