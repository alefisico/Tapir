export SCRAM_ARCH=slc6_amd64_gcc530

scram project -n CMSSW CMSSW CMSSW_8_0_21
cd CMSSW/src/
eval `scramv1 runtime -sh`

git cms-init
git cms-merge-topic -u vhbb:vhbbHeppy80X

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH --branch meanalysis-80x
cd $CMSSW_BASE/src/TTH

git submodule update --init --recursive

cd $CMSSW_BASE/src

#FIXME: combine is not yet 80X?
#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit --branch 74x-root6
#after scram b clean, these need to be copied again
cp -R TTH/MEIntegratorStandalone/libs/* ../lib/$SCRAM_ARCH/
scram setup lhapdf
