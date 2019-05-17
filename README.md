# Installation

```bash
cmsrel CMSSW_10_2_12
cd CMSSW_10_2_12/src/
cmsenv

git cms-init
git cms-merge-topic cms-nanoAOD:master-102X   ### merging latest version of cms-nanoAOD
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools 

## this is a temporary fix. It just includes all the JECs and PU files.
wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Autumn18_RunA_V8_DATA.tar.gz
wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Autumn18_RunB_V8_DATA.tar.gz
wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Autumn18_RunC_V8_DATA.tar.gz
wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Autumn18_RunD_V8_DATA.tar.gz
wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Autumn18_V8_MC.tar.gz 
for ifile in `ls *gz`; do tar -xvf ${ifile} -C $CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/jme/; done
rm *gz
wget https://github.com/alefisico/nanoAOD-tools/raw/102X/python/postprocessing/data/pileup/pileup_Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.root -P $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/


### adding all the packages needed
git clone ssh://git@gitlab.cern.ch:7999/algomez/tthbb13.git TTH --branch 10_2_X  ## this is temporary 
git clone https://gitlab.cern.ch/Zurich_ttH/MEIntegratorStandalone.git -b 10_2_X TTH/MEIntegratorStandalone
git clone ssh://git@gitlab.cern.ch:7999/ttH/CommonClassifier.git TTH/CommonClassifier
git clone https://gitlab.cern.ch/kit-cn-cms-public/RecoLikelihoodReconstruction.git TTH/RecoLikelihoodReconstruction
git clone ssh://git@gitlab.cern.ch:7999/chreisse/TTH_massfit.git TTH/DNN   ########## THIS IS NOT NEEDED


mkdir -p $CMSSW_BASE/lib/$SCRAM_ARCH/
cp -R TTH/MEIntegratorStandalone/libs/* $CMSSW_BASE/lib/$SCRAM_ARCH/
scram setup lhapdf
scram setup TTH/MEIntegratorStandalone/deps/gsl.xml

cmsenv
scram b -j 8
```

Note that if you run `scram b clean`, the matrix element library OpenLoops will be deleted from CMSSW, which will result in errors like
~~~
[OpenLoops] ERROR: register_process: proclib folder not found, check install_path or install libraries.
~~~
In order to fix this, you have to re-copy the libraries:

```bash
mkdir -p $CMSSW_BASE/lib/$SCRAM_ARCH/
cp -R TTH/MEIntegratorStandalone/libs/* $CMSSW_BASE/lib/$SCRAM_ARCH/
scram setup lhapdf
scram setup TTH/MEIntegratorStandalone/deps/gsl.xml

cmsenv
scram b -j 8
```
*More info coming up*
