#####################################
##### This script sum the genWeights from nanoAOD
##### To run: python computeGenWeights.py -d NAMEOFDATASET
#####################################

#!/usr/bin/env python
import argparse, os, shutil, sys
import numpy as np
import ROOT
from root_numpy import root2array, tree2array
from dbs.apis.dbsClient import DbsApi  ## talk to DBS to get list of files in this dataset
dbsGlobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')


#####################################
def computeGenWeights( inputFiles, outputName ):
    """docstring for computeGenWeights"""

    ### Open root files
    intree = ROOT.TChain("Runs")
    if isinstance(inputFiles, list):
        for iFile in inputFiles: intree.Add(iFile)
    else: intree.Add(inputFiles)
    print intree.GetEntries()

    ### Convert root tree to numpy array, applying cuts
    arrays = tree2array( intree,
                            branches=['genEventCount'],
                            selection='',
                            #stop=1000,  #### to test only, run only 1000 events
                            )

    #tmp = arrays['genWeight']/arrays['genWeight'][0]
    #print 'Total number of events in sample: ', intree.GetEntries()
    print 'Event weights per file: ', arrays['genEventCount']
    print 'Total number of events in sample: ', sum(arrays['genEventCount'])
    #print 'Total sum of genWeights in sample: ', np.sum(tmp, dtype=np.float64)



#####################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--datasets", action='store', dest="datasets", default="ttHTobb", help="Name of dataset to process" )
    parser.add_argument("-v", "--version", action='store', dest="version", default="v00", help="Version" )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    ### dictonary with samples, the second item in the list is dbsGlobal or dbsPhys03
    dictSamples = {}
    dictSamples['TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8'] = ['/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['ttHTobb_ttTo2L2Nu_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_ttTo2L2Nu_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8'] = ['/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8'] = ['/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8'] = ['/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8'] = ['/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM', dbsGlobal, 1 ]
    dictSamples['ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8'] = ['/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM', dbsGlobal, 1 ]
    #dictSamples[''] = [ '' ]

    ### To choose dataset from dictSamples
    processingSamples = {}
    if 'all' in args.datasets:
        for sam in dictSamples: processingSamples[ sam ] = dictSamples[ sam ]
    else:
        for sam in dictSamples:
            if sam.startswith( args.datasets ): processingSamples[ sam ] = dictSamples[ sam ]
    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

    for isample, jsample  in processingSamples.items():

        ### Create a list from the dataset
        fileDictList = jsample[1].listFiles(dataset=jsample[0],validFileOnly=1)
        print ("dataset %s has %d files" % (jsample[0], len(fileDictList)))
        # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        #allfiles = [ "root://cms-xrd-global.cern.ch/"+dic['logical_file_name'] for dic in fileDictList ]
        allfiles = [ "root://xrootd-cms.infn.it/"+dic['logical_file_name'] for dic in fileDictList ]

        computeGenWeights( allfiles, isample )
