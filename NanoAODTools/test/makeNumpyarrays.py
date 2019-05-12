#####################################
#####   This script is ....
#####################################

#!/usr/bin/env python
import argparse, os, shutil, sys
from collections import OrderedDict
import numpy as np
import pandas as pd
import h5py
import ROOT
from root_numpy import root2array, tree2array
from dbs.apis.dbsClient import DbsApi  ## talk to DBS to get list of files in this dataset
dbsGlobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')

##### name of variables in nanoAOD
variables = [
    "luminosityBlock",
    "run",
    "event",
    "Jet_pt",
    "Jet_eta",
    "Jet_phi",
    "Jet_mass",
    "Jet_btagDeepB",
    "nJet",
    "FatJet_pt",
    "FatJet_eta",
    "FatJet_phi",
    "FatJet_mass",
    "FatJet_btagHbb",
    "nFatJet",
    "Muon_pt",
    "Muon_eta",
    "Muon_phi",
    "Muon_mass",
    "nMuon",
    "Electron_pt",
    "Electron_eta",
    "Electron_phi",
    "Electron_mass",
    "nElectron",
    "MET_pt",
    "MET_phi",
    "MET_sumEt"
]

### list from /mnt/t3nfs01/data01/shome/creissel/TTH/sw/CMSSW_9_4_9/src/TTH/DNN/datasets/Feb12/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8.h5
#array(['njets', 'jets_pt_0', 'jets_pt_1', 'jets_pt_2', 'jets_pt_3',
#       'jets_pt_4', 'jets_pt_5', 'jets_pt_6', 'jets_pt_7', 'jets_pt_8',
#       'jets_pt_9', 'jets_eta_0', 'jets_eta_1', 'jets_eta_2',
#       'jets_eta_3', 'jets_eta_4', 'jets_eta_5', 'jets_eta_6',
#       'jets_eta_7', 'jets_eta_8', 'jets_eta_9', 'jets_phi_0',
#       'jets_phi_1', 'jets_phi_2', 'jets_phi_3', 'jets_phi_4',
#       'jets_phi_5', 'jets_phi_6', 'jets_phi_7', 'jets_phi_8',
#       'jets_phi_9', 'jets_mass_0', 'jets_mass_1', 'jets_mass_2',
#       'jets_mass_3', 'jets_mass_4', 'jets_mass_5', 'jets_mass_6',
#       'jets_mass_7', 'jets_mass_8', 'jets_mass_9', 'jets_btagDeepCSV_0',
#       'jets_btagDeepCSV_1', 'jets_btagDeepCSV_2', 'jets_btagDeepCSV_3',
#       'jets_btagDeepCSV_4', 'jets_btagDeepCSV_5', 'jets_btagDeepCSV_6',
#       'jets_btagDeepCSV_7', 'jets_btagDeepCSV_8', 'jets_btagDeepCSV_9',
#       'nleps', 'leps_pt_0', 'leps_pt_1', 'leps_eta_0', 'leps_eta_1',
#       'leps_phi_0', 'leps_phi_1', 'leps_mass_0', 'leps_mass_1', 'met_pt',
#       'met_phi', 'met_sumEt', 'evt', 'run', 'lumi', 'nBDeepCSVM',
#       'leps_px_0', 'leps_py_0', 'leps_pz_0', 'leps_en_0', 'leps_px_1',
#       'leps_py_1', 'leps_pz_1', 'leps_en_1', 'jets_px_0', 'jets_py_0',
#       'jets_pz_0', 'jets_en_0', 'jets_px_1', 'jets_py_1', 'jets_pz_1',
#       'jets_en_1', 'jets_px_2', 'jets_py_2', 'jets_pz_2', 'jets_en_2',
#       'jets_px_3', 'jets_py_3', 'jets_pz_3', 'jets_en_3', 'jets_px_4',
#       'jets_py_4', 'jets_pz_4', 'jets_en_4', 'jets_px_5', 'jets_py_5',
#       'jets_pz_5', 'jets_en_5', 'jets_px_6', 'jets_py_6', 'jets_pz_6',
#       'jets_en_6', 'jets_px_7', 'jets_py_7', 'jets_pz_7', 'jets_en_7',
#       'jets_px_8', 'jets_py_8', 'jets_pz_8', 'jets_en_8', 'jets_px_9',
#       'jets_py_9', 'jets_pz_9', 'jets_en_9', 'nbtags'], dtype=object)


