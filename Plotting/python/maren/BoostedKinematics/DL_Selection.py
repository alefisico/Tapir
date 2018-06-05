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

cats = ["dl"]
criteriaT = ["pt","btag","Wmass","Tmass","DRl","frec","Ropt","tau32"]
criteriaH = ["pt","btag1","btag2","bbtag","DRl","mass","softdropmass","tau21"]
scenarios = ["Hsl","Hdl","Tsl","HTsl","THsl"]
obj = ["Higgs","Top","HiggsAK8"]
nfatjets = ["One","More"]
options = ["matched","unmatched"]
mtop =  173.21
mHiggs = 125.09
mW = 80.385
mins = [0,0,0,-1,0,0,0,0]
maxs = [600,1,1,1,5,600,600,1]


Cat = {}
Count = {}
nFat = {}
Distributions = {}

for i in cats:
    Cat[i] = {}
    Count[i] = {}
    nFat[i] = {}
    Distributions[i] = {}
    for j in obj:
        Cat[i][j] = {}
        Count[i][j] = {}
        nFat[i][j] = ROOT.TH1F("Nfatjets_{}_{}".format(i,j),"Nfatjets_{}_{}".format(i,j),8,0,8)
        Distributions[i][j] = {}
        for k in nfatjets: 
            Cat[i][j][k] = ROOT.TH1F("{}_{}_{}fatjet".format(i,j,k),"{}_{}_{}fatjet".format(i,j,k),8,0,8)
            for m in range(1,9):
                if "Higgs" in j:
                    Cat[i][j][k].GetXaxis().SetBinLabel(m,criteriaH[m-1])
                else:
                    Cat[i][j][k].GetXaxis().SetBinLabel(m,criteriaT[m-1])
            Count[i][j][k] = ROOT.TH1F("Count{}_{}_{}fatjet".format(i,j,k),"{}_{}_{}fatjet".format(i,j,k),1,0,1)
            Distributions[i][j][k] = {}
            for l in options: 
                Distributions[i][j][k][l] = {}
                for m in criteriaH:
                    ind = criteriaH.index(m)
                    Distributions[i][j][k][l][m] = ROOT.TH1F("{}_{}_{}fatjet_{}_{}".format(i,j,k,l,m),"{}_{}_{}fatjet_{}_{}".format(i,j,k,l,m),50,mins[ind],maxs[ind])


