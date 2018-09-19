# TOC

- [Installation](#installation)
- [Running](#running)
- [Samples](#samples)
- [Misc](#misc)

# Installation
Setup on SLC6 in a clean directory (no CMSSW) on a **shared file system (NFS)**
~~~
$ mkdir -p ~/tth/sw
$ cd ~/tth/sw
$ wget --no-check-certificate https://gitlab.cern.ch/Zurich_ttH/tthbb13/raw/SwitchNanoAOD/setup.sh
$ source setup.sh
~~~
This will download CMSSW, the `tthbb13` code and all the dependencies.

In order to compile the code, run
~~~
$ cd ~/tth/sw/CMSSW/src
$ cmsenv
$ scram b -j 8
~~~

Note that if you run `scram b clean`, the matrix element library OpenLoops will be deleted from CMSSW, which will result in errors like
~~~
[OpenLoops] ERROR: register_process: proclib folder not found, check install_path or install libraries.
~~~
In order to fix this, you have to re-copy the libraries, see the end of `setup.sh` for the recipe.

# Running
## Step0: environment

Generally for running the code, `cmsenv` is sufficient. For some plotting tasks,
we use a local python environment that can be configured on T3_CH_PSI
through
~~~
source MEAnalysis/rq/env.sh
~~~

## Step1: Running the nanoAOD code

NanoAOD links:
1. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD
2. https://github.com/cms-nanoAOD/cmssw/issues

## Step2: tthbb13 code
Using the nanoAOD-tree, we will run the ttH(bb) and matrix element code (tthbb13). The code is configured mainly from two files:

1. A flat configuration in [MEAnalysis/data/default.cfg](https://gitlab.cern.ch/Zurich_ttH/tthbb13/blob/SwitchNanoAOD/MEAnalysis/data/default.cfg) specifying the samples and analysis categories. This configuration should be preferred for most future options.

2. A python configuration in [MEAnalysis/python/MEAnalysis_cfg_heppy.py](https://gitlab.cern.ch/Zurich_ttH/tthbb13/blob/SwitchNanoAOD/MEAnalysis/python/MEAnalysis_cfg_heppy.py) used for the MEM configuration and specifying the object (jet, lepton) cuts.


In order to test the `tthbb13` code, run:
~~~
python $CMSSW_BASE/src/TTH/MEAnalysis/test/test_MEAnalysis_heppy.py --sample ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8
~~~
This will call
~~~
python $CMSSW_BASE/src/TTH/MEAnalysis/python/MEAnalysis_heppy.py MEAnalysis/data/default.cfg --sample SAMPLE_NAME
~~~

Steps 1-2 can be run together on the grid using crab, see [MEAnalysis/crab_nano/multicrab_94X.py](https://gitlab.cern.ch/algomez/tthbb13/blob/SwitchNanoAOD_946patch1/MEAnalysis/crab_nano/multicrab_94X.py). To run a test crab job:
~~~
python multicrab_94X.py --workflow testing --tag Jun19
~~~
here, workflow is defined in [these lines](https://gitlab.cern.ch/algomez/tthbb13/blob/SwitchNanoAOD_946patch1/MEAnalysis/crab_nano/multicrab_94X.py#L13) and --tag is for bookkeeping purposes.

To produce the subsequent `.txt` files used for local running, see the script `Plotting/python/christina/ttbar_classification/getFilesCrab.py` as:
~~~
python Plotting/python/christina/ttbar_classification/getFilesCrab.py --path /pnfs/psi.ch/cms/trivcat/store/user/algomez/tth/v00_20180810 --outpath /mnt/t3nfs01/data01/shome/creissel/tth/2017/sw/CMSSW_9_4_5_cand1/src/TTH/MEAnalysis/gc/datasets  --onlytthbb
~~~
The path argument refers to the location of the crab output files; onlytthbb refers tot he kind of Ntuples used; and outpath is the location of the folder created by the script. In this folder you have a `.txt` file per dataset found in the path argument.
 

## Step3 (optional): skim with `projectSkim`

When some of the samples are done, you can produce smallish (<10GB) skims of the files using local batch jobs. These can be used for direct analysis by hand.

~~~
$ cd TTH/MEAnalysis/gc
$ source makeEnv.sh #make an uncommited script to properly set the environment on the batch system
v./grid-control/go.py confs/projectSkim.conf
... #wait and make note of the task name, which is like GC123445
$ ./hadd.py /path/to/output/GC123445/ #call our merge script
~~~

This will produce some skimmed ntuples in
~~~
/mnt/t3nfs01/data01/shome/Zurich_ttH/tth/gc/projectSkim/GCe0f041d65b98:
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8 <= unmerged
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8.root <= merged file
...
Jul15_leptonic_v1__TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
Jul15_leptonic_v1__TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
Jul15_leptonic_v1__TTTo2L2Nu_13TeV-powheg.root
Jul15_leptonic_v1__TT_TuneCUETP8M1_13TeV-powheg-pythia8.root
~~~

The total processed yields (ngen) can be extracted with
~~~
$ cd TTH/MEAnalysis/gc
$ ./grid-control/go.py confs/count.conf
...
$ ./hadd.py /path/to/output/GC1234/
$ python $CMSSW_BASE/src/TTH/MEAnalysis/python/getCounts.py /path/to/output/GC1234/
~~~

The counts need to be introduced to `TTH/Plotting/python/Datacards/config_*.cfg` as the `ngen` flags for the samples.

## Step4: Histograms with systematic distributions per category
In order to industrially produce all variated histograms, they are configured through
`default.cfg` and called through `sparsinator.py`

~~~
$ cd TTH/MEAnalysis/gc
$ ./grid-control/go.py confs/sparse.conf
...
$ hadd -f sparse.root /path/to/output/GC1234/
~~~

The output file will contain per-category histograms.

## Step3-6 in one go: `launcher.py`

If you are running this step for the first time, you need to create an empty "logs" folder in the rq directory.

There is a new workflow in order to run all the post-ntuplization steps in one workflow. It relies on a central "job broker" and a launcher script.
**Important**: only one broker can run per T3 UI!

Start the job broker (redis database) by going to
~~~
cd TTH/MEAnalysis/rq/
source env.sh
./server.sh
~~~

Then in another screen, launch jobs that will connect to the broker and wait for instructions
~~~
cd TTH/MEAnalysis/rq/
source env.sh
./sub.sh
~~~

Then launch the actual workflow
~~~
source env.sh
python launcher.py TTH/Plotting/python/Datacards/config_*.cfg
~~~

You will see the progress of various steps, the results will end up in `TTH/MEAnalysis/rq/results`.

When you're done, don't forget to free up your jobs:
~~~
qdel -u $USER
~~~

# Samples

The currently used samples are listed below. Generally, they are stored at T3_CH_PSI.

## NanoAOD (step1)

| production name | comments |
|-----------------|----------|
| [NanoCrabProdXmas](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/NanoCrabProdXmas) | no boosted or hadronic triggers |
| [nano_05Feb2018](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/nano_05Feb2018) | nanoAODv1, 2016 datasets |
| [Apr16](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/Apr16) | 2017 datasets, no btag shape scale factor(step1) |
| [May1](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/May21) | data, relatively complete |
| [May2](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/May2) | MC |

## tthbb13 (step2)

| production name | base NanoAOD run | comments |
|-----------------|--------------|----------|
| [Jan26](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/Jan26) | NanoCrabProdXmas | |
| [Apr16](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/Apr16) | Apr16 | no trigger |
| [NanoBoostedMEM_Mar15](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/NanoBoostedMEM_Mar15) | RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1 | postprocessing,MEM,Boosted |
| [May1](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/May21) | May1 | data, no nPVs |
| [May2](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/SwitchNanoAOD/MEAnalysis/gc/datasets/May2) | May2 | MC, no btagSF, wrong lepton veto criteria |

## Delphes files
| process | tag | number of events | comments |
|-----------------|--------------|----------|----------|
| [ttH(bb)](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/chreisse06/MEAnalysis/gc/datasets/Jun04/Delphes_ttH.txt) | Jun04 | 3720000 | old Delphes topology with AK5 jets |
| [ttbb](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/chreisse06/MEAnalysis/gc/datasets/Jun04/Delphes_ttbb_inclusive.txt) | Jun04 | 1920000 | old Delphes topology with AK5 jets, wrong BR of top decays |
| [ttH(bb)](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/chreisse08/MEAnalysis/gc/datasets/Aug21_Delphes/ttHbb.txt) | Aug21_Delphes | 5529368 | new Delphes topology, boosted variabled included |
| [ttbar](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/chreisse06/MEAnalysis/gc/datasets/Aug21_Delphes/ttbar.txt) | Aug21_Delphes | 2540000 | new Delphes topology, boosted variables included |
| [ttbb (SL)](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/chreisse06/MEAnalysis/gc/datasets/Aug21_Delphes/ttbb_semileptonic.txt) | Aug21_Delphes | 2740000 | new Delphes topology (AK4 jets), boosted variables included |
| [ttbb (FH)](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/chreisse06/MEAnalysis/gc/datasets/Aug21_Delphes/ttbb_hadronic.txt) | Aug21_Delphes | 2980000 | new Delphes topology (AK4 jets), boosted variables included |
| [ttbb (DL)](https://gitlab.cern.ch/Zurich_ttH/tthbb13/tree/chreisse06/MEAnalysis/gc/datasets/Aug21_Delphes/ttbb_dileptonic.txt) | Aug21_Delphes | 2080000 | new Delphes topology (AK4 jets), boosted variables included |

# Misc

## Copying nanoAOD ntuples

The nanoAOD ntuples that are produced centrally are generally located on various
T2 centers, we want to copy them to T3_CH_PSI for analysis.

To do that, we extract the list of files corresponding to a dataset using the
script `MEAnalysis/test/das_query.sh` and actually the copy the files using
a grid-control workflow in `MEAnalysis/gc/confs/copyData.conf`.

## Continous integration (CI)

We test the code regularly using the gitlab CI system. Since we are accessing
the samples from T3_CH_PSI, this currently requires a valid proxy at CERN.

## Evaluate transfer functions

Transfer functions map the measured properties of jets by the detector to the underlying generated particles. These are needed for the computation of the MEM. To evaluate these, a ROOT file containing the necessary information needs to be computed first (jets and generated quarks). To do this, run the `MEAnalysis/python/JetTranfer.py` script, or use the grid-control workflow in `MEAnalysis/gc/confs/transfer.conf` .

Next the transfer functions are calculated via the `Plotting/python/TransferFunctions/CreateTF/TFmain.py` script. Before running the script, the config file needs to be created, specifiying the location of the input root file:

~~~
python config.py
~~~

Then run the transfer functions, specifying again the file name:

~~~
python TFmain.py TTToHadronic_TuneCP5_13TeV-powheg-pythia8
~~~

This produces the pickle file `TFMatrix.dat` needed to run the MEM code. Finally, to obtain the corresponding ROOT file which is needed for instance for the common classifier, run the `MEAnalysis/test/testTransferFunctions.py` script specifiying the pickle file for the resolved jet transfer functions (and the subjet transfer functions):

~~~
python testTransferFunctions.py [resolved jets transfer functions] [subjets transfer functions]
~~~

## OpenLOOPS

Compile the signal and background amplitudes, which will be placed in `OpenLoops/proclib`.
~~~
./openloops libinstall pphtt compile_extra=1
./openloops libinstall ppttjj compile_extra=1
~~~

# Known issues and bugs

## Compilation failed

Errors when compiling the code:
~~~
>> Compiling  /builds/Zurich_ttH/CMSSW_9_4_4/src/Fireworks/Core/src/FWGeoTopNodeGL.cc
In file included from /cvmfs/cms.cern.ch/slc6_amd64_gcc630/lcg/root/6.10.08/include/TGLIncludes.h:21:0,
                 from /builds/Zurich_ttH/CMSSW_9_4_4/src/Fireworks/Core/src/FWGeoTopNodeGL.cc:4:
/cvmfs/cms.cern.ch/slc6_amd64_gcc630/lcg/root/6.10.08/include/GL/glew.h:1141:20: fatal error: GL/glu.h: No such file or directory
 #include <GL/glu.h>
                    ^
~~~

This means that the base CMSSW release for nanoAOD has been updated, see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Recipe_for_CMSSW_9_4_X_and_the_c

## Installing newer matplotlib

~~~
pip install --no-deps -I --prefix $CMSSW_BASE/piplibs matplotlib kiwisolver
cd $CMSSW_BASE/piplibs
wget http://www.qhull.org/download/qhull-2015-src-7.2.0.tgz
tar xf qhull-2015-src-7.2.0.tgz
cd qhull-2015.2
make
cd $CMSSW_BASE
LD_PRELOAD=$CMSSW_BASE/piplibs/qhull-2015.2/lib/libqhull_r.so PYTHONPATH=$CMSSW_BASE/piplibs/lib/python2.7/site-packages/:$PYTHONPATH python ../Plotting/python/joosep/controlPlot.py ~/tth/gc/sparse/May16.root
~~~
