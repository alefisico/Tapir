#!/usr/bin/env python

import sys,os,time
import argparse, shutil
from collections import OrderedDict
from multiprocessing import Process
from ROOT import *
from array import array
from dbs.apis.dbsClient import DbsApi
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')

#####################################################################
Variables = OrderedDict()
#Variables['NAMEinTree'] = [ histoName, bins, xmin, xmax ]
#### Event variables
Variables['nPVs']      = [ 'nPVs', 100, 0, 100 ]
Variables['met_pt']    = [ 'met_pt', 1000, 0, 1000 ]
Variables['met_phi']   = [ 'met_phi', 50, -3.0, 3.0 ]
Variables['Wmass']    = [ 'Wmass', 1000, 0, 1000 ]
Variables['mbb_closest']    = [ 'mbb_closest', 1000, 0, 1000 ]
Variables['ll_mass']    = [ 'll_mass', 1000, 0, 1000 ]
Variables['ll_pt']    = [ 'll_pt', 1000, 0, 1000 ]
######TMP
Variables['ttCls']    = [ 'ttCls', 100, -10, 90 ]
Variables['is_sl']    = [ 'is_sl', 10, 0, 10 ]
Variables['is_dl']    = [ 'is_dl', 10, 0, 10 ]
Variables['is_fh']    = [ 'is_fh', 10, 0, 10 ]
Variables['triggerDecision']    = [ 'triggerDecision', 10, 0, 10 ]
Variables['HLT_ttH_SL_el']    = [ 'HLT_ttH_SL_el', 10, 0, 10 ]
Variables['HLT_ttH_SL_mu']    = [ 'HLT_ttH_SL_mu', 10, 0, 10 ]
Variables['Flag_METFilters']    = [ 'Flag_METFilters', 10, 0, 10 ]
Variables['passMETFilters']    = [ 'passMETFilters', 10, 0, 10 ]
Variables['mem_tth_SL_1w2h2t_p']    = [ 'mem_tth_SL_1w2h2t_p', 100, 0, 1 ]


#### Jets
Variables['njets']      = [ 'njets', 20, 0, 20 ]
Variables['jets_pt']    = [ 'jets_pt', 100, 0, 1000 ]
Variables['jets_eta']   = [ 'jets_eta', 50, -3.0, 3.0 ]
Variables['jets_phi']   = [ 'jets_phi', 50, -3.0, 3.0 ]
Variables['nBDeepCSVM'] = [ 'nbjets', 20, 0, 20 ]
for ij in range(8):
    Variables['jets_pt['+str(ij)+']']  = [ 'jetsByPt_'+str(ij)+'_pt', 100, 0, 1000 ]
    Variables['jets_eta['+str(ij)+']'] = [ 'jetsByPt_'+str(ij)+'_eta', 50, -3.0, 3.0 ]
    Variables['jets_phi['+str(ij)+']'] = [ 'jetsByPt_'+str(ij)+'_phi', 50, -3.0, 3.0 ]
    Variables['jets_btagDeepCSV['+str(ij)+']'] = [ 'jetsByPt_'+str(ij)+'_btag', 50, -3.0, 3.0 ]

#### Leptons
Variables['nleps']      = [ 'nleps', 10, 0, 10 ]
Variables['leps_pt']    = [ 'leps_pt', 100, 0, 1000 ]
Variables['leps_eta']   = [ 'leps_eta', 50, -3.0, 3.0 ]
Variables['leps_phi']   = [ 'leps_phi', 50, -3.0, 3.0 ]
Variables['leps_iso']   = [ 'leps_iso', 40, 0, .20 ]
for il in range(2):
    Variables['leps_pt['+str(il)+']']  = [ 'lepsByPt_'+str(il)+'_pt', 100, 0, 1000 ]
    Variables['leps_eta['+str(il)+']'] = [ 'lepsByPt_'+str(il)+'_eta', 50, -3.0, 3.0 ]
    Variables['leps_phi['+str(il)+']'] = [ 'lepsByPt_'+str(il)+'_phi', 50, -3.0, 3.0 ]
    Variables['leps_iso['+str(il)+']'] = [ 'lepsByPt_'+str(il)+'_iso', 40, 0, .20 ]
    Variables['leps_pdgId['+str(il)+']'] = [ 'lepsByPt_'+str(il)+'_pdgId', 40, -20, 20 ]

