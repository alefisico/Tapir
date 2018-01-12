export SCRAM_ARCH=slc6_amd64_gcc630

scram project -n CMSSW CMSSW CMSSW_9_4_1
cd CMSSW/src/
eval `scramv1 runtime -sh`

git cms-init
git cms-merge-topic cms-nanoAOD:master
git cms-merge-topic kschweiger:HeppyttHbb_Jan12
git checkout -b nanoAOD cms-nanoAOD/master

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

cd $CMSSW_BASE/src
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
