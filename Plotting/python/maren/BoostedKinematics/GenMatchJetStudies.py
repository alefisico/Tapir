#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses

class JetCollection:
    def __init__(self, tree, n,name):
        self.pt = getattr(tree,"{}_pt".format(name))[n]
        self.eta = getattr(tree,"{}_eta".format(name))[n]
        self.phi = getattr(tree,"{}_phi".format(name))[n]
        self.mass = getattr(tree,"{}_mass".format(name))[n]
        if name == "FatjetCA15":
            self.tau3 = getattr(tree,"{}_tau3".format(name))[n]
            self.tau2 = getattr(tree,"{}_tau2".format(name))[n]
            self.tau1 = getattr(tree,"{}_tau1".format(name))[n]
            self.bbtag = getattr(tree,"{}_bbtag".format(name))[n]
        if name == "FatjetCA15SoftDrop" or name == "HTTV2" or name == "FatJet":
            self.subJetIdx1 = getattr(tree,"{}_subJetIdx1".format(name))[n]
            self.subJetIdx2 = getattr(tree,"{}_subJetIdx2".format(name))[n]
        if name == "HTTV2": 
            self.subJetIdx3 = getattr(tree,"{}_subJetIdx3".format(name))[n]   
            self.fRec = getattr(tree,"{}_fRec".format(name))[n]   
            self.Ropt = getattr(tree,"{}_Ropt".format(name))[n]   
            self.RoptCalc = getattr(tree,"{}_RoptCalc".format(name))[n]   
        if name == "FatjetCA15SoftDropSubjets" or name == "HTTV2Subjets":
            self.btag = getattr(tree,"{}_btag".format(name))[n]
        if name == "SubJet":
            self.btag = getattr(tree,"{}_btagCSVV2".format(name))[n]
        if name == "FatJet":
            self.tau3 = getattr(tree,"{}_tau3".format(name))[n]
            self.tau2 = getattr(tree,"{}_tau2".format(name))[n]
            self.tau1 = getattr(tree,"{}_tau1".format(name))[n]
            self.bbtag = getattr(tree,"{}_btagHbb".format(name))[n]
            self.tau21 = self.tau2 / self.tau1 if self.tau1 > 0.0 else 0.0
            self.tau32 = self.tau3 / self.tau2 if self.tau2 > 0.0 else 0.0  
            self.msoftdrop = getattr(tree,"{}_msoftdrop".format(name))[n]
        pass
    @staticmethod
    def make_array(input,name):
        return [JetCollection(input, i, name) for i in range(getattr(input,"n{}".format(name)))]

def Get_DeltaR_two_objects_coord(obj1_eta, obj1_phi, obj2_eta, obj2_phi ):

    pi = math.pi

    del_phi = abs( obj1_phi - obj2_phi )
    if del_phi > pi: del_phi = 2*pi - del_phi

    delR = pow( pow(obj1_eta-obj2_eta,2) + pow(del_phi,2) , 0.5 )

    return delR

def Get_DeltaR_two_objects(obj1, obj2):

    for obj in [ obj1, obj2 ]:
        if not ( hasattr( obj, 'phi' ) or hasattr( obj, 'eta' ) ):
            print "Can't calculate Delta R: objects don't have right attributes"
            return 0

    pi = math.pi

    del_phi = abs( obj1.phi - obj2.phi )
    if del_phi > pi: del_phi = 2*pi - del_phi

    delR = pow( pow(obj1.eta-obj2.eta,2) + pow(del_phi,2) , 0.5 )

    return delR

########################################
# Define Input Files and
# output directory
########################################

basepath = 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat'

# for the filename: basepath + filename + .root
full_file_names = {}
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v

#full_file_names = {}
#full_file_names["v"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/chreisse/tth/Apr16/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Apr16/180416_072654/0000/tree_100.root"
#full_file_names["v"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/chreisse/tth/Apr16/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Apr16/180416_072809/0000/tree_100.root"


########################################
# Create histograms, saved in file
########################################

CA15GenHiggspT = ROOT.TH1F("CA15GenHiggspT","CA15GenHiggspT",200,0,1000)
CA15GenHiggsDR = ROOT.TH1F("CA15GenHiggsDR","CA15GenHiggsDR",100,0,5)
CA15GenHiggspTDR = ROOT.TH2F("CA15GenHiggspTDR","CA15GenHiggspTDR",200,0,1000,100,0,5)
CA15GenToppTDR = ROOT.TH2F("CA15GenToppTDR","CA15GenToppTDR",200,0,1000,100,0,5)
CA15GenToppTDR2 = ROOT.TH2F("CA15GenToppTDR2","CA15GenToppTDR2",200,0,1000,100,0,5)
CA15GenToppT = ROOT.TH1F("CA15GenToppT","CA15GenToppT",200,0,1000)
CA15GenTopHadpT = ROOT.TH1F("CA15GenTopHadpT","CA15GenTopHadpT",200,0,1000)
CA15GenTopHiggs = ROOT.TH2F("CA15GenTopHiggs","CA15GenTopHiggs",200,0,1000,200,0,1000)
CA15GenTopHadHiggs = ROOT.TH2F("CA15GenTopHadHiggs","CA15GenTopHadHiggs",200,0,1000,200,0,1000)
CA15GenDRTopHiggs = ROOT.TH1F("CA15GenDRTopHiggs","CA15GenDRTopHiggs",50,0,5)
CA15GenDRTopTop = ROOT.TH1F("CA15GenDRTopTop","CA15GenDRTopTop",50,0,5)
CA15GenDRHadTopHiggs = ROOT.TH1F("CA15GenDRHadTopHiggs","CA15GenDRHadTopHiggs",50,0,5)
CA15GenWDR = ROOT.TH1F("CA15GenWDR","CA15GenWDR",100,0,5)
CA15GenWpTDR = ROOT.TH2F("CA15GenWpTDR","CA15GenWpTDR",200,0,1000,100,0,5)
CA15GenWpT = ROOT.TH1F("CA15GenWpT","CA15GenWpT",200,0,1000)
CA15GenHadWDR = ROOT.TH1F("CA15GenHadWDR","CA15GenHadWDR",100,0,5)
CA15GenHadWpTDR = ROOT.TH2F("CA15GenHadWpTDR","CA15GenHadWpTDR",200,0,1000,100,0,5)
CA15GenHadWpT = ROOT.TH1F("CA15GenHadWpT","CA15GenHadWpT",200,0,1000)
CA15GenNumbers = ROOT.TH1F("CA15GenNumbers","CA15GenNumbers",200,0,200)

