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

class Jet:
    def __init__(self, tree, n,name):
        self.pt = getattr(tree,"{}_pt".format(name))[n]
        self.eta = getattr(tree,"{}_eta".format(name))[n]
        self.phi = getattr(tree,"{}_phi".format(name))[n]
        self.mass = getattr(tree,"{}_mass".format(name))[n]
        if name == "jets":
            self.btagDeepCSV = getattr(tree,"{}_btagDeepCSV".format(name))[n]
        pass
    @staticmethod
    def make_array(input,name):
        return [Jet(input, i, name) for i in range(getattr(input,"n{}".format(name)))]

class SubJetTop:
    def __init__(self, tree, n,name):
        self.pt = getattr(tree,"topCandidate_sj{}pt".format(n))[0]
        self.eta = getattr(tree,"topCandidate_sj{}eta".format(n))[0]
        self.phi = getattr(tree,"topCandidate_sj{}phi".format(n))[0]
        self.mass = getattr(tree,"topCandidate_sj{}mass".format(n))[0]
        self.btag = getattr(tree,"topCandidate_sj{}btag".format(n))[0]
        pass
    @staticmethod
    def make_array(input,name):
        return [SubJetTop(input, i, name) for i in range(1,4) if input.ntopCandidate > 0]

class SubJetHiggs:
    def __init__(self, tree, n,name):
        self.pt = getattr(tree,"higgsCandidate_sj{}pt".format(n))[0]
        self.eta = getattr(tree,"higgsCandidate_sj{}eta".format(n))[0]
        self.phi = getattr(tree,"higgsCandidate_sj{}phi".format(n))[0]
        self.mass = getattr(tree,"higgsCandidate_sj{}mass".format(n))[0]
        self.btag = getattr(tree,"higgsCandidate_sj{}btag".format(n))[0]
        pass
    @staticmethod
    def make_array(input,name):
        return [SubJetHiggs(input, i, name) for i in range(1,3) if input.nhiggsCandidate > 0]


########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {} 
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v

#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Jun29_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Jun29_withME/180629_212218/0000/tree_117.root"
#full_file_names["TTH2"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_43.root"
#full_file_names["TTH3"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_44.root"
#full_file_names["TTH4"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_45.root"
#full_file_names["TTH5"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_46.root"
#full_file_names["TTH6"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_47.root"
#full_file_names["TTH7"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_48.root"
#full_file_names["TTH8"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_49.root"
#full_file_names["TTH9"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_50.root"
#full_file_names["TTH10"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_51.root"
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
resolved = anc[:4]
boosted = anc[4:]
cats = ["higgs","top"]
criteria = ["gen","boosted"]
limits = [100,1,1,100]

jettype = ["njets","nbjets","njetsb","nbjetsb","jetsdiff","jetsdiffb"] 

evttype = ["new","old"]

quarks = ["hb","tb","tl"]
variables = ["pt","eta","phi","mass"]

pt = {}
pt2 = {}
matching = {}
jets = {}

numNE = ROOT.TH1F("numNE","numNE",10,0,10)
dist = ROOT.TH1F("distbquark","distbquark",100,0,5)
for i in cats:
    pt[i] = {}
    pt2[i] = {}
    for j in criteria:
        pt[i][j] = ROOT.TH1F("pt_{}_{}".format(i,j),"pt_{}_{}".format(i,j),100,0,800)
        pt2[i][j] = ROOT.TH1F("pt_ResEvents_{}_{}".format(i,j),"pt_ResEvents_{}_{}".format(i,j),100,0,800)
for i in jettype:
    jets[i] = ROOT.TH1F("njet_{}".format(i),"njet_{}".format(i),20,-10,10)
for i in evttype:
    matching[i] = ROOT.TH1F("matching_{}".format(i),"matching_{}".format(i),10,0,10)

count = {}
for i in evttype:
    count[i] = {}
    for j in quarks:
        count[i][j] = {}
        for l in variables:
            m = variables.index(l)
            count[i][j][l] = ROOT.TH1F("count_{}_{}_{}".format(i,j,l),"count_{}_{}_{}".format(i,j,l),100,-limits[m],limits[m])



