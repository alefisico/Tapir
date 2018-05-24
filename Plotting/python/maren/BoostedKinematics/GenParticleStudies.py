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

GenHiggspT = ROOT.TH1F("GenHiggspT","GenHiggspT",200,0,1000)
GenHiggsDR = ROOT.TH1F("GenHiggsDR","GenHiggsDR",100,0,5)
GenHiggspTDR = ROOT.TH2F("GenHiggspTDR","GenHiggspTDR",200,0,1000,100,0,5)
GenToppTDR = ROOT.TH2F("GenToppTDR","GenToppTDR",200,0,1000,100,0,5)
GenToppTDR2 = ROOT.TH2F("GenToppTDR2","GenToppTDR2",200,0,1000,100,0,5)
GenToppT = ROOT.TH1F("GenToppT","GenToppT",200,0,1000)
GenTopHadpT = ROOT.TH1F("GenTopHadpT","GenTopHadpT",200,0,1000)
GenTopHiggs = ROOT.TH2F("GenTopHiggs","GenTopHiggs",200,0,1000,200,0,1000)
GenTopHadHiggs = ROOT.TH2F("GenTopHadHiggs","GenTopHadHiggs",200,0,1000,200,0,1000)
GenDRTopHiggs = ROOT.TH1F("GenDRTopHiggs","GenDRTopHiggs",50,0,5)
GenDRTopTop = ROOT.TH1F("GenDRTopTop","GenDRTopTop",50,0,5)
GenDRHadTopHiggs = ROOT.TH1F("GenDRHadTopHiggs","GenDRHadTopHiggs",50,0,5)
GenWDR = ROOT.TH1F("GenWDR","GenWDR",100,0,5)
GenWpTDR = ROOT.TH2F("GenWpTDR","GenWpTDR",200,0,1000,100,0,5)
GenWpT = ROOT.TH1F("GenWpT","GenWpT",200,0,1000)
GenHadWDR = ROOT.TH1F("GenHadWDR","GenHadWDR",100,0,5)
GenHadWpTDR = ROOT.TH2F("GenHadWpTDR","GenHadWpTDR",200,0,1000,100,0,5)
GenHadWpT = ROOT.TH1F("GenHadWpT","GenHadWpT",200,0,1000)
GenNumbers = ROOT.TH1F("GenNumbers","GenNumbers",200,0,200)

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
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.GenWBoson = nanoTreeGenClasses.GenWBoson.make_array(event.GenParticle)
        event.GenHadW = filter(lambda x: (x.decayMode==1), event.GenWBoson)
        #event.GenLepTop = filter(lambda x: (x.decayMode==0), event.GenTop)
        #event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        #event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        #event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        #event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        #event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")
        #event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        #event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")



        for k in range(0,len(event.GenHiggsBoson)):
            GenHiggspT.Fill(event.GenHiggsBoson[k].pt,event.Generator_weight)
            dsub = Get_DeltaR_two_objects(event.GenBQuarkFromH[0],event.GenBQuarkFromH[1])
            GenHiggsDR.Fill(dsub,event.Generator_weight)
            GenHiggspTDR.Fill(event.GenHiggsBoson[k].pt,dsub,event.Generator_weight)


        for k in range(0,len(event.GenWBoson)):
            GenWpT.Fill(event.GenWBoson[k].pt,event.Generator_weight)
            subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,event.GenWBoson[k])) 
            if len(subj) >=2:
                dsub = Get_DeltaR_two_objects(subj[0],subj[1])
                GenWDR.Fill(dsub,event.Generator_weight)
                GenWpTDR.Fill(event.GenWBoson[k].pt,dsub,event.Generator_weight)
            if event.GenWBoson[k].decayMode == 1:
                GenHadWpT.Fill(event.GenWBoson[k].pt,event.Generator_weight)
                subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,event.GenWBoson[k])) 
                if len(subj) >= 2:
                    dsub = Get_DeltaR_two_objects(subj[0],subj[1])
                    GenHadWDR.Fill(dsub,event.Generator_weight)
                    GenHadWpTDR.Fill(event.GenWBoson[k].pt,dsub,event.Generator_weight)


        for k in range(0,len(event.GenTop)):
            GenT = ROOT.TLorentzVector()
            GenT.SetPtEtaPhiM(event.GenTop[k].pt,event.GenTop[k].eta,event.GenTop[k].phi,event.GenTop[k].mass)
            GenToppT.Fill(GenT.Pt(),event.Generator_weight)
        for k in event.GenHadTop:
            GenTopHadpT.Fill(k.pt,event.Generator_weight)
            if len(event.GenWZQuark) == 2:
                closest = -1
                dist = 10
                for l in range(len(event.GenBQuarkFromTop)):
                    dr = Get_DeltaR_two_objects(event.GenBQuarkFromTop[l],k)
                    if dr<dist:
                        dist = dr
                        closest = l
                GenB = ROOT.TLorentzVector()
                GenB.SetPtEtaPhiM(event.GenBQuarkFromTop[closest].pt,event.GenBQuarkFromTop[closest].eta,event.GenBQuarkFromTop[closest].phi,event.GenBQuarkFromTop[closest].mass)
                GenW1 = ROOT.TLorentzVector()
                GenW1.SetPtEtaPhiM(event.GenWZQuark[0].pt,event.GenWZQuark[0].eta,event.GenWZQuark[0].phi,event.GenWZQuark[0].mass)
                GenW2 = ROOT.TLorentzVector()
                GenW2.SetPtEtaPhiM(event.GenWZQuark[1].pt,event.GenWZQuark[1].eta,event.GenWZQuark[1].phi,event.GenWZQuark[1].mass)
                d1 = Get_DeltaR_two_objects(event.GenBQuarkFromTop[closest],event.GenWZQuark[0])
                d2 = Get_DeltaR_two_objects(event.GenBQuarkFromTop[closest],event.GenWZQuark[1])
                d3 = Get_DeltaR_two_objects(event.GenWZQuark[0],event.GenWZQuark[1])
                try:
                    s = (d1+d2+d3)/2
                    area = math.sqrt(s*(s-d1)*(s-d2)*(s-d3))
                    rad = (d1*d2*d3)/(4*area)
                    GenToppTDR.Fill(k.pt,rad,event.Generator_weight)

                    jet12 = GenB + GenW1
                    jet13 = GenB + GenW2
                    jet23 = GenW1 + GenW2
                    a = Get_DeltaR_two_objects(event.GenBQuarkFromTop[closest],event.GenWZQuark[0])
                    b = Get_DeltaR_two_objects(event.GenWZQuark[0],event.GenWZQuark[1])
                    c = Get_DeltaR_two_objects(event.GenWZQuark[1],event.GenBQuarkFromTop[closest])
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
                    GenToppTDR2.Fill(GenT.Pt(),rad2,event.Generator_weight)
                except:
                    pass


        if len(event.GenHiggsBoson)>0 and len(event.GenTop)>0:
            for k in range(0,len(event.GenTop)):
                GenTopHiggs.Fill(event.GenTop[k].pt,event.GenHiggsBoson[0].pt,event.Generator_weight)
                distance = Get_DeltaR_two_objects(event.GenTop[k],event.GenHiggsBoson[0])
                GenDRTopHiggs.Fill(distance,event.Generator_weight)
                if event.GenTop[k].decayMode==1:
                    GenTopHadHiggs.Fill(event.GenTop[k].pt,event.GenHiggsBoson[0].pt,event.Generator_weight)
                    GenDRHadTopHiggs.Fill(distance,event.Generator_weight)

        if len(event.GenTop)==2:
            GenDRTopTop.Fill(Get_DeltaR_two_objects(event.GenTop[0],event.GenTop[1]),event.Generator_weight)

        #Now get numbers of boosted events
        if sample == "ttH":
            GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHiggsBoson)> 0 and len(event.GenHadTop)> 0:
                if event.GenHadTop[0].pt < 200:
                    if event.GenHiggsBoson[0].pt < 200:
                        GenNumbers.Fill(1,event.Generator_weight)
                    if event.GenHiggsBoson[0].pt > 200:
                        GenNumbers.Fill(2,event.Generator_weight)
                    if event.GenHiggsBoson[0].pt > 300:
                        GenNumbers.Fill(3,event.Generator_weight)
                if event.GenHadTop[0].pt > 200:
                    if event.GenHiggsBoson[0].pt < 200:
                        GenNumbers.Fill(4,event.Generator_weight)
                    if event.GenHiggsBoson[0].pt > 200:
                        GenNumbers.Fill(5,event.Generator_weight)
                    if event.GenHiggsBoson[0].pt > 300:
                        GenNumbers.Fill(6,event.Generator_weight)
                if event.GenHadTop[0].pt > 300:
                    if event.GenHiggsBoson[0].pt < 200:
                        GenNumbers.Fill(7,event.Generator_weight)
                    if event.GenHiggsBoson[0].pt > 200:
                        GenNumbers.Fill(8,event.Generator_weight)
                    if event.GenHiggsBoson[0].pt > 300:
                        GenNumbers.Fill(9,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHiggsBoson)> 0 and len(event.GenHadTop) > 0:
                if event.GenHadTop[0].pt < 200:
                    if event.GenHadW[0].pt < 100:
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(10,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(11,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(12,event.Generator_weight)
                    if event.GenHadW[0].pt > 100:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(13,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(14,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(15,event.Generator_weight)  
                    if event.GenHadW[0].pt > 150:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(16,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(17,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(18,event.Generator_weight)   
                    if event.GenHadW[0].pt > 200:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(19,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(20,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(21,event.Generator_weight)     
                    if event.GenHadW[0].pt > 300:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(22,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(23,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(24,event.Generator_weight)   
                if event.GenHadTop[0].pt > 200:
                    if event.GenHadW[0].pt < 100:
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(25,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(26,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(27,event.Generator_weight)
                    if event.GenHadW[0].pt > 100:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(28,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(29,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(30,event.Generator_weight)  
                    if event.GenHadW[0].pt > 150:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(31,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(32,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(33,event.Generator_weight)   
                    if event.GenHadW[0].pt > 200:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(34,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(35,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(36,event.Generator_weight)     
                    if event.GenHadW[0].pt > 300:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(37,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(38,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(39,event.Generator_weight)  
                if event.GenHadTop[0].pt > 300:
                    if event.GenHadW[0].pt < 100:
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(40,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(41,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(42,event.Generator_weight)
                    if event.GenHadW[0].pt > 100:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(43,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(44,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(45,event.Generator_weight)  
                    if event.GenHadW[0].pt > 150:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(46,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(47,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(48,event.Generator_weight)   
                    if event.GenHadW[0].pt > 200:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(49,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(50,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(51,event.Generator_weight)     
                    if event.GenHadW[0].pt > 300:   
                        if event.GenHiggsBoson[0].pt < 200:
                            GenNumbers.Fill(52,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 200:
                            GenNumbers.Fill(53,event.Generator_weight)
                        if event.GenHiggsBoson[0].pt > 300:
                            GenNumbers.Fill(54,event.Generator_weight)      

        else:
            GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHadTop) > 0:
                if event.GenHadW[0].pt < 100:
                    if event.GenHadTop[0].pt < 200:
                        GenNumbers.Fill(10,event.Generator_weight)
                    if event.GenHadTop[0].pt > 200:
                        GenNumbers.Fill(25,event.Generator_weight)
                    if event.GenHadTop[0].pt > 300:
                        GenNumbers.Fill(40,event.Generator_weight)
                if event.GenHadW[0].pt > 100:   
                    if event.GenHadTop[0].pt < 200:
                        GenNumbers.Fill(13,event.Generator_weight)
                    if event.GenHadTop[0].pt > 200:
                        GenNumbers.Fill(28,event.Generator_weight)
                    if event.GenHadTop[0].pt > 300:
                        GenNumbers.Fill(43,event.Generator_weight)  
                if event.GenHadW[0].pt > 150:   
                    if event.GenHadTop[0].pt < 200:
                        GenNumbers.Fill(16,event.Generator_weight)
                    if event.GenHadTop[0].pt > 200:
                        GenNumbers.Fill(31,event.Generator_weight)
                    if event.GenHadTop[0].pt > 300:
                        GenNumbers.Fill(46,event.Generator_weight)   
                if event.GenHadW[0].pt > 200:   
                    if event.GenHadTop[0].pt < 200:
                        GenNumbers.Fill(19,event.Generator_weight)
                    if event.GenHadTop[0].pt > 200:
                        GenNumbers.Fill(34,event.Generator_weight)
                    if event.GenHadTop[0].pt > 300:
                        GenNumbers.Fill(49,event.Generator_weight)     
                if event.GenHadW[0].pt > 300:   
                    if event.GenHadTop[0].pt < 200:
                        GenNumbers.Fill(22,event.Generator_weight)
                    if event.GenHadTop[0].pt > 200:
                        GenNumbers.Fill(37,event.Generator_weight)
                    if event.GenHadTop[0].pt > 300:
                        GenNumbers.Fill(52,event.Generator_weight) 

 
results = ROOT.TFile("GenParticleStudies.root","recreate")
GenHiggspT.Write()
GenHiggsDR.Write()
GenHiggspTDR.Write()
GenToppTDR.Write()
GenToppTDR2.Write()
GenToppT.Write()
GenTopHadpT.Write()
GenTopHiggs.Write()
GenTopHadHiggs.Write()
GenDRTopHiggs.Write()
GenDRTopTop.Write()
GenDRHadTopHiggs.Write()
GenWDR.Write()
GenWpTDR.Write()
GenWpT.Write()
GenHadWDR.Write()
GenHadWpTDR.Write()
GenHadWpT.Write()
GenNumbers.Write()