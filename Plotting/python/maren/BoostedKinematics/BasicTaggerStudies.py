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
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf

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
            self.tau31 = self.tau3 / self.tau2 if self.tau2 > 0.0 else 0.0  
            self.msoftdrop = getattr(tree,"{}_msoftdrop".format(name))[n]
        pass
    @staticmethod
    def make_array(input,name):
        return [JetCollection(input, i, name) for i in range(getattr(input,"n{}".format(name)))]

def MatchFatjets(objs,jets):

    # Loosely match the fatjets to the tops
    n_matched_fatjet = Match_two_lists(
        objs, 'objs',
        jets, 'fatjet',
        R_cut = 1.5 )

    # New list of tops after n_subjettiness cut is applied
    obj_with_info = []

    for o in objs:

        # Skip unmatched tops
        if not hasattr( o, 'matched_fatjet' ):
            for i in jets:
                print Get_DeltaR_two_objects(o,i)
            print 'Warning: Candidate unmatchable to fatjet!'
            continue

        fatjet = o.matched_fatjet

        # Get n_subjettiness from the matched fatjet
        tau32 = fatjet.tau3 / fatjet.tau2 if fatjet.tau2 > 0.0 else 0.0 
        tau21 = fatjet.tau2 / fatjet.tau1 if fatjet.tau1 > 0.0 else 0.0 
        tau31 = fatjet.tau3 / fatjet.tau1 if fatjet.tau1 > 0.0 else 0.0 

        # Set n_subjettiness, tau_N and the bbtag
        o.tau32 = tau32
        o.tau21 = tau21
        o.tau31 = tau31
        o.tau1 = fatjet.tau1
        o.tau2 = fatjet.tau2
        o.tau3 = fatjet.tau3
        
        o.bbtag = fatjet.bbtag

        o.ungroomedMass = fatjet.mass

        # Calculate delRopt
        if hasattr(o, 'Ropt'):
            o.delRopt = o.Ropt - o.RoptCalc

        # Append the httCandidate class to the list
        obj_with_info.append(o)

    return obj_with_info

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



#Define DL. Only considers leptons, not jets.
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

cats = ["sl","dl"]
variables = ["pt","eta","btag1","btag2","btag3","bbtag","DRl","mass","softdropmass","tau32","tau21","tau31","fRec","Ropt"]
jettype = ["CA15","AK8","HTT","AK4","AK4b","AK4woFJ","AK4woFJb","AK4woSJ","AK4woSJb"]
scenarios = ["matchedT","matchedH","unmatched","all"]
mtop =  173.21
mHiggs = 125.09
mW = 80.385
mins = [0,-5,0,0,0,-1,0,0,0,0,0,0,0,-5]
maxs = [600,5,1,1,1,1,5,600,600,1,1,1,5,5]



nJet = {}
matchedJet = {}
Count = {}
Distributions = {}