#####################################
def convertRootToNumpy( inputFiles, outputName, listOfCuts ):
    """docstring for convertRootToNumpy"""

    ### Open root files
    intree = ROOT.TChain("Events")
    if isinstance(inputFiles, list):
        for iFile in inputFiles: intree.Add(iFile)
    else: intree.Add(inputFiles)

    print 'Branches to store: ', variables
    ### Convert root tree to numpy array, applying cuts
    arrays = tree2array( intree,
                            branches= variables,
                            selection=listOfCuts,
                            ##stop=1000,  #### to test only, run only 1000 events
                            )
    ### Create final arrays
    finalDict = OrderedDict()
    finalDict['evt'] = arrays['event']
    finalDict['run'] = arrays['run']
    finalDict['lumi'] = arrays['luminosityBlock']
    finalDict['met_pt'] = arrays['MET_pt']
    finalDict['met_phi'] = arrays['MET_phi']
    finalDict['met_sumEt'] = arrays['MET_sumEt']
    finalDict['njets'] = arrays['nJet']
    finalDict['nBDeepCSVM'] = np.zeros(len(arrays))
    finalDict['nleps'] = arrays['nMuon']+arrays['nElectron']

    ### Creating zero arrays for p4 leps and jets
    for var in [ 'pt', 'eta', 'phi', 'mass', 'px', 'py', 'pz', 'en', 'btagDeepCSV', 'doubleB' ]:
        for i in range(10):
            if not var.endswith('doubleB'): finalDict['jets_'+var+'_'+str(i)] = np.zeros(len(arrays))
        for i in range(5):
            if not var.endswith('CSV'): finalDict['fatjets_'+var+'_'+str(i)] = np.zeros(len(arrays))
        for i in range(2):
            if not var.startswith( ('btag', 'doubleB') ): finalDict['leps_'+var+'_'+str(i)] = np.zeros(len(arrays))


    for ievt in range(len(arrays['nJet'])):

        ### Leptons
        leps_pt = np.append( arrays['Muon_pt'][ievt], arrays['Electron_pt'][ievt] )
        leps_eta = np.append( arrays['Muon_eta'][ievt], arrays['Electron_eta'][ievt] )
        leps_phi = np.append( arrays['Muon_phi'][ievt], arrays['Electron_phi'][ievt] )
        leps_mass = np.append( arrays['Muon_mass'][ievt], arrays['Electron_mass'][ievt] )

        for ilep in range( len(leps_pt) ):
            if ilep>1: break
            tmpLepTLV = ROOT.TLorentzVector()
            tmpLepTLV.SetPtEtaPhiM( leps_pt[ilep], leps_eta[ilep], leps_phi[ilep], leps_mass[ilep]  )
            finalDict['leps_pt_'+str(ilep)][ievt] = tmpLepTLV.Pt()
            finalDict['leps_eta_'+str(ilep)][ievt] = tmpLepTLV.Eta()
            finalDict['leps_phi_'+str(ilep)][ievt] = tmpLepTLV.Phi()
            finalDict['leps_mass_'+str(ilep)][ievt] = tmpLepTLV.M()
            finalDict['leps_px_'+str(ilep)][ievt] = tmpLepTLV.Px()
            finalDict['leps_py_'+str(ilep)][ievt] = tmpLepTLV.Py()
            finalDict['leps_pz_'+str(ilep)][ievt] = tmpLepTLV.Pz()
            finalDict['leps_en_'+str(ilep)][ievt] = tmpLepTLV.E()

        ### Jet
        for ijet in range(arrays['nJet'][ievt]):
            if ijet>9: break
            tmpJetTLV = ROOT.TLorentzVector()
            tmpJetTLV.SetPtEtaPhiM( arrays['Jet_pt'][ievt][ijet], arrays['Jet_eta'][ievt][ijet], arrays['Jet_phi'][ievt][ijet], arrays['Jet_mass'][ievt][ijet]  )
            finalDict['jets_pt_'+str(ijet)][ievt] = tmpJetTLV.Pt()
            finalDict['jets_eta_'+str(ijet)][ievt] = tmpJetTLV.Eta()
            finalDict['jets_phi_'+str(ijet)][ievt] = tmpJetTLV.Phi()
            finalDict['jets_mass_'+str(ijet)][ievt] = tmpJetTLV.M()
            finalDict['jets_px_'+str(ijet)][ievt] = tmpJetTLV.Px()
            finalDict['jets_py_'+str(ijet)][ievt] = tmpJetTLV.Py()
            finalDict['jets_pz_'+str(ijet)][ievt] = tmpJetTLV.Pz()
            finalDict['jets_en_'+str(ijet)][ievt] = tmpJetTLV.E()
            finalDict['jets_btagDeepCSV_'+str(ijet)][ievt] = arrays['Jet_btagDeepB'][ievt][ijet]
            #print arrays['Jet_pt'][ievt][ijet], arrays['Jet_eta'][ievt][ijet], arrays['Jet_phi'][ievt][ijet], arrays['Jet_mass'][ievt][ijet]
            #print tmpJetTLV.Pt()
        finalDict['nBDeepCSVM'][ievt] = (arrays['Jet_btagDeepB'][ievt]>.4941).sum()

        ### FatJet
        for ifatjet in range(arrays['nFatJet'][ievt]):
            if ifatjet>4: break
            tmpFatJetTLV = ROOT.TLorentzVector()
            tmpFatJetTLV.SetPtEtaPhiM( arrays['FatJet_pt'][ievt][ifatjet], arrays['FatJet_eta'][ievt][ifatjet], arrays['FatJet_phi'][ievt][ifatjet], arrays['FatJet_mass'][ievt][ifatjet]  )
            finalDict['fatjets_pt_'+str(ifatjet)][ievt] = tmpFatJetTLV.Pt()
            finalDict['fatjets_eta_'+str(ifatjet)][ievt] = tmpFatJetTLV.Eta()
            finalDict['fatjets_phi_'+str(ifatjet)][ievt] = tmpFatJetTLV.Phi()
            finalDict['fatjets_mass_'+str(ifatjet)][ievt] = tmpFatJetTLV.M()
            finalDict['fatjets_px_'+str(ifatjet)][ievt] = tmpFatJetTLV.Px()
            finalDict['fatjets_py_'+str(ifatjet)][ievt] = tmpFatJetTLV.Py()
            finalDict['fatjets_pz_'+str(ifatjet)][ievt] = tmpFatJetTLV.Pz()
            finalDict['fatjets_en_'+str(ifatjet)][ievt] = tmpFatJetTLV.E()
            finalDict['fatjets_doubleB_'+str(ifatjet)][ievt] = arrays['FatJet_btagHbb'][ievt][ifatjet]
    #print finalDict

    ### Save array to npy/h5
    #np.save(outputName, finalDict)
    finaldf = pd.DataFrame.from_dict(finalDict)
    finaldf.to_hdf(outputName+'.h5', key='df', format='t', mode='w')
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

    ### List of cuts (preselection)
    listOfCuts='nJet>0 && Jet_pt>30 && abs(Jet_eta)<2.4 && nFatJet>0 && FatJet_pt>200 && abs(FatJet_eta)<2.4 && (nMuon>0 || nElectron>0) && Muon_pt>30 && abs(Muon_eta)<2.4 && Electron_pt>30 && abs(Electron_eta)<2.4 && MET_pt>20 '

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
