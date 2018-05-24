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
            self.frec = getattr(tree,"{}_fRec".format(name))[n]   
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
            self.msoftdrop = getattr(tree,"{}_msoftdrop".format(name))[n]
        pass
    @staticmethod
    def make_array(input,name):
        return [JetCollection(input, i, name) for i in range(getattr(input,"n{}".format(name)))]


def Get_DeltaR_two_objects_coord(obj1_eta, obj1_phi, obj2_eta, obj2_phi ):

    #for obj in [ obj1, obj2 ]:
    #    if not ( hasattr( obj, 'phi' ) or hasattr( obj, 'eta' ) ):
    #        print "Can't calculate Delta R: objects don't have right attributes"
    #        return 0

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

def GetCategory(event,conf):
    for id_type in ["SL", "DL", "veto"]:
        sumleps = []
        event.mu = event.Muon
        event.el = event.Electron
        for lep_flavour in ["mu", "el"]:
            lepcuts = conf.leptons[lep_flavour][id_type]
            incoll = getattr(event, lep_flavour)
            
            #The isolation type and cut value to be used
            isotype = conf.leptons[lep_flavour]["isotype"]
            isocut = lepcuts.get("iso", None)


            #Filter leptons by pt and eta
            leps = filter(
                lambda x, lepcuts=lepcuts: (
                    x.pt > lepcuts.get("pt", 0) #pt cut may be optional in case of DL
                    and abs(x.eta) < lepcuts["eta"]
                ), incoll
            )

            #Apply isolation cut
            for lep in leps:
                lep.iso = getattr(lep, isotype)
            if not isocut is None:

                #Inverted isolation cut
                if lepcuts.get("isoinverted", False):
                    leps = filter(
                        lambda x, isotype=isotype, isocut=isocut: abs(getattr(x, isotype)) >= isocut, leps
                    )
                #Normal isolation cut
                else:
                    leps = filter(
                        lambda x, isotype=isotype, isocut=isocut: abs(getattr(x, isotype)) < isocut, leps
                    )
            
            #Apply ID cut 
            leps = filter(lepcuts["idcut"], leps)

            sumleps += leps
            lepname = lep_flavour + "_" + id_type
            setattr(event, lepname, leps)
            setattr(event, "n_"+  lepname, len(leps))
        #end of lep_flavour loop
        setattr(event, "lep_{0}".format(id_type), sumleps)
        setattr(event, "n_lep_{0}".format(id_type), len(sumleps))
    #end of id_type loop
    event.lep_SL = sorted(event.lep_SL, key=lambda x: x.pt, reverse=True)
    event.lep_DL = sorted(event.lep_DL, key=lambda x: x.pt, reverse=True)
    event.lep_veto = sorted(event.lep_veto, key=lambda x: x.pt, reverse=True)

    #Apply two-stage pt cut on DL leptons
    lep_DL_afterpt = []
    for lep in event.lep_DL:
        if len(lep_DL_afterpt) == 0:
            ptcut = conf.leptons["DL"]["pt_leading"]
        else: 
            ptcut = conf.leptons["DL"]["pt_subleading"]
        if lep.pt > ptcut:
            lep_DL_afterpt += [lep]
    event.lep_DL = lep_DL_afterpt
    event.n_lep_DL = len(event.lep_DL)

    event.is_sl = (event.n_lep_SL == 1 and event.n_lep_veto == 1)
    event.is_dl = (event.n_lep_DL == 2 and event.n_lep_veto == 2)
    event.is_fh = (not event.is_sl and not event.is_dl)

def MatchToCand(genParticle,jets,dist=1.5):
    part = None
    for i in jets:
        dr = Get_DeltaR_two_objects(genParticle,i)
        if dr < dist:
            dist = dr
            part = i
    return part

def Get_min_delR(objs1, objs2, R_cut = 'def' ):

    # Use self.R_cut if R_cut is not specified
    if R_cut == 'def':
        R_cut = 0.3

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

def Match_two_lists(objs1_orig, label1, objs2_orig, label2, R_cut = 'def' ):

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


