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
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf


from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *


########################################
# Define Input Files and
# output directory
########################################

                                         
full_file_names = {}
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v

#full_file_names = {}
#full_file_names["v1"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_129.root"
#full_file_names["v2"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_33.root"
#full_file_names["v3"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_34.root"
#full_file_names["v4"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_35.root"
#full_file_names["v5"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_207.root"
#full_file_names["v6"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_208.root"
#full_file_names["v7"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_209.root"
#full_file_names["v8"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Apr09_v1/170409_111637/0000/tree_210.root"


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
massuncor = array( 'f', [ 0. ] )
ptdr = array( 'f', [ 0. ] )
nsj = array( 'i', [ 0 ] )
nsub = array( 'f', [ 0. ] )
nsub2 = array( 'f', [ 0. ] )
bbtag = array( 'f', [ 0. ] )
btagf = array( 'f', [ 0. ] )
btags = array( 'f', [ 0. ] )
frec = array( 'f', [ 0. ] )
fromtop = array( 'i', [ 0 ] )
evt = array( 'i', [ 0 ] )
t2.Branch("mass",mass,"mass/F")
t2.Branch("massuncor",massuncor,"mass/F")
t2.Branch("ptdr",ptdr,"ptdr/F")
t2.Branch("nsj",nsj,"nsj/I")
t2.Branch("nsub",nsub,"nsub/F")
t2.Branch("nsub2",nsub2,"nsub2/F")
t2.Branch("bbtag",bbtag,"bbtag/F")
t2.Branch("btagf",btagf,"btagf/F")
t2.Branch("btags",btags,"btags/F")
t2.Branch("frec",frec,"frec/F")
t2.Branch("fromtop",fromtop,"fromtop/I")
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

        #if counter > 1000:
        #    break

        #if counter < 6495:
        #    continue

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event

        counter += 1
        
        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)     
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        
        
        GetCategory(event,python_conf)

        #Get event category
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue


        #First apply all general cuts on objects
        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4 and x.mass>50), event.FatjetCA15SoftDrop)
        event.FatjetCA15 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15)
        event.HTTV2 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.HTTV2)
        event.GenHadTop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHadTop)
        event.GenHiggsBoson = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHiggsBoson)

        matched_fatjet = Match_two_lists(
        event.FatjetCA15SoftDrop, 'CA15SD',
        event.FatjetCA15, 'CA15',0.5)

        event.FatjetCA15 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.FatjetCA15)

        matched_fatjet = Match_two_lists(
        event.HTTV2, 'HTT',
        event.FatjetCA15SoftDrop, 'CA15SD',1.0)

        event.HTTV2 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.HTTV2)

        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)

        event.FatjetCA15 =  filter(lambda x: (hasattr(x,"matched_HTT")), event.FatjetCA15)
        if cat == "sl":
            for i in event.HTTV2:
                setattr(i,"drl",Get_DeltaR_two_objects(i,event.lep_SL[0]))
                subjets = [event.HTTV2Subjets[i.subJetIdx1].btag,event.HTTV2Subjets[i.subJetIdx2].btag,event.HTTV2Subjets[i.subJetIdx3].btag]
                subjets = sorted(subjets)
                setattr(i,"btagmax",subjets[2])
                setattr(i,"btagsecond",subjets[1])
                matched = 0
                for gentop in event.GenHadTop:
                    if Get_DeltaR_two_objects(i,gentop) < 0.6:
                        matched = 1
                setattr(i,"matched",matched)

                #Get corrected mass from subjets
                s1 = lvec(event.HTTV2Subjets[i.subJetIdx1])
                s2 = lvec(event.HTTV2Subjets[i.subJetIdx2])
                s3 = lvec(event.HTTV2Subjets[i.subJetIdx3])
                vtop = s1+s2+s3
                setattr(i,"massreco",vtop.M())

            event.HTTV2 = filter(lambda x: (x.drl>1.5 and x.btagmax > 0.1522), event.HTTV2)

        if cat == "dl":
            event.HTTV2 = []


        for fatjet in event.HTTV2:
            dr = 0
            evt[0] = event.event
            massuncor[0] = fatjet.mass
            mass[0] = fatjet.massreco
            frec[0] = fatjet.frec
            nsub[0] =  float(getattr(fatjet.matched_CA15SD,"tau2")/getattr(fatjet.matched_CA15SD,"tau1"))
            #nsub[0] =  float(fatjet.tau2/fatjet.tau1)
            nsub2[0] =  float(getattr(fatjet.matched_CA15SD,"tau3")/getattr(fatjet.matched_CA15SD,"tau2"))
            #nsub2[0] =  float(fatjet.tau3/fatjet.tau2)
            bbtag[0] = getattr(fatjet.matched_CA15SD,"bbtag")
            subjets = [event.HTTV2Subjets[fatjet.subJetIdx1], \
            event.HTTV2Subjets[fatjet.subJetIdx2], \
            event.HTTV2Subjets[fatjet.subJetIdx3]]
            #nsj[0] = nsubjets
            btag1 = max(subjets[0].btag,subjets[1].btag)
            btag2 = min(subjets[0].btag,subjets[1].btag)
            btagf[0] = btag1
            btags[0] = btag2
            if fatjet.matched == 1:
                fromtop[0] = 1
            else:
                fromtop[0] = 0
            t2.Fill()

f.Close()
print counter 
BDTInput = ROOT.TFile("out.root","recreate")
t2.Write()
BDTInput.Close()