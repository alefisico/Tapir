import nanoTreeClasses
import nanoTreeGenClasses
import ROOT
import logging
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class EventAnalyzer(Module):

    def __init__(self, isMC):
        self.isMC = isMC

    def analyze(self, event):
        #event.lumi = getattr(event, "luminosityBlock", None)
    	#event.evt = long(getattr(event, "event", None))
        #event.json = getattr(event, "json", None)
        #event.json_silver = getattr(event, "json_silver", None)

        #event.Electron = nanoTreeClasses.Electron.make_array(event, MC = self.isMC)
        #event.Muon = nanoTreeClasses.Muon.make_array(event, MC = self.isMC)
        #event.met = nanoTreeClasses.met.make_obj(event, MC = self.isMC)
        event.Jet = nanoTreeClasses.Jet.make_array(event, MC = self.isMC)
        event.ttCls = getattr(event, "genTtbarId", None)%100
        #event.heavyFlavourCategory = getattr(event, "heavyFlavourCategory", None)

        event.PV = nanoTreeClasses.PV.make_array(event)
        #event.pileUpVertex_z = pileUpVertex_z.make_array(event)
        event.Pileup_nPU = getattr(event, "Pileup_nPU", None)
        event.Pileup_nTrueInt = getattr(event, "Pileup_nTrueInt", None)
        event.nPVs = getattr(event, "PV_npvs", None)
        #event.bx = getattr(event, "bx", None)
        #event.rho = getattr(event, "rho", None)

        event.GenJet = nanoTreeGenClasses.GenJet.make_array(event)
        #event.genHiggsDecayMode = getattr(event, "genHiggsDecayMode", None)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(event)
        event.GenLepFromTop = nanoTreeGenClasses.GenLepFromTop.make_array(event.GenParticle)
    	event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
    	event.GenLepFromTau = nanoTreeGenClasses.GenLepFromTau.make_array(event.GenParticle)
    	event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
    	event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
    	event.GenTaus = nanoTreeGenClasses.GenTaus.make_array(event.GenParticle)
    	event.GenLep = nanoTreeGenClasses.GenLep.make_array(event.GenParticle)
    	event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
    	event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
    	event.GenNuFromTop = nanoTreeGenClasses.GenNuFromTop.make_array(event.GenParticle)
    	event.GenNu = nanoTreeGenClasses.GenNu.make_array(event.GenParticle)
    	event.GenNuFromTau = nanoTreeGenClasses.GenNuFromTau.make_array(event.GenParticle)
    	event.GenGluonFromTop = nanoTreeGenClasses.GenGluonFromTop.make_array(event.GenParticle)
    	event.GenGluonFromB = nanoTreeGenClasses.GenGluonFromB.make_array(event.GenParticle)
    	nanoTreeGenClasses.Jet_addmc(event.Jet,event.GenJet)

        event.LHEScaleWeight = nanoTreeClasses.LHEScaleWeight.make_array(event)
        event.LHEPdfWeight = nanoTreeClasses.LHEPdfWeight.make_array(event)
        event.LHE_Njets = getattr(event, "LHE_Njets", None)
        event.LHE_Nb = getattr(event, "LHE_Nb", None)
        event.LHE_Nc = getattr(event, "LHE_Nc", None)
        event.LHE_Nglu = getattr(event, "LHE_Nglu", None)
        event.LHE_Nuds = getattr(event, "LHE_Nuds", None)
        event.LHE_Vpt = getattr(event, "LHE_Vpt", None)
        event.LHE_HT = getattr(event, "LHE_HT", None)



        #event.triggerEmulationWeight = getattr(event, "triggerEmulationWeight", None)
        #event.btagWeightCSV_down_jesPileUpPtBB = getattr(event, "btagWeightCSV_down_jesPileUpPtBB", None)
        #event.btagWeightCSV_down_jesFlavorQCD = getattr(event, "btagWeightCSV_down_jesFlavorQCD", None)
        #event.btagWeightCSV_down_jesAbsoluteScale = getattr(event, "btagWeightCSV_down_jesAbsoluteScale", None)
        #event.btagWeightCSV_down_jesPileUpPtRef = getattr(event, "btagWeightCSV_down_jesPileUpPtRef", None)
        #event.btagWeightCSV_down_jesRelativeFSR = getattr(event, "btagWeightCSV_down_jesRelativeFSR", None)
        #event.btagWeightCSV_down_jesTimePtEta = getattr(event, "btagWeightCSV_down_jesTimePtEta", None)
        #event.btagWeightCSV_down_hf = getattr(event, "btagWeightCSV_down_hf", None)
        #event.btagWeightCSV_down_cferr1 = getattr(event, "btagWeightCSV_down_cferr1", None)
        #event.btagWeightCMVAV2_up_hf = getattr(event, "btagWeightCMVAV2_up_hf", None)
        #event.btagWeightCMVAV2_down_hfstats2 = getattr(event, "btagWeightCMVAV2_down_hfstats2", None)
        #event.btagWeightCSV_down_cferr2 = getattr(event, "btagWeightCSV_down_cferr2", None)
        #event.btagWeightCSV_down_jes = getattr(event, "btagWeightCSV_down_jes", None)
        #event.btagWeightCSV_down_jesAbsoluteMPFBias = getattr(event, "btagWeightCSV_down_jesAbsoluteMPFBias", None)
        #event.btagWeightCSV_down_lf = getattr(event, "btagWeightCSV_down_lf", None)
        #event.btagWeightCSV_down_jesPilenanoTreeGenClassesUpPtEC1 = getattr(event, "btagWeightCSV_down_jesPileUpPtEC1", None)
        #event.btagWeightCMVAV2_down_hfstats1 = getattr(event, "btagWeightCMVAV2_down_hfstats1", None)
        #event.btagWeightCSV_up_lf = getattr(event, "btagWeightCSV_up_lf", None)
        #event.btagWeightCMVAV2 = getattr(event, "btagWeightCMVAV2", None)
        #event.btagWeightCSV_down_lfstats2 = getattr(event, "btagWeightCSV_down_lfstats2", None)
        #event.btagWeightCSV_up_jesPileUpPtRef = getattr(event, "btagWeightCSV_up_jesPileUpPtRef", None)
        #event.btagWeightCSV_down_lfstats1 = getattr(event, "btagWeightCSV_down_lfstats1", None)
        #evenself.mass = GenParticle[n].masst.btagWeightCSV_up_jesFlavorQCD = getattr(event, "btagWeightCSV_up_jesFlavorQCD", None)
        #event.btagWeightCSV_down_jesPileUpDataMC = getattr(event, "btagWeightCSV_down_jesPileUpDataMC", None)
        #event.btagWeightCSV_up_lfstats1 = getattr(event, "btagWeightCSV_up_lfstats1", None)
        #event.btagWeightCMVAV2_down_lf = getattr(event, "btagWeightCMVAV2_down_lf", None)
        #event.btagWeightCSV_up_lfstats2 = getattr(event, "btagWeightCSV_up_lfstats2", None)
        #event.btagWeightCSV = getattr(event, "btagWeightCSV", None)
        #event.btagWeightCSV_up_cferr2 = getattr(event, "btagWeightCSV_up_cferr2", None)
        #event.btagWeightCSV_up_jesAbsoluteMPFBias = getattr(event, "btagWeightCSV_up_jesAbsoluteMPFBias", None)
        #event.btagWeightCSV_up_jesSinglePionECAL = getattr(event, "btagWeightCSV_up_jesSinglePionECAL", None)
        #event.btagWeightCSV_up_cferr1 = getattr(event, "btagWeightCSV_up_cferr1", None)
        #event.btagWeightCSV_up_jesPileUpPtBB = getattr(event, "btagWeightCSV_up_jesPileUpPtBB", None)
        #event.btagWeightCMVAV2_down_hf = getattr(event, "btagWeightCMVAV2_down_hf", None)
        #event.btagWeightCMVAV2_up_lfstats2 = getattr(event, "btagWeightCMVAV2_up_lfstats2", None)
        #event.btagWeightCMVAV2_up_hfstats2 = getattr(event, "btagWeightCMVAV2_up_hfstats2", None)
        #event.btagWeightCMVAV2_up_hfstats1 = getattr(event, "btagWeightCMVAV2_up_hfstats1", None)
        #event.btagWeightCSV_up_jesAbsoluteScale = getattr(event, "btagWeightCSV_up_jesAbsoluteScale", None)
        #event.btagWeightCMVAV2_up_lfstats1 = getattr(event, "btagWeightCMVAV2_up_lfstats1", None)
        #event.btagWeightCMVAV2_down_cferr2 = getattr(event, "btagWeightCMVAV2_down_cferr2", None)
        #event.btagWeightCSV_up_hf = getattr(event, "btagWeightCSV_up_hf", None)
        #event.btagWeightCSV_up_jesPileUpPtEC1 = getattr(event, "btagWeightCSV_up_jesPileUpPtEC1", None)
        #event.btagWeightCMVAV2_down_cferr1 = getattr(event, "btagWeightCMVAV2_down_cferr1", None)
        #event.btagWeightCSV_up_jesRelativeFSR = getattr(event, "btagWeightCSV_up_jesRelativeFSR", None)
        #event.btagWeightCSV_up_jesTimePtEta = getattr(event, "btagWeightCSV_up_jesTimePtEta", None)
        #event.btagWeightCSV_up_jes = getattr(event, "btagWeightCSV_up_jes", None)
        #event.btagWeightCMVAV2_up_jes = getattr(event, "btagWeightCMVAV2_up_jes", None)
        #event.btagWeightCSV_down_jesSinglePionECAL = getattr(event, "btagWeightCSV_down_jesSinglePionECAL", None)
        #event.btagWeightCMVAV2_up_lf = getattr(event, "btagWeightCMVAV2_up_lf", None)
        #event.btagWeightCSV_down_hfstats2 = getattr(event, "btagWeightCSV_down_hfstats2", None)
        #event.btagWeightCSV_up_jesPileUpDataMC = getattr(event, "btagWeightCSV_up_jesPileUpDataMC", None)
        #event.btagWeightCSV_down_hfstats1 = getattr(event, "btagWeightCSV_down_hfstats1", None)
        #event.btagWeightCSV_down_jesSinglePionHCAL = getattr(event, "btagWeightCSV_down_jesSinglePionHCAL", None)
        #event.btagWeightCMVAV2_up_cferr1 = getattr(event, "btagWeightCMVAV2_up_cferr1", None)
        #event.btagWeightCMVAV2_up_cferr2 = getattr(event, "btagWeightCMVAV2_up_cferr2", None)
        #event.btagWeightCMVAV2_down_lfstats1 = getattr(event, "btagWeightCMVAV2_down_lfstats1", None)
        #event.btagWeightCMVAV2_down_lfstats2 = getattr(event, "btagWeightCMVAV2_down_lfstats2", None)
        #event.btagWeightCSV_up_hfstats2 = getattr(event, "btagWeightCSV_up_hfstats2", None)
        #event.btagWeightCSV_up_hfstats1 = getattr(event, "btagWeightCSV_up_hfstats1", None)
        #event.btagWeightCMVAV2_down_jes = getattr(event, "btagWeightCMVAV2_down_jes", None)
        #event.btagWeightCSV_up_jesSinglePionHCAL = getattr(event, "btagWeightCSV_up_jesSinglePionHCAL", None)

        return True