def MatchFatjets(objs,jets):

    # Loosely match the fatjets to the tops
    n_matched_fatjet = Match_two_lists(
        objs, 'objs',
        event.FatjetCA15, 'fatjet',
        R_cut = 1.0 )


    # New list of tops after n_subjettiness cut is applied
    obj_with_info = []

    for o in objs:

        # Skip unmatched tops
        if not hasattr( o, 'matched_fatjet' ):
            print 'Warning: Candidate unmatchable to fatjet!'
            continue

        fatjet = o.matched_fatjet

        # Get n_subjettiness from the matched fatjet
        tau32 = fatjet.tau3 / fatjet.tau2 if fatjet.tau2 > 0.0 else 0.0 
        tau21 = fatjet.tau2 / fatjet.tau1 if fatjet.tau1 > 0.0 else 0.0 

        # Set n_subjettiness, tau_N and the bbtag
        o.tau32 = tau32
        o.tau21 = tau21
        o.tau1 = fatjet.tau1
        o.tau2 = fatjet.tau2
        o.tau3 = fatjet.tau3
        
        o.bbtag = fatjet.bbtag

        # Calculate delRopt
        if hasattr(o, 'Ropt'):
            o.delRopt = o.Ropt - o.RoptCalc

        # Append the httCandidate class to the list
        obj_with_info.append(o)

    return obj_with_info


########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {}
#for k,v in files.iteritems():
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v


#full_file_names["TTH"] = "root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/mameinha/ttHTobb_M125_TuneCUETP8M2_13TeV-powheg-pythia8/BoostedNanoAOD_Feb12_ttH/180212_074120/0000/out_13.root"


########################################
# Create histograms, saved in file
########################################

cats = ["sl","dl"]
criteriaT = ["pt","btag","Wmass","Tmass","DRl","frec","Ropt","tau32"]
criteriaH = ["pt","btag1","btag2","bbtag","DRl","mass","softdropmass","tau21"]
scenarios = ["Hsl","Hdl","Tsl","HTsl","THsl"]
obj = ["Higgs","Top","HiggsAK8","HiggsafterTop","TopAfterHiggs"]
mtop =  173.21
mHiggs = 125.09
mW = 80.385


Cat = {}
Count = {}

for i in cats:
    Cat[i] = {}
    Count[i] = {}
    for j in obj:
        Cat[i][j] = ROOT.TH1F("{}_{}".format(i,j),"{}_{}".format(i,j),8,0,8)
        for m in range(1,9):
            if "Higgs" in j:
                Cat[i][j].GetXaxis().SetBinLabel(m,criteriaH[m-1])
            else:
                Cat[i][j].GetXaxis().SetBinLabel(m,criteriaT[m-1])
        Count[i][j] = ROOT.TH1F("Count{}_{}".format(i,j),"{}_{}".format(i,j),1,0,1)



