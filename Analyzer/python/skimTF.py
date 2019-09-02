import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from TTH.Analyzer.utils import match_deltaR, remove_duplicates
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class skimTF(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nQuarkMatched", "I" )
        self.out.branch("Quark_pt", "F", lenVar="nQuarkMatched" )
        self.out.branch("Quark_eta", "F", lenVar="nQuarkMatched" )
        self.out.branch("Quark_phi", "F", lenVar="nQuarkMatched" )
        self.out.branch("Quark_mass", "F", lenVar="nQuarkMatched" )
        self.out.branch("Quark_pdgId", "F", lenVar="nQuarkMatched" )
        self.out.branch("Quark_num_matches", "F", lenVar="nQuarkMatched" )
        self.out.branch("Quark_match_dr", "F", lenVar="nQuarkMatched" )
        self.out.branch("Jetmatched_pt", "F", lenVar="nQuarkMatched" )
        self.out.branch("Jetmatched_eta", "F", lenVar="nQuarkMatched" )
        self.out.branch("Jetmatched_phi", "F", lenVar="nQuarkMatched" )
        self.out.branch("Jetmatched_mass", "F", lenVar="nQuarkMatched" )
        self.out.branch("Jetmatched_btagCSV", "F", lenVar="nQuarkMatched" )
        self.out.branch("Jetmatched_btagDeepFlav", "F", lenVar="nQuarkMatched" )
        self.out.branch("Jetmatched_btagDeepCSV", "F", lenVar="nQuarkMatched" )
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        genParticles = Collection(event, "GenPart")
        jets = Collection(event, "Jet")

        genBQuarkFromTop = GenBQuarkFromTop( genParticles )
        genWZQuark = GenWZQuark( genParticles )
        genBQuarkFromH = GenBQuarkFromHiggs( genParticles )

        all_quarks = genBQuarkFromTop + genWZQuark + genBQuarkFromH
        cleaned_quarks = remove_duplicates(all_quarks)

        #Take particles from the hard process
        #http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
        cleaned_quarks = filter(lambda x: x.status == 23, cleaned_quarks)

        #for obj in sorted(cleaned_quarks, key=lambda x: x.pt, reverse=True):
        #    print obj.pt, obj.eta, obj.phi, obj.pdgId

        matches = match_deltaR(cleaned_quarks, jets, 0.3)
        sorted_matches = sorted(matches, key=lambda x: (x[0], x[2]))
        matches_by_quark = {}
        for quark_idx, jet_idx, dr in sorted_matches:
            if not matches_by_quark.has_key(quark_idx):
                matches_by_quark[quark_idx] = []
            matches_by_quark[quark_idx] += [(jet_idx, dr)]

        for quark in cleaned_quarks:
            quark.num_matches = 0
            quark.match_pt = 0
            quark.match_eta = 0
            quark.match_phi = 0
            quark.match_mass = 0
            quark.match_pdgId = 0
            quark.match_dr = 0
            quark.match_btagCSV = 0
            quark.match_btagDeepCSV = 0
            quark.match_btagDeepFlav = 0

        for quark_idx in matches_by_quark.keys():
            quark = cleaned_quarks[quark_idx]
            quark.num_matches = len(matches_by_quark[quark_idx])
            if quark.num_matches > 0:
                jet_idx, dr = matches_by_quark[quark_idx][0]
                best_match = jets[jet_idx]
                quark.match_pt = best_match.pt
                quark.match_eta = best_match.eta
                quark.match_phi = best_match.phi
                quark.match_mass = best_match.mass
                quark.match_btagCSV = best_match.btagCSVV2
                quark.match_btagDeepCSV = best_match.btagDeepB
                quark.match_btagDeepFlav = best_match.btagDeepFlavB
                quark.match_dr = dr

        self.out.fillBranch("nQuarkMatched", len(cleaned_quarks))
        self.out.fillBranch("Quark_pt", [ quark.pt for quark in cleaned_quarks ])
        self.out.fillBranch("Quark_eta", [ quark.eta for quark in cleaned_quarks ])
        self.out.fillBranch("Quark_phi", [ quark.phi for quark in cleaned_quarks ])
        self.out.fillBranch("Quark_mass", [ quark.mass for quark in cleaned_quarks ])
        self.out.fillBranch("Quark_pdgId", [ quark.pdgId for quark in cleaned_quarks ])
        self.out.fillBranch("Quark_num_matches", [ quark.num_matches for quark in cleaned_quarks ])
        self.out.fillBranch("Quark_match_dr", [ quark.match_dr for quark in cleaned_quarks ])
        self.out.fillBranch("Jetmatched_pt", [ quark.match_pt for quark in cleaned_quarks ])
        self.out.fillBranch("Jetmatched_eta", [ quark.match_eta for quark in cleaned_quarks ])
        self.out.fillBranch("Jetmatched_phi", [ quark.match_phi for quark in cleaned_quarks ])
        self.out.fillBranch("Jetmatched_mass", [ quark.match_mass for quark in cleaned_quarks ])
        self.out.fillBranch("Jetmatched_btagCSV", [ quark.match_btagCSV for quark in cleaned_quarks ])
        self.out.fillBranch("Jetmatched_btagDeepCSV", [ quark.match_btagDeepCSV for quark in cleaned_quarks ])
        self.out.fillBranch("Jetmatched_btagDeepFlav", [ quark.match_btagDeepFlav for quark in cleaned_quarks ])

        return True



def getDaughters(GenParticle,gp):
    ret = []
    tmpListGenParticles = list(GenParticle)
    for part in GenParticle:
        if part != gp:
            if part.genPartIdxMother == tmpListGenParticles.index(gp):
                ret.append(part)
    return ret

def GenBQuarkFromTop(GenParticle):
    ret = []
    for gP in GenParticle:
        if abs(gP.pdgId) == 5 and gP.genPartIdxMother>0:
            mom = GenParticle[gP.genPartIdxMother]
            if abs(mom.pdgId)  == 6:
                dauids = [abs(dau.pdgId) for dau in getDaughters(GenParticle,mom)]
                if 6 not in dauids:
                    ret.append(gP)
    return ret

def GenWZQuark(GenParticle):
    ret = []
    for gP in GenParticle:
        if gP.genPartIdxMother>0:
            if abs(gP.pdgId) <= 5 and abs(GenParticle[gP.genPartIdxMother].pdgId) in [23,24]:
                ret.append(gP)
    return ret

def GenBQuarkFromHiggs(GenParticle):
    ret = []
    for gP in GenParticle:
        if abs(gP.pdgId) in [3,4,5] and gP.genPartIdxMother>0:
            mom = GenParticle[gP.genPartIdxMother]
            if abs(mom.pdgId)  == 25:
                dauids = [abs(dau.pdgId) for dau in getDaughters(GenParticle,mom)]
                if 25 not in dauids:
                    ret.append(gP)
    return ret

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
skimmerTF = lambda : skimTF()
