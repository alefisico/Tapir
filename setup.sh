#when updating this file, don't forget to update also .gitlab-ci.yml
export SCRAM_ARCH=slc6_amd64_gcc630

cmsrel CMSSW_9_4_6_patch1
cd CMSSW_9_4_6_patch1/src/
eval `scramv1 runtime -sh`
cmsenv 
git cms-init

#As long as this is the only change to heppy, it not worth dealing w/ merge conflicts in cmssw 
#Was git cms-merge-topic jpata:heppy_fixes
git cms-addpkg PhysicsTools/HeppyCore
sed -i s/json=None/json=None,\ **kwargs/g PhysicsTools/HeppyCore/python/framework/config.py
sed -i s/triggers=triggers/triggers=triggers,\ **kwargs/g PhysicsTools/HeppyCore/python/framework/config.py

#merge rebased version of mmeinhard:BoostedNanoAOD
#inlcudes nanoAOD/master from April 7
git cms-merge-topic kschweiger:BoostedMiniAODReBaseMasterMay19


git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
#If need some additional patches on nanoAOD-tools, do this:
#cd PhysicsTools/NanoAODTools
#git remote add korbinian-nanoTools https://github.com/kschweiger/nanoAOD-tools.git
#git fetch korbinian-nanoTools
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




