#!/usr/bin/env python

import sys,os,time
import argparse, shutil
from collections import OrderedDict
from multiprocessing import Process
from ROOT import *
from array import array
from dbs.apis.dbsClient import DbsApi
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')
currentDir = os.getcwd()
gROOT.SetBatch()

#####################################################################
Variables = OrderedDict()
#Variables['NAMEinTree'] = [ histoName, bins, xmin, xmax ]
#### Event variables
Variables['nPVs']      = [ 'nPVs', 100, 0, 100 ]
Variables['met_pt']    = [ 'met_pt', 1000, 0, 1000 ]
Variables['met_phi']   = [ 'met_phi', 50, -3.0, 3.0 ]
Variables['Wmass']    = [ 'Wmass', 1000, 0, 1000 ]
#Variables['mbb_closest']    = [ 'mbb_closest', 1000, 0, 1000 ]
#Variables['ll_mass']    = [ 'll_mass', 1000, 0, 1000 ]
#Variables['ll_pt']    = [ 'll_pt', 1000, 0, 1000 ]
#######TMP
Variables['is_sl']    = [ 'is_sl', 10, 0, 10 ]
Variables['is_dl']    = [ 'is_dl', 10, 0, 10 ]
Variables['triggerDecision']    = [ 'triggerDecision', 3, 0, 3 ]
#Variables['HLT_ttH_SL_el']    = [ 'HLT_ttH_SL_el', 3, 0, 3 ]
#Variables['HLT_ttH_SL_mu']    = [ 'HLT_ttH_SL_mu', 3, 0, 3 ]
#Variables['HLT_ttH_DL_mumu']    = [ 'HLT_ttH_DL_mumu', 3, 0, 3 ]
#Variables['HLT_ttH_DL_elmu']    = [ 'HLT_ttH_DL_elmu', 3, 0, 3 ]
#Variables['HLT_ttH_DL_elel']    = [ 'HLT_ttH_DL_elel', 3, 0, 3 ]
Variables['Flag_METFilters']    = [ 'Flag_METFilters', 10, 0, 10 ]
Variables['passMETFilters']    = [ 'passMETFilters', 10, 0, 10 ]
#Variables['mem_tth_SL_1w2h2t_p']    = [ 'mem_tth_SL_1w2h2t_p', 100, 0, 1 ]
#Variables['(mem_tth_SL_2w2h2t_p)/(mem_tth_SL_2w2h2t_p+0.1*mem_ttbb_SL_2w2h2t_p)']    = [ 'mem_SL_2w2h2t', 100, 0, 1 ]
#
#
##### Jets
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

### ttbar classification
ttCls = OrderedDict()
ttCls['ttll'] = '(ttCls<1)'
ttCls['ttcc'] = '(ttCls>40) && (ttCls<50)'
ttCls['ttb'] = '(ttCls==51)'
ttCls['tt2b'] = '(ttCls==52)'
ttCls['ttbb'] = '(ttCls>52) && (ttCls<57)'


############################################################################
def getHistoFromTree( chain, plotVar, weights, cuts, histo, skipEvents=0 ):
    """Uses TChain Draw to create histogram"""

    numEntries = int( chain.GetEntries() )  ### because I am taking every 5 events
    print '|---> Plotting: '+plotVar+'>>'+str(histo.GetName()), numEntries, chain.GetEntries(), cuts
    chain.Draw( plotVar+'>>'+str(histo.GetName()), weights*cuts, 'goff', numEntries, skipEvents ) ### goff no graphics generated

    return histo


############################################################################
def myPlotAnalyzer( myChain, listCuts, sample, isData, eventCountTree, UNC ):

    print '--- Sample ', sample

    ###################### Opening output file
    outputFileName = sample+'_'+args.version+'.root'
    outputFile = TFile( outputFileName, 'RECREATE' )

    ###################### Counting numEvents
    if not isData:
        allHistos[ "genEventSumW_"+sample ] = TH1F( "genEventSumw_"+sample, "genEventSumw_"+sample, 1, 0, 1 )
        eventCountTree.GetEntry(0)
        allHistos[ "genEventSumW_"+sample ].SetBinContent( 1, eventCountTree.genEventSumw )

    ###################### Defining histos
    for sel in listCuts:
        for var, infoVar in Variables.items():
            if sample.startswith('TTTo'):
                for ttXX, ttXXcond in ttCls.items():
                    allHistos[ sel+'_'+infoVar[0]+"_"+sample+'_'+ttXX ] = TH1F( sel+'_'+infoVar[0]+"_"+sample+'_'+ttXX, sel+'_'+infoVar[0]+"_"+sample+'_'+ttXX, infoVar[1], infoVar[2], infoVar[3] )
            else:
                allHistos[ sel+'_'+infoVar[0]+"_"+sample ] = TH1F( sel+'_'+infoVar[0]+"_"+sample, sel+'_'+infoVar[0]+"_"+sample, infoVar[1], infoVar[2], infoVar[3] )

    for h in allHistos: allHistos[h].Sumw2()

    ######### Running the Analysis
    for selName, selInfo in listCuts.items():
        for var, varInfo in Variables.items():
            histoName = selName+'_'+varInfo[0]+'_'+sample
            SF = TCut("1") if isData else TCut('puWeight*(genWeight/genWeight)')
            if sample.startswith('TTTo'):
                for ttXX, ttXXcond in ttCls.items():
                    newHistoName = histoName+'_'+ttXX
                    newListCuts = selInfo + TCut( ttXXcond )
                    getHistoFromTree( myChain, var, SF, newListCuts, allHistos[ newHistoName ] )
            else:
                getHistoFromTree( myChain, var, SF, selInfo, allHistos[ histoName ] )

    ##### Closing
    outputFile.Write()
    print 'Writing output file: '+ outputFileName
    outputFile.Close()



