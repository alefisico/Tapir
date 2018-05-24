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

# ==============================================================================
# Simple algorithm that matches the smallest delta R for two lists of objects
def Get_min_delR( objs1, objs2, R_cut = 'def' ):

    # Use self.R_cut if R_cut is not specified
    if R_cut == 'def':
        R_cut = self.R_cut

    n_objs1 = len(objs1)
    n_objs2 = len(objs2)

    Rmat = [[ Get_DeltaR_two_objects(objs1[i], objs2[j]) \
        for j in range(n_objs2)] for i in range(n_objs1) ]

    Rmin = 9999.0
    
    for i in range(n_objs1):
        for j in range(n_objs2):
            if Rmat[i][j] < Rmin and Rmat[i][j] < R_cut:
                Rmin = Rmat[i][j]
                i_min = i
                j_min = j

    if Rmin == 9999.0: return ( 'No link', 0, 0)

    return (i_min, j_min, Rmin)

# ==============================================================================
def Match_two_lists( objs1_orig, label1,
                     objs2_orig, label2,
                     R_cut = 'def' ):

    # Check if object is not a list; if so, convert it to a list
    # (This allows to conveniently pass single objects to the function as well)
    if hasattr( objs1_orig, 'eta' ) and hasattr( objs1_orig, 'phi' ):
        objs1_orig = [ objs1_orig ]
    if hasattr( objs2_orig, 'eta' ) and hasattr( objs2_orig, 'phi' ):
        objs2_orig = [ objs2_orig ]

    # Create list of indices
    objs1 = range(len(objs1_orig))
    objs2 = range(len(objs2_orig))
        
    # Attempt matching until the shortest list is depleted, or until there are
    # no more matches with delR < delR_cut
    n_matches = min( len(objs1), len(objs2) )

    for i_match in range(n_matches):

        # Attempt a match (map indices to objects first)
        tmp1 = [objs1_orig[i] for i in objs1]
        tmp2 = [objs2_orig[i] for i in objs2]
        (i1, i2, delR) = Get_min_delR( tmp1, tmp2, R_cut )

        # Return the attempt number if no more matches could be made
        if i1 == 'No link':
            return i_match

        # Pop the matched indices from the lists for the next iteration
        matched_obj1 = objs1.pop(i1)
        matched_obj2 = objs2.pop(i2)

        # Record the match in the original objs
        setattr(objs1_orig[matched_obj1],
                'matched_{0}'.format( label2 ),
                objs2_orig[matched_obj2])

        setattr(objs2_orig[matched_obj2],
                'matched_{0}'.format( label1 ),
                objs1_orig[matched_obj1])

        # Record the delR value in the original objs
        setattr(objs1_orig[matched_obj1],
                'matched_{0}_delR'.format( label2 ),
                delR)

        setattr(objs2_orig[matched_obj2],
                'matched_{0}_delR'.format( label1 ),
                delR)
        
    return n_matches

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
        event.GenJetAK8 = nanoTreeGenClasses.GenJetAK8.make_array(ttree)
        event.SubGenJetAK8 = nanoTreeGenClasses.SubGenJetAK8.make_array(ttree)


        #genobt_to_match = event.GenHiggsBoson+event.GenHiggsBoson+event.GenWBoson

        matched_objects = Match_two_lists(
            event.GenHiggsBoson+event.GenTop+event.GenWBoson, 'object',
            event.GenJetAK8, 'genjet',0.5)
        

        #Do all the matching here for all objects and fatjets
        for i in event.GenHiggsBoson:
            if hasattr(i,"matched_genjet"):
                matched_subjets = Match_two_lists(
                event.GenBQuarkFromH, 'quark',
                event.SubGenJetAK8, 'gensubjet',0.3)
                cnt = 1
                for j in event.GenBQuarkFromH:
                    if hasattr(j,"matched_gensubjet"):
                        setattr(i,"matched_subjet{}".format(cnt),j.matched_gensubjet)
                        cnt += 1


        leftoversubjets = []
        for x in event.SubGenJetAK8:
            if not hasattr(x,"matched_gensubjet"):
                leftoversubjets.append(x)

        for i in event.GenWBoson:
            if hasattr(i,"matched_genjet"): 
                subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,i))[:2]
                matched_subjets = Match_two_lists(
                subj, 'quark',
                leftoversubjets, 'gensubjet',0.3)
                cnt = 1
                for j in subj:
                    if hasattr(j,"matched_gensubjet"):
                        setattr(i,"matched_subjet{}".format(cnt),j.matched_gensubjet)
                        cnt += 1


        leftoversubjets2 = []
        for x in leftoversubjets:
            if not hasattr(x,"matched_gensubjet"):
                leftoversubjets2.append(x)

        for i in event.GenTop:
            if hasattr(i,"matched_genjet"): 
                subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,i))[:2]
                bs = sorted(event.GenBQuarkFromTop, key = lambda x: Get_DeltaR_two_objects(x,i))[:1]
                quark_decays = subj + bs
                matched_subjets = Match_two_lists(
                quark_decays, 'quark',
                leftoversubjets, 'gensubjet',0.3)
                cnt = 1
                for j in quark_decays:
                    if hasattr(j,"matched_gensubjet"):
                        setattr(i,"matched_subjet{}".format(cnt),j.matched_gensubjet)
                        cnt += 1


        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenHadW = filter(lambda x: (x.decayMode==1), event.GenWBoson)

        #Now do the actual code
        for k in range(0,len(event.GenHiggsBoson)):
            if hasattr(event.GenHiggsBoson[k],"matched_genjet"):
                fa = event.GenHiggsBoson[k].matched_genjet
                GenHiggspT.Fill(fa.pt,event.Generator_weight)
                if hasattr(event.GenHiggsBoson[k],"matched_subjet1") and hasattr(event.GenHiggsBoson[k],"matched_subjet2"):
                    s1 = event.GenHiggsBoson[k].matched_subjet1
                    s2 = event.GenHiggsBoson[k].matched_subjet2
                    dsub = Get_DeltaR_two_objects(s1,s2)
                    GenHiggsDR.Fill(dsub,event.Generator_weight)
                    GenHiggspTDR.Fill(fa.pt,dsub,event.Generator_weight)


        for k in range(0,len(event.GenWBoson)):
            if hasattr(event.GenWBoson[k],"matched_genjet"):
                fa = event.GenWBoson[k].matched_genjet
                GenWpT.Fill(fa.pt,event.Generator_weight)
                if event.GenWBoson[k].decayMode == 1:
                    GenHadWpT.Fill(fa.pt,event.Generator_weight)
                if hasattr(event.GenWBoson[k],"matched_subjet1") and hasattr(event.GenWBoson[k],"matched_subjet2"):
                    s1 = event.GenWBoson[k].matched_subjet1
                    s2 = event.GenWBoson[k].matched_subjet2
                    dsub = Get_DeltaR_two_objects(s1,s2)
                    GenWDR.Fill(dsub,event.Generator_weight)
                    GenWpTDR.Fill(fa.pt,dsub,event.Generator_weight)
                    if event.GenWBoson[k].decayMode == 1:
                        GenHadWDR.Fill(dsub,event.Generator_weight)
                        GenHadWpTDR.Fill(fa.pt,dsub,event.Generator_weight)             

        for k in range(0,len(event.GenTop)):
            if hasattr(event.GenTop[k],"matched_genjet"):
                fa = event.GenTop[k].matched_genjet
                GenToppT.Fill(fa.pt,event.Generator_weight)
        for k in range(0,len(event.GenHadTop)):
            if hasattr(event.GenHadTop[k],"matched_genjet"):
                fa = event.GenHadTop[k].matched_genjet
                GenTopHadpT.Fill(fa.pt,event.Generator_weight)
            if hasattr(event.GenHadTop[k],"matched_gensubjet1") and hasattr(event.GenHadTop[k],"matched_gensubjet2") and hasattr(event.GenHadTop[k],"matched_gensubjet3"):
                fa3 = event.GenHadTop[k].matched_genjet
                sjb = event.GenHadTop[k].matched_gensubjet1
                sjl1 = event.GenHadTop[k].matched_gensubjet2
                sjl2 = event.GenHadTop[k].matched_gensubjet3
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
                    GenToppTDR.Fill(fa3.pt,rad,event.Generator_weight)

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
                GenToppTDR2.Fill(fa3.pt,rad2,event.Generator_weight)

        if len(event.GenHiggsBoson)>0 and len(event.GenTop)>0:
            for k in range(0,len(event.GenTop)):
                if hasattr(event.GenTop[k],"matched_genjet") and hasattr(event.GenHiggsBoson[0],"matched_genjet"):
                    fa = event.GenTop[k].matched_genjet
                    faH = event.GenHiggsBoson[0].matched_genjet
                    GenTopHiggs.Fill(fa.pt,faH.pt,event.Generator_weight)
                    distance = Get_DeltaR_two_objects(fa,faH)
                    GenDRTopHiggs.Fill(distance,event.Generator_weight)
                    if event.GenTop[k].decayMode==1:
                        GenTopHadHiggs.Fill(fa.pt,faH.pt,event.Generator_weight)
                        GenDRHadTopHiggs.Fill(distance,event.Generator_weight)
 
        if len(event.GenTop)==2:
            if hasattr(event.GenTop[0],"matched_genjet") and hasattr(event.GenTop[1],"matched_genjet"):
                fa = event.GenTop[0].matched_genjet
                fa2 = event.GenTop[1].matched_genjet
                GenDRTopTop.Fill(Get_DeltaR_two_objects(fa,fa2),event.Generator_weight)

        #Now get numbers of boosted events
        if sample == "ttH":
            GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHiggsBoson)> 0 and len(event.GenHadTop)> 0 and hasattr(event.GenHiggsBoson[0],"matched_genjet") and hasattr(event.GenHadTop[0],"matched_genjet"):
                a = event.GenHiggsBoson[0].matched_genjet
                b = event.GenHadTop[0].matched_genjet
                if b.pt < 200:
                    if a.pt < 200:
                        GenNumbers.Fill(1,event.Generator_weight)
                    if a.pt > 200:
                        GenNumbers.Fill(2,event.Generator_weight)
                    if a.pt > 300:
                        GenNumbers.Fill(3,event.Generator_weight)
                if b.pt > 200:
                    if a.pt < 200:
                        GenNumbers.Fill(4,event.Generator_weight)
                    if a.pt > 200:
                        GenNumbers.Fill(5,event.Generator_weight)
                    if a.pt > 300:
                        GenNumbers.Fill(6,event.Generator_weight)
                if b.pt > 300:
                    if a.pt < 200:
                        GenNumbers.Fill(7,event.Generator_weight)
                    if a.pt > 200:
                        GenNumbers.Fill(8,event.Generator_weight)
                    if a.pt > 300:
                        GenNumbers.Fill(9,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHiggsBoson) > 0 and len(event.GenHadTop) > 0 \
                and hasattr(event.GenHiggsBoson[0],"matched_genjet") and hasattr(event.GenHadTop[0],"matched_genjet") and hasattr(event.GenHadW[0],"matched_genjet"):
                a = event.GenHiggsBoson[0].matched_genjet
                b = event.GenHadTop[0].matched_genjet
                c = event.GenHadW[0].matched_genjet
                if b.pt < 200:
                    if c.pt < 100:
                        if a.pt < 200:
                            GenNumbers.Fill(10,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(11,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(12,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            GenNumbers.Fill(13,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(14,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(15,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            GenNumbers.Fill(16,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(17,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(18,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            GenNumbers.Fill(19,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(20,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(21,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            GenNumbers.Fill(22,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(23,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(24,event.Generator_weight)   
                if b.pt > 200:
                    if c.pt < 100:
                        if a.pt < 200:
                            GenNumbers.Fill(25,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(26,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(27,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            GenNumbers.Fill(28,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(29,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(30,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            GenNumbers.Fill(31,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(32,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(33,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            GenNumbers.Fill(34,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(35,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(36,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            GenNumbers.Fill(37,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(38,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(39,event.Generator_weight)  
                if b.pt > 300:
                    if c.pt < 100:
                        if a.pt < 200:
                            GenNumbers.Fill(40,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(41,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(42,event.Generator_weight)
                    if c.pt > 100:   
                        if a.pt < 200:
                            GenNumbers.Fill(43,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(44,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(45,event.Generator_weight)  
                    if c.pt > 150:   
                        if a.pt < 200:
                            GenNumbers.Fill(46,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(47,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(48,event.Generator_weight)   
                    if c.pt > 200:   
                        if a.pt < 200:
                            GenNumbers.Fill(49,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(50,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(51,event.Generator_weight)     
                    if c.pt > 300:   
                        if a.pt < 200:
                            GenNumbers.Fill(52,event.Generator_weight)
                        if a.pt > 200:
                            GenNumbers.Fill(53,event.Generator_weight)
                        if a.pt > 300:
                            GenNumbers.Fill(54,event.Generator_weight)      

        else:
            GenNumbers.Fill(0,event.Generator_weight)
            if len(event.GenHadW) > 0 and len(event.GenHadTop) > 0 \
            and hasattr(event.GenHadTop[0],"matched_genjet") and hasattr(event.GenHadW[0],"matched_genjet"):
                b = event.GenHadTop[0].matched_genjet
                c = event.GenHadW[0].matched_genjet
                if c.pt < 100:
                    if b.pt < 200:
                        GenNumbers.Fill(10,event.Generator_weight)
                    if b.pt > 200:
                        GenNumbers.Fill(25,event.Generator_weight)
                    if b.pt > 300:
                        GenNumbers.Fill(40,event.Generator_weight)
                if c.pt > 100:   
                    if b.pt < 200:
                        GenNumbers.Fill(13,event.Generator_weight)
                    if b.pt > 200:
                        GenNumbers.Fill(28,event.Generator_weight)
                    if b.pt > 300:
                        GenNumbers.Fill(43,event.Generator_weight)  
                if c.pt > 150:   
                    if b.pt < 200:
                        GenNumbers.Fill(16,event.Generator_weight)
                    if b.pt > 200:
                        GenNumbers.Fill(31,event.Generator_weight)
                    if b.pt > 300:
                        GenNumbers.Fill(46,event.Generator_weight)   
                if c.pt > 200:   
                    if b.pt < 200:
                        GenNumbers.Fill(19,event.Generator_weight)
                    if b.pt > 200:
                        GenNumbers.Fill(34,event.Generator_weight)
                    if b.pt > 300:
                        GenNumbers.Fill(49,event.Generator_weight)     
                if c.pt > 300:   
                    if b.pt < 200:
                        GenNumbers.Fill(22,event.Generator_weight)
                    if b.pt > 200:
                        GenNumbers.Fill(37,event.Generator_weight)
                    if b.pt > 300:
                        GenNumbers.Fill(52,event.Generator_weight) 


 
results = ROOT.TFile("GenMatchGenJetStudies.root","recreate")
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

