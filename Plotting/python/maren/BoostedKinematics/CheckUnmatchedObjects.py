#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf
import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses


from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

#Define cuts for taggers
class Conf:
    boost = {
        "top": {
            #Cuts set by "default"
            "pt":   200,
            "eta":  2.4,
            "drl": 1.0, #In SL events distance to lepton candidate
            "btagL": "DeepCSVL",
            #Cuts optained by optimization procedure
            "mass_inf": 160,
            "mass_sup": 280,
            "tau32SD": 0.8,
            "frec": 0.3,
        },
        "higgs": {
            #Cuts set by "default"
            "pt":   200,
            "eta":  2.4,
            "msoft": 50,
            #Cuts optained by optimization procedure
            "bbtag": 0.4,
            "btagSL": 0.7,
            "tau21SD": 0.7,
        },
    }


########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {}
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v 



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_219.root"
#full_file_names["TTH1"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_222.root"
#full_file_names["TTH2"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_223.root"
#full_file_names["TTH3"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_224.root"
#full_file_names["TTH4"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_225.root"
#full_file_names["TTH5"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_226.root"
#full_file_names["TTH6"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_227.root"
#full_file_names["TTH7"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_228.root"
#full_file_names["TTH8"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_229.root"
#full_file_names["TTH9"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_230.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["sl","dl"]
particles = ["top","higgs","topl"]




Distances = {}
DistancesTop = {}
DistancesHiggs = {}

for i in cats:
    Distances[i] = {}
    DistancesTop[i] = {}
    DistancesHiggs[i] = {}
    for j in particles:
        Distances[i][j] = ROOT.TH1F("Distances_{}_{}".format(i,j),"Distances_{}_{}".format(i,j),50,-5,5)
        Distances[i][j].Sumw2()
        DistancesTop[i][j] = ROOT.TH1F("DistancesTop_{}_{}".format(i,j),"DistancesTop_{}_{}".format(i,j),50,0,5)
        DistancesTop[i][j].Sumw2()
        DistancesHiggs[i][j] = ROOT.TH1F("DistancesHiggs_{}_{}".format(i,j),"DistancesHiggs_{}_{}".format(i,j),50,0,5)
        DistancesHiggs[i][j].Sumw2()