#################################################################################
if __name__ == '__main__':

    usage = 'usage: %prog [options]'

    parser = argparse.ArgumentParser()
    parser.add_argument( '-s', '--singleFile', action='store_true', dest='singleFile', default=False, help='Run one file at the time (true) or the whole dataset (false)' )
    parser.add_argument( '-i', '--inputFile', action='store', dest='inputFile', default='/store/user/algomez/ttH/nanoPostMEAnalysis/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_102X_v02p1/190426_153044/0000/tree_115.root', help='Input file' )
    parser.add_argument( '-d', '--dataset', action='store', dest='dataset', default='ttHTobb', help='Type of sample' )
    parser.add_argument( '-u', '--unc', action='store',  dest='unc', default='', help='Process: all or single.' )
    parser.add_argument( '-b', '--batchSys', action='store_true',  dest='batchSys', default=False, help='Where to run: True lxplus, False psi.' )
    parser.add_argument( '-v', '--version', action='store', default='v01', dest='version', help='Version of the RUNAnalysis file.' )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)


    if 'Run2018' in args.dataset: isData=True
    else: isData=False
    ############# Selection
    presel = OrderedDict()
    ## General
    metFilters = TCut('(Flag_goodVertices==1) && (Flag_globalSuperTightHalo2016Filter==1) && (Flag_HBHENoiseFilter==1) && (Flag_HBHENoiseIsoFilter==1) && (Flag_EcalDeadCellTriggerPrimitiveFilter==1) && (Flag_BadPFMuonFilter==1) && (Flag_BadChargedCandidateFilter==1) && (Flag_eeBadScFilter==1) && (Flag_ecalBadCalibFilter==1)')
    ### DL
    jetCutDL = TCut( '(njets>1) && (jets_pt[Iteration$]>20) && (jets_pt[0]>30) && (jets_pt[1]>30) && (abs(jets_eta[Iteration$])<2.4) && (nBDeepCSVM>0)')
    lepCutDL = TCut( '(nleps==2) && (abs(leps_eta[Iteration$])<2.4) && (leps_pt[0]>25) && (leps_pt[1]>25)' )
    metCutDL = TCut( '(met_pt>40)' )
    triggerCutDL = TCut('(HLT_ttH_DL_elel==1) || (HLT_ttH_DL_mumu==1) || (HLT_ttH_DL_elmu==1)')
    selDL = metFilters + jetCutDL + lepCutDL + metCutDL + triggerCutDL

    ### SL
    jetCutSL = TCut( '(njets>3) && (jets_pt[Iteration$]>30) && (abs(jets_eta[Iteration$])<2.4) && (nBDeepCSVM>1)')
    lepCutSL = TCut( '(nleps==1) && (abs(leps_eta[Iteration$])<2.4) && (leps_pt[0]>30)' )
    metCutSL = TCut( '(met_pt>20)' )
    triggerCutSL = TCut('(HLT_ttH_SL_el==1) || (HLT_ttH_SL_mu==1)')
    selSL = metFilters + jetCutSL + lepCutSL + metCutSL + triggerCutSL

    presel['SL'] = selSL
    presel['DL'] = selDL
#    if args.dataset.startswith( ( 'SingleMuon', 'TTToSemi' ) ): presel['SL'] = selSL
#    elif args.dataset.startswith( ('DoubleMuon', 'MuonEG', 'TTTo2L2Nu' ) ): presel['DL'] = selDL
#    elif args.dataset.startswith( ('ttHTobb', 'EGamma', 'ST_' ) ):
#        presel['SL'] = selSL
#        presel['DL'] = selDL
#    else: print 'Incorrect ttbar decay. Options: SL, DL, FH'

    ##### Opening root files
    if not isData:
        eventCount = TChain("Runs")
        tmpEventCountFile = "root://cms-xrd-global.cern.ch/"+str(args.inputFile) if not args.inputFile.startswith('root') else args.inputFile
        print 'Adding :', tmpEventCountFile
        eventCount.Add( tmpEventCountFile )

    myChain = TChain("tree")
    tmpFile = ("root://cms-xrd-global.cern.ch/"+str(args.inputFile) if not args.inputFile.startswith('root') else args.inputFile).replace('nano_postprocessed', 'tree')
    print 'Adding :', tmpFile
    myChain.Add( tmpFile )

    allHistos = OrderedDict()
    myPlotAnalyzer( myChain, presel, args.dataset, isData, ('' if isData else eventCount), '' )
