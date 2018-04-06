export SCRAM_ARCH=slc6_amd64_gcc630

scram project -n CMSSW CMSSW CMSSW_9_4_4
cd CMSSW/src/
eval `scramv1 runtime -sh`

git cms-init
git cms-merge-topic cms-nanoAOD:master
git cms-merge-topic kschweiger:HeppyttHbb_Jan12
git checkout -b nanoAOD cms-nanoAOD/master
git cms-merge-topic -s ours mmeinhard:BoostedNanoAOD
git cms-merge-topic jpata:heppy_fixes #fix for Heppy DataComponent