for i in cats:
    nJet[i] = {}
    matchedJet[i] = {}
    Distributions[i] = {}
    Count[i]= ROOT.TH1F("Count_{}".format(i),"Count_{}".format(i),50,0,600)
    for j in jettype:
        nJet[i][j] = ROOT.TH1F("nJet_{}_{}".format(i,j),"nJet_{}_{}".format(i,j),30,0,30)
        matchedJet[i][j] = ROOT.TH1F("MatchedJet_{}_{}".format(i,j),"MatchedJet_{}_{}".format(i,j),50,0,600)
        Distributions[i][j] = {}
        for l in scenarios: 
            Distributions[i][j][l] = {}
            for m in variables:
                ind = variables.index(m)
                Distributions[i][j][l][m] = ROOT.TH1F("Distribution_{}_{}_{}_{}".format(i,j,l,m),"{}_{}_{}_{}".format(i,j,l,m),50,mins[ind],maxs[ind])


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
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        event.Jet = nanoTreeClasses.Jet.make_array(ttree, MC = True)

        event.FatjetCA15SoftDrop = MatchFatjets(event.FatjetCA15SoftDrop,event.FatjetCA15)
        event.HTTV2 = MatchFatjets(event.HTTV2,event.FatjetCA15)

        GetCategory(event,python_conf)

        #Let's first only consider DL events
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue

        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenHadW = filter(lambda x: (x.decayMode==1), event.GenWBoson)



        #Do all the matching here for all objects and fatjets

        matched_objectsCA15 = Match_two_lists(
            event.GenHiggsBoson, 'genHiggs_CA15',
            event.FatjetCA15SoftDrop, 'jetCA15',0.5)

        matched_objectsCA15 = Match_two_lists(
            event.GenTop, 'genTop_CA15',
            event.FatjetCA15SoftDrop, 'jetCA15',0.5)

        matched_objectsAK8 = Match_two_lists(
            event.GenHiggsBoson, 'genHiggs_AK8',
            event.FatjetAK8, 'jet_AK8',0.5)

        matched_objectsAK8 = Match_two_lists(
            event.GenTop, 'genTop_AK8',
            event.FatjetAK8, 'jet_AK8',0.5)

        matched_objectsHTT = Match_two_lists(
            event.GenHadTop, 'genTop_HTT',
            event.HTTV2, 'jet_HTT',0.5)

        for t in ["CA15","AK8"]:
            for i in event.GenHiggsBoson:
                if hasattr(i,"matched_jet_{}".format(t)):
                    s = getattr(i,"matched_jet_{}".format(t))
                    if getattr(s,"subJetIdx1") < 0 or getattr(s,"subJetIdx2") < 0:
                        continue
                    if t == "CA15":
                        subs = [event.FatjetCA15SoftDropSubjets[getattr(s,"subJetIdx1")], \
                        event.FatjetCA15SoftDropSubjets[getattr(s,"subJetIdx2")]]
                    elif t == "AK8":
                        subs = [event.FatjetAK8Subjets[getattr(s,"subJetIdx1")], \
                        event.FatjetAK8Subjets[getattr(s,"subJetIdx2")]]
                    matched_subjets = Match_two_lists(
                    event.GenBQuarkFromH, "quark_{}".format(t),
                    subs, "subjet_{}".format(t),0.3)
                    cnt = 1
                    for j in event.GenBQuarkFromH:
                        if hasattr(j,"matched_subjet_{}".format(t)):
                            setattr(i,"matched_subjet{}_{}".format(cnt,1),getattr(j,"matched_subjet_{}".format(t)))
                            cnt += 1

            for i in event.GenTop:
                if hasattr(i,"matched_jet_{}".format(t)):
                    s = getattr(i,"matched_jet_{}".format(t))
                    if getattr(s,"subJetIdx1") < 0 or getattr(s,"subJetIdx2") < 0:
                        continue
                    if t == "CA15":
                        subs = [event.FatjetCA15SoftDropSubjets[getattr(s,"subJetIdx1")], \
                        event.FatjetCA15SoftDropSubjets[getattr(s,"subJetIdx2")]]
                    elif t == "AK8":
                        subs = [event.FatjetAK8Subjets[getattr(s,"subJetIdx1")], \
                        event.FatjetAK8Subjets[getattr(s,"subJetIdx2")]]
                    subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,i))[:2]
                    bs = sorted(event.GenBQuarkFromTop, key = lambda x: Get_DeltaR_two_objects(x,i))[:1]
                    matched_subjets = Match_two_lists(
                    subj+bs, "quark_{}".format(t),
                    subs, "subjet_{}".format(t),0.3)
                    cnt = 1
                    for j in subj+bs:
                        if hasattr(j,"matched_subjet_{}".format(t)):
                            setattr(i,"matched_subjet{}_{}".format(cnt,1),getattr(j,"matched_subjet_{}".format(t)))
                            cnt += 1

        for i in event.GenTop:
            if hasattr(i,"matched_jet_HTT"):
                s = getattr(i,"matched_jet_HTT")
                subs = [event.HTTV2Subjets[getattr(s,"subJetIdx1")], \
                    event.HTTV2Subjets[getattr(s,"subJetIdx2")], \
                    event.HTTV2Subjets[getattr(s,"subJetIdx3")]]
                subj = sorted(event.GenWZQuark, key = lambda x: Get_DeltaR_two_objects(x,i))[:2]
                bs = sorted(event.GenBQuarkFromTop, key = lambda x: Get_DeltaR_two_objects(x,i))[:1]
                matched_subjets = Match_two_lists(
                subj+bs, "quark_{}".format(t),
                subs, "subjet_{}".format(t),0.3)
                cnt = 1
                for j in subj+bs:
                    if hasattr(j,"matched_subjet_{}".format(t)):
                        setattr(i,"matched_subjet{}_{}".format(cnt,1),getattr(j,"matched_subjet_{}".format(t)))
                        cnt += 1


        #Fiducial cut on generator level objects
        GenHadTopPt = filter(lambda x: (x.pt > 150 and abs(x.eta) < 2.4), event.GenHadTop)
        GenHiggsBosonPt = filter(lambda x: (x.pt > 150 and abs(x.eta) < 2.4), event.GenHiggsBoson)


        #Now do the actual code

        fatjets_to_match = event.HTTV2 + event.FatjetCA15SoftDrop + event.FatjetAK8
        matched_objects = Match_two_lists(
            event.Jet, 'AK4jet',
            fatjets_to_match, 'Fatjet',1.0)

        subjets_to_match = event.HTTV2Subjets + event.FatjetCA15SoftDropSubjets + event.FatjetAK8Subjets
        matched_objects2 = Match_two_lists(
            event.Jet, 'AK4jet',
            subjets_to_match, 'Subjet',0.3)

        event.JetB = filter(lambda x: (x.btagDeepCSV>0.4941), event.Jet)

        isolatedAK4 = filter(lambda x: (not hasattr(x,"matched_Fatjet")), event.Jet)
        isolatedAK4B = filter(lambda x: (not hasattr(x,"matched_Fatjet")), event.JetB)

        isolatedAK4bis = filter(lambda x: (not hasattr(x,"matched_Subjet")), event.Jet)
        isolatedAK4Bbis = filter(lambda x: (not hasattr(x,"matched_Subjet")), event.JetB)

        nJet[cat]["CA15"].Fill(len(event.FatjetCA15SoftDrop))
        nJet[cat]["AK8"].Fill(len(event.FatjetAK8))
        nJet[cat]["HTT"].Fill(len(event.HTTV2))
        nJet[cat]["AK4"].Fill(len(event.Jet))
        nJet[cat]["AK4b"].Fill(len(event.JetB))
        nJet[cat]["AK4woFJ"].Fill(len(isolatedAK4))
        nJet[cat]["AK4woFJb"].Fill(len(isolatedAK4B))
        nJet[cat]["AK4woSJ"].Fill(len(isolatedAK4bis))
        nJet[cat]["AK4woSJb"].Fill(len(isolatedAK4Bbis))

        #Now get the distributions
        for i in event.FatjetCA15SoftDrop: 
            match = None
            if hasattr(i,"matched_genHiggs_CA15"):
                match = "matchedH"
            elif hasattr(i,"matched_genTop_CA15"):
                match = "matchedT"
            else:
                match = "unmatched"
            for plots in [match, "all"]:
                Distributions[cat]["CA15"][plots]["pt"].Fill(i.pt,event.Generator_weight)
                Distributions[cat]["CA15"][plots]["eta"].Fill(i.eta,event.Generator_weight)
                btag1 = event.FatjetCA15SoftDropSubjets[i.subJetIdx1].btag
                btag2 = event.FatjetCA15SoftDropSubjets[i.subJetIdx2].btag
                Distributions[cat]["CA15"][plots]["btag1"].Fill(max(btag1,btag2),event.Generator_weight)
                Distributions[cat]["CA15"][plots]["btag2"].Fill(min(btag1,btag2),event.Generator_weight)
                setattr(i,"btagf",max(btag1,btag2))
                setattr(i,"btags",min(btag1,btag2))
                Distributions[cat]["CA15"][plots]["bbtag"].Fill(i.bbtag,event.Generator_weight)
                Distributions[cat]["CA15"][plots]["mass"].Fill(i.ungroomedMass,event.Generator_weight)
                Distributions[cat]["CA15"][plots]["softdropmass"].Fill(i.mass,event.Generator_weight)
                Distributions[cat]["CA15"][plots]["tau32"].Fill(i.tau32,event.Generator_weight)
                Distributions[cat]["CA15"][plots]["tau21"].Fill(i.tau21,event.Generator_weight)
                Distributions[cat]["CA15"][plots]["tau31"].Fill(i.tau31,event.Generator_weight)
                setattr(i,"msoftdrop",i.mass)
                if cat == "sl":
                    Distributions[cat]["CA15"][plots]["DRl"].Fill(Get_DeltaR_two_objects(i,event.lep_SL[0]),event.Generator_weight)


        for i in event.FatjetAK8: 
            match = None
            if hasattr(i,"matched_genHiggs_AK8"):
                match = "matchedH"
            elif hasattr(i,"matched_genTop_AK8"):
                match = "matchedT"
            else:
                match = "unmatched"
            for plots in [match, "all"]:
                Distributions[cat]["AK8"][plots]["pt"].Fill(i.pt,event.Generator_weight)
                Distributions[cat]["AK8"][plots]["eta"].Fill(i.eta,event.Generator_weight)
                if i.subJetIdx1 >= 0 and i.subJetIdx2 >= 0:
                    btag1 = event.FatjetAK8Subjets[i.subJetIdx1].btag
                    btag2 = event.FatjetAK8Subjets[i.subJetIdx2].btag
                    Distributions[cat]["AK8"][plots]["btag1"].Fill(max(btag1,btag2),event.Generator_weight)
                    Distributions[cat]["AK8"][plots]["btag2"].Fill(min(btag1,btag2),event.Generator_weight)
                    setattr(i,"btagf",max(btag1,btag2))
                    setattr(i,"btags",min(btag1,btag2))
                Distributions[cat]["AK8"][plots]["bbtag"].Fill(i.bbtag,event.Generator_weight)
                Distributions[cat]["AK8"][plots]["mass"].Fill(i.mass,event.Generator_weight)
                Distributions[cat]["AK8"][plots]["softdropmass"].Fill(i.msoftdrop,event.Generator_weight)
                Distributions[cat]["AK8"][plots]["tau32"].Fill(i.tau32,event.Generator_weight)
                Distributions[cat]["AK8"][plots]["tau21"].Fill(i.tau21,event.Generator_weight)
                Distributions[cat]["AK8"][plots]["tau31"].Fill(i.tau31,event.Generator_weight)
                if cat == "sl":
                    Distributions[cat]["AK8"][plots]["DRl"].Fill(Get_DeltaR_two_objects(i,event.lep_SL[0]),event.Generator_weight)

        for i in event.HTTV2: 
            match = None
            if hasattr(i,"matched_genTop_HTT"):
                match = "matchedT"
            else:
                match = "unmatched"
            for plots in [match, "all"]:
                Distributions[cat]["HTT"][plots]["pt"].Fill(i.pt,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["eta"].Fill(i.eta,event.Generator_weight)
                btag1 = event.HTTV2Subjets[i.subJetIdx1].btag
                btag2 = event.HTTV2Subjets[i.subJetIdx2].btag
                btag3 = event.HTTV2Subjets[i.subJetIdx3].btag
                li = [btag1,btag2,btag3]
                li = sorted(li)
                setattr(i,"btagf",li[2])
                setattr(i,"btags",li[1])
                setattr(i,"btagl",li[0])
                Distributions[cat]["HTT"][plots]["btag1"].Fill(i.btagf,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["btag2"].Fill(i.btags,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["btag3"].Fill(i.btagl,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["bbtag"].Fill(i.bbtag,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["mass"].Fill(i.mass,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["tau32"].Fill(i.tau32,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["tau21"].Fill(i.tau21,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["tau31"].Fill(i.tau31,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["fRec"].Fill(i.fRec,event.Generator_weight)
                Distributions[cat]["HTT"][plots]["Ropt"].Fill(i.Ropt-i.RoptCalc,event.Generator_weight)
                if cat == "sl":
                    Distributions[cat]["HTT"][plots]["DRl"].Fill(Get_DeltaR_two_objects(i,event.lep_SL[0]),event.Generator_weight)

        for i in event.Jet: 
            for plots in ["all"]:
                Distributions[cat]["AK4"][plots]["pt"].Fill(i.pt,event.Generator_weight)
                Distributions[cat]["AK4"][plots]["eta"].Fill(i.eta,event.Generator_weight)
                Distributions[cat]["AK4"][plots]["btag1"].Fill(i.btagDeepCSV,event.Generator_weight)
                Distributions[cat]["AK4"][plots]["mass"].Fill(i.mass,event.Generator_weight)

        for i in event.JetB: 
            for plots in ["all"]:
                Distributions[cat]["AK4b"][plots]["pt"].Fill(i.pt,event.Generator_weight)
                Distributions[cat]["AK4b"][plots]["eta"].Fill(i.eta,event.Generator_weight)
                Distributions[cat]["AK4b"][plots]["btag1"].Fill(i.btagDeepCSV,event.Generator_weight)
                Distributions[cat]["AK4b"][plots]["mass"].Fill(i.mass,event.Generator_weight)
 
 
results = ROOT.TFile("BasicTaggerStudies.root","recreate")
for i in cats:
    Count[i].Write()
    for j in jettype:
        nJet[i][j].Write()
        matchedJet[i][j].Write()
        for l in scenarios: 
            for m in variables:
                ind = variables.index(m)
                Distributions[i][j][l][m].Write()


