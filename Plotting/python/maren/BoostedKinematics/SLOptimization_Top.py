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

class PassingJet:
    def __init__(self, vector, jet):
        self.jet = jet
        self.passes = vector


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
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v
#SKIP_EVENTS = int(os.environ["SKIP_EVENTS"]) 
#MAX_EVENTS = int(os.environ["MAX_EVENTS"]) 



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/chreisse/tth/Apr16/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Apr16/180416_072809/0000/tree_100.root"
#full_file_names["TTH"] = "root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/mameinha/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/BoostedNanoAOD_Feb12/180212_074220/0000/out_1.root"

########################################
# Create histograms, saved in file
########################################

cats = ["sl"]
criteriaT = ["pt","btag1","btag2","bbtag","DRl","mass","softdropmass","tau32","eta","fRec","Ropt","btag3"]
scenarios = ["TCA15","TAK8","THTT"]
options = ["matched","unmatched"]
mtop =  173.21
mHiggs = 125.09
mW = 80.385
mins = [0,0,0,-1,0,0,0,0,-5,0,-5,0]
maxs = [600,1,1,1,5,600,600,1,5,2,5,1]
features = ["S1","B","S2"]
efficiency = ["sig","bkgttH","bkgTT","Tot","TotttH","TotTT"]



nFat = {}
matchedFatjet = {}
Count = {}
Distributions = {}
SBs = {}
eff = {}
drs = {}