############################################################################

ttCls = OrderedDict()
ttCls['ttll'] = '(ttCls<1)'
ttCls['ttcc'] = '(ttCls>40) && (ttCls<50)'
ttCls['ttb'] = '(ttCls==51)'
ttCls['tt2b'] = '(ttCls==52)'
ttCls['ttbb'] = '(ttCls>52) && (ttCls<57)'


############################################################################
def getHistoFromTree( chain, plotVar, weights, cuts, histo, skipEvents=0 ):
    """docstring for getHistoFromTree"""

    numEntries = int( chain.GetEntries() )  ### because I am taking every 5 events
    print '|---> Plotting: '+plotVar+'>>'+str(histo.GetName()), numEntries, chain.GetEntries(), cuts
    chain.Draw( plotVar+'>>'+str(histo.GetName()), weights*cuts, 'goff', numEntries, skipEvents ) ### goff no graphics generated

    return histo

############################################################################
def get2DHistoFromTree( fileName, treeName, plotVar1, plotVar2, weights, cuts, histo, percentage, skipEvents=0 ):
    """docstring for getHistoFromTree"""

    chain = TChain( treeName )
    chain.Add( fileName )
    numEntries = int( chain.GetEntries()*percentage*(1 if Decimal(percentage)%1==0 else 5) )  ### because I am taking every 5 events
    cuts = (cuts if Decimal(percentage)%1==0 else TCut('Entry$%5==0')+cuts)
    print '|---> Plotting: '+plotVar1+':'+plotVar2+'>>'+str(histo.GetName()), cuts
    chain.Draw( plotVar2+':'+plotVar1+'>>'+str(histo.GetName()), weights*cuts, 'goff', numEntries, skipEvents )

    return histo

############################################################################
def myPlotAnalyzer( myChain, listCuts, sample, UNC ):

    print '--- Sample ', sample

    ###################### Opening output file
    outputFileName = sample+'_'+args.version+'.root'
    outputFile = TFile( outputFileName, 'RECREATE' )

    ###################### Defining histos
    allHistos[ "eventProcessed_"+sample ] = TH1F( "eventProcessed_"+sample, "eventProcessed_"+sample, 1, 0, 1 )
    for var, infoVar in Variables.items():
        if sample.startswith('TTTo'):
            for ttXX, ttXXcond in ttCls.items():
                allHistos[ infoVar[0]+"_"+sample+'_'+ttXX ] = TH1F( infoVar[0]+"_"+sample+'_'+ttXX, infoVar[0]+"_"+sample+'_'+ttXX, infoVar[1], infoVar[2], infoVar[3] )
        else:
            allHistos[ infoVar[0]+"_"+sample ] = TH1F( infoVar[0]+"_"+sample, infoVar[0]+"_"+sample, infoVar[1], infoVar[2], infoVar[3] )

    for h in allHistos: allHistos[h].Sumw2()

    ######### Running the Analysis
    myChain.Draw( '1>>'+str(allHistos[ "eventProcessed_"+sample ].GetName()), '')
    for var, varInfo in Variables.items():
        histoName = varInfo[0]+'_'+sample
        SF = TCut("1")  ### tmp
        if sample.startswith('TTTo'):
            for ttXX, ttXXcond in ttCls.items():
                newHistoName = histoName+'_'+ttXX
                newListCuts = listCuts + TCut( ttXXcond )
                getHistoFromTree( myChain, var, SF, newListCuts, allHistos[ newHistoName ] )
        else:
            getHistoFromTree( myChain, var, SF, listCuts, allHistos[ histoName ] )

    ##### Closing
    outputFile.Write()
    print 'Writing output file: '+ outputFileName
    outputFile.Close()



