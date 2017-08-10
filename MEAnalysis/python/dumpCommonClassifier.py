import ROOT
import sys, os, json, math, copy
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
from PhysicsTools.HeppyCore.statistics.tree import Tree
import numpy as np

class Jet:
    def __init__(self, *args, **kwargs):
        self.pt = kwargs.get("pt")
        self.eta = kwargs.get("eta")
        self.phi = kwargs.get("phi")
        self.mass = kwargs.get("mass")

        self.csv = kwargs.get("csv")
        self.cmva = kwargs.get("cmva")
        self.corrections = kwargs.get("corrections")

class Scenario:
    def __init__(self, *args, **kwargs):
        self.jets = kwargs.get("jets")
        self.leps_p4 = kwargs.get("leps_p4")
        self.leps_charge = kwargs.get("leps_charge")
        self.met_pt = kwargs.get("met_pt")
        self.met_phi = kwargs.get("met_phi")
        self.systematic_index = kwargs.get("systematic_index")

def createOutput(jet_corrections, max_jets, max_leps):
    outfile = ROOT.TFile('out.root', 'recreate')
    tree = Tree('tree', 'MEM tree')

    tree.var('numJets', the_type=int)
    tree.var('numBTags', the_type=int)

    tree.var('njets', the_type=int)
    for v in ["jet_pt", "jet_eta", "jet_phi", "jet_mass", "jet_csv", "jet_cmva"]:
        tree.vector(v, "njets", maxlen=max_jets, the_type=float, storageType="F")

    for corr in jet_corrections:
        tree.vector("jet_" + corr, "njets", maxlen=max_jets, the_type=float, storageType="F")
        if corr != "corr" and corr != "corr_JER":
            tree.var('numJets_' + corr.replace("corr_", ""), the_type=int)
            tree.var('numBTags_' + corr.replace("corr_", ""), the_type=int)

    for v in ["jet_type"]:
        tree.vector(v, "njets", maxlen=max_jets, the_type=int, storageType="i")
    
    tree.var('nleps', the_type=int)
    for v in ["lep_pt", "lep_eta", "lep_phi", "lep_mass", "lep_charge"]:
        tree.vector(v, "nleps", maxlen=max_leps, the_type=float, storageType="F")
    
    tree.var('met_pt', the_type=float, storageType="F")
    tree.var('met_phi', the_type=float, storageType="F")
       
    for v in ["event", "run", "lumi"]:
        tree.var(v, the_type=int, storageType="L")
    return outfile, tree

def createLeptons(event, max_leps):
    leps_p4 = []
    leps_charge = []
    for ilep in range(event.nleps)[:max_leps]:
        p4 = [
            event.leps_pt[ilep],
            event.leps_eta[ilep],
            event.leps_phi[ilep],
            event.leps_mass[ilep]
        ]
        leps_p4 += [p4]
        leps_charge += [math.copysign(1, event.leps_pdgId[ilep])]
    return leps_p4, leps_charge

def createJets(event, jet_corrections, max_jets):
    jets = []

    for ijet in range(event.njets)[:max_jets]:
        jets += [Jet(
            pt = event.jets_pt[ijet],
            eta = event.jets_eta[ijet],
            phi = event.jets_phi[ijet],
            mass = event.jets_mass[ijet],
            csv = event.jets_btagCSV[ijet],
            cmva = event.jets_btagCMVA[ijet],
            corrections = {corr: getattr(event, "jets_"+corr)[ijet] for corr in jet_corrections}
        )]

    return jets

def fillTree(tree, event, jet_corrections, jets, leps_p4, leps_charge):
    tree.fill('numJets', event.numJets)
    tree.fill('numBTags', event.nBCSVM)

    tree.fill('njets', len(jets))
    tree.vfill('jet_pt', [x.pt for x in jets])
    tree.vfill('jet_eta', [x.eta for x in jets])
    tree.vfill('jet_phi', [x.phi for x in jets])
    tree.vfill('jet_mass', [x.mass for x in jets])
    tree.vfill('jet_csv', [x.csv for x in jets])
    tree.vfill('jet_cmva', [x.cmva for x in jets])
    for corr in jet_corrections:
        tree.vfill('jet_' + corr, [x.corrections[corr] for x in jets])
        if corr != "corr" and corr != "corr_JER":
            corr_name = corr.replace("corr_", "")
            tree.fill('numJets_' + corr_name, getattr(event, 'numJets_' + corr_name))
            tree.fill('numBTags_' + corr_name, getattr(event, 'nBCSVM_' + corr_name))

    tree.fill('nleps', len(leps_p4))
    tree.vfill('lep_pt', [x[0] for x in leps_p4])
    tree.vfill('lep_eta', [x[1] for x in leps_p4])
    tree.vfill('lep_phi', [x[2] for x in leps_p4])
    tree.vfill('lep_mass', [x[3] for x in leps_p4])
    tree.vfill('lep_charge', leps_charge)
    
    tree.fill('met_pt', event.met_pt)
    tree.fill('met_phi', event.met_phi)
    
    tree.fill('event', event.evt)
    tree.fill('run', event.run)
    tree.fill('lumi', event.lumi)
        
    tree.tree.Fill()

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        prefix, sample_name = get_prefix_sample(os.environ["DATASETPATH"])
        an_name, analysis = analysisFromConfig(os.environ.get("ANALYSIS_CONFIG"))
    else:
        sample = "ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default.cfg")
        file_names = analysis.get_sample(sample).file_names[:1]

    chain = ROOT.TChain("tree")
    for fi in file_names:
        chain.AddFile(getSitePrefix(fi))
    
    max_jets = 10
    max_leps = 2

    jet_corrections = map(
        lambda x: x.replace("jets_", ""),
        filter(
            lambda x: x.startswith("jets_corr"),
            [br.GetName() for br in chain.GetListOfBranches()]
        )
    )

    outfile, tree = createOutput(jet_corrections, max_jets, max_leps)

    for iEv, event in enumerate(chain):
        if iEv % 100 == 0:
            print iEv
        accept = (event.is_sl or event.is_dl)

        if not accept:
            continue
        hypo = -1

        leps_p4, leps_charge = createLeptons(event, max_leps)
        jets = createJets(event, jet_corrections, max_jets)

        fillTree(tree, event, jet_corrections, jets, leps_p4, leps_charge)
    
    outfile.Write()