########################################
# Run code
########################################


for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("tree")

    print full_file_names[l]

    sample = ""
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"


    counter = 0

    for event in ttree :
        counter += 1

        #if counter > 20000:
        #    break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.evt

        matchtop = 0
        matchhiggs = 0

        if event.boosted == 1:
            if event.nhiggsCandidate > 0 and event.ntopCandidate > 0:
                typ = "both"
            elif event.nhiggsCandidate > 0 and event.ntopCandidate == 0:
                typ = "higgs"
            elif event.nhiggsCandidate == 0 and event.ntopCandidate > 0:
                typ = "top"
            if event.nhiggsCandidate > 0 and event.nMatch_b_higgs == 2:
                matchhiggs = 1
            if event.ntopCandidate > 0 and event.nMatch_b_htt == 1 and event.nMatch_q_htt == 2:
                matchtop = 1


        event.mem_resolved = 0
        event.mem_boosted = 0
        event.cat_resolved = None
        event.cat_boosted = None
        for m in resolved:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                event.mem_resolved = getattr(event,"mem_{}_p".format(m))
                event.cat_resolved = m
        for m in boosted:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                event.mem_boosted = getattr(event,"mem_{}_p".format(m))
                event.cat_boosted = m


        TopSubjet = SubJetTop.make_array(ttree,"GenQFromW")
        HiggsSubjet = SubJetHiggs.make_array(ttree,"GenQFromW")
        GenBFromHiggs = Jet.make_array(ttree,"GenBFromHiggs")
        GenBFromTop = Jet.make_array(ttree,"GenBFromTop")
        GenQFromW = Jet.make_array(ttree,"GenQFromW")

        #Filter out newly boosted events
        if event.cat_resolved is not None:
            #if event.cat_boosted is None:
            if event.ngenHiggs > 0:
                pt2["higgs"]["gen"].Fill(event.genHiggs_pt[0],event.genWeight)
            if event.ngenTopHad > 0:
                pt2["top"]["gen"].Fill(event.genTopHad_pt[0],event.genWeight)
            if event.cat_boosted is not None:
                if event.ntopCandidate > 0:
                    if matchtop == 1:
                        matching["old"].Fill(1,event.genWeight)
                    else:
                        matching["old"].Fill(2,event.genWeight)

                    sorted(TopSubjet, key=lambda x: x.btag, reverse=True)
                    matched_genb = Match_two_lists(
                    [TopSubjet[0]], 'subjetsTop',
                    GenBFromTop, 'genQuark',0.3)
                    matched_genl = Match_two_lists(
                    [TopSubjet[1]] + [TopSubjet[2]], 'subjetsTop',
                    GenQFromW, 'genQuark',0.3)
                    for subjet in TopSubjet:
                        if subjet.pt > 30:
                            index = TopSubjet.index(subjet)
                            if hasattr(subjet,"matched_genQuark"):
                                for var in variables:
                                    if index == 0:
                                        count["old"]["tb"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))
                                    else:
                                        count["old"]["tl"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))

                if event.nhiggsCandidate > 0:
                    if matchhiggs == 1:
                        matching["old"].Fill(3,event.genWeight)
                    else:
                        matching["old"].Fill(4,event.genWeight)

                    matched_gen = Match_two_lists(
                    HiggsSubjet, 'subjetsHiggs',
                    GenBFromHiggs, 'genQuark',0.3) 
                    for subjet in HiggsSubjet:
                        if hasattr(subjet,"matched_genQuark"):
                            for var in variables:
                                count["old"]["hb"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))


        #
            continue
        if event.cat_boosted is None:
            continue

        numNE.Fill(0,event.genWeight)

        if typ == "top":
            numNE.Fill(1,event.genWeight)
        if typ == "higgs":
            numNE.Fill(2,event.genWeight)
        if typ == "both":
            numNE.Fill(3,event.genWeight)
        if event.cat_boosted == "SL_2w2h2t_sj":
            numNE.Fill(4,event.genWeight)
        elif event.cat_boosted == "SL_1w2h2t_sj":
            numNE.Fill(5,event.genWeight)
        elif event.cat_boosted == "SL_0w2h2t_sj":
            numNE.Fill(6,event.genWeight)
        elif event.cat_boosted == "DL_0w2h2t_sj":
            numNE.Fill(7,event.genWeight)




        if event.ngenHiggs > 0 and event.nhiggsCandidate > 0:
            pt["higgs"]["gen"].Fill(event.genHiggs_pt[0],event.genWeight)
        if event.nhiggsCandidate > 0:
            pt["higgs"]["boosted"].Fill(event.higgsCandidate_pt[0],event.genWeight)
        if event.ngenTopHad > 0 and event.ntopCandidate > 0:
            pt["top"]["gen"].Fill(event.genTopHad_pt[0],event.genWeight)
        if event.ntopCandidate > 0:
            pt["top"]["boosted"].Fill(event.topCandidate_pt[0],event.genWeight)

        jets["njets"].Fill(event.numJets,event.genWeight)
        jets["nbjets"].Fill(event.nBDeepCSVM,event.genWeight)
        jets["njetsb"].Fill(event.n_boosted_bjets+event.n_boosted_ljets,event.genWeight)
        jets["nbjetsb"].Fill(event.n_boosted_bjets,event.genWeight)
        jets["jetsdiff"].Fill(event.n_boosted_bjets+event.n_boosted_ljets-event.numJets,event.genWeight)
        jets["jetsdiffb"].Fill(event.n_boosted_bjets-event.nBDeepCSVM,event.genWeight)


        bquarks = GenBFromHiggs + GenBFromTop

        Jets = Jet.make_array(ttree,"jets")


        ### Make some check for untagged jets - Why is b-tagging not working so well?
        if event.nBDeepCSVM  < 4:
            for j in Jets:
                if j.pt > 30 and abs(j.eta) < 2.4 and j.btagDeepCSV < 0.4941:

                    matched_fatjet = Match_two_lists(
                    j, 'jet',
                    bquarks, 'quark',5)

                    if hasattr(j,"matched_quark"):
                        dist.Fill(Get_DeltaR_two_objects(j,j.matched_quark),event.genWeight)

        ### Now try to investigate matching fractions and kinematics
        #First matching fractions:

        if event.ntopCandidate > 0:
            if matchtop == 1:
                matching["new"].Fill(1,event.genWeight)
            else:
                matching["new"].Fill(2,event.genWeight)
        if event.nhiggsCandidate > 0:
            if matchhiggs == 1:
                matching["new"].Fill(3,event.genWeight)
            else:
                matching["new"].Fill(4,event.genWeight)


        #Now kinematics

        if event.ntopCandidate > 0:
            sorted(TopSubjet, key=lambda x: x.btag, reverse=True)
            matched_genb = Match_two_lists(
            [TopSubjet[0]], 'subjetsTop',
            GenBFromTop, 'genQuark',0.3)
            matched_genl = Match_two_lists(
            [TopSubjet[1]] + [TopSubjet[2]], 'subjetsTop',
            GenQFromW, 'genQuark',0.3)
            for subjet in TopSubjet:
                if subjet.pt > 30:
                    index = TopSubjet.index(subjet)
                    if hasattr(subjet,"matched_genQuark"):
                        for var in variables:
                            if index == 0:
                                count["new"]["tb"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))
                            else:
                                count["new"]["tl"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))

        if event.nhiggsCandidate > 0:
            matched_gen = Match_two_lists(
            HiggsSubjet, 'subjetsHiggs',
            GenBFromHiggs, 'genQuark',0.3) 
            for subjet in HiggsSubjet:
                if hasattr(subjet,"matched_genQuark"):
                    for var in variables:
                        count["new"]["hb"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))


results = ROOT.TFile("out.root","recreate")
numNE.Write()
dist.Write()
for i in jettype:
    jets[i].Write()
for i in cats:
    for j in criteria:
        pt[i][j].Write()
        pt2[i][j].Write()

for i in evttype:
    matching[i].Write()
    for j in quarks:
        for l in variables:
            count[i][j][l].Write()
 