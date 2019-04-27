#####################################
#####   This script is ....
#####################################

#!/usr/bin/env python
import argparse, os, shutil, sys
import numpy as np
import ROOT
from root_numpy import root2array, tree2array
from dbs.apis.dbsClient import DbsApi  ## talk to DBS to get list of files in this dataset
dbsGlobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')

##### dictionary with variables
variables = {}
variables["luminosityBlock"] = 'lumi'
variables["run"] = 'run'
variables["event"] = 'event'
variables["Jet_pt"] = 'jets_pt'
variables["Jet_eta"] = 'jets_eta'
variables["Jet_phi"] = 'jets_phi'
variables["Jet_mass"] = 'jets_mass'
variables["Jet_btagDeepB"] = 'jets_btagDeepB'
variables["nJet"] = 'njets'
variables["FatJet_pt"] = 'fatjets_pt'
variables["FatJet_eta"] = 'fatjets_eta'
variables["FatJet_phi"] = 'fatjets_phi'
variables["FatJet_mass"] = 'fatjets_mass'
variables["FatJet_btagHbb"] = 'fatjets_btagHbb'
variables["nFatJet"] = 'nfatjets'
variables["Muon_pt"] = 'muons_pt'
variables["Muon_eta"] = 'muons_eta'
variables["Muon_phi"] = 'muons_phi'
variables["Muon_mass"] = 'muons_mass'
variables["nMuon"] = 'nmuons'
variables["Electron_pt"] = 'electrons_pt'
variables["Electron_eta"] = 'electrons_eta'
variables["Electron_phi"] = 'electrons_phi'
variables["Electron_mass"] = 'electrons_mass'
variables["nElectron"] = 'nelectrons'


#####################################
def convertRootToNumpy( inputFiles, outputName, listOfCuts ):
    """docstring for convertRootToNumpy"""

    ### Open root files
    intree = ROOT.TChain("Events")
    if isinstance(inputFiles, list):
        for iFile in inputFiles: intree.Add(iFile)
    else: intree.Add(inputFiles)

    ### Rename root branches
    branchesToStore = []
    newNames = []
    for oldVar, newVar in variables.items():
        branchesToStore.append(oldVar)
        newNames.append(newVar)
    print 'Branches to store: ', branchesToStore

    ### Convert root tree to numpy array, applying cuts
    arrays = tree2array( intree,
                            branches= branchesToStore,
                            selection=listOfCuts,
                            #stop=1000,  #### to test only, run only 1000 events
                            )
    arrays.dtype.names = newNames   ## name the arrays according to variables[]

    ### Save array to npy
    np.save(outputName, arrays)
    print('Done')

#####################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--singleFile", action='store_true', dest="singleFile", default=False, help="Flag, to run on a single file" )
    parser.add_argument("-i", "--inputFile", action='store', dest="inputFile", default='/store/mc/RunIIFall17NanoAODv4/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/280000/17B6FD34-5496-A141-86FF-D07FA215EB0A.root', help="To run on single file" )
    parser.add_argument("-o", "--outputFile", action='store', dest="outputFile", default='out', help="Name of output file" )
    parser.add_argument("-d", "--datasets", action='store', dest="datasets", default="ttHTobb", help="Name of dataset to process" )
    parser.add_argument("-v", "--version", action='store', dest="version", default="v00", help="Version" )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    ### dictonary with samples, to run local
    dictSamples = {}
    dictSamples['ttHTobb'] = [ '/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', dbsGlobal ]
    #dictSamples[''] = [ '' ]

    ### List of cuts
    listOfCuts='nJet>3 && Jet_pt>30 && abs(Jet_eta)<2.4 && nFatJet>0 && (nMuon>0 || nElectron>0)'

    ### To run script one file at the time, for condor
    if args.singleFile:
        if not args.inputFile.startswith('root'): ifile = "root://cms-xrd-global.cern.ch/"+args.inputFile
        else: ifile = args.inputFile
        print 'Converting ', ifile
        convertRootToNumpy( ifile, args.datasets+'_'+args.outputFile, listOfCuts )

    ### To run script with the dataset
    else:
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
            allfiles = [ "root://cms-xrd-global.cern.ch/"+dic['logical_file_name'] for dic in fileDictList ]

            dummy=0
            for ifile in allfiles:
                print 'Converting ', ifile
                convertRootToNumpy( ifile, isample+"_"+str(dummy), listOfCuts )
                dummy+=1

            print "Done. Output files: ", isample