######################################
# Run code
########################################

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("nanoAOD/Events")

    print full_file_names[l]

    sample = ""
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"

    higgscuts = Conf.boost["higgs"]
    topcuts = Conf.boost["top"]

    counter  = 0 

    for event in ttree :
        counter += 1

        #if counter > 10000:
        #    break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event


        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenLepTop = filter(lambda x: (x.decayMode==0), event.GenTop)
        #Fiducial cut on Higgs
        GenHiggsBosonPt = filter(lambda x: (x.pt > 150 and abs(x.eta) < 2.4), event.GenHiggsBoson)
        GenHadTopPt = filter(lambda x: (x.pt > 150 and abs(x.eta) < 2.4), event.GenHadTop)

        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")



        GetCategory(event,python_conf)

        #Let's only consider SL events for top tagging
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue



        matched_fatjet = Match_two_lists(
            event.FatjetCA15SoftDrop, 'CA15SD',
            event.FatjetCA15, 'CA15',0.6)

        event.FatjetCA15 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.FatjetCA15)

        for i in event.FatjetCA15:
            if event.is_sl:
                setattr(i,"drl",Get_DeltaR_two_objects(i,event.lep_SL[0]))
            else:
                setattr(i,"drl",-1)
            setattr(i,"softdropmass",i.matched_CA15SD.mass)
            subjets = [event.FatjetCA15SoftDropSubjets[i.matched_CA15SD.subJetIdx1].btag,event.FatjetCA15SoftDropSubjets[i.matched_CA15SD.subJetIdx2].btag]
            subjets = sorted(subjets)
            setattr(i,"btag1",subjets[1])
            setattr(i,"btag2",subjets[0])
            matched = 0
            for genhiggs in event.GenHiggsBoson:
                if Get_DeltaR_two_objects(i,genhiggs) < 0.6:
                    matched = 1
            setattr(i,"matched",matched)
            setattr(i,"tau21SD",i.matched_CA15SD.tau21)
            setattr(i,"bbtagSD",i.matched_CA15SD.bbtag)
            setattr(i,"subJetIdx1",i.matched_CA15SD.subJetIdx1)
            setattr(i,"subJetIdx2",i.matched_CA15SD.subJetIdx2)
            #Get corrected mass from subjets
            s1 = lvec(event.FatjetCA15SoftDropSubjets[i.subJetIdx1])
            s2 = lvec(event.FatjetCA15SoftDropSubjets[i.subJetIdx2])
            v = s1+s2
            setattr(i,"massrecoSD",v.M())



        btag_wp = 0.1522

        Higgs = filter(
            lambda x, higgscuts=higgscuts: (
                x.pt > higgscuts["pt"]
                and abs(x.eta) < higgscuts["eta"]  
                and x.massrecoSD > higgscuts["msoft"]             
                and x.tau21SD < higgscuts["tau21SD"]
                and x.bbtag > higgscuts["bbtag"]
                and x.btag2 > higgscuts["btagSL"]
            ), event.FatjetCA15
        )


        matched_fatjet = Match_two_lists(
            event.HTTV2, 'HTT',
            event.FatjetCA15, 'CA15',0.6)

        #event.HTTV2 =  filter(lambda x: (hasattr(x,"matched_CA15")), event.HTTV2)

        matched_fatjet = Match_two_lists(
            event.HTTV2, 'HTT',
            event.FatjetCA15SoftDrop, 'CA15SD',0.6)

        event.HTTV2 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.HTTV2)

        if event.is_sl:
            for i in event.HTTV2:
                setattr(i,"drl",Get_DeltaR_two_objects(i,event.lep_SL[0]))
                subjets = [event.HTTV2Subjets[i.subJetIdx1].btag,event.HTTV2Subjets[i.subJetIdx2].btag,event.HTTV2Subjets[i.subJetIdx3].btag]
                subjets = sorted(subjets)
                setattr(i,"btag1",subjets[2])
                setattr(i,"btag2",subjets[1])
                setattr(i,"btag3",subjets[0])
                matched = 0
                for gentop in event.GenHadTop:
                    if Get_DeltaR_two_objects(i,gentop) < 0.6:
                        matched = 1
                setattr(i,"matched",matched)
                setattr(i,"tau32SD",i.matched_CA15SD.tau32)
                setattr(i,"softdropmass",i.matched_CA15SD.mass)
                if hasattr(i,"matched_CA15"):
                    setattr(i,"tau32",i.matched_CA15.tau32)
                else:
                    setattr(i,"tau32",-1)
                #Get corrected mass from subjets
                s1 = lvec(event.HTTV2Subjets[i.subJetIdx1])
                s2 = lvec(event.HTTV2Subjets[i.subJetIdx2])
                s3 = lvec(event.HTTV2Subjets[i.subJetIdx3])
                vtop = s1+s2+s3
                setattr(i,"massreco",vtop.M())
        else:
            event.HTTV2 = []

        btag_wp = 0.1522

        Top = filter(
            lambda x, topcuts=topcuts: (
                x.pt > topcuts["pt"]
                and abs(x.eta) < topcuts["eta"]
                and x.drl > topcuts["drl"]
                and x.btag1 > btag_wp
                and x.tau32SD < topcuts["tau32SD"]
                and x.massreco > topcuts["mass_inf"]
                and x.massreco < topcuts["mass_sup"]
                and x.frec < topcuts["frec"]
            ), event.HTTV2
        )


        if sample == "ttH":
            for t in Top:
                if t.matched == 0:
                    for gentop in event.GenHadTop:
                        DistancesTop[cat]["top"].Fill(Get_DeltaR_two_objects(t,gentop),event.Generator_weight)
                    DistancesTop[cat]["higgs"].Fill(Get_DeltaR_two_objects(t,event.GenHiggsBoson[0]),event.Generator_weight)
                    if len(event.GenHadTop):
                        Distances[cat]["top"].Fill(Get_DeltaR_two_objects(t,event.GenHadTop[0])-Get_DeltaR_two_objects(t,event.GenHiggsBoson[0]),event.Generator_weight)
                    for gentop in event.GenLepTop:
                        DistancesTop[cat]["topl"].Fill(Get_DeltaR_two_objects(t,gentop),event.Generator_weight)
            for h in Higgs:
                if h.matched == 0:
                    DistancesHiggs[cat]["higgs"].Fill(Get_DeltaR_two_objects(h,event.GenHiggsBoson[0]),event.Generator_weight)
                    for gentop in event.GenHadTop:
                        DistancesHiggs[cat]["top"].Fill(Get_DeltaR_two_objects(h,gentop),event.Generator_weight)
                    for gentop in event.GenLepTop:
                        DistancesHiggs[cat]["topl"].Fill(Get_DeltaR_two_objects(h,gentop),event.Generator_weight)
                    if len(event.GenHadTop):
                        Distances[cat]["higgs"].Fill(Get_DeltaR_two_objects(h,event.GenHiggsBoson[0])-Get_DeltaR_two_objects(h,event.GenHadTop[0]),event.Generator_weight)



results = ROOT.TFile("out.root","recreate")
for i in cats:
    for j in particles:
        Distances[i][j].Write()
        DistancesTop[i][j].Write()
        DistancesHiggs[i][j].Write()