########################################
# Run code
########################################

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("Events")

    counter = 0

    #Here matched means Delta R < 0.8 to generated particle or jet or whatever...

    for event in ttree :
        if counter == 30000:
            break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event
        counter += 1

        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenLepTop = filter(lambda x: (x.decayMode==0), event.GenTop)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")

        event.FatjetAK8 = filter(lambda x: (x.pt > 300 and abs(x.eta) < 2.4), event.FatjetAK8)
        event.HTTV2 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.HTTV2)
        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15SoftDrop)

        event.FatjetCA15SoftDrop = MatchFatjets(event.FatjetCA15SoftDrop,event.FatjetCA15)
        event.HTTV2 = MatchFatjets(event.HTTV2,event.FatjetCA15)

        GetCategory(event,python_conf)

        #Let's first only consider DL events
        cat = None
        if event.is_dl:
            cat = "dl"
        else:
            continue

        nFat["dl"]["Higgs"].Fill(len(event.FatjetCA15SoftDrop)) #These are after basic pt, eta cuts!
        nFat["dl"]["HiggsAK8"].Fill(len(event.FatjetAK8)) #These are after basic pt, eta cuts!
        nFat["dl"]["Top"].Fill(len(event.HTTV2)) #These are after basic pt, eta cuts!

        if len(event.FatjetCA15SoftDrop) == 0 and len(event.FatjetAK8) == 0:
            continue

        #Which other criteria should the event satisfy?
        #Let's just go with sl selection, no requirement on 
        #number of jets because we want to be as inclusive as possible
        #Maybe add later on that we want at least two other BCSVM jets?


        #Check matching when only one fatjet. Also plot some distributions for correctly and uncorrectly matched.
        if len(event.FatjetCA15SoftDrop) == 1:
            Count["dl"]["Higgs"]["One"].Fill(0)
            drH = Get_DeltaR_two_objects(event.FatjetCA15SoftDrop[0],event.GenHiggsBoson[0])
            matched = "unmatched"
            if drH < 0.8:
                matched = "matched"
                for i in range (0,9):
                    Cat["dl"]["Higgs"]["One"].Fill(i)

            #And fill some basic distributions      
            Distributions["dl"]["Higgs"]["One"][matched]["pt"].Fill(event.FatjetCA15SoftDrop[0].pt)
            btag1 = event.FatjetCA15SoftDropSubjets[event.FatjetCA15SoftDrop[0].subJetIdx1].btag
            btag2 = event.FatjetCA15SoftDropSubjets[event.FatjetCA15SoftDrop[0].subJetIdx2].btag
            Distributions["dl"]["Higgs"]["One"][matched]["btag1"].Fill(max(btag1,btag2))
            Distributions["dl"]["Higgs"]["One"][matched]["btag2"].Fill(min(btag1,btag2))
            Distributions["dl"]["Higgs"]["One"][matched]["bbtag"].Fill(event.FatjetCA15SoftDrop[0].bbtag)
            MatchedUngroomedFatjet = MatchToCand(event.FatjetCA15SoftDrop[0],event.FatjetCA15)
            Distributions["dl"]["Higgs"]["One"][matched]["mass"].Fill(MatchedUngroomedFatjet.mass)
            Distributions["dl"]["Higgs"]["One"][matched]["softdropmass"].Fill(event.FatjetCA15SoftDrop[0].mass)
            Distributions["dl"]["Higgs"]["One"][matched]["tau21"].Fill(event.FatjetCA15SoftDrop[0].tau21)

        if len(event.FatjetAK8) == 1:
            Count["dl"]["HiggsAK8"]["One"].Fill(0)
            drH = Get_DeltaR_two_objects(event.FatjetAK8[0],event.GenHiggsBoson[0])
            matched = "unmatched"
            if drH < 0.8:
                matched = "matched"
                for i in range (0,9):
                    Cat["dl"]["HiggsAK8"]["One"].Fill(i)

            #And fill some basic distributions      
            Distributions["dl"]["HiggsAK8"]["One"][matched]["pt"].Fill(event.FatjetAK8[0].pt)
            Distributions["dl"]["HiggsAK8"]["One"][matched]["bbtag"].Fill(event.FatjetAK8[0].bbtag)
            Distributions["dl"]["HiggsAK8"]["One"][matched]["mass"].Fill(MatchedUngroomedFatjet.mass)
            Distributions["dl"]["HiggsAK8"]["One"][matched]["softdropmass"].Fill(event.FatjetAK8[0].msoftdrop)
            Distributions["dl"]["HiggsAK8"]["One"][matched]["tau21"].Fill(event.FatjetAK8[0].tau21)


        #Check now what happens when there is more than one fatjet
        if len(event.FatjetCA15SoftDrop) > 1:
            Count["dl"]["Higgs"]["More"].Fill(0)

            matched = -1
            dist = 10
            for i in event.FatjetCA15SoftDrop:
                drH = Get_DeltaR_two_objects(i,event.GenHiggsBoson[0])
                if drH < 0.8:
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

            #pT
            Hpt = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.pt, reverse=True)
            if Hpt[0].matched == "matched":
                Cat[cat]["Higgs"]["More"].Fill(0)
            #Btags
            for i in event.FatjetCA15SoftDrop:
                btag1 = event.FatjetCA15SoftDropSubjets[i.subJetIdx1].btag
                btag2 = event.FatjetCA15SoftDropSubjets[i.subJetIdx2].btag
                i.btagF = max(btag1,btag2)
                i.btagS = min(btag1,btag2)
            HbtagF = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.btagF, reverse=True)
            if HbtagF[0].matched == "matched":
                Cat[cat]["Higgs"]["More"].Fill(1)
            HbtagS = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.btagS, reverse=True)
            if HbtagS[0].matched == "matched":
                Cat[cat]["Higgs"]["More"].Fill(2)
            #bbtag
            Hbbtag = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.bbtag, reverse=True)
            if Hbbtag[0].matched == "matched":
                Cat[cat]["Higgs"]["More"].Fill(3)
            #Mass
            Hmass = min(enumerate(event.FatjetCA15), key=lambda x: abs(x[1].mass-mHiggs))
            MatchedFatjet = MatchToCand(event.FatjetCA15[Hmass[0]],event.FatjetCA15SoftDrop)
            if MatchedFatjet is not None and MatchedFatjet.matched == "matched":
                Cat[cat]["Higgs"]["More"].Fill(5)
            #Mass softdrop
            HmassSD = min(enumerate(event.FatjetCA15SoftDrop), key=lambda x: abs(x[1].mass-mHiggs))
            if event.FatjetCA15SoftDrop[HmassSD[0]].matched == "matched":
                Cat[cat]["Higgs"]["More"].Fill(6)
            #Tau21
            Ht21 = sorted(event.FatjetCA15SoftDrop, key=lambda x: x.tau21, reverse=False)
            if Ht21[0].matched == "matched":
                Cat[cat]["Higgs"]["More"].Fill(7)


            #And fill some basic distributions  
            for i in event.FatjetCA15SoftDrop:    
                Distributions["dl"]["Higgs"]["More"][i.matched]["pt"].Fill(i.pt)
                btag1 = event.FatjetCA15SoftDropSubjets[i.subJetIdx1].btag
                btag2 = event.FatjetCA15SoftDropSubjets[i.subJetIdx2].btag
                Distributions["dl"]["Higgs"]["More"][i.matched]["btag1"].Fill(max(btag1,btag2))
                Distributions["dl"]["Higgs"]["More"][i.matched]["btag2"].Fill(min(btag1,btag2))
                Distributions["dl"]["Higgs"]["More"][i.matched]["bbtag"].Fill(i.bbtag)
                MatchedUngroomedFatjet = MatchToCand(i,event.FatjetCA15)
                Distributions["dl"]["Higgs"]["More"][i.matched]["mass"].Fill(MatchedUngroomedFatjet.mass)
                Distributions["dl"]["Higgs"]["More"][i.matched]["softdropmass"].Fill(i.mass)
                Distributions["dl"]["Higgs"]["More"][i.matched]["tau21"].Fill(i.tau21)


        if len(event.FatjetAK8) > 1:
            Count["dl"]["HiggsAK8"]["More"].Fill(0)

            matched = -1
            dist = 10
            for i in event.FatjetAK8:
                drH = Get_DeltaR_two_objects(i,event.GenHiggsBoson[0])
                if drH < 0.8:
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

            #pT
            Hpt = sorted(event.FatjetAK8, key=lambda x: x.pt, reverse=True)
            if Hpt[0].matched == "matched":
                Cat[cat]["HiggsAK8"]["More"].Fill(0)
            #bbtag
            Hbbtag = sorted(event.FatjetAK8, key=lambda x: x.bbtag, reverse=True)
            if Hbbtag[0].matched == "matched":
                Cat[cat]["HiggsAK8"]["More"].Fill(3)
            #Mass
            Hmass = min(enumerate(event.FatjetAK8), key=lambda x: abs(x[1].mass-mHiggs))
            if Hmass[1].matched == "matched":
                Cat[cat]["HiggsAK8"]["More"].Fill(5)
            #Mass softdrop
            HmassSD = min(enumerate(event.FatjetAK8), key=lambda x: abs(x[1].msoftdrop-mHiggs))
            if HmassSD[1].matched == "matched":
                Cat[cat]["HiggsAK8"]["More"].Fill(6)
            #Tau21
            Ht21 = sorted(event.FatjetAK8, key=lambda x: x.tau21, reverse=False)
            if Ht21[0].matched == "matched":
                Cat[cat]["HiggsAK8"]["More"].Fill(7)


            #And fill some basic distributions  
            for i in event.FatjetAK8:    
                Distributions["dl"]["HiggsAK8"]["More"][i.matched]["pt"].Fill(i.pt)
                btag1 = event.FatjetAK8Subjets[i.subJetIdx1].btag
                btag2 = event.FatjetAK8Subjets[i.subJetIdx2].btag
                Distributions["dl"]["HiggsAK8"]["More"][i.matched]["btag1"].Fill(max(btag1,btag2))
                Distributions["dl"]["HiggsAK8"]["More"][i.matched]["btag2"].Fill(min(btag1,btag2))
                Distributions["dl"]["HiggsAK8"]["More"][i.matched]["bbtag"].Fill(i.bbtag)
                Distributions["dl"]["HiggsAK8"]["More"][i.matched]["mass"].Fill(i.mass)
                Distributions["dl"]["HiggsAK8"]["More"][i.matched]["softdropmass"].Fill(i.msoftdrop)
                Distributions["dl"]["HiggsAK8"]["More"][i.matched]["tau21"].Fill(i.tau21)




results = ROOT.TFile("DL_Selection.root","recreate")
for i in cats:
    for j in obj:
        nFat[i][j].Write()
        for k in nfatjets: 
            if Count[i][j][k].GetEntries() > 0:
                Cat[i][j][k].Scale(1./Count[i][j][k].GetEntries())
            Cat[i][j][k].Write()
            Count[i][j][k].Write()
            for l in options: 
                for m in criteriaH:
                    Distributions[i][j][k][l][m].Write()
