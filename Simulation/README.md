# Simulation instructions

### LHE-GENSIM files for RunIISummer15wmLHEGS-MCRUN2_71_V1-v1

This instructions are based on this (sample)[https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/TOP-RunIIFall17wmLHEGS-00034]

~~~
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_9_3_4
cd CMSSW_9_3_4/src
cmsenv
git cms-init
git clone git@github.com:alefisico/Tapir.git -b v934
scram b -j 5
~~~

To run step0 (GENSIM from lhe file):
python config file is: `step0_LHESIM_crab_cfg.py`
crab file is: `crab_submit.py`
