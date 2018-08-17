################################################################################################
#
# Files saved at: /mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/sync
# Run tthbb13 with python python/MEAnalysis_heppy.py data/config_sync.cfg \
#                  --sample ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8 \
#                  --files /mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/sync/ttHbb/nano_ttH_sync_postprocessed.root \
#                  --numEvents 999999999
#
################################################################################################


import ROOT
import time
import sys
from collections import OrderedDict
#############################################################
############### Configure Logging
import logging
log_format = (
    '[%(asctime)s] %(levelname)-8s %(funcName)-20s %(message)s')
logging.basicConfig(
    filename='info.log',
    format=log_format,
    level=logging.INFO,
)

formatter = logging.Formatter(log_format)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
#############################################################
#############################################################
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
if True:
    ROOT.gErrorIgnoreLevel = ROOT.kWarning# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;

def makeOutputline(eventOutputDict):
    outputline = ""
    nkeys = len(eventOutputDict.keys())
    for ikey, key in enumerate(eventOutputDict.keys()):
        #Converting the floats to a sting with 4 digit precision
        if isinstance(eventOutputDict[key], float):
            value = "{:.4f}".format(eventOutputDict[key])
            if value.endswith(".0000"):
                value = value[:-len(".0000")]
        else:
            value = str(eventOutputDict[key])
        if ikey != nkeys-1:
            outputline += value+","
        else:
            outputline += value
    return outputline
    
