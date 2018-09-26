# Tapir analyzer

This is a very early stage of a MEMAnalyzer using [MOMemta](https://momemta.github.io/) and CMSSW tools.

In this package, MoMEMta and MEMAnalyzer/MOMemtaTutorials are submodules link to the MoMEmta package.

## Instructions

~~~
cmsrel CMSSW_9_4_9
cd CMSSW_9_4_9/src/
cmsenv
git cms-init
git clone git@github.com:alefisico/Tapir.git -b v949
scram b -j 8
~~~

To compile MoMEMta (it needs cmake version >=3.7):
~~~
cd $CMSSW_BASE/src/Tapir/MoMEMta/
mkdir build; cd build
/cvmfs/cms.cern.ch/${SCRAM_ARCH}/external/cmake/3.7.0/bin/cmake .. -DCMAKE_INSTALL_PREFIX=../install/ -DPYTHON_BINDINGS=ON
make -j 8
~~~

To compile examples:
~~~
cd $CMSSW_BASE/src/Tapir/MEMAnalyzer/MOMemtaTutorials/
mkdir build; cd build
/cvmfs/cms.cern.ch/slc6_amd64_gcc630/external/cmake/3.7.0/bin/cmake .. -DCMAKE_PREFIX_PATH=${CMSSW_BASE}/src/Tapir/MoMEMta/build/
make -j 8
~~~