for i in cats:
    nFat[i] = {}
    matchedFatjet[i] = {}
    Distributions[i] = {}
    Count[i]= ROOT.TH1F("Count_{}".format(i),"Count_{}".format(i),50,0,600)
    SBs[i] = {}
    eff[i] = {}
    drs[i] = {}
    for j in scenarios:
        nFat[i][j] = ROOT.TH1F("Nfatjets_{}_{}".format(i,j),"Nfatjets_{}_{}".format(i,j),8,0,8)
        matchedFatjet[i][j] = ROOT.TH1F("MatchedFatjet_{}_{}".format(i,j),"MatchedFatjet_{}_{}".format(i,j),50,0,600)
        Distributions[i][j] = {}
        SBs[i][j] = {}
        eff[i][j] = {}
        drs[i][j] = ROOT.TH2F("DR_pt_{}_{}".format(i,j),"DR_pt_{}_{}".format(i,j),50,0,600,20,0,5)
        for l in options: 
            Distributions[i][j][l] = {}
            for m in criteriaT:
                ind = criteriaT.index(m)
                Distributions[i][j][l][m] = ROOT.TH1F("{}_{}_{}_{}".format(i,j,l,m),"{}_{}_{}_{}".format(i,j,l,m),50,mins[ind],maxs[ind])
        for l in features:
            SBs[i][j][l] = {}
            for m in ["btag1","btag2","bbtag"]:               
                SBs[i][j][l][m] = ROOT.TH1F("{}_{}_{}_{}".format(i,j,l,m),"{}_{}_{}_{}".format(i,j,l,m),50,0,50)
        for l in efficiency:
            eff[i][j][l] = {}
            for m in ["btag1","btag2","bbtag"]:               
                eff[i][j][l][m] = ROOT.TH1F("{}_{}_{}_{}".format(i,j,l,m),"{}_{}_{}_{}".format(i,j,l,m),3,0,3)


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

    var = ["mass","tau21","bbtag","btagf","btags"]
    cutpoints = {}
    cutpoints["min"] = {}
    cutpoints["max"] = {}
    cutpoints["min"]["mass"] = [50]
    cutpoints["min"]["tau21"] = [0]
    cutpoints["min"]["bbtag"] = [0.5,0.7]
    cutpoints["min"]["btagf"] = [0.95,0.975]
    cutpoints["min"]["btags"] = [0.7,0.8]

    cutpoints["max"]["mass"] = [600]
    cutpoints["max"]["tau21"] = [0.7,0.8]
    cutpoints["max"]["bbtag"] = [1]
    cutpoints["max"]["btagf"] = [1]
    cutpoints["max"]["btags"] = [1]

    maxlength = 1
    for g in ["min","max"]:
        for h in var:
            maxlength *= len(cutpoints[g][h])

    counter = 0

    #Here matched means Delta R < 0.8 to generated particle or jet or whatever...

    for event in ttree :
        counter += 1
        #if counter > 10000:
        #    break
        #if counter < SKIP_EVENTS:
        #    continue
        #if counter >= MAX_EVENTS+SKIP_EVENTS:
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
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")


        event.FatjetAK8 = filter(lambda x: (x.pt > 300 and abs(x.eta) < 2.4), event.FatjetAK8)
        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15SoftDrop)
        event.HTTV2 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.HTTV2)
        #Fiducial cut on gen Higgs boson
        GenHadTopPt = filter(lambda x: (x.pt > 150 and abs(x.eta) < 2.4), event.GenHadTop)

        GetCategory(event,python_conf)

        #Let's first only consider DL events
        cat = None
        if event.is_sl:
            cat = "sl"
        else:
            continue

        #if len(GenHadTop) == 0:
        #    continue

        nFat["sl"]["TCA15"].Fill(len(event.FatjetCA15SoftDrop),event.Generator_weight) #These are after basic pt, eta cuts!
        nFat["sl"]["TAK8"].Fill(len(event.FatjetAK8),event.Generator_weight) #These are after basic pt, eta cuts!
        nFat["sl"]["THTT"].Fill(len(event.HTTV2),event.Generator_weight)
        if len(event.FatjetAK8) == 0 and len(event.FatjetCA15SoftDrop) == 0 and len(event.HTTV2):
            continue

        event.FatjetCA15SoftDrop = MatchFatjets(event.FatjetCA15SoftDrop,event.FatjetCA15)

        event.HTTV2 = MatchFatjets(event.HTTV2,event.FatjetCA15)


        if len(GenHadTopPt) > 0:
            Count["sl"].Fill(GenHadTopPt[0].pt,event.Generator_weight)


        if len(event.GenHadTop) > 0:
            CA15sorted = sorted(event.FatjetCA15SoftDrop, key = lambda x: Get_DeltaR_two_objects(x,event.GenHadTop[0])) 
            AK8sorted = sorted(event.FatjetAK8, key = lambda x: Get_DeltaR_two_objects(x,event.GenHadTop[0])) 
            HTTsorted = sorted(event.HTTV2, key = lambda x: Get_DeltaR_two_objects(x,event.GenHadTop[0]))
            if len(CA15sorted):
                drs["sl"]["TCA15"].Fill(event.GenHadTop[0].pt, Get_DeltaR_two_objects(CA15sorted[0],event.GenHadTop[0]),event.Generator_weight)
            if len(AK8sorted):
                drs["sl"]["TAK8"].Fill(event.GenHadTop[0].pt, Get_DeltaR_two_objects(AK8sorted[0],event.GenHadTop[0]),event.Generator_weight)
            if len(HTTsorted):
                drs["sl"]["THTT"].Fill(event.GenHadTop[0].pt, Get_DeltaR_two_objects(HTTsorted[0],event.GenHadTop[0]),event.Generator_weight)




        if len(GenHadTopPt) > 0:
            for i in event.FatjetCA15SoftDrop:
                if Get_DeltaR_two_objects(i,GenHadTopPt[0])<1.0:
                    matchedFatjet["sl"]["TCA15"].Fill(GenHadTopPt[0].pt,event.Generator_weight)
                    break

            for i in event.FatjetAK8:
                if Get_DeltaR_two_objects(i,GenHadTopPt[0])<1.0:
                    matchedFatjet["sl"]["TAK8"].Fill(GenHadTopPt[0].pt,event.Generator_weight)
                    break

            for i in event.HTTV2:
                if Get_DeltaR_two_objects(i,GenHadTopPt[0])<1.0:
                    matchedFatjet["sl"]["THTT"].Fill(GenHadTopPt[0].pt,event.Generator_weight)
                    break


        matched = -1
        dist = 10
            
        for i in event.FatjetCA15SoftDrop:
            if len(GenHadTopPt) > 0:
                drH = Get_DeltaR_two_objects(i,GenHadTopPt[0])
            else:
                drH = 10
            if drH < 1.0:
                if matched == -1:
                    i.matched = "matched"
                    matched = event.FatjetCA15SoftDrop.index(i)
                    dist = drH
                else:
                    if drH < dist:
                        event.FatjetCA15SoftDrop[matched].matched = "unmatched"
                        i.matched = "matched"
                        matched = i
                        dist = drH
                    if drH >= dist:
                        i.matched = "unmatched"

                            
            else:
                i.matched = "unmatched"



        #And fill some basic distributions  
        for i in event.FatjetCA15SoftDrop: 
            Distributions["sl"]["TCA15"][i.matched]["pt"].Fill(i.pt,event.Generator_weight)
            Distributions["sl"]["TCA15"][i.matched]["eta"].Fill(i.eta,event.Generator_weight)
            btag1 = event.FatjetCA15SoftDropSubjets[i.subJetIdx1].btag
            btag2 = event.FatjetCA15SoftDropSubjets[i.subJetIdx2].btag
            Distributions["sl"]["TCA15"][i.matched]["btag1"].Fill(max(btag1,btag2),event.Generator_weight)
            Distributions["sl"]["TCA15"][i.matched]["btag2"].Fill(min(btag1,btag2),event.Generator_weight)
            setattr(i,"btagf",max(btag1,btag2))
            setattr(i,"btags",min(btag1,btag2))
            Distributions["sl"]["TCA15"][i.matched]["bbtag"].Fill(i.bbtag,event.Generator_weight)
            MatchedUngroomedFatjet = MatchToCand(i,event.FatjetCA15)
            Distributions["sl"]["TCA15"][i.matched]["mass"].Fill(MatchedUngroomedFatjet.mass,event.Generator_weight)
            Distributions["sl"]["TCA15"][i.matched]["softdropmass"].Fill(i.mass,event.Generator_weight)
            Distributions["sl"]["TCA15"][i.matched]["tau32"].Fill(i.tau32,event.Generator_weight)
            setattr(i,"msoftdrop",i.mass)
            Distributions["sl"]["TCA15"][i.matched]["DRl"].Fill(Get_DeltaR_two_objects(i,event.lep_SL[0]),event.Generator_weight)


        #AK8 jets now
        matched = -1
        dist = 10

            
        for i in event.FatjetAK8:
            if len(GenHadTopPt) > 0:
                drH = Get_DeltaR_two_objects(i,GenHadTopPt[0])
            else:
                drH = 10
            if drH < 1.0:
                if matched == -1:
                    i.matched = "matched"
                    matched = event.FatjetAK8.index(i)
                    dist = drH
                else:
                    if drH < dist:
                        event.FatjetAK8[matched].matched = "unmatched"
                        i.matched = "matched"
                        matched = i
                        dist = drH
                    if drH >= dist:
                        i.matched = "unmatched"

                            
            else:
                i.matched = "unmatched"



        #And fill some basic distributions  
        for i in event.FatjetAK8: 
            Distributions["sl"]["TAK8"][i.matched]["pt"].Fill(i.pt,event.Generator_weight)
            Distributions["sl"]["TAK8"][i.matched]["eta"].Fill(i.eta,event.Generator_weight)
            btag1 = event.FatjetAK8Subjets[i.subJetIdx1].btag
            btag2 = event.FatjetAK8Subjets[i.subJetIdx2].btag
            Distributions["sl"]["TAK8"][i.matched]["btag1"].Fill(max(btag1,btag2),event.Generator_weight)
            Distributions["sl"]["TAK8"][i.matched]["btag2"].Fill(min(btag1,btag2),event.Generator_weight)
            setattr(i,"btagf",max(btag1,btag2))
            setattr(i,"btags",min(btag1,btag2))
            Distributions["sl"]["TAK8"][i.matched]["bbtag"].Fill(i.bbtag,event.Generator_weight)
            Distributions["sl"]["TAK8"][i.matched]["mass"].Fill(i.mass,event.Generator_weight)
            Distributions["sl"]["TAK8"][i.matched]["softdropmass"].Fill(i.msoftdrop,event.Generator_weight)
            Distributions["sl"]["TAK8"][i.matched]["tau32"].Fill(i.tau32,event.Generator_weight)
            Distributions["sl"]["TAK8"][i.matched]["DRl"].Fill(Get_DeltaR_two_objects(i,event.lep_SL[0]),event.Generator_weight)


        #HTTV2 jets now
        matched = -1
        dist = 10

            
        for i in event.HTTV2:
            if len(GenHadTopPt) > 0:
                drH = Get_DeltaR_two_objects(i,GenHadTopPt[0])
            else:
                drH = 10
            if drH < 1.0:
                if matched == -1:
                    i.matched = "matched"
                    matched = event.HTTV2.index(i)
                    dist = drH
                else:
                    if drH < dist:
                        event.HTTV2[matched].matched = "unmatched"
                        i.matched = "matched"
                        matched = i
                        dist = drH
                    if drH >= dist:
                        i.matched = "unmatched"

                            
            else:
                i.matched = "unmatched"



        #And fill some basic distributions  
        for i in event.HTTV2: 
            Distributions["sl"]["THTT"][i.matched]["pt"].Fill(i.pt,event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["eta"].Fill(i.eta,event.Generator_weight)
            btag1 = event.HTTV2Subjets[i.subJetIdx1].btag
            btag2 = event.HTTV2Subjets[i.subJetIdx2].btag
            btag3 = event.HTTV2Subjets[i.subJetIdx3].btag
            li = [btag1,btag2,btag3]
            li = sorted(li)
            setattr(i,"btagf",li[2])
            setattr(i,"btags",li[1])
            setattr(i,"btagl",li[0])
            Distributions["sl"]["THTT"][i.matched]["btag1"].Fill(i.btagf,event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["btag2"].Fill(i.btags,event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["btag3"].Fill(i.btagl,event.Generator_weight)
            #Distributions["sl"]["THTT"][i.matched]["bbtag"].Fill(i.bbtag,event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["mass"].Fill(i.mass,event.Generator_weight)
            #Distributions["sl"]["THTT"][i.matched]["softdropmass"].Fill(i.msoftdrop,event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["tau32"].Fill(i.tau32,event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["DRl"].Fill(Get_DeltaR_two_objects(i,event.lep_SL[0]),event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["fRec"].Fill(i.fRec,event.Generator_weight)
            Distributions["sl"]["THTT"][i.matched]["Ropt"].Fill(i.Ropt-i.RoptCalc,event.Generator_weight)

results = ROOT.TFile("SLOptimization_Top.root","recreate")
for i in cats:
    Count[i].Write()
    for j in scenarios:
        nFat[i][j].Write()
        matchedFatjet[i][j].Write()
        drs[i][j].Write()
        for l in options: 
            for m in criteriaT:
                ind = criteriaT.index(m)
                Distributions[i][j][l][m].Write()
        for l in features:
            for m in ["btag1","btag2","bbtag"]:               
                SBs[i][j][l][m].Write()
        for l in efficiency:
            for m in ["btag1","btag2","bbtag"]:               
                eff[i][j][l][m].Write()
