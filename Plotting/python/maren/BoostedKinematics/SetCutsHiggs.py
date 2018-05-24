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
            self.tau21 = self.tau2 / self.tau1 if self.tau1 > 0.0 else 0.0
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
#fn = os.environ['FILE_NAMES'].split(' ')
#for v in fn:
#    full_file_names[v] = v

#full_file_names = {}
#full_file_names["v"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/chreisse/tth/Apr16/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Apr16/180416_072654/0000/tree_100.root"
full_file_names["v"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/chreisse/tth/Apr16/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Apr16/180416_072809/0000/tree_100.root"


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

tau21 = [200,1000,50]
bbtag = [0,1000,50]
btag2 = [0,1000,50]


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
        if counter > 1000:
            break


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


        #genobt_to_match = event.GenHiggsBoson+event.GenHiggsBoson+event.GenWBoson

        matched_fatjet = Match_two_lists(
            event.FatjetCA15SoftDrop, 'CA15SD',
            event.FatjetCA15, 'CA15',0.5)

        matched_fatjet = Match_two_lists(
            event.GenHiggsBoson, 'Higgs',
            event.FatjetCA15, 'CA15',0.5)

        

        #Do all the matching here for all objects and fatjets
        """for i in event.GenHiggsBoson:
            if hasattr(i,"matched_CA15"):
                if hasattr(getattr(i,"matched_CA15"),"matched_CA15SD"):
                    setattr(event.GenHiggsBoson,"matched_CA15SD",getattr(i,"matched_CA15"))"""

        #Now do the actual code
        for jet in event.FatjetCA15:
            if hasattr(jet,"matched_CA15SD"):
                btagSL = min(event.FatjetCA15SoftDropSubjets[jet.matched_CA15SD.subJetIdx1].btag,event.FatjetCA15SoftDropSubjets[jet.matched_CA15SD.subJetIdx2].btag)
                for i in range(tau21[0],tau21[1],tau21[2]):
                    for j in range(bbtag[0],bbtag[1],bbtag[2]):
                        for k in range(btag2[0],btag2[1],btag2[2]):
                            i2 = i/float(1000)
                            j2 = j/float(1000)
                            k2 = k/float(1000)
                            #print i2, j2, k2
                            if jet.tau21 < i2 and jet.bbtag > j2 and btagSL > k2:
                                print " I won!" 


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

