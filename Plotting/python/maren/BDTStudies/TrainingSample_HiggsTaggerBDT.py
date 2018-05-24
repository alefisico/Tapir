#imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
from array import array


import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses

if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsHelpers import *

########################################
# Define helper functions
########################################


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

if socket.gethostname() == "t3ui02":
    basepath = 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat'
else:
    basepath = 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat'
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
#for k,v in files.iteritems():
#fn = os.environ['FILE_NAMES'].split(' ')
#for v in fn:
#    full_file_names[v] = basepath + v

#full_file_names = {}
full_file_names["v1"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/chreisse/tth/Apr16/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Apr16/180416_072809/0000/tree_101.root"
#full_file_names["v2"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_204.root"
#full_file_names["v3"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_205.root"
#full_file_names["v4"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_206.root"
#full_file_names["v5"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_207.root"
#full_file_names["v6"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_208.root"
#full_file_names["v7"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_209.root"
#full_file_names["v8"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_210.root"



#full_file_names = {}
#full_file_names["v"] = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/mameinha/tth/Apr09_v1/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Apr09_v1/170409_111531/0000/tree_100.root"
#full_file_names["v"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr12_v1/SingleMuon/Apr12_v1/170412_122435/0000/tree_100.root"

#class InputVars():
#    def __init__(self, mass = 0, nsub = 0, bbtag = 0, btagf = 0, btags = 0):
#        self.mass = mass
#        self.nsub = nsub
#        self.bbtag = bbtag
#        self.btagf = btagf 
#        self.btags = btags

t2 = ROOT.TTree("t2","a Tree with fatjets")
#ivars = InputVars()
mass = array( 'f', [ 0. ] )
ptdr = array( 'f', [ 0. ] )
nsj = array( 'i', [ 0 ] )
nsub = array( 'f', [ 0. ] )
nsub2 = array( 'f', [ 0. ] )
bbtag = array( 'f', [ 0. ] )
btagf = array( 'f', [ 0. ] )
btags = array( 'f', [ 0. ] )
fromhiggs = array( 'i', [ 0 ] )
evt = array( 'i', [ 0 ] )
t2.Branch("mass",mass,"mass/F")
t2.Branch("ptdr",ptdr,"ptdr/F")
t2.Branch("nsj",nsj,"nsj/I")
t2.Branch("nsub",nsub,"nsub/F")
t2.Branch("nsub2",nsub2,"nsub2/F")
t2.Branch("bbtag",bbtag,"bbtag/F")
t2.Branch("btagf",btagf,"btagf/F")
t2.Branch("btags",btags,"btags/F")
t2.Branch("fromhiggs",fromhiggs,"fromhiggs/I")
t2.Branch("evt",evt,"evt/I")


for l in full_file_names:
    print full_file_names[l] 
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"


    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("nanoAOD/Events")

    
    counter  = 0
    for event in ttree :

        #if counter > 10000:
        #    break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event


        counter += 1
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

        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15SoftDrop)

        matched_fatjet = Match_two_lists(
            event.FatjetCA15SoftDrop, 'CA15SD',
            event.FatjetCA15, 'CA15',0.5)

        event.FatjetCA15 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.FatjetCA15)

        # Lepton selection
        #if ev.nselLeptons == 0:
        #    continue
        #if ev.leps_pt[0] < 30:
        #    continue


        """numJets = 0
        nBCSVM = 0
        for i in range(ev.nJet):
            if ev.Jet_pt[i]>20:
                numJets += 1
                if ev.Jet_btagCSV[i]>0.8484:
                    nBCSVM += 1
        # Calculate number of jets
        if nBCSVM < 3:
            continue

        if numJets < 3:
            continue"""

        for fatjet in event.FatjetCA15:
            dr = 0
            evt[0] = event.event
            mass[0] = getattr(fatjet.matched_CA15SD,"mass")
            nsub[0] =  float(fatjet.tau2/fatjet.tau1)
            nsub2[0] =  float(fatjet.tau3/fatjet.tau2)
            bbtag[0] = float(fatjet.bbtag)
            subjets = [event.FatjetCA15SoftDropSubjets[getattr(fatjet.matched_CA15SD,"subJetIdx1")], \
            event.FatjetCA15SoftDropSubjets[getattr(fatjet.matched_CA15SD,"subJetIdx2")]]
            #nsj[0] = nsubjets
            btag1 = max(subjets[0].btag,subjets[1].btag)
            btag2 = min(subjets[0].btag,subjets[1].btag)
            btagf[0] = btag1
            btags[0] = btag2
            if sample == "ttH" and Get_DeltaR_two_objects(fatjet,event.GenHiggsBoson[0])<1.0:
                fromhiggs[0] = 1
            else:
                fromhiggs[0] = 0
            t2.Fill()
            counter += 1
f.Close()
print counter 
BDTInput = ROOT.TFile("TestingSample_Higgs.root","recreate")
t2.Write()
BDTInput.Close()