def makeSyncTable(inputFile, outputName, isData):
    t0 = time.time()
    rFile = ROOT.TFile(inputFile, "READ")
    tree = rFile.Get("tree")
    eventOutput = OrderedDict()
    eventOutput.update({"run": -1})
    eventOutput.update({"lumi": -1})
    eventOutput.update({"event": -1})
    eventOutput.update({"is_e": -1})
    eventOutput.update({"is_mu": -1})
    eventOutput.update({ "is_ee": -1})
    eventOutput.update({"is_emu": -1})
    eventOutput.update({"is_mumu": -1})
    eventOutput.update({"n_jets": -1})
    eventOutput.update({"n_btags": -1})
    eventOutput.update({"lep1_pt": -1})
    eventOutput.update({"lep1_eta": -1})
    eventOutput.update({"lep1_iso": -1})
    eventOutput.update({"lep1_pdgId": -1})
    eventOutput.update({"lep1_idSF": -1})
    eventOutput.update({"lep1_isoSF": -1})
    eventOutput.update({"lep2_pt": -1})
    eventOutput.update({"lep2_eta": -1})
    eventOutput.update({"lep2_iso": -1})
    eventOutput.update({"lep2_idSF": -1})
    eventOutput.update({"lep2_isoSF": -1})
    eventOutput.update({"lep2_pdgId": -1})
    eventOutput.update({"jet1_pt": -1})
    eventOutput.update({"jet1_eta": -1})
    eventOutput.update({"jet1_phi": -1})
    eventOutput.update({"jet1_jesSF": -1})
    eventOutput.update({"jet1_jesSF_up": -1})
    eventOutput.update({"jet1_jesSF_down": -1})
    eventOutput.update({"jet1_jesSF_PileUpDataMC_down": -1})
    eventOutput.update({"jet1_jesSF_RelativeFSR_up": -1})
    eventOutput.update({"jet1_jerSF_nominal": -1})
    eventOutput.update({"jet1_csv": -1})
    eventOutput.update({"jet1_PUJetId": -1})
    eventOutput.update({"jet1_PUJetDiscriminant": -1})
    eventOutput.update({"jet2_pt": -1})
    eventOutput.update({"jet2_eta": -1})
    eventOutput.update({"jet2_phi": -1})
    eventOutput.update({"jet2_jesSF": -1})
    eventOutput.update({"jet2_jesSF_up": -1})
    eventOutput.update({"jet2_jesSF_down": -1})
    eventOutput.update({"jet2_jesSF_PileUpDataMC_down": -1})
    eventOutput.update({"jet2_jesSF_RelativeFSR_up": -1})
    eventOutput.update({"jet2_jerSF_nominal": -1})
    eventOutput.update({"jet2_csv": -1})
    eventOutput.update({"jet2_PUJetId": -1})
    eventOutput.update({"jet2_PUJetDiscriminant": -1})
    eventOutput.update({"MET_pt": -1})
    eventOutput.update({"MET_phi": -1})
    eventOutput.update({"mll": -1})
    eventOutput.update({"ttHFCategory": -1})
    eventOutput.update({"ttHFGenFilterTag": -1})
    eventOutput.update({"n_interactions": -1})
    eventOutput.update({"puWeight": -1})
    eventOutput.update({"csvSF": -1})
    eventOutput.update({"csvSF_lf_up": -1})
    eventOutput.update({"csvSF_hf_down": -1})
    eventOutput.update({"csvSF_cErr1_down": -1})

    output = ""
    nVars = len(eventOutput.keys())
    for ikey, key in enumerate(eventOutput.keys()):
        if ikey != nVars-1:
            output+=key+","
        else:
            output+=key
    output+="\n"
    logging.info("Using file %s",rFile.GetName())
    logging.info("Ipened tree %s",tree)
    nEvents = tree.GetEntries()
    logging.info("Will loop over %s events", nEvents)
    tdiff = time.time()
    for iev in range(nEvents):
        
        for key in eventOutput.keys():
            eventOutput[key] = -1
            
        tree.GetEvent(iev)
        if iev%5000 == 0 and iev != 0:
            logging.info("Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff))
            tdiff = time.time()

        #Meta varibales
        eventOutput["run"] = tree.run
        eventOutput["lumi"] = tree.lumi
        eventOutput["event"] = tree.evt
        #Categories
        eventOutput["is_e"] = int(tree.is_sl and abs(tree.leps_pdgId[0]) == 11)
        eventOutput["is_mu"] = int(tree.is_sl and abs(tree.leps_pdgId[0]) == 13)
        eventOutput["is_ee"] = int(tree.is_dl and abs(tree.leps_pdgId[0] == 11) and abs(tree.leps_pdgId[1]) == 11)
        eventOutput["is_emu"] = int(tree.is_dl
                                    and (
                                        (abs(tree.leps_pdgId[0]) == 11 and abs(tree.leps_pdgId[1]) == 13)
                                        or (abs(tree.leps_pdgId[0]) == 13 and abs(tree.leps_pdgId[1]) == 11)
                                    )
        )
        eventOutput["is_mumu"] = int(tree.is_dl and abs(tree.leps_pdgId[0]) == 13 and abs(tree.leps_pdgId[1]) == 13)
        #Leptons
        if tree.is_sl or tree.is_dl:
            eventOutput["lep1_pt"] = tree.leps_pt[0]
            eventOutput["lep1_eta"] = tree.leps_eta[0] 
            eventOutput["lep1_iso"] = tree.leps_iso[0] 
            eventOutput["lep1_pdgId"] = tree.leps_pdgId[0]
            eventOutput["lep1_idSF"] = tree.leps_SF_IdCutTight[0]
            eventOutput["lep1_isoSF"] = tree.leps_SF_IsoTight[0] #We also have a *Loose SF. Which to use?
        if tree.is_dl:
	    eventOutput["lep2_pt"] = tree.leps_pt[1]
            eventOutput["lep2_eta"] = tree.leps_eta[1] 
            eventOutput["lep2_iso"] = tree.leps_iso[1] 
            eventOutput["lep2_pdgId"] = tree.leps_pdgId[1]
            eventOutput["lep2_isoSF"] = tree.leps_SF_IdCutTight[1]
            eventOutput["lep2_idSF"] = tree.leps_SF_IsoTight[1]
        #Jets
        eventOutput["n_jets"] = tree.numJets
        eventOutput["n_btags"] = tree.nBDeepCSVM
        if tree.njets >= 1:
	    eventOutput["jet1_pt"] = tree.jets_pt[0]
            eventOutput["jet1_eta"] = tree.jets_eta[0]
            eventOutput["jet1_phi"] = tree.jets_phi[0]
            eventOutput["jet1_jesSF"] = tree.jets_corr_JEC[0]
            if not isData:
                eventOutput["jet1_jesSF_up"] = tree.jets_corr_JEC_Up[0]
	        eventOutput["jet1_jesSF_down"] = tree.jets_corr_JEC_Down[0]
                eventOutput["jet1_jesSF_PileUpDataMC_down"] = tree.jets_corr_JEC_PileUpDataMC_Down[0]
                eventOutput["jet1_jesSF_RelativeFSR_up"] = tree.jets_corr_JEC_RelativeFSR_Up[0]
                eventOutput["jet1_jerSF_nominal"] = tree.jets_corr_JER[0]
            eventOutput["jet1_csv"] = tree.jets_btagDeepCSV[0]
            eventOutput["jet1_PUJetId"] = tree.jets_puId[0]
        if tree.njets >= 2:
            #eventOutput["jet1_PUJetDiscriminant"] = tree.jets
	    eventOutput["jet2_pt"] = tree.jets_pt[1]
            eventOutput["jet2_eta"] = tree.jets_eta[1]
            eventOutput["jet2_phi"] = tree.jets_phi[1]
            eventOutput["jet2_jesSF"] = tree.jets_corr_JEC[1]
            if not isData:
                eventOutput["jet2_jesSF_up"] = tree.jets_corr_JEC_Up[1]
                eventOutput["jet2_jesSF_down"] = tree.jets_corr_JEC_Down[1]
	        eventOutput["jet2_jesSF_PileUpDataMC_down"] = tree.jets_corr_JEC_PileUpDataMC_Down[1]
                eventOutput["jet2_jesSF_RelativeFSR_up"] = tree.jets_corr_JEC_RelativeFSR_Up[1]
                eventOutput["jet2_jerSF_nominal"] = tree.jets_corr_JER[1]
	    eventOutput["jet2_csv"] = tree.jets_btagDeepCSV[1]
            eventOutput["jet2_PUJetId"] = tree.jets_puId[1]
            #eventOutput["jet2_PUJetDiscriminant"] = tree.jets
        eventOutput["MET_pt"] = tree.met_pt
        eventOutput["MET_phi"] = tree.met_phi
        if tree.is_dl:
            eventOutput["mll"] = tree.ll_mass
        eventOutput["ttHFCategory"] = tree.ttCls
        #eventOutput["ttHFGenFilterTag"] = 
        eventOutput["n_interactions"] = tree.nPVs
        eventOutput["puWeight"] = tree.puWeight
        eventOutput["csvSF"] = tree.btagWeight_shape
        eventOutput["csvSF_lf_up"] = tree.btagWeight_shapeLFUp
        eventOutput["csvSF_hf_down"] = tree.btagWeight_shapeHFDown
        eventOutput["csvSF_cErr1_down"] = tree.btagWeight_shapeCFERR1Down
        
        

        ########################################################
        ############# Writing all values in a line #############
        if iev != nEvents-1:
            output += makeOutputline(eventOutput)+"\n"
        else:
            output += makeOutputline(eventOutput)
        ########################################################
        ########################################################

    logging.info("Writing file %s.csv", outputName)
    with open(outputName+".csv", 'w') as f:
        f.write(output)
        
    logging.info("Total time: {0:8f}".format(time.time()-t0))
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Runs nanoAOD postprocessing')
    parser.add_argument(
        '--inFile',
        action="store",
        type=str,
        help="tthbb13 output file used as input",
        required=True,
    )
    parser.add_argument(
        '--outName',
        action="store",
        type=str,
        help="Name of the output file (enter w/o extention)",
        required=True,
    )
    parser.add_argument(
        '--isData',
        action="store_true",
        help="Set to true if running on data",
    )
    args = parser.parse_args(sys.argv[1:])
    makeSyncTable(inputFile = args.inFile, outputName = args.outName, isData = args.isData)