########################################
# Run code
########################################

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("Events")

    counter = 0

    print "_____________________",ttree.GetEntries()

    for event in ttree :
        if counter == 25000:
            break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event
        counter += 1

        #event.Jet = nanoTreeClasses.Jet.make_array(ttree, MC = True)
        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        #event.GenJet = nanoTreeGenClasses.GenJet.make_array(ttree)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        #event.GenLepFromTop = nanoTreeGenClasses.GenLepFromTop.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")

        #event.FatjetAK8 = filter(lambda x: (x.pt > 300 and abs(x.eta) < 2.4), event.FatjetAK8)
        event.HTTV2 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.HTTV2)
        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15SoftDrop)

        event.FatjetCA15SoftDrop = MatchFatjets(event.FatjetCA15SoftDrop,event.FatjetCA15)
        event.HTTV2 = MatchFatjets(event.HTTV2,event.FatjetCA15)

        GetCategory(event,python_conf)


        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue
        if len(event.FatjetCA15SoftDrop) > 0:

            Count[cat]["Higgs"].Fill(0)

            Matchedhiggscan = MatchToCand(event.GenHiggsBoson[0],event.FatjetCA15SoftDrop)
            MatchedhiggscanUngroomed = MatchToCand(event.GenHiggsBoson[0],event.FatjetCA15)

            #pT
            Hpt = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.pt, reverse=True)
            if Hpt[0] == Matchedhiggscan:
                Cat[cat]["Higgs"].Fill(0)
            #Tau21
            Ht21 = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.tau21, reverse=False)
            if Ht21[0] == Matchedhiggscan:
                Cat[cat]["Higgs"].Fill(7)
            #bbtag
            Hbbtag = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.bbtag, reverse=True)
            if Hbbtag[0] == Matchedhiggscan:
                Cat[cat]["Higgs"].Fill(3)
            #Mass
            Hmass = min(enumerate(event.FatjetCA15), key=lambda x: abs(x[1].mass-mHiggs))
            if event.FatjetCA15[Hmass[0]] == MatchedhiggscanUngroomed:
                Cat[cat]["Higgs"].Fill(5)
            #Mass softdrop
            HmassSD = min(enumerate(event.FatjetCA15SoftDrop), key=lambda x: abs(x[1].mass-mHiggs))
            if event.FatjetCA15SoftDrop[HmassSD[0]] == Matchedhiggscan:
                Cat[cat]["Higgs"].Fill(6)
            #Btags
            for i in event.FatjetCA15SoftDrop:
                btag1 = event.FatjetCA15SoftDropSubjets[i.subJetIdx1].btag
                btag2 = event.FatjetCA15SoftDropSubjets[i.subJetIdx2].btag
                i.btagF = max(btag1,btag2)
                i.btagS = min(btag1,btag2)

            HbtagF = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.btagF, reverse=True)
            if HbtagF[0] == Matchedhiggscan:
                Cat[cat]["Higgs"].Fill(1)
            HbtagS = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.btagS, reverse=True)
            if HbtagS[0] == Matchedhiggscan:
                Cat[cat]["Higgs"].Fill(2)
            #DeltaR to lepton
            if event.is_sl:
                lepton = event.lep_SL[0]
                HDR = max(enumerate(event.FatjetCA15SoftDrop), key=lambda x: abs(Get_DeltaR_two_objects(x[1],lepton)))
                if event.FatjetCA15SoftDrop[HDR[0]] == Matchedhiggscan:
                    Cat[cat]["Higgs"].Fill(4)


        if len(event.HTTV2) > 0:

            Matchedtopcand = []
            for i in event.GenTop:
                if i.decayMode == 1:
                    Matchedtopcand.append(MatchToCand(i,event.HTTV2))

            Count[cat]["Top"].Fill(0)

            #pT
            Tpt = sorted(event.HTTV2, key=lambda x: x.pt, reverse=True)
            if Tpt[0] in Matchedtopcand:
                Cat[cat]["Top"].Fill(0)
            #Tau21
            Tt32 = sorted(event.HTTV2, key=lambda x: x.tau32, reverse=False)
            if Tt32[0] in Matchedtopcand:
                Cat[cat]["Top"].Fill(7)
            #Mass
            Tmass = min(enumerate(event.HTTV2), key=lambda x: abs(x[1].mass-mtop))
            if event.HTTV2[Tmass[0]] in Matchedtopcand:
                Cat[cat]["Top"].Fill(3)
            #frec
            Tfrec = sorted(event.HTTV2, key=lambda x: x.frec, reverse=False)
            if Tfrec[0] in Matchedtopcand:
                Cat[cat]["Top"].Fill(5)
            #Ropt
            TRopt = sorted(event.HTTV2, key=lambda x: x.delRopt, reverse=False)
            if TRopt[0] in Matchedtopcand:
                Cat[cat]["Top"].Fill(6)
            #DeltaR to lepton
            if event.is_sl:
                lepton = event.lep_SL[0]
                TDR = max(enumerate(event.HTTV2), key=lambda x: abs(Get_DeltaR_two_objects(x[1],lepton)))
                if event.HTTV2[TDR[0]] in Matchedtopcand:
                    Cat[cat]["Top"].Fill(4)
            #Btags
            for i in event.HTTV2:
                Wsubjets = []
                btag1 = event.HTTV2Subjets[i.subJetIdx1].btag
                btag2 = event.HTTV2Subjets[i.subJetIdx2].btag
                btag3 = event.HTTV2Subjets[i.subJetIdx3].btag
                i.btagF = max(btag1,btag2,btag3)
                i.btagS = min(btag1,btag2,btag3)
                if btag1 == max(btag1,btag2,btag3):
                    Wsubjets = [i.subJetIdx2,i.subJetIdx3]
                elif btag2 == max(btag1,btag2,btag3):
                    Wsubjets = [i.subJetIdx1,i.subJetIdx3]
                else:
                    Wsubjets = [i.subJetIdx1,i.subJetIdx2]
                W1 = ROOT.TLorentzVector()
                W2 = ROOT.TLorentzVector()
                W1.SetPtEtaPhiM(event.HTTV2Subjets[Wsubjets[0]].pt,event.HTTV2Subjets[Wsubjets[0]].eta,event.HTTV2Subjets[Wsubjets[0]].phi,event.HTTV2Subjets[Wsubjets[0]].mass)
                W2.SetPtEtaPhiM(event.HTTV2Subjets[Wsubjets[1]].pt,event.HTTV2Subjets[Wsubjets[1]].eta,event.HTTV2Subjets[Wsubjets[1]].phi,event.HTTV2Subjets[Wsubjets[1]].mass)
                W3 = W1 + W2
                i.Wmass = W3.M()
            TbtagF = sorted(event.HTTV2, key=lambda x: x.btagF, reverse=True)
            if TbtagF[0] in Matchedtopcand:
                Cat[cat]["Top"].Fill(1)
            #Wmass
            TmassW = min(enumerate(event.HTTV2), key=lambda x: abs(x[1].Wmass-mW))
            if event.HTTV2[TmassW[0]] in Matchedtopcand:
                Cat[cat]["Top"].Fill(2)

        #Higgs AK8
        if len(event.FatjetAK8) > 0:

            #if cat == "sl":
            #    continue

            Count[cat]["HiggsAK8"].Fill(0)

            Matchedhiggscan = MatchToCand(event.GenHiggsBoson[0],event.FatjetAK8)

            #pT
            Hpt = sorted(event.FatjetAK8, key=lambda x: x.pt, reverse=True)
            if Get_DeltaR_two_objects(Hpt[0],event.GenHiggsBoson[0])<0.8:
                Cat[cat]["HiggsAK8"].Fill(0)
            #Tau21
            Ht21 = sorted(event.FatjetAK8, key=lambda x: x.tau21, reverse=False)
            if Get_DeltaR_two_objects(Ht21[0],event.GenHiggsBoson[0])<0.8:
                Cat[cat]["HiggsAK8"].Fill(7)
            #bbtag
            Hbbtag = sorted(event.FatjetAK8, key=lambda x: x.bbtag, reverse=True)
            if Get_DeltaR_two_objects(Hbbtag[0],event.GenHiggsBoson[0])<0.8:
                Cat[cat]["HiggsAK8"].Fill(3)
            #Mass
            Hmass = min(enumerate(event.FatjetAK8), key=lambda x: abs(x[1].mass-mHiggs))
            if Get_DeltaR_two_objects(event.FatjetAK8[Hmass[0]],event.GenHiggsBoson[0])<0.8:
                Cat[cat]["HiggsAK8"].Fill(5)
            #Mass softdrop
            HmassSD = min(enumerate(event.FatjetAK8), key=lambda x: abs(x[1].msoftdrop-mHiggs))
            if Get_DeltaR_two_objects(event.FatjetAK8[HmassSD[0]],event.GenHiggsBoson[0])<0.8:
                Cat[cat]["HiggsAK8"].Fill(6)
            #Btags
            """for i in event.FatjetAK8:
                btag1 = event.FatjetAK8Subjets[i.subJetIdx1].btag
                btag2 = event.FatjetAK8Subjets[i.subJetIdx2].btag
                i.btagF = max(btag1,btag2)
                i.btagS = min(btag1,btag2)

            HbtagF = sorted(event.FatjetAK8, key=lambda x: x.btagF, reverse=False)
            if HbtagF[0] == Matchedhiggscan:
                Cat[cat]["HiggsAK8"].Fill(1)
            HbtagS = sorted(event.FatjetAK8, key=lambda x: x.btagS, reverse=False)
            if HbtagS[0] == Matchedhiggscan:
                Cat[cat]["HiggsAK8"].Fill(2)"""
            #DeltaR to lepton
            if event.is_sl:
                lepton = event.lep_SL[0]
                HDR = max(enumerate(event.FatjetAK8), key=lambda x: abs(Get_DeltaR_two_objects(x[1],lepton)))
                if Get_DeltaR_two_objects(event.FatjetAK8[HDR[0]],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsAK8"].Fill(4)


            #Now do double matching in SL:
            if event.is_dl:
                continue

            if len(event.HTTV2) == 0 or len(event.FatjetCA15SoftDrop) == 0:
                continue

            #Choose top first by furthest to the lepton

            lepton = event.lep_SL[0]
            TDR = max(enumerate(event.HTTV2), key=lambda x: abs(Get_DeltaR_two_objects(x[1],lepton)))
            topCandidate = event.HTTV2[TDR[0]]

            MatchedFatjet = MatchToCand(topCandidate,event.FatjetCA15SoftDrop,dist=0.8)
            MatchedFatjetUngroomed = MatchToCand(topCandidate,event.FatjetCA15,dist=0.8)
            FilteredHCand = filter(lambda x: (x != MatchedFatjet), event.FatjetCA15SoftDrop)
            FilteredHCandUngroomed = filter(lambda x: (x != MatchedFatjetUngroomed), event.FatjetCA15)

            if len(FilteredHCand) > 0:

                Count[cat]["HiggsafterTop"].Fill(0)

                #Matchedhiggscan = MatchToCand(event.GenHiggsBoson[0],event.FilteredHCand)

                #pT
                Hpt = sorted(FilteredHCand, key=lambda x: x.pt, reverse=True)
                if Get_DeltaR_two_objects(Hpt[0],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsafterTop"].Fill(0)
                #Tau21
                Ht21 = sorted(FilteredHCand, key=lambda x: x.tau21, reverse=False)
                if Get_DeltaR_two_objects(Ht21[0],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsafterTop"].Fill(7)
                #bbtag
                Hbbtag = sorted(FilteredHCand, key=lambda x: x.bbtag, reverse=True)
                if Get_DeltaR_two_objects(Hbbtag[0],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsafterTop"].Fill(3)
                #Mass
                Hmass = min(enumerate(FilteredHCandUngroomed), key=lambda x: abs(x[1].mass-mHiggs))
                if Get_DeltaR_two_objects(FilteredHCandUngroomed[Hmass[0]],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsafterTop"].Fill(5)
                #Mass softdrop
                HmassSD = min(enumerate(FilteredHCand), key=lambda x: abs(x[1].mass-mHiggs))
                if Get_DeltaR_two_objects(FilteredHCand[HmassSD[0]],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsafterTop"].Fill(6)
                #Btags
                for i in FilteredHCand:
                    btag1 = event.FatjetCA15SoftDropSubjets[i.subJetIdx1].btag
                    btag2 = event.FatjetCA15SoftDropSubjets[i.subJetIdx2].btag
                    i.btagF = max(btag1,btag2)
                    i.btagS = min(btag1,btag2)

                HbtagF = sorted(FilteredHCand, key=lambda x: x.btagF, reverse=True)
                if Get_DeltaR_two_objects(HbtagF[0],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsafterTop"].Fill(1)
                HbtagS = sorted(FilteredHCand, key=lambda x: x.btagS, reverse=True)
                if Get_DeltaR_two_objects(HbtagS[0],event.GenHiggsBoson[0])<0.8:
                    Cat[cat]["HiggsafterTop"].Fill(2)
                #DeltaR to lepton
                if event.is_sl:
                    lepton = event.lep_SL[0]
                    HDR = max(enumerate(FilteredHCand), key=lambda x: abs(Get_DeltaR_two_objects(x[1],lepton)))
                    if Get_DeltaR_two_objects(FilteredHCand[HDR[0]],event.GenHiggsBoson[0])<0.8:
                        Cat[cat]["HiggsafterTop"].Fill(4)

            #Choose Higgs first by double btag
            Hbbtag = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.bbtag, reverse=True)
            higgsCandidate = Hbbtag[0]

            MatchedHTT = MatchToCand(higgsCandidate,event.HTTV2,dist=0.8)
            FilteredTCand = filter(lambda x: (x != MatchedHTT), event.HTTV2)

            if len(FilteredTCand) > 0:

                Count[cat]["TopAfterHiggs"].Fill(0)

                if len(event.GenHadTop) == 0:
                    continue

                #pT
                Tpt = sorted(FilteredTCand, key=lambda x: x.pt, reverse=True)
                if Get_DeltaR_two_objects(Tpt[0],event.GenHadTop[0]) < 0.8:
                    Cat[cat]["TopAfterHiggs"].Fill(0)
                #Tau21
                Tt32 = sorted(FilteredTCand, key=lambda x: x.tau32, reverse=False)
                if Get_DeltaR_two_objects(Tt32[0],event.GenHadTop[0]) < 0.8:
                    Cat[cat]["TopAfterHiggs"].Fill(7)
                #Mass
                Tmass = min(enumerate(FilteredTCand), key=lambda x: abs(x[1].mass-mtop))
                if Get_DeltaR_two_objects(FilteredTCand[Tmass[0]],event.GenHadTop[0]) < 0.8:
                    Cat[cat]["TopAfterHiggs"].Fill(3)
                #frec
                Tfrec = sorted(FilteredTCand, key=lambda x: x.frec, reverse=False)
                if Get_DeltaR_two_objects(Tfrec[0],event.GenHadTop[0]) < 0.8:
                    Cat[cat]["TopAfterHiggs"].Fill(5)
                #Ropt
                TRopt = sorted(FilteredTCand, key=lambda x: x.delRopt, reverse=False)
                if Get_DeltaR_two_objects(TRopt[0],event.GenHadTop[0]) < 0.8:
                    Cat[cat]["TopAfterHiggs"].Fill(6)
                #DeltaR to lepton
                if event.is_sl:
                    lepton = event.lep_SL[0]
                    TDR = max(enumerate(FilteredTCand), key=lambda x: abs(Get_DeltaR_two_objects(x[1],lepton)))
                    if Get_DeltaR_two_objects(FilteredTCand[TDR[0]],event.GenHadTop[0]) < 0.8:
                        Cat[cat]["TopAfterHiggs"].Fill(4)
                #Btags
                for i in FilteredTCand:
                    Wsubjets = []
                    btag1 = event.HTTV2Subjets[i.subJetIdx1].btag
                    btag2 = event.HTTV2Subjets[i.subJetIdx2].btag
                    btag3 = event.HTTV2Subjets[i.subJetIdx3].btag
                    i.btagF = max(btag1,btag2,btag3)
                    i.btagS = min(btag1,btag2,btag3)
                    if btag1 == max(btag1,btag2,btag3):
                        Wsubjets = [i.subJetIdx2,i.subJetIdx3]
                    elif btag2 == max(btag1,btag2,btag3):
                        Wsubjets = [i.subJetIdx1,i.subJetIdx3]
                    else:
                        Wsubjets = [i.subJetIdx1,i.subJetIdx2]
                    W1 = ROOT.TLorentzVector()
                    W2 = ROOT.TLorentzVector()
                    W1.SetPtEtaPhiM(event.HTTV2Subjets[Wsubjets[0]].pt,event.HTTV2Subjets[Wsubjets[0]].eta,event.HTTV2Subjets[Wsubjets[0]].phi,event.HTTV2Subjets[Wsubjets[0]].mass)
                    W2.SetPtEtaPhiM(event.HTTV2Subjets[Wsubjets[1]].pt,event.HTTV2Subjets[Wsubjets[1]].eta,event.HTTV2Subjets[Wsubjets[1]].phi,event.HTTV2Subjets[Wsubjets[1]].mass)
                    W3 = W1 + W2
                    i.Wmass = W3.M()
                TbtagF = sorted(FilteredTCand, key=lambda x: x.btagF, reverse=True)
                if Get_DeltaR_two_objects(TbtagF[0],event.GenHadTop[0]) < 0.8:
                    Cat[cat]["TopAfterHiggs"].Fill(1)
                #Wmass
                TmassW = min(enumerate(FilteredTCand), key=lambda x: abs(x[1].Wmass-mW))
                if Get_DeltaR_two_objects(FilteredTCand[TmassW[0]],event.GenHadTop[0]) < 0.8:
                    Cat[cat]["TopAfterHiggs"].Fill(2)




results = ROOT.TFile("IdentifierTopHiggs.root","recreate")
for i in cats:
    for j in obj:
        if Count[i][j].GetEntries() > 0:
            Cat[i][j].Scale(1/Count[i][j].GetEntries())
        Cat[i][j].Write()
        Count[i][j].Write()



