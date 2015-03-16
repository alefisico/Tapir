export SCRAM_ARCH=slc6_amd64_gcc481

scram project -n CMSSW CMSSW CMSSW_7_2_2_patch2
cd CMSSW/src/
cmsenv
git cms-addpkg PhysicsTools/PatAlgos

#for top tagger
git cms-addpkg DataFormats/JetReco
git cms-addpkg RecoJets/JetAlgorithms
git cms-addpkg RecoJets/JetProducers

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH
cd TTH
git checkout jpata/meanalysis-heppy
git clone https://github.com/jpata/Code.git MEIntegratorStandalone
cd MEIntegratorStandalone
git checkout dev
cd ../..
cp TTH/MEAnalysis/libs/*.so ../lib/$SCRAM_ARCH/

#to apply a the top tagger as a patch
git apply -3 --ignore-whitespace --ignore-space-change --exclude DataFormats/PatCandidates/src/classes_def_objects.xml TTH/0001-merged-HepTopTagger.patch

#create a commit for the toptagger to have a clean HEAD 
git checkout -b merge-toptagger
git commit -am "merged toptagger"

#Get the vhbb-heppy code
git cms-merge-topic vhbb:vhbbHeppy722patch2

#Get the fixed TChain code
git cms-merge-topic jpata:heppy-chain-lfn

scram setup lhapdf

#copy fastjet libraries
#cp $CMSSW_BASE/external/$SCRAM_ARCH/lib/* $CMSSW_BASE/lib/$SCRAM_ARCH/

# And build:
# scram b -j 10
