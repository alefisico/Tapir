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

dictSamples = {}
dictSamples[ 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8' ] = [  '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8' ] = [ '/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8' ] = [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM',
        '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM', '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19_ext1-v1/NANOAODSIM' ]
dictSamples[ 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19_ext1-v1/NANOAODSIM' ]
dictSamples[ 'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19_ext1-v1/NANOAODSIM' ]
dictSamples[ 'ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8' ] = [ '/ST_t-channel_top_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8' ] = [ '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8' ] = [ '/THW_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8' ] = [ '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'WW_TuneCP5_13TeV-pythia8' ] = [ '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/WW_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'WZ_TuneCP5_13TeV-pythia8' ] = [ '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'ZZ_TuneCP5_13TeV-pythia8' ] = [ '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM' ]
dictSamples[ 'QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8' ] = [ '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v2/NANOAODSIM', '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', '/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v2/NANOAODSIM' ]
#    dictSamples[ 'ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02p1-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#    dictSamples[ 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#    dictSamples[ 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#    dictSamples[ 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#    dictSamples[ 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8' ] = [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#    dictSamples[ 'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8' ] = [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8' ] = [ '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8' ] = [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8' ] = [ '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'WW_TuneCP5_13TeV-pythia8' ] = [ '/WW_TuneCP5_13TeV-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#    dictSamples[ 'WZ_TuneCP5_13TeV-pythia8' ] = [ '/WZ_TuneCP5_13TeV-pythia8/algomez-NANOAOD_v02-5fb730f1ae83631a3be7a3e2c0ea6b8f/USER' ]
#    dictSamples[ 'ZZ_TuneCP5_13TeV-pythia8' ] = [ '/ZZ_TuneCP5_13TeV-pythia8/algomez-NANOAOD_v02-5fb730f1ae83631a3be7a3e2c0ea6b8f/USER' ]
#    dictSamples[ 'QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8' ] = [ '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/algomez-NANOAOD_v02-5fb730f1ae83631a3be7a3e2c0ea6b8f/USER' ]


#####################################
def computeGenWeights( inputFiles, outputName ):
    """docstring for computeGenWeights"""

    ### Open root files
    intree = ROOT.TChain("Runs")
    intree2 = ROOT.TChain("Events")
    if isinstance(inputFiles, list):
        for iFile in inputFiles:
            intree.Add(iFile)
            intree2.Add(iFile)
    else:
        intree.Add(inputFiles)
        intree2.Add(inputFiles)
    print intree.GetEntries()

    ### Convert root tree to numpy array, applying cuts
    arrays = tree2array( intree,
                            branches=['genEventCount', 'genEventSumw', 'genEventSumw2'],
                            selection='',
                            #stop=1000,  #### to test only, run only 1000 events
                            )
    arrays2 = tree2array( intree2,
                            branches=['genWeight'],
                            selection='',
                            #stop=1000,  #### to test only, run only 1000 events
                            )

    #tmp = arrays['genWeight']/arrays['genWeight'][0]
    #print 'Total number of events in sample: ', intree.GetEntries()
    #print 'Event weights per file: ', arrays['genEventSumw']
    print 'Total number of genEventCount in sample: ', sum(arrays['genEventCount'])
    print 'Total number of genEventSumw in sample: ', sum(arrays['genEventSumw'])
    print 'Total number of genEventSumw2 in sample: ', sum(arrays['genEventSumw2'])
    print 'Total sum of genWeights in sample: ', sum(arrays2['genWeight'])
    print 'Total sum of sign(genWeights) in sample: ', sum(np.sign(arrays2['genWeight']))



#####################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--datasets", action='store', dest="datasets", default="ttHTobb", help="Name of dataset to process" )
    parser.add_argument("-v", "--version", action='store', dest="version", default="v00", help="Version" )
    parser.add_argument("-y", "--year", action='store', choices=[ '2016', '2017', '2018' ],  default="2017", help="Version" )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    ### To choose dataset from dictSamples
    processingSamples = {}
    if 'all' in args.datasets:
        for sam in dictSamples: processingSamples[ sam ] = dictSamples[ sam ][ 0 if args.year.startswith('2016') else ( 1 if args.year.startswith('2017') else 2 ) ]
    else:
        for sam in dictSamples:
            if sam.startswith( args.datasets ): processingSamples[ sam ] = dictSamples[ sam ][ 0 if args.year.startswith('2016') else ( 1 if args.year.startswith('2017') else 2 ) ]
    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

    print(processingSamples)
    for isample, jsample  in processingSamples.items():

        ### Create a list from the dataset
        fileDictList = ( dbsPhys03 if jsample.endswith('USER') else dbsGlobal).listFiles(dataset=jsample,validFileOnly=1)
        print ("dataset %s has %d files" % (jsample, len(fileDictList)))
        # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        #allfiles = [ "root://cms-xrd-global.cern.ch/"+dic['logical_file_name'] for dic in fileDictList ]
        allfiles = [ "root://xrootd-cms.infn.it/"+dic['logical_file_name'] for dic in fileDictList ]

        computeGenWeights( allfiles, isample )