AK8GenHiggspT = ROOT.TH1F("AK8GenHiggspT","AK8GenHiggspT",200,0,1000)
AK8GenHiggsDR = ROOT.TH1F("AK8GenHiggsDR","AK8GenHiggsDR",100,0,5)
AK8GenHiggspTDR = ROOT.TH2F("AK8GenHiggspTDR","AK8GenHiggspTDR",200,0,1000,100,0,5)
AK8GenToppTDR = ROOT.TH2F("AK8GenToppTDR","AK8GenToppTDR",200,0,1000,100,0,5)
AK8GenToppTDR2 = ROOT.TH2F("AK8GenToppTDR2","AK8GenToppTDR2",200,0,1000,100,0,5)
AK8GenToppT = ROOT.TH1F("AK8GenToppT","AK8GenToppT",200,0,1000)
AK8GenTopHadpT = ROOT.TH1F("AK8GenTopHadpT","AK8GenTopHadpT",200,0,1000)
AK8GenTopHiggs = ROOT.TH2F("AK8GenTopHiggs","AK8GenTopHiggs",200,0,1000,200,0,1000)
AK8GenTopHadHiggs = ROOT.TH2F("AK8GenTopHadHiggs","AK8GenTopHadHiggs",200,0,1000,200,0,1000)
AK8GenDRTopHiggs = ROOT.TH1F("AK8GenDRTopHiggs","AK8GenDRTopHiggs",50,0,5)
AK8GenDRTopTop = ROOT.TH1F("AK8GenDRTopTop","AK8GenDRTopTop",50,0,5)
AK8GenDRHadTopHiggs = ROOT.TH1F("AK8GenDRHadTopHiggs","AK8GenDRHadTopHiggs",50,0,5)
AK8GenWDR = ROOT.TH1F("AK8GenWDR","AK8GenWDR",100,0,5)
AK8GenWpTDR = ROOT.TH2F("AK8GenWpTDR","AK8GenWpTDR",200,0,1000,100,0,5)
AK8GenWpT = ROOT.TH1F("AK8GenWpT","AK8GenWpT",200,0,1000)
AK8GenHadWDR = ROOT.TH1F("AK8GenHadWDR","AK8GenHadWDR",100,0,5)
AK8GenHadWpTDR = ROOT.TH2F("AK8GenHadWpTDR","AK8GenHadWpTDR",200,0,1000,100,0,5)
AK8GenHadWpT = ROOT.TH1F("AK8GenHadWpT","AK8GenHadWpT",200,0,1000)
AK8GenNumbers = ROOT.TH1F("AK8GenNumbers","AK8GenNumbers",200,0,200)

