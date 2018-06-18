#!/usr/bin/env python

import ROOT
#from Tapir.memAnalyzer.nanoTreeClasses import Jet
#from Tapir.memAnalyzer.nanoTreeGenClasses import *
import Tapir.memAnalyzer.nanoTreeClasses
import Tapir.memAnalyzer.nanoTreeGenClasses

def classifyJetsAndGenParticles( tree ):
    """docstring for classifyJetsAndGenParticles"""
   
    for ievent in range(tree.GetEntries()):
        if (ievent%1000==0): 
            print ievent  
        tree.GetEntry(ievent)

        #jet = Jet.make_array( tree, MC=True )
        #print jet
        genJet = nanoTreeGenClasses.GenJet.make_array(tree)
        genParticle = nanoTreeGenClasses.GenParticle.make_array(tree)
        genLepFromTop = nanoTreeGenClasses.GenLepFromTop.make_array(GenParticle)
        genBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(GenParticle)
        genWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(GenParticle)
        genBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(GenParticle)

        all_quarks = GenBQuarkFromTop + GenWZQuark + GenBQuarkFromH
        cleaned_quarks = remove_duplicates(all_quarks)

        #Take particles from the hard process
        #http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
        cleaned_quarks = filter(lambda x: x.status == 23, cleaned_quarks)

        for obj in sorted(cleaned_quarks, key=lambda x: x.pt, reverse=True):
            print obj.pt, obj.eta, obj.phi, obj.pdgId




if __name__ == '__main__':

    tree = ROOT.TChain("Events")
    tree.Add("root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/18C1BD10-B842-E811-87AA-6CC2173D6B10.root")

    classifyJetsAndGenParticles( tree )
