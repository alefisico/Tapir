export SCRAM_ARCH=slc6_amd64_gcc630

scram project -n CMSSW CMSSW CMSSW_9_4_5_cand1
cd CMSSW/src/
eval `scramv1 runtime -sh`

#need to add these always also to ../.gitlab-ci.yml in the compile stage
git cms-init
git cms-merge-topic kschweiger:cmssw945c1_boostedNano #Created with cmsswSetup.sh

git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
#Until nanoAOD tools RP#68 is merged:
cd PhysicsTools/NanoAODTools
git remote add korbinian-nanoTools https://github.com/kschweiger/nanoAOD-tools.git
git fetch korbinian-nanoTools
git cherry-pick 1875f7198e87e25626e3c10341e44ca18a33ae77
cd $CMSSW_BASE/src

#get the TTH code
git clone ssh://git@gitlab.cern.ch:7999/jpata/tthbb13.git TTH --branch SwitchNanoAOD
cd $CMSSW_BASE/src/TTH

git submodule update --init --recursive

cd $CMSSW_BASE/src

#FIXME: combine is not yet 80X?
#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit --branch 74x-root6
#after scram b clean, these need to be copied again
cp -R TTH/MEIntegratorStandalone/libs/* ../lib/$SCRAM_ARCH/
scram setup lhapdf
scram setup TTH/MEIntegratorStandalone/deps/gsl.xml


