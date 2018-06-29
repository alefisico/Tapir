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



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_129.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["sl"]
criteriaT = ["mass","massreco","softdropmass",]
options = ["matched","unmatched"]
scenarios = ["allHTT","HTT"]
mins = [0,0,0]
maxs = [600,600,600]



nFat = {}
matchedFatjet = {}
Count = {}
Distributions = {}


for i in cats:
    nFat[i] = {}
    matchedFatjet[i] = {}
    Distributions[i] = {}
    Count[i] = ROOT.TH1F("Count_{}".format(i),"Count_{}".format(i),50,0,600)
    Count[i].Sumw2()
    for j in scenarios:
        nFat[i][j] = ROOT.TH1F("Nfatjets_{}_{}".format(i,j),"Nfatjets_{}_{}".format(i,j),8,0,8)
        nFat[i][j].Sumw2()
        matchedFatjet[i][j] = ROOT.TH1F("MatchedFatjet_{}_{}".format(i,j),"MatchedFatjet_{}_{}".format(i,j),50,0,600)
        matchedFatjet[i][j].Sumw2()
        Distributions[i][j] = {}
        for l in options: 
            Distributions[i][j][l] = {}
            for m in criteriaT:
                ind = criteriaT.index(m)
                Distributions[i][j][l][m] = ROOT.TH1F("{}_{}_{}_{}".format(i,j,l,m),"{}_{}_{}_{}".format(i,j,l,m),50,mins[ind],maxs[ind])
                Distributions[i][j][l][m].Sumw2()


########################################
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
        #event.GenLepTop = filter(lambda x: (x.decayMode==0), event.GenTop)
        #Fiducial cut on top quark
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
        else:
            continue



        matched_fatjet = Match_two_lists(
            event.HTTV2, 'HTT',
            event.FatjetCA15, 'CA15',0.6)

        #event.HTTV2 =  filter(lambda x: (hasattr(x,"matched_CA15")), event.HTTV2)

        matched_fatjet = Match_two_lists(
            event.HTTV2, 'HTT',
            event.FatjetCA15SoftDrop, 'CA15SD',0.6)

        event.HTTV2 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.HTTV2)


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

        nFat["sl"]["allHTT"].Fill(len(event.HTTV2),event.Generator_weight)
        nFat["sl"]["HTT"].Fill(len(Top),event.Generator_weight)

 
        #And fill some basic distributions  
        for i in event.HTTV2: 
            if i.matched == 1:
                match = "matched"
            else:
                match = "unmatched"
            Distributions["sl"]["allHTT"][match]["mass"].Fill(i.mass,event.Generator_weight)
            Distributions["sl"]["allHTT"][match]["massreco"].Fill(i.massreco,event.Generator_weight)
            Distributions["sl"]["allHTT"][match]["softdropmass"].Fill(i.softdropmass,event.Generator_weight)


        for i in Top: 
            if i.matched == 1:
                match = "matched"
            else:
                match = "unmatched"
            Distributions["sl"]["HTT"][match]["mass"].Fill(i.mass,event.Generator_weight)
            Distributions["sl"]["HTT"][match]["massreco"].Fill(i.massreco,event.Generator_weight)
            Distributions["sl"]["HTT"][match]["softdropmass"].Fill(i.softdropmass,event.Generator_weight)



results = ROOT.TFile("out.root","recreate")
for i in cats:
    for j in scenarios:
        for l in options: 
            for m in criteriaT:
                Distributions[i][j][l][m].Write()
