#!/bin/bash
PATH=/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/bin/slc6_amd64_gcc491:/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/external/slc6_amd64_gcc491/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/bin/slc6_amd64_gcc491:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/external/slc6_amd64_gcc491/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/llvm/3.6/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/bin:/cvmfs/cms.cern.ch/common:/cvmfs/cms.cern.ch/bin:/bin:/mnt/t3nfs01/data01/shome/gregor/anaconda2/bin:/gridware/sge/bin/lx24-amd64:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/mnt/t3nfs01/data01/swshare/psit3/bin:/mnt/t3nfs01/data01/shome/gregor/bin
LD_LIBRARY_PATH=/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/biglib/slc6_amd64_gcc491:/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/lib/slc6_amd64_gcc491:/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/external/slc6_amd64_gcc491/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/biglib/slc6_amd64_gcc491:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/lib/slc6_amd64_gcc491:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/external/slc6_amd64_gcc491/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/llvm/3.6/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/lib64:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/lib
PYTHONPATH=/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/python:/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/lib/slc6_amd64_gcc491:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/python:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/lib/slc6_amd64_gcc491:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/coral/CORAL_2_3_21-odfocd8/slc6_amd64_gcc491/python:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/coral/CORAL_2_3_21-odfocd8/slc6_amd64_gcc491/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/pyqt/4.8.1-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python-ldap/2.4.10-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-scipy/0.8.0-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-matplotlib/1.2.1-cms3/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/yoda/1.3.1/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/sip/4.11.2-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/llvm/3.6/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-sqlalchemy/0.8.2-eccfad/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-pytz/2014.7/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-pycurl/7.19.0-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-python-dateutil/1.1-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-numpy/1.6.1-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-lint/0.25.1-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-ipython/3.1.0-odfocd/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-dxr/1.0-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-cx-oracle/5.1-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-cjson/1.0.5-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/frontier_client/2.8.11/python/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/das-client/2.5.0-cms/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/cython/0.22/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/rivet/2.2.1-odfocd/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-odfocd5/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/pyminuit2/0.0.1-odfocd5/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-pygithub/1.23.0-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-networkx/1.8.1-cms3/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-pygments/1.6-cms/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-parsimonious/0.6.1/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-ordereddict/1.1/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-markupsafe/0.23/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-jinja/2.7.2/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-futures/2.2.0/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/py2-dablooms/0.9.1/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/professor/1.0.0-odfocd5/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/dbs-client/DBS_2_1_9-cms/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/dbs-client/DBS_2_1_9-cms/lib/DBSAPI:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/cvs2git/5419-cms/lib
GENREFLEX=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-odfocd5/bin/genreflex
ROOTSYS=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-odfocd5/
ROOT_INCLUDE_PATH=/mnt/t3nfs01/data01/shome/gregor/CMSSW_FOR_COMBINE/CMSSW_7_4_7/src:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_7/src:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/coral/CORAL_2_3_21-odfocd8/include/LCG:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/mctester/1.25.0a-odfocd5/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-odfocd5/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/QtDesigner:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/tauolapp/1.1.5-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/charybdis/1.003-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/thepeg/1.9.2p1-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/sherpa/2.1.1-odfocd2/include/SHERPA-MC:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/QtOpenGL:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/QtGui:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/pythia8/205-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/herwig/6.521-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/QtScript:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/Qt3Support:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/classlib/3.1.3-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/lhapdf/6.1.5-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/cgal/4.2-jlbgio/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/tkonlinesw/2.7.0-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/Qt:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/QtCore:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/qt/4.8.1-cms/include/QtXml:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/mcdb/1.0.2-cms/interface:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libungif/4.1.4-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libtiff/3.9.4-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libpng/1.6.16/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/geant4/10.00.p02-cms/include/Geant4:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/frontier_client/2.8.11/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/evtgenlhc/9.1-cms:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/pcre/7.9__8.33-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/boost/1.57.0-jlbgio/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xz/5.0.3__5.1.2alpha-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xrootd/4.0.4-odfocd/include/xrootd/private:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/vdt/v0.3.2-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/valgrind/3.10.1/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/toprex/4.23-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/tbb/43_20141023oss/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/tauola/27.121.5-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/sigcpp/2.2.10-cms/include/sigc++-2.0:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/rivet/2.2.1-odfocd/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/sqlite/3.7.17-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/protobuf/2.4.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/pacparser/1.3.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/oracle/11.2.0.3.0__10.2.0.4.0-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/meschach/1.2.pCMS1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libhepml/0.2.1-cms/interface:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/ktjet/1.06-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/jimmy/4.2-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/jemalloc/3.5.0-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libxml2/2.7.7-cms/include/libxml2:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/herwigpp/2.7.1-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/heppdt/3.03.00-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/hector/1_3_4-odfocd6/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gsl/1.10-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libjpg/8b-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xerces-c/2.8.0-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gdbm/1.10-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/fftw3/3.3.2-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/fftjet/1.5.0-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/fastjet/3.1.0-odfocd/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/expat/2.0.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/hepmc/2.06.07-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/dpm/1.8.0.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/dcap/2.47.8-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/db4/4.4.20-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/curl/7.28.0-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/cppunit/1.12.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/clhep/2.1.4.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/openssl/0.9.8e__1.0.1-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/pythia6/426-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/photos/215.5-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/zlib/1.2.8-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libuuid/2.22.2-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/castor/2.1.13.9-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/castor/2.1.13.9-cms/include/shift:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/cascade/2.2.04-koleij/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/bz2lib/1.0.5-cms/include:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms/include/python2.7:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/include/c++/4.9.1:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/include/c++/4.9.1/x86_64-redhat-linux-gnu:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/include/c++/4.9.1/backward:/usr/local/include:/usr/include

ORIG=`pwd`
BASE=`dirname $1`
FILE=`basename $1`

#cd $BASE
#combine -n result -M Asymptotic -t -1 $FILE
#cd $ORIG

cd $BASE
text2workspace.py $FILE -m 125 -b -o model.root
combine model.root -M Asymptotic --minimizerStrategy 0 --minimizerTolerance 0.1 -m 125 -n sig_0_5 -t -1 --expectSignal=0.5
combine model.root -M Asymptotic --minimizerStrategy 0 --minimizerTolerance 0.1 -m 125 -n sig_1_0 -t -1 --expectSignal=1.0
combine model.root -M Asymptotic --minimizerStrategy 0 --minimizerTolerance 0.1 -m 125 -n sig_1_5 -t -1 --expectSignal=1.5
combine model.root -M Asymptotic --minimizerStrategy 0 --minimizerTolerance 0.1 -m 125 -n sig_2_0 -t -1 --expectSignal=2.0
cd $ORIG
