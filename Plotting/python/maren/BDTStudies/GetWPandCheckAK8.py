#OK, Assume that I have found the target efficiency I want to find for my Higgs and top tagger. 
#Scan variables to find point with the efficiency I want and choose the one which also has the highest 
#background rejection rate.

#imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
from array import array


import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf

from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *

if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsHelpers import *

########################################
# Define Input Files and
# output directory
########################################

                                      
# for the filename: basepath + filename + .root
full_file_names = {} 
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v

#full_file_names = {}
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_129.root"
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_46.root"


criteria = ["pass","total"]


countH = {}
countT = {}


for i in criteria:
    countH[i] = ROOT.TH3F("countH_{}".format(i),"countH_{}".format(i),100,0,1,100,0,1,100,0,1)
    countT[i] = ROOT.TH3F("countT_{}".format(i),"countT_{}".format(i),100,0,400,100,0,1,100,0,1)


for l in full_file_names:
    print full_file_names[l] 
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"


    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("nanoAOD/Events")

    
    counter  = 0
    for event in ttree :

        #if counter > 20000:
        #    break

        #if counter < 6495:
        #    continue

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event

        counter += 1
        
        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)  
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.FatjetAK8 = nanoTreeClasses.FatjetAK8.make_array(ttree)     
        event.SubjetAK8 = nanoTreeClasses.SubjetAK8.make_array(ttree)
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        
        
        GetCategory(event,python_conf)

        #Get event category
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue

        if cat == "dl":
            continue

        #First apply all general cuts on objects
        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4 and x.mass>50), event.FatjetCA15SoftDrop)
        event.FatjetCA15 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15)
        event.FatjetAK8 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetAK8)
        event.HTTV2 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.HTTV2)
        event.GenHadTop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHadTop)
        event.GenHiggsBoson = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHiggsBoson)

        matched_fatjet = Match_two_lists(
            event.FatjetCA15SoftDrop, 'CA15SD',
            event.FatjetCA15, 'CA15',0.5)

        event.FatjetCA15 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.FatjetCA15)

        matched_fatjet = Match_two_lists(
            event.HTTV2, 'HTT',
            event.FatjetCA15SoftDrop, 'CA15SD',0.5)

        event.HTTV2 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.HTTV2)

        for i in event.HTTV2:
            setattr(i,"drl",Get_DeltaR_two_objects(i,event.lep_SL[0]))
            subjets = [event.HTTV2Subjets[i.subJetIdx1].btag,event.HTTV2Subjets[i.subJetIdx2].btag,event.HTTV2Subjets[i.subJetIdx3].btag]
            subjets = sorted(subjets)
            setattr(i,"btagmax",subjets[2])
            setattr(i,"btagsecond",subjets[1])
            matched = 0
            for gentop in event.GenHadTop:
                if Get_DeltaR_two_objects(i,gentop) < 0.6:
                    matched = 1
            setattr(i,"matched",matched)
            setattr(i,"tau32SD",i.matched_CA15SD.tau32)
            s1 = lvec(event.HTTV2Subjets[i.subJetIdx1])
            s2 = lvec(event.HTTV2Subjets[i.subJetIdx2])
            s3 = lvec(event.HTTV2Subjets[i.subJetIdx3])
            vtop = s1+s2+s3
            setattr(i,"massreco",vtop.M())
        event.HTTV2 = filter(lambda x: (x.drl>1.5 and x.btagmax > 0.1522), event.HTTV2)

        for i in event.HTTV2:    
            countT["total"].Fill(i.mass,i.tau32SD,i.frec,event.Generator_weight)
            if i.matched == 1:
                countT["pass"].Fill(i.mass,i.tau32SD,i.frec,event.Generator_weight)



        #Do the higgs now
        if len(event.SubjetAK8) == 0:
            continue

        for i in event.FatjetAK8:
            setattr(i,"softdropmass",i.msoftdrop)
            subjets = [event.SubjetAK8[i.subJetIdx1].btag,event.SubjetAK8[i.subJetIdx2].btag]
            subjets = sorted(subjets)
            setattr(i,"btagmax",subjets[1])
            setattr(i,"btagmin",subjets[0])
            matched = 0
            for genhiggs in event.GenHiggsBoson:
                if Get_DeltaR_two_objects(i,genhiggs) < 0.6:
                    matched = 1
            setattr(i,"matched",matched)
            if getattr(i,"tau1") > 0:
                setattr(i,"tau21SD",float(getattr(i,"tau2")/getattr(i,"tau1")))
            else:
                setattr(i,"tau21SD",-1)
        event.FatjetAK8 = filter(lambda x: (x.softdropmass>50.0), event.FatjetAK8)
 

        for i in event.FatjetAK8:
            countH["total"].Fill(i.tau21SD,i.bbtag,i.btagmin,event.Generator_weight)
            if i.matched == 1:
                countH["pass"].Fill(i.tau21SD,i.bbtag,i.btagmin,event.Generator_weight)

f.Close()
print counter 
BDTInput = ROOT.TFile("out.root","recreate")
for j in criteria:
    countT[j].Write()
    countH[j].Write()
BDTInput.Close()