# Installation

```bash
cmsrel CMSSW_10_6_5
cd CMSSW_10_6_5/src/
cmsenv

git cms-init
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools 


### adding all the packages needed
git clone ssh://git@gitlab.cern.ch:7999/algomez/tthbb13.git TTH --branch 10_6_5
git clone https://gitlab.cern.ch/Zurich_ttH/MEIntegratorStandalone.git -b 10_2_X TTH/MEIntegratorStandalone
git clone ssh://git@gitlab.cern.ch:7999/ttH/CommonClassifier.git TTH/CommonClassifier -b 10_2X_MVAvars
git clone https://gitlab.cern.ch/kit-cn-cms-public/RecoLikelihoodReconstruction.git TTH/RecoLikelihoodReconstruction
git clone git@github.com:cms-jet/JetToolbox.git JMEAnalysis/JetToolbox -b jetToolbox_102X_v2


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

## More information

 * For instructions on how to run private nanoAOD samples [click here](NanoAODTools/README.md)
 * For instructions on how to run the analyzer, [click here](Analyzer)
 * To run btag PDFs, follow [this instructions](Analyzer/test/btagPdf/README.md).
 * To run transfer functions, follow [this instructions](Analyzer/test/transferFunctions/README.md).
