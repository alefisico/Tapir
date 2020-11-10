#!/usr/bin/python
import sys,os,time
import argparse, shutil
import CRABClient
from dbs.apis.dbsClient import DbsApi
#from computeGenWeights import dictSamples as allSamples
from datasets import dictSamples, checkDict
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')
dbsglobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

usage = 'usage: %prog [options]'

parser = argparse.ArgumentParser()
parser.add_argument( '-d', '--dataset', action='store', dest='dataset', default='ttHTobb', help='Type of sample' )
parser.add_argument("-y", "--year", action='store', choices=[ '2016', '2017', '2018' ],  default="2017", help="Version" )
parser.add_argument("-n", "--nano", action='store', choices=[ 'nanoAOD', 'nanoAODPost' ],  default="nanoAODPost", help="nanoAOD or nanoAODPost" )
try: args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

##### Samples
allSamples = {}
allSamples['SingleMuon_Run2016Bv1']  = '/SingleMuon/Run2016B-02Apr2020_ver1-v1/NANOAOD'
allSamples['SingleMuon_Run2016Bv2']  = '/SingleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD'
allSamples['SingleMuon_Run2016C']  = '/SingleMuon/Run2016C-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2016D']  = '/SingleMuon/Run2016D-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2016E']  = '/SingleMuon/Run2016E-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2016F']  = '/SingleMuon/Run2016F-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2016G']  = '/SingleMuon/Run2016G-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2016H']  = '/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2017B']  = '/SingleMuon/Run2017B-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2017C']  = '/SingleMuon/Run2017C-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2017D']  = '/SingleMuon/Run2017D-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2017E']  = '/SingleMuon/Run2017E-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2017F']  = '/SingleMuon/Run2017F-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2018A']  = '/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2018B']  = '/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2018C']  = '/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD'
allSamples['SingleMuon_Run2018D']  = '/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2016Bv1']  = '/SingleElectron/Run2016B-02Apr2020_ver1-v1/NANOAOD'
allSamples['SingleElectron_Run2016Bv2']  = '/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD'
allSamples['SingleElectron_Run2016C']  = '/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2016D']  = '/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2016E']  = '/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2016F']  = '/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2016G']  = '/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2016H']  = '/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2017B']  = '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2017C']  = '/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2017D']  = '/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2017E']  = '/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2017F']  = '/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2018A']  = '/EGamma/Run2018A-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2018B']  = '/EGamma/Run2018B-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2018C']  = '/EGamma/Run2018C-02Apr2020-v1/NANOAOD'
allSamples['SingleElectron_Run2018D']  = '/EGamma/Run2018D-02Apr2020-v1/NANOAOD'


## trick to run only in specific samples
processingSamples = {}
#if args.dataset.startswith('Single'):
#    for sam in allSamples:
#        if sam.startswith( args.dataset ) and sam.startswith('Single') and sam.split('Run')[1].startswith(args.year): processingSamples[ sam ] = allSamples[ sam ]

if args.dataset.startswith('all'):
    for sam in dictSamples:
        try: processingSamples[ sam ] = checkDict( sam, dictSamples )[args.year][args.nano][0]
        except KeyError: continue
else:
    for sam in dictSamples:
        if sam.startswith(args.dataset):
            try: processingSamples[ sam ] = checkDict( sam, dictSamples )[args.year][args.nano][0]
            except KeyError: continue

print processingSamples
for sample, jsample in processingSamples.items():

    ### Create a list from the dataset
    lfnList = []
    if isinstance( jsample, list ):
        for jsam in jsample:
            fileDictList = ( dbsPhys03 if jsam.endswith('USER') else dbsglobal).listFiles(dataset=jsam,validFileOnly=1)
            tmpfiles = [ "root://xrootd-cms.infn.it/"+dic['logical_file_name'] for dic in fileDictList ]
            lfnList = lfnList + tmpfiles
    else:
        if jsample:
            print jsample
            fileDictList = ( dbsPhys03 if jsample.endswith('USER') else dbsglobal).listFiles(dataset=jsample,validFileOnly=1)
            # DBS client returns a list of dictionaries, but we want a list of Logical File Names
            #lfnList = [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]
            lfnList = [ 'root://xrootd-cms.infn.it/'+dic['logical_file_name'] for dic in fileDictList ]

    if len(lfnList)>0:
        print "dataset %s has %d files" % (jsample, len(lfnList))
        textFile = open( 'txtFiles/'+sample+'_'+args.year+'.txt', 'w')
        textFile.write("\n".join(lfnList))
    else: print( sample, 'does not exist')

