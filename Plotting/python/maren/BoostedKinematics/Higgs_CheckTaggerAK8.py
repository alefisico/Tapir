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
            "drl": 1.5, #In SL events distance to lepton candidate
            "btagL": "DeepCSVL",
            #Cuts optained by optimization procedure
            "mass_inf": 160,
            "mass_sup": 380,
            "tau32SD": 0.8,
            "frec": 0.65,
        },
        "higgs": {
            #Cuts set by "default"
            "pt":   300,
            "eta":  2.4,
            "msoft": 50,
            #Cuts optained by optimization procedure
            "bbtag": 0.25,
            "btagSL": 0.5,
            "tau21": 0.8,
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


#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_130.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["sl","dl"]
criteriaH = ["pt","btag1","btag2","DRl","bbtag","mass","softdropmass","tau21","eta","ptsub","etasub","masssub"]
options = ["matched","unmatched"]
scenarios = ["allHiggs","Higgs"]
#mins = [0,0,0,0,-1,-1,0,0,0,0,-5,0,-5,0]
#maxs = [600,1,1,5,1,1,500,600,1,1,5,600,5,300]

mins = [0,0,0,0,-1,0,0,0,-5,0,-5,0]
maxs = [800,1,1,5,1,400,400,1,5,600,5,200]

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
            for m in criteriaH:
                ind = criteriaH.index(m)
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

    higgscuts = Conf.boost["higgs"]

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
        #Fiducial cut on Higgs
        GenHiggsBosonPt = filter(lambda x: (x.pt > 150 and abs(x.eta) < 2.4), event.GenHiggsBoson)

        event.FatjetAK8 = nanoTreeClasses.FatjetAK8.make_array(ttree)
        event.SubjetAK8 = nanoTreeClasses.SubjetAK8.make_array(ttree)



        GetCategory(event,python_conf)

        #Let's only consider SL events for top tagging
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue


        event.FatjetAK8 = filter(lambda x: (x.subJetIdx1 >= 0 and x.subJetIdx2 >= 0), event.FatjetAK8)


        for i in event.FatjetAK8:
            if event.is_sl:
                setattr(i,"drl",Get_DeltaR_two_objects(i,event.lep_SL[0]))
            else:
                setattr(i,"drl",-1)
            setattr(i,"softdropmass",i.msoftdrop)
            subjets = [event.SubjetAK8[i.subJetIdx1].btag,event.SubjetAK8[i.subJetIdx2].btag]
            subjets = sorted(subjets)
            setattr(i,"btag1",subjets[1])
            setattr(i,"btag2",subjets[0])
            matched = 0
            for genhiggs in event.GenHiggsBoson:
                if Get_DeltaR_two_objects(i,genhiggs) < 0.6:
                    matched = 1
            setattr(i,"matched",matched)
            if i.tau1 > 0:
                setattr(i,"tau21",i.tau2/i.tau1)
            else:
                setattr(i,"tau21",-1)
            setattr(i,"subJetIdx1",i.subJetIdx1)
            setattr(i,"subJetIdx2",i.subJetIdx2)
            #Get corrected mass from subjets
            s1 = lvec(event.SubjetAK8[i.subJetIdx1])
            s2 = lvec(event.SubjetAK8[i.subJetIdx2])
            v = s1+s2
            setattr(i,"massrecoSD",v.M())



        btag_wp = 0.1522

        Higgs = filter(
            lambda x, higgscuts=higgscuts: (
                x.pt > higgscuts["pt"]
                and abs(x.eta) < higgscuts["eta"]  
                and x.massrecoSD > higgscuts["msoft"]             
                and x.tau21 < higgscuts["tau21"]
                and x.bbtag > higgscuts["bbtag"]
                and x.btag2 > higgscuts["btagSL"]
            ), event.FatjetAK8
        )

        nFat[cat]["allHiggs"].Fill(len(event.FatjetAK8),event.Generator_weight)
        nFat[cat]["Higgs"].Fill(len(Higgs),event.Generator_weight)

        if len(GenHiggsBosonPt) > 0:
            Count[cat].Fill(GenHiggsBosonPt[0].pt,event.Generator_weight)


        if len(GenHiggsBosonPt) > 0:
            for i in event.FatjetAK8:
                if Get_DeltaR_two_objects(i,GenHiggsBosonPt[0])<0.6:
                    matchedFatjet[cat]["allHiggs"].Fill(GenHiggsBosonPt[0].pt,event.Generator_weight)
                    break
            for i in Higgs:
                if Get_DeltaR_two_objects(i,GenHiggsBosonPt[0])<0.6:
                    matchedFatjet[cat]["Higgs"].Fill(GenHiggsBosonPt[0].pt,event.Generator_weight)
                    break

        #And fill some basic distributions  
        for i in event.FatjetAK8: 
            if i.matched == 1:
                match = "matched"
            else:
                match = "unmatched"
            Distributions[cat]["allHiggs"][match]["pt"].Fill(i.pt,event.Generator_weight)
            Distributions[cat]["allHiggs"][match]["eta"].Fill(i.eta,event.Generator_weight)
            Distributions[cat]["allHiggs"][match]["btag1"].Fill(i.btag1,event.Generator_weight)
            Distributions[cat]["allHiggs"][match]["btag2"].Fill(i.btag2,event.Generator_weight)
            Distributions[cat]["allHiggs"][match]["mass"].Fill(i.mass,event.Generator_weight)
            Distributions[cat]["allHiggs"][match]["softdropmass"].Fill(i.massrecoSD,event.Generator_weight)
            Distributions[cat]["allHiggs"][match]["tau21"].Fill(i.tau21,event.Generator_weight)
            Distributions[cat]["allHiggs"][match]["DRl"].Fill(i.drl)
            Distributions[cat]["allHiggs"][match]["bbtag"].Fill(i.bbtag,event.Generator_weight)
            subjets = [event.SubjetAK8[i.subJetIdx1],event.SubjetAK8[i.subJetIdx2]]
            for j in subjets:
                Distributions[cat]["allHiggs"][match]["ptsub"].Fill(j.pt,event.Generator_weight)
                Distributions[cat]["allHiggs"][match]["etasub"].Fill(j.eta,event.Generator_weight)
                Distributions[cat]["allHiggs"][match]["masssub"].Fill(j.mass,event.Generator_weight)


        for i in Higgs: 
            if i.matched == 1:
                match = "matched"
            else:
                match = "unmatched"
            Distributions[cat]["Higgs"][match]["pt"].Fill(i.pt,event.Generator_weight)
            Distributions[cat]["Higgs"][match]["eta"].Fill(i.eta,event.Generator_weight)
            Distributions[cat]["Higgs"][match]["btag1"].Fill(i.btag1,event.Generator_weight)
            Distributions[cat]["Higgs"][match]["btag2"].Fill(i.btag2,event.Generator_weight)
            Distributions[cat]["Higgs"][match]["mass"].Fill(i.mass,event.Generator_weight)
            Distributions[cat]["Higgs"][match]["softdropmass"].Fill(i.massrecoSD,event.Generator_weight)
            Distributions[cat]["Higgs"][match]["tau21"].Fill(i.tau21,event.Generator_weight)
            Distributions[cat]["Higgs"][match]["DRl"].Fill(i.drl)
            Distributions[cat]["Higgs"][match]["bbtag"].Fill(i.bbtag,event.Generator_weight)
            subjets = [event.SubjetAK8[i.subJetIdx1],event.SubjetAK8[i.subJetIdx2]]
            for j in subjets:
                Distributions[cat]["Higgs"][match]["ptsub"].Fill(j.pt,event.Generator_weight)
                Distributions[cat]["Higgs"][match]["etasub"].Fill(j.eta,event.Generator_weight)
                Distributions[cat]["Higgs"][match]["masssub"].Fill(j.mass,event.Generator_weight)

results = ROOT.TFile("out.root","recreate")
for i in cats:
    Count[i].Write()
    for j in scenarios:
        nFat[i][j].Write()
        matchedFatjet[i][j].Write()
        for l in options: 
            for m in criteriaH:
                Distributions[i][j][l][m].Write()