#################################################################################
if __name__ == '__main__':

    usage = 'usage: %prog [options]'

    parser = argparse.ArgumentParser()
    parser.add_argument( '-s', '--sample', action='store', dest='samples', default='ttHTobb', help='Type of sample' )
    parser.add_argument( '-a', '--anChannel', action='store', dest='anChannel', default='SL', help='Type of ttbar decay: SL, DL' )
    parser.add_argument( '-u', '--unc', action='store',  dest='unc', default='', help='Process: all or single.' )
    parser.add_argument( '-l', '--lumi', action='store', type=float, default=1787, help='Luminosity, example: 1.' )
    parser.add_argument( '-b', '--batchSys', action='store_true',  dest='batchSys', default=False, help='Where to run: True lxplus, False psi.' )
    parser.add_argument( '-v', '--version', action='store', default='v01', dest='version', help='Version of the RUNAnalysis file.' )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    ##### Selection
    if args.anChannel.startswith('SL'):
        jetCut = TCut( '(njets>3) && (jets_pt[Iteration$]>30) && (abs(jets_eta[Iteration$])<2.4) && (nBDeepCSVM>1)')
        lepCut = TCut( '(nleps>0) && (abs(leps_eta[Iteration$])<2.4) && (leps_pt[0]>30)' )
        metCut = TCut( '(met_pt>20)' )
    elif args.anChannel.startswith('DL'):
        pass
    else: print 'Incorrect ttbar decay. Options: SL, DL, FH'
    preselection = jetCut + lepCut + metCut

    ##### Samples
    allSamples = {}
    allSamples[ 'EGamma_Run2018A' ] = '/EGamma/algomez-EGamma_Run2018A_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'EGamma_Run2018B' ] = '/EGamma/algomez-EGamma_Run2018B_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'EGamma_Run2018C' ] = '/EGamma/algomez-EGamma_Run2018C_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'EGamma_Run2018D' ] = '/EGamma/algomez-EGamma_Run2018D_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-8f87a7a44696406b0351f755f100b05c/USER'
    allSamples[ 'SingleMuon_Run2018A' ] = '/SingleMuon/algomez-SingleMuon_Run2018A_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'SingleMuon_Run2018B' ] = '/SingleMuon/algomez-SingleMuon_Run2018B_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'SingleMuon_Run2018C' ] = '/SingleMuon/algomez-SingleMuon_Run2018C_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'SingleMuon_Run2018D' ] = '/SingleMuon/algomez-SingleMuon_Run2018D_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-8f87a7a44696406b0351f755f100b05c/USER'
    allSamples[ 'DoubleMuon_Run2018A' ] = '/DoubleMuon/algomez-DoubleMuon_Run2018A_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'DoubleMuon_Run2018B' ] = '/DoubleMuon/algomez-DoubleMuon_Run2018B_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'DoubleMuon_Run2018C' ] = '/DoubleMuon/algomez-DoubleMuon_Run2018C_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'
    allSamples[ 'DoubleMuon_Run2018D' ] = '/DoubleMuon/algomez-DoubleMuon_Run2018D_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-8f87a7a44696406b0351f755f100b05c/USER'
    #allSamples[ ''] = '/MuonEG/algomez-tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0cddb9e2402d2a936e94a815e9296873/USER'

    allSamples[ 'ttHTobb' ] = '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-82f9a1e3d3dcf76bf6a4a44034cf6840/USER'
    allSamples[ 'TTToSemiLeptonic' ] = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/algomez-TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-0607c559a339ced63de31d38b5efa1f6/USER'
    allSamples[ 'TTTo2L2Nu' ] = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/algomez-TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_102X_v02p1-1c5958aa15d63140fc83aaccef484714/USER'

    ## trick to run only in specific samples
    dictSamples = OrderedDict()
    for sam in allSamples:
            if sam.startswith( args.samples ): dictSamples[ sam ] = allSamples[ sam ]
    allHistos = {}  ## dict for histos

    for sample, jsample in dictSamples.items():

        ##### Create a list from the dataset
        fileDictList = dbsPhys03.listFiles(dataset=jsample,validFileOnly=1)
        print "dataset %s has %d files" % (jsample, len(fileDictList))
        # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        allfiles = [ "root://cms-xrd-global.cern.ch/"+dic['logical_file_name'].replace('nano_postprocessed', 'tree') for dic in fileDictList ]  ## Previous step publish nano files but not tree, this is a trick to list

        ##### Opening root files
        myChain = TChain("tree")
        #dummy=0
        for ifile in allfiles:
            tmpFile = xroot+str(ifile) if not ifile.startswith('root') else ifile
            print 'Adding :', tmpFile
            myChain.Add( tmpFile )
            #dummy+=1
            #if dummy>0: break

        p = Process( target=myPlotAnalyzer, args=( myChain, preselection, sample, '' ) )
        p.start()
        p.join()
