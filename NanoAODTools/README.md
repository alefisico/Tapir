# ttHbb13 nanoAODTools

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