HTTGenHiggspT = ROOT.TH1F("HTTGenHiggspT","HTTGenHiggspT",200,0,1000)
HTTGenHiggsDR = ROOT.TH1F("HTTGenHiggsDR","HTTGenHiggsDR",100,0,5)
HTTGenHiggspTDR = ROOT.TH2F("HTTGenHiggspTDR","HTTGenHiggspTDR",200,0,1000,100,0,5)
HTTGenToppTDR = ROOT.TH2F("HTTGenToppTDR","HTTGenToppTDR",200,0,1000,100,0,5)
HTTGenToppTDR2 = ROOT.TH2F("HTTGenToppTDR2","HTTGenToppTDR2",200,0,1000,100,0,5)
HTTGenToppT = ROOT.TH1F("HTTGenToppT","HTTGenToppT",200,0,1000)
HTTGenTopHadpT = ROOT.TH1F("HTTGenTopHadpT","HTTGenTopHadpT",200,0,1000)
HTTGenTopHiggs = ROOT.TH2F("HTTGenTopHiggs","HTTGenTopHiggs",200,0,1000,200,0,1000)
HTTGenTopHadHiggs = ROOT.TH2F("HTTGenTopHadHiggs","HTTGenTopHadHiggs",200,0,1000,200,0,1000)
HTTGenDRTopHiggs = ROOT.TH1F("HTTGenDRTopHiggs","HTTGenDRTopHiggs",50,0,5)
HTTGenDRTopTop = ROOT.TH1F("HTTGenDRTopTop","HTTGenDRTopTop",50,0,5)
HTTGenDRHadTopHiggs = ROOT.TH1F("HTTGenDRHadTopHiggs","HTTGenDRHadTopHiggs",50,0,5)
HTTGenWDR = ROOT.TH1F("HTTGenWDR","HTTGenWDR",100,0,5)
HTTGenWpTDR = ROOT.TH2F("HTTGenWpTDR","HTTGenWpTDR",200,0,1000,100,0,5)
HTTGenWpT = ROOT.TH1F("HTTGenWpT","HTTGenWpT",200,0,1000)
HTTGenHadWDR = ROOT.TH1F("HTTGenHadWDR","HTTGenHadWDR",100,0,5)
HTTGenHadWpTDR = ROOT.TH2F("HTTGenHadWpTDR","HTTGenHadWpTDR",200,0,1000,100,0,5)
HTTGenHadWpT = ROOT.TH1F("HTTGenHadWpT","HTTGenHadWpT",200,0,1000)
HTTGenNumbers = ROOT.TH1F("HTTGenNumbers","HTTGenNumbers",200,0,200)

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("nanoAOD/Events")

    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"

    counter = 0 
    for event in ttree :

        counter += 1
        #if counter > 10000:
        #    break


        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event

        #if event.nMuon == 0 and event.nElectron == 0:
        #    continue

        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.GenWBoson = nanoTreeGenClasses.GenWBoson.make_array(event.GenParticle)
        event.GenJet = nanoTreeGenClasses.GenJet.make_array(ttree)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")

        usedCA15 = []
        usedAK8 = []

        #Do all the matching here for all objects and fatjets
        for i in event.GenHiggsBoson:
            fs15 = sorted(event.FatjetCA15SoftDrop, key = lambda x: Get_DeltaR_two_objects(x,i))
            if len(event.FatjetCA15SoftDrop) > 0 and Get_DeltaR_two_objects(fs15[0],i) < 0.5:
                setattr(i,"matchCA15",event.FatjetCA15SoftDrop.index(fs15[0]))
                usedCA15.append(event.FatjetCA15SoftDrop.index(fs15[0]))
                fa = event.FatjetCA15SoftDrop[i.matchCA15]
                s1 = event.FatjetCA15SoftDropSubjets[fa.subJetIdx1]
                s2 = event.FatjetCA15SoftDropSubjets[fa.subJetIdx2]
                d1 = Get_DeltaR_two_objects(s1,event.GenBQuarkFromH[0])
                d2 = Get_DeltaR_two_objects(s1,event.GenBQuarkFromH[1])
                d3 = Get_DeltaR_two_objects(s2,event.GenBQuarkFromH[0])
                d4 = Get_DeltaR_two_objects(s2,event.GenBQuarkFromH[1])
                if (d1 < 0.3 and d4 < 0.3) or (d2 < 0.3 and d3 < 0.3):
                    setattr(i,"matchCA15_s1",event.FatjetCA15SoftDropSubjets.index(s1))
                    setattr(i,"matchCA15_s2",event.FatjetCA15SoftDropSubjets.index(s2))

            fs08 = sorted(event.FatjetAK8, key = lambda x: Get_DeltaR_two_objects(x,i))
            if len(event.FatjetAK8) > 0 and Get_DeltaR_two_objects(fs08[0],i) < 0.5:
                setattr(i,"matchAK8",event.FatjetAK8.index(fs08[0]))
                usedAK8.append(event.FatjetAK8.index(fs08[0]))
                fa = event.FatjetAK8[i.matchAK8]
                if fa.subJetIdx1 > 0 and fa.subJetIdx2 > 0:
                    s1 = event.FatjetAK8Subjets[fa.subJetIdx1]
                    s2 = event.FatjetAK8Subjets[fa.subJetIdx2]
                    d1 = Get_DeltaR_two_objects(s1,event.GenBQuarkFromH[0])
                    d2 = Get_DeltaR_two_objects(s1,event.GenBQuarkFromH[1])
                    d3 = Get_DeltaR_two_objects(s2,event.GenBQuarkFromH[0])
                    d4 = Get_DeltaR_two_objects(s2,event.GenBQuarkFromH[1])
                    if (d1 < 0.3 and d4 < 0.3) or (d2 < 0.3 and d3 < 0.3):
                        setattr(i,"matchAK8_s1",event.FatjetAK8Subjets.index(s1))
                        setattr(i,"matchAK8_s2",event.FatjetAK8Subjets.index(s2))

        for i in event.GenTop:
            if len(event.FatjetCA15SoftDrop) > 0:
                fs15 = sorted(event.FatjetCA15SoftDrop, key = lambda x: Get_DeltaR_two_objects(x,i))
                if Get_DeltaR_two_objects(fs15[0],i) < 0.5 and event.FatjetCA15SoftDrop.index(fs15[0]) not in usedCA15:
                    setattr(i,"matchCA15",event.FatjetCA15SoftDrop.index(fs15[0]))
            if len(event.FatjetAK8) > 0:
                fs08 = sorted(event.FatjetAK8, key = lambda x: Get_DeltaR_two_objects(x,i))
                if Get_DeltaR_two_objects(fs08[0],i) < 0.5 and event.FatjetAK8.index(fs08[0]) not in usedAK8:
                    setattr(i,"matchAK8",event.FatjetAK8.index(fs08[0]))
            if len(event.HTTV2) > 0:
                htt = sorted(event.HTTV2, key = lambda x: Get_DeltaR_two_objects(x,i))
                if Get_DeltaR_two_objects(htt[0],i) < 0.5:
                    setattr(i,"matchHTT",event.HTTV2.index(htt[0]))
                    fa = event.HTTV2[i.matchHTT]
                    s1 = event.HTTV2Subjets[fa.subJetIdx1]
                    s2 = event.HTTV2Subjets[fa.subJetIdx2]
                    s3 = event.HTTV2Subjets[fa.subJetIdx3]
                    sjs = [s1,s2,s3]
                    sjs = sorted(sjs, key = lambda x: x.btag) 
                    subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,i)) 
                    if len(subj) >=2:
                        tops = sorted(event.GenBQuarkFromTop, key = lambda x: Get_DeltaR_two_objects(x,i))
                        d5 = Get_DeltaR_two_objects(sjs[2],tops[0])
                        d1 = Get_DeltaR_two_objects(sjs[0],subj[0])
                        d2 = Get_DeltaR_two_objects(sjs[0],subj[1])
                        d3 = Get_DeltaR_two_objects(sjs[1],subj[0])
                        d4 = Get_DeltaR_two_objects(sjs[1],subj[1])
                        if (d1 < 0.3 and d4 < 0.3 and d5 < 0.3) or (d2 < 0.3 and d3 < 0.3 and d5 < 0.3):
                            setattr(i,"matchHTT_s1",event.HTTV2Subjets.index(sjs[2]))
                            setattr(i,"matchHTT_s2",event.HTTV2Subjets.index(sjs[1]))
                            setattr(i,"matchHTT_s3",event.HTTV2Subjets.index(sjs[0]))

        for i in event.GenWBoson:
            fs15 = sorted(event.FatjetCA15SoftDrop, key = lambda x: Get_DeltaR_two_objects(x,i))
            if len(event.FatjetCA15SoftDrop) > 0 and Get_DeltaR_two_objects(fs15[0],i) < 0.5 and event.FatjetCA15SoftDrop.index(fs15[0]) not in usedCA15:
                setattr(i,"matchCA15",event.FatjetCA15SoftDrop.index(fs15[0]))
                subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,i)) 
                if len(subj) >=2:
                    fa = event.FatjetCA15SoftDrop[i.matchCA15]
                    s1 = event.FatjetCA15SoftDropSubjets[fa.subJetIdx1]
                    s2 = event.FatjetCA15SoftDropSubjets[fa.subJetIdx2]
                    d1 = Get_DeltaR_two_objects(s1,subj[0])
                    d2 = Get_DeltaR_two_objects(s1,subj[1])
                    d3 = Get_DeltaR_two_objects(s2,subj[0])
                    d4 = Get_DeltaR_two_objects(s2,subj[1])
                    if (d1 < 0.3 and d4 < 0.3) or (d2 < 0.3 and d3 < 0.3):
                        setattr(i,"matchCA15_s1",event.FatjetCA15SoftDropSubjets.index(s1))
                        setattr(i,"matchCA15_s2",event.FatjetCA15SoftDropSubjets.index(s2))

            fs08 = sorted(event.FatjetAK8, key = lambda x: Get_DeltaR_two_objects(x,i))
            if len(event.FatjetAK8) > 0 and Get_DeltaR_two_objects(fs08[0],i) < 0.5 and event.FatjetAK8.index(fs08[0]) not in usedAK8:
                setattr(i,"matchAK8",event.FatjetAK8.index(fs08[0]))
                subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,i)) 
                if len(subj) >=2:
                    fa = event.FatjetAK8[i.matchAK8]
                    if fa.subJetIdx1 > 0 and fa.subJetIdx2 > 0:
                        s1 = event.FatjetAK8Subjets[fa.subJetIdx1]
                        s2 = event.FatjetAK8Subjets[fa.subJetIdx2]
                        d1 = Get_DeltaR_two_objects(s1,subj[0])
                        d2 = Get_DeltaR_two_objects(s1,subj[1])
                        d3 = Get_DeltaR_two_objects(s2,subj[0])
                        d4 = Get_DeltaR_two_objects(s2,subj[1])
                        if (d1 < 0.3 and d4 < 0.3) or (d2 < 0.3 and d3 < 0.3):
                            setattr(i,"matchAK8_s1",event.FatjetAK8Subjets.index(s1))
                            setattr(i,"matchAK8_s2",event.FatjetAK8Subjets.index(s2))

        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenHadW = filter(lambda x: (x.decayMode==1), event.GenWBoson)

        #Now do the actual code
        for k in range(0,len(event.GenHiggsBoson)):
            if hasattr(event.GenHiggsBoson[k],"matchCA15"):
                fa = event.FatjetCA15SoftDrop[event.GenHiggsBoson[k].matchCA15]
                CA15GenHiggspT.Fill(fa.pt,event.Generator_weight)
                if hasattr(event.GenHiggsBoson[k],"matchCA15_s1"):
                    s1 = event.FatjetCA15SoftDropSubjets[event.GenHiggsBoson[k].matchCA15_s1]
                    s2 = event.FatjetCA15SoftDropSubjets[event.GenHiggsBoson[k].matchCA15_s2]
                    dsub = Get_DeltaR_two_objects(s1,s2)
                    CA15GenHiggsDR.Fill(dsub,event.Generator_weight)
                    CA15GenHiggspTDR.Fill(fa.pt,dsub,event.Generator_weight)

            if hasattr(event.GenHiggsBoson[k],"matchAK8"):
                fa = event.FatjetAK8[event.GenHiggsBoson[k].matchAK8]
                AK8GenHiggspT.Fill(fa.pt,event.Generator_weight)
                if hasattr(event.GenHiggsBoson[k],"matchAK8_s1"):
                    s1 = event.FatjetAK8Subjets[event.GenHiggsBoson[k].matchAK8_s1]
                    s2 = event.FatjetAK8Subjets[event.GenHiggsBoson[k].matchAK8_s2]
                    dsub = Get_DeltaR_two_objects(s1,s2)
                    AK8GenHiggsDR.Fill(dsub,event.Generator_weight)
                    AK8GenHiggspTDR.Fill(fa.pt,dsub,event.Generator_weight)


        for k in range(0,len(event.GenWBoson)):
            if hasattr(event.GenWBoson[k],"matchCA15"):
                fa = event.FatjetCA15SoftDrop[event.GenWBoson[k].matchCA15]
                CA15GenWpT.Fill(fa.pt,event.Generator_weight)
                if event.GenWBoson[k].decayMode == 1:
                    CA15GenHadWpT.Fill(fa.pt,event.Generator_weight)
                if hasattr(event.GenWBoson[k],"matchCA15_s1"):
                    s1 = event.FatjetCA15SoftDropSubjets[event.GenWBoson[k].matchCA15_s1]
                    s2 = event.FatjetCA15SoftDropSubjets[event.GenWBoson[k].matchCA15_s2]
                    dsub = Get_DeltaR_two_objects(s1,s2)
                    CA15GenWDR.Fill(dsub,event.Generator_weight)
                    CA15GenWpTDR.Fill(fa.pt,dsub,event.Generator_weight)
                    if event.GenWBoson[k].decayMode == 1:
                        CA15GenHadWDR.Fill(dsub,event.Generator_weight)
                        CA15GenHadWpTDR.Fill(fa.pt,dsub,event.Generator_weight)


            if hasattr(event.GenWBoson[k],"matchAK8"):
                fa = event.FatjetAK8[event.GenWBoson[k].matchAK8]
                AK8GenWpT.Fill(fa.pt,event.Generator_weight)
                if event.GenWBoson[k].decayMode == 1:
                    AK8GenHadWpT.Fill(fa.pt,event.Generator_weight)
                if hasattr(event.GenWBoson[k],"matchAK8_s1"):
                    s1 = event.FatjetAK8Subjets[event.GenWBoson[k].matchAK8_s1]
                    s2 = event.FatjetAK8Subjets[event.GenWBoson[k].matchAK8_s2]
                    dsub = Get_DeltaR_two_objects(subj[0],subj[1])
                    AK8GenWDR.Fill(dsub,event.Generator_weight)
                    AK8GenWpTDR.Fill(fa.pt,dsub,event.Generator_weight)
                    if event.GenWBoson[k].decayMode == 1:
                        AK8GenHadWDR.Fill(dsub,event.Generator_weight)
                        AK8GenHadWpTDR.Fill(fa.pt,dsub,event.Generator_weight)                

        for k in range(0,len(event.GenTop)):
            if hasattr(event.GenTop[k],"matchCA15"):
                fa = event.FatjetCA15SoftDrop[event.GenTop[k].matchCA15]
                CA15GenToppT.Fill(fa.pt,event.Generator_weight)
            if hasattr(event.GenTop[k],"matchAK8"):
                fa2 = event.FatjetAK8[event.GenTop[k].matchAK8]
                AK8GenToppT.Fill(fa2.pt,event.Generator_weight)
            if hasattr(event.GenTop[k],"matchHTT"):
                fa3 = event.HTTV2[event.GenTop[k].matchHTT]
                HTTGenToppT.Fill(fa3.pt,event.Generator_weight)
        for k in range(0,len(event.GenHadTop)):
            if hasattr(event.GenHadTop[k],"matchCA15"):
                fa = event.FatjetCA15SoftDrop[event.GenHadTop[k].matchCA15]
                CA15GenTopHadpT.Fill(fa.pt,event.Generator_weight)
            if hasattr(event.GenHadTop[k],"matchAK8"):
                fa2 = event.FatjetAK8[event.GenHadTop[k].matchAK8]
                AK8GenTopHadpT.Fill(fa2.pt,event.Generator_weight)
            if hasattr(event.GenHadTop[k],"matchHTT"):
                fa3 = event.HTTV2[event.GenHadTop[k].matchHTT]
                HTTGenTopHadpT.Fill(fa3.pt,event.Generator_weight)




            if hasattr(event.GenHadTop[k],"matchHTT_s1"):
                fa3 = event.HTTV2[event.GenHadTop[k].matchHTT]
                sjb = event.HTTV2Subjets[event.GenHadTop[k].matchHTT_s1]
                sjl1 = event.HTTV2Subjets[event.GenHadTop[k].matchHTT_s2]
                sjl2 = event.HTTV2Subjets[event.GenHadTop[k].matchHTT_s3]
                GenB = ROOT.TLorentzVector()
                GenB.SetPtEtaPhiM(sjb.pt,sjb.eta,sjb.phi,sjb.mass)
                GenW1 = ROOT.TLorentzVector()
                GenW1.SetPtEtaPhiM(sjl1.pt,sjl1.eta,sjl1.phi,sjl1.mass)
                GenW2 = ROOT.TLorentzVector()
                GenW2.SetPtEtaPhiM(sjl2.pt,sjl2.eta,sjl2.phi,sjl2.mass)
                d1 = Get_DeltaR_two_objects(sjb,sjl1)
                d2 = Get_DeltaR_two_objects(sjb,sjl2)
                d3 = Get_DeltaR_two_objects(sjl1,sjl2)
                s = (d1+d2+d3)/2
                area = math.sqrt(s*(s-d1)*(s-d2)*(s-d3))
                if area > 0:
                    rad = (d1*d2*d3)/(4*area)
                    HTTGenToppTDR.Fill(fa3.pt,rad,event.Generator_weight)

                jet12 = GenB + GenW1
                jet13 = GenB + GenW2
                jet23 = GenW1 + GenW2
                a = Get_DeltaR_two_objects(sjb,sjl1)
                b = Get_DeltaR_two_objects(sjl1,sjl2)
                c = Get_DeltaR_two_objects(sjl2,sjb)
                dR1 = a
                dR2 = a

                if a <= b and a <= c:
                    dR1 = a
                    dR2 = Get_DeltaR_two_objects_coord(jet12.Eta(),jet12.Phi(),GenW2.Eta(),GenW2.Phi())
                if b < a and b <= c:
                    dR1 = b
                    dR2 = Get_DeltaR_two_objects_coord(jet23.Eta(),jet23.Phi(),GenB.Eta(),GenB.Phi())
                if c < a and c < b:
                    dR1 = c
                    dR2 = Get_DeltaR_two_objects_coord(jet13.Eta(),jet13.Phi(),GenW1.Eta(),GenW1.Phi())
                rad2 = max(dR1,dR2)
                HTTGenToppTDR2.Fill(fa3.pt,rad2,event.Generator_weight)
                #except:
                #    pass


        if len(event.GenHiggsBoson)>0 and len(event.GenTop)>0:
            for k in range(0,len(event.GenTop)):
                if hasattr(event.GenTop[k],"matchCA15") and hasattr(event.GenHiggsBoson[0],"matchCA15"):
                    fa = event.FatjetCA15SoftDrop[event.GenTop[k].matchCA15]
                    faH = event.FatjetCA15SoftDrop[event.GenHiggsBoson[0].matchCA15]
                    CA15GenTopHiggs.Fill(fa.pt,faH.pt,event.Generator_weight)
                    distance = Get_DeltaR_two_objects(fa,faH)
                    CA15GenDRTopHiggs.Fill(distance,event.Generator_weight)
                    if event.GenTop[k].decayMode==1:
                        CA15GenTopHadHiggs.Fill(fa.pt,faH.pt,event.Generator_weight)
                        CA15GenDRHadTopHiggs.Fill(distance,event.Generator_weight)
                if hasattr(event.GenTop[k],"matchAK8") and hasattr(event.GenHiggsBoson[0],"matchAK8"):
                    fa2 = event.FatjetAK8[event.GenTop[k].matchAK8]
                    faH2 = event.FatjetAK8[event.GenHiggsBoson[0].matchAK8]
                    AK8GenTopHiggs.Fill(fa2.pt,faH2.pt,event.Generator_weight)
                    distance2 = Get_DeltaR_two_objects(fa2,faH2)
                    AK8GenDRTopHiggs.Fill(distance2,event.Generator_weight)
                    if event.GenTop[k].decayMode==1:
                        AK8GenTopHadHiggs.Fill(fa2.pt,faH2.pt,event.Generator_weight)
                        AK8GenDRHadTopHiggs.Fill(distance2,event.Generator_weight)

        if len(event.GenTop)==2:
            if hasattr(event.GenTop[0],"matchCA15") and hasattr(event.GenTop[1],"matchCA15"):
                fa = event.FatjetCA15SoftDrop[event.GenTop[0].matchCA15]
                fa2 = event.FatjetCA15SoftDrop[event.GenTop[1].matchCA15]
                CA15GenDRTopTop.Fill(Get_DeltaR_two_objects(fa,fa2),event.Generator_weight)
            if hasattr(event.GenTop[0],"matchAK8") and hasattr(event.GenTop[1],"matchAK8"):
                fa3 = event.FatjetAK8[event.GenTop[0].matchAK8]
                fa4 = event.FatjetAK8[event.GenTop[1].matchAK8]
                AK8GenDRTopTop.Fill(Get_DeltaR_two_objects(fa3,fa4),event.Generator_weight)
            if hasattr(event.GenTop[0],"matchHTT") and hasattr(event.GenTop[1],"matchHTT"):
                fa3 = event.HTTV2[event.GenTop[0].matchHTT]
                fa4 = event.HTTV2[event.GenTop[1].matchHTT]
                HTTGenDRTopTop.Fill(Get_DeltaR_two_objects(fa3,fa4),event.Generator_weight)

        #Now get numbers of boosted events
        if sample == "ttH":
            CA15GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHiggsBoson)> 0 and len(event.GenHadTop)> 0 and hasattr(event.GenHiggsBoson[0],"matchCA15") and hasattr(event.GenHadTop[0],"matchCA15"):
                a = event.FatjetCA15SoftDrop[event.GenHiggsBoson[0].matchCA15]
                b = event.FatjetCA15SoftDrop[event.GenHadTop[0].matchCA15]
                if b.pt < 200:
                    if a.pt < 200:
                        CA15GenNumbers.Fill(1,event.Generator_weight)
                    if a.pt > 200:
                        CA15GenNumbers.Fill(2,event.Generator_weight)
                    if a.pt > 300:
                        CA15GenNumbers.Fill(3,event.Generator_weight)
                if b.pt > 200:
                    if a.pt < 200:
                        CA15GenNumbers.Fill(4,event.Generator_weight)
                    if a.pt > 200:
                        CA15GenNumbers.Fill(5,event.Generator_weight)
                    if a.pt > 300:
                        CA15GenNumbers.Fill(6,event.Generator_weight)
                if b.pt > 300:
                    if a.pt < 200:
                        CA15GenNumbers.Fill(7,event.Generator_weight)
                    if a.pt > 200:
                        CA15GenNumbers.Fill(8,event.Generator_weight)
                    if a.pt > 300:
                        CA15GenNumbers.Fill(9,event.Generator_weight)
            if len(event.GenHiggsBoson)> 0 and len(event.GenHadTop)> 0 and hasattr(event.GenHiggsBoson[0],"matchCA15") and hasattr(event.GenHadTop[0],"matchHTT"):
                a = event.FatjetCA15SoftDrop[event.GenHiggsBoson[0].matchCA15]
                b = event.HTTV2[event.GenHadTop[0].matchHTT]
                if b.pt < 200:
                    if a.pt < 200:
                        HTTGenNumbers.Fill(1,event.Generator_weight)
                    if a.pt > 200:
                        HTTGenNumbers.Fill(2,event.Generator_weight)
                    if a.pt > 300:
                        HTTGenNumbers.Fill(3,event.Generator_weight)
                if b.pt > 200:
                    if a.pt < 200:
                        HTTGenNumbers.Fill(4,event.Generator_weight)
                    if a.pt > 200:
                        HTTGenNumbers.Fill(5,event.Generator_weight)
                    if a.pt > 300:
                        HTTGenNumbers.Fill(6,event.Generator_weight)
                if b.pt > 300:
                    if a.pt < 200:
                        HTTGenNumbers.Fill(7,event.Generator_weight)
                    if a.pt > 200:
                        HTTGenNumbers.Fill(8,event.Generator_weight)
                    if a.pt > 300:
                        HTTGenNumbers.Fill(9,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHiggsBoson) > 0 and len(event.GenHadTop) > 0 \
                and hasattr(event.GenHiggsBoson[0],"matchCA15") and hasattr(event.GenHadTop[0],"matchCA15") and hasattr(event.GenHadW[0],"matchCA15"):
                a = event.FatjetCA15SoftDrop[event.GenHiggsBoson[0].matchCA15]
                b = event.FatjetCA15SoftDrop[event.GenHadTop[0].matchCA15]
                c = event.FatjetCA15SoftDrop[event.GenHadW[0].matchCA15]
                if b.pt < 200:
                    if c.pt < 100:
                        if a.pt < 200:
                            CA15GenNumbers.Fill(10,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(11,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(12,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(13,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(14,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(15,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(16,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(17,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(18,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(19,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(20,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(21,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(22,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(23,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(24,event.Generator_weight)   
                if b.pt > 200:
                    if c.pt < 100:
                        if a.pt < 200:
                            CA15GenNumbers.Fill(25,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(26,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(27,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(28,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(29,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(30,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(31,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(32,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(33,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(34,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(35,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(36,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(37,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(38,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(39,event.Generator_weight)  
                if b.pt > 300:
                    if c.pt < 100:
                        if a.pt < 200:
                            CA15GenNumbers.Fill(40,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(41,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(42,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(43,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(44,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(45,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(46,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(47,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(48,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(49,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(50,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(51,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            CA15GenNumbers.Fill(52,event.Generator_weight)
                        if a.pt > 200:
                            CA15GenNumbers.Fill(53,event.Generator_weight)
                        if a.pt > 300:
                            CA15GenNumbers.Fill(54,event.Generator_weight)      

        else:
            CA15GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHadTop) > 0 \
            and hasattr(event.GenHadTop[0],"matchCA15") and hasattr(event.GenHadW[0],"matchCA15"):
                b = event.FatjetCA15SoftDrop[event.GenHadTop[0].matchCA15]
                c = event.FatjetCA15SoftDrop[event.GenHadW[0].matchCA15]
                if c.pt < 100:
                    if b.pt < 200:
                        CA15GenNumbers.Fill(10,event.Generator_weight)
                    if b.pt > 200:
                        CA15GenNumbers.Fill(25,event.Generator_weight)
                    if b.pt > 300:
                        CA15GenNumbers.Fill(40,event.Generator_weight)
                if c.pt > 100:   
                    if b.pt < 200:
                        CA15GenNumbers.Fill(13,event.Generator_weight)
                    if b.pt > 200:
                        CA15GenNumbers.Fill(28,event.Generator_weight)
                    if b.pt > 300:
                        CA15GenNumbers.Fill(43,event.Generator_weight)  
                if c.pt > 150:   
                    if b.pt < 200:
                        CA15GenNumbers.Fill(16,event.Generator_weight)
                    if b.pt > 200:
                        CA15GenNumbers.Fill(31,event.Generator_weight)
                    if b.pt > 300:
                        CA15GenNumbers.Fill(46,event.Generator_weight)   
                if c.pt > 200:   
                    if b.pt < 200:
                        CA15GenNumbers.Fill(19,event.Generator_weight)
                    if b.pt > 200:
                        CA15GenNumbers.Fill(34,event.Generator_weight)
                    if b.pt > 300:
                        CA15GenNumbers.Fill(49,event.Generator_weight)     
                if c.pt > 300:   
                    if b.pt < 200:
                        CA15GenNumbers.Fill(22,event.Generator_weight)
                    if b.pt > 200:
                        CA15GenNumbers.Fill(37,event.Generator_weight)
                    if b.pt > 300:
                        CA15GenNumbers.Fill(52,event.Generator_weight) 


        #Now get numbers of boosted events
        if sample == "ttH":
            AK8GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHiggsBoson)> 0 and len(event.GenHadTop)> 0 and hasattr(event.GenHiggsBoson[0],"matchAK8") and hasattr(event.GenHadTop[0],"matchAK8"):
                a = event.FatjetAK8[event.GenHiggsBoson[0].matchAK8]
                b = event.FatjetAK8[event.GenHadTop[0].matchAK8]
                if b.pt < 200:
                    if a.pt < 200:
                        AK8GenNumbers.Fill(1,event.Generator_weight)
                    if a.pt > 200:
                        AK8GenNumbers.Fill(2,event.Generator_weight)
                    if a.pt > 300:
                        AK8GenNumbers.Fill(3,event.Generator_weight)
                if b.pt > 200:
                    if a.pt < 200:
                        AK8GenNumbers.Fill(4,event.Generator_weight)
                    if a.pt > 200:
                        AK8GenNumbers.Fill(5,event.Generator_weight)
                    if a.pt > 300:
                        AK8GenNumbers.Fill(6,event.Generator_weight)
                if b.pt > 300:
                    if a.pt < 200:
                        AK8GenNumbers.Fill(7,event.Generator_weight)
                    if a.pt > 200:
                        AK8GenNumbers.Fill(8,event.Generator_weight)
                    if a.pt > 300:
                        AK8GenNumbers.Fill(9,event.Generator_weight)
            if len(event.GenHiggsBoson)> 0 and len(event.GenHadTop)> 0 and hasattr(event.GenHiggsBoson[0],"matchAK8") and hasattr(event.GenHadTop[0],"matchHTT"):
                a = event.FatjetAK8[event.GenHiggsBoson[0].matchAK8]
                b = event.HTTV2[event.GenHadTop[0].matchHTT]
                if b.pt < 200:
                    if a.pt < 200:
                        HTTGenNumbers.Fill(1,event.Generator_weight)
                    if a.pt > 200:
                        HTTGenNumbers.Fill(2,event.Generator_weight)
                    if a.pt > 300:
                        HTTGenNumbers.Fill(3,event.Generator_weight)
                if b.pt > 200:
                    if a.pt < 200:
                        HTTGenNumbers.Fill(4,event.Generator_weight)
                    if a.pt > 200:
                        HTTGenNumbers.Fill(5,event.Generator_weight)
                    if a.pt > 300:
                        HTTGenNumbers.Fill(6,event.Generator_weight)
                if b.pt > 300:
                    if a.pt < 200:
                        HTTGenNumbers.Fill(7,event.Generator_weight)
                    if a.pt > 200:
                        HTTGenNumbers.Fill(8,event.Generator_weight)
                    if a.pt > 300:
                        HTTGenNumbers.Fill(9,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHiggsBoson) > 0 and len(event.GenHadTop) > 0 \
                and hasattr(event.GenHiggsBoson[0],"matchAK8") and hasattr(event.GenHadTop[0],"matchAK8") and hasattr(event.GenHadW[0],"matchAK8"):
                a = event.FatjetAK8[event.GenHiggsBoson[0].matchAK8]
                b = event.FatjetAK8[event.GenHadTop[0].matchAK8]
                c = event.FatjetAK8[event.GenHadW[0].matchAK8]
                if b.pt < 200:
                    if c.pt < 100:
                        if a.pt < 200:
                            AK8GenNumbers.Fill(10,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(11,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(12,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(13,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(14,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(15,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(16,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(17,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(18,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(19,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(20,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(21,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(22,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(23,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(24,event.Generator_weight)   
                if b.pt > 200:
                    if c.pt < 100:
                        if a.pt < 200:
                            AK8GenNumbers.Fill(25,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(26,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(27,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(28,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(29,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(30,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(31,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(32,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(33,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(34,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(35,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(36,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(37,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(38,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(39,event.Generator_weight)  
                if b.pt > 300:
                    if c.pt < 100:
                        if a.pt < 200:
                            AK8GenNumbers.Fill(40,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(41,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(42,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(43,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(44,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(45,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(46,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(47,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(48,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(49,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(50,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(51,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            AK8GenNumbers.Fill(52,event.Generator_weight)
                        if a.pt > 200:
                            AK8GenNumbers.Fill(53,event.Generator_weight)
                        if a.pt > 300:
                            AK8GenNumbers.Fill(54,event.Generator_weight)      

        else:
            AK8GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHadTop) > 0 \
            and hasattr(event.GenHadTop[0],"matchAK8") and hasattr(event.GenHadW[0],"matchAK8"):
                b = event.FatjetAK8[event.GenHadTop[0].matchAK8]
                c = event.FatjetAK8[event.GenHadW[0].matchAK8]
                if c.pt < 100:
                    if b.pt < 200:
                        AK8GenNumbers.Fill(10,event.Generator_weight)
                    if b.pt > 200:
                        AK8GenNumbers.Fill(25,event.Generator_weight)
                    if b.pt > 300:
                        AK8GenNumbers.Fill(40,event.Generator_weight)
                if c.pt > 100:   
                    if b.pt < 200:
                        AK8GenNumbers.Fill(13,event.Generator_weight)
                    if b.pt > 200:
                        AK8GenNumbers.Fill(28,event.Generator_weight)
                    if b.pt > 300:
                        AK8GenNumbers.Fill(43,event.Generator_weight)  
                if c.pt > 150:   
                    if b.pt < 200:
                        AK8GenNumbers.Fill(16,event.Generator_weight)
                    if b.pt > 200:
                        AK8GenNumbers.Fill(31,event.Generator_weight)
                    if b.pt > 300:
                        AK8GenNumbers.Fill(46,event.Generator_weight)   
                if c.pt > 200:   
                    if b.pt < 200:
                        AK8GenNumbers.Fill(19,event.Generator_weight)
                    if b.pt > 200:
                        AK8GenNumbers.Fill(34,event.Generator_weight)
                    if b.pt > 300:
                        AK8GenNumbers.Fill(49,event.Generator_weight)     
                if c.pt > 300:   
                    if b.pt < 200:
                        AK8GenNumbers.Fill(22,event.Generator_weight)
                    if b.pt > 200:
                        AK8GenNumbers.Fill(37,event.Generator_weight)
                    if b.pt > 300:
                        AK8GenNumbers.Fill(52,event.Generator_weight) 

 
results = ROOT.TFile("GenMatchJetStudies.root","recreate")
CA15GenHiggspT.Write()
CA15GenHiggsDR.Write()
CA15GenHiggspTDR.Write()
CA15GenToppTDR.Write()
CA15GenToppTDR2.Write()
CA15GenToppT.Write()
CA15GenTopHadpT.Write()
CA15GenTopHiggs.Write()
CA15GenTopHadHiggs.Write()
CA15GenDRTopHiggs.Write()
CA15GenDRTopTop.Write()
CA15GenDRHadTopHiggs.Write()
CA15GenWDR.Write()
CA15GenWpTDR.Write()
CA15GenWpT.Write()
CA15GenHadWDR.Write()
CA15GenHadWpTDR.Write()
CA15GenHadWpT.Write()
CA15GenNumbers.Write()

AK8GenHiggspT.Write()
AK8GenHiggsDR.Write()
AK8GenHiggspTDR.Write()
AK8GenToppTDR.Write()
AK8GenToppTDR2.Write()
AK8GenToppT.Write()
AK8GenTopHadpT.Write()
AK8GenTopHiggs.Write()
AK8GenTopHadHiggs.Write()
AK8GenDRTopHiggs.Write()
AK8GenDRTopTop.Write()
AK8GenDRHadTopHiggs.Write()
AK8GenWDR.Write()
AK8GenWpTDR.Write()
AK8GenWpT.Write()
AK8GenHadWDR.Write()
AK8GenHadWpTDR.Write()
AK8GenHadWpT.Write()
AK8GenNumbers.Write()

HTTGenHiggspT.Write()
HTTGenHiggsDR.Write()
HTTGenHiggspTDR.Write()
HTTGenToppTDR.Write()
HTTGenToppTDR2.Write()
HTTGenToppT.Write()
HTTGenTopHadpT.Write()
HTTGenTopHiggs.Write()
HTTGenTopHadHiggs.Write()
HTTGenDRTopHiggs.Write()
HTTGenDRTopTop.Write()
HTTGenDRHadTopHiggs.Write()
HTTGenWDR.Write()
HTTGenWpTDR.Write()
HTTGenWpT.Write()
HTTGenHadWDR.Write()
HTTGenHadWpTDR.Write()
HTTGenHadWpT.Write()
HTTGenNumbers.Write()
