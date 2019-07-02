# Evaluate transfer functions

Transfer functions map the measured properties of jets by the detector to the underlying generated particles. These are needed for the computation of the MEM.

## Create root files with quark-jet matched information

To calculate transfer functions first we need to match the quarks from generator information with reconstructed jets. This is done by running the script [runSkimmerTF.py](runSkimmerTF.py). This is a nanoAOD postprocessing-like python script which applies some basic selection and then runs [TTH/Analyzer/python/skimTF.py](../python/skimTF.py) for the matching part.

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

Next the transfer functions are calculated via the [TFmain.py](TFmain.py) script. Before running the script, a config file needs to be created where several parameters like the samples, input variables and pt and eta splitting are defined. In the `TFmain.py` script one can find another `dictSamples` dictionary where the output dataset of the previous step can be defined. Then to run it:

~~~bash
python config.py NAME_SAMPLE
~~~
where the `NAME_SAMPLE` is the key label of the `dictSamples`. Then run the transfer functions, specifying again the key label:

~~~bash
python TFmain.py NAME_SAMPLE
~~~

This produces the pickle file `TFMatrix.dat` inside a folder named as the `NAME_SAMPLE` parameter. This is needed to run the MEM code. 

To run this last step in condor there is a [condorJob_TF.sub](condorJob_TF.sub) script. One just need to modify the first parameter `labelProcess` in the head of the script with the `NAME_SAMPLE` and then just:

```bash
condor_submit condorJob_TF.sub
```

Finally, to obtain the corresponding ROOT file which is needed for instance for the [CommonClassifier](https://gitlab.cern.ch/ttH/CommonClassifier), run the [createRootTF.py](createRootTF.py) script specifiying the pickle file for the transfer functions:

~~~bash
python createRootTF.py NAME_SAMPLE/TFMatrix.dat
~~~
