# ttH(bb) MEM code for Run 2

Setup on SLC6 in a clean directory (no CMSSW) on a **shared file system (NFS)**
~~~
$ mkdir -p ~/tth/sw
$ cd ~/tth/sw
$ wget --no-check-certificate https://gitlab.cern.ch/jpata/tthbb13/raw/SwitchNanoAOD/setup.sh
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

## Step0: environment

We use rootpy in the plotting code, which is installed on T3_CH_PSI locally in `/swshare/anaconda`.

## Step1: Running the nanoAOD code

NanoAOD links:
1. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD
2. https://github.com/cms-nanoAOD/cmssw/issues

## Step2: tthbb13 code
Using the nanoAOD-tree, we will run the ttH(bb) and matrix element code (tthbb13). The code is configured mainly from two files:

1. A flat configuration in https://gitlab.cern.ch/jpata/tthbb13/blob/SwitchNanoAOD/MEAnalysis/data/default.cfg specifying the samples and analysis categories. This configuration should be preferred for most future options.
2. A python configuration in https://gitlab.cern.ch/jpata/tthbb13/blob/SwitchNanoAOD/MEAnalysis/python/MEAnalysis_cfg_heppy.py used for the MEM configuration and specifying the object (jet, lepton) cuts. 

In order to test the `tthbb13` code, run:
~~~
$ python $CMSSW_BASE/src/TTH/MEAnalysis/python/test_MEAnalysis_heppy.py --sample ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8
~~~

This will call
~~~
python $CMSSW_BASE/src/TTH/MEAnalysis/python/MEAnalysis_heppy.py MEAnalysis/data/default.cfg --sample SAMPLE_NAME
~~~

## Step3 (optional): skim with `projectSkim`

When some of the samples are done, you can produce smallish (<10GB) skims of the files using local batch jobs.

~~~
$ cd TTH/MEAnalysis/gc
$ source makeEnv.sh #make an uncommited script to properly set the environment on the batch system
v./grid-control/go.py confs/projectSkim.conf
... #wait
$ ./hadd.py /path/to/output/GC1234/ #call our merge script
~~~

This will produce some skimmed ntuples in
~~~
/mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GCe0f041d65b98:
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

# Continous integration (CI)

We test the code regularly using the gitlab CI system. Since we are accessing the samples from T3_CH_PSI, this currently requires a valid proxy at CERN. 

