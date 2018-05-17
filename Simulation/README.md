# Simulation instructions

### LHE-GENSIM files for RunIISummer15wmLHEGS-MCRUN2_71_V1-v1

This instructions are based on this sample: https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIISummer15wmLHEGS-00482

```
export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_1_25
cd CMSSW_7_1_25/src
cmsenv
git cms-init
git clone git@github.com:alefisico/Tapir.git -b v7125
scram b -j 5
```

To run step0 (GENSIM from lhe file):
python config file is: `step0_LHESIM_crab_cfg.py`
crab file is: `crab_submit.py`
