import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


listOutputs = [
    [ 'Wmass', 'F', 'Best reconstructed W candidate mass' ],
    [ 'mbb_closest', 'F', 'Mass of geometrically closest bb pair' ],
    [ 'mjjmin', 'F', 'Minimus mass of all jet pairs'],
    [ 'min_dr_btag', 'F', 'DR between closest b tags' ],
    [ 'mass_drpair_btag', 'F', 'Mass of closest b tag pair' ],
    [ 'mass_drpair_untag', 'F', 'Mass of closest jet pair' ],
    [ 'centralitymass', 'F', 'HT over invariant mass of all jets' ],
    [ 'cat', 'I', 'ME category', 'catn' ],
#    [ 'cat_btag', 'I', 'ME category (b-tag)', 'cat_btag_n' ],
#    [ 'cat_gen', 'I', 'top decay category (-1 unknown, 0 single-leptonic, 1 di-leptonic, 2 fully hadronic)', 'cat_gen_n' ],
#    [ 'fh_region', 'I', 'FH region for QCD estimation' ],
    [ 'btag_LR_4b_2b_btagCSV', 'F', '4b vs 2b b-tag likelihood ratio using the CSV tagger' ],
    [ 'btag_LR_4b_2b_btagDeepCSV', 'F', '4b vs 2b b-tag likelihood ratio using the DeepCSV tagger' ],
    [ 'btag_LR_4b_3b_btagCSV', 'F', '' ],
    [ 'btag_LR_4b_3b_btagDeepCSV', 'F', '' ],
    [ 'btag_LR_3b_2b_btagCSV', 'F', '' ],
    [ 'btag_LR_3b_2b_btagDeepCSV', 'F', '' ],
    [ 'btag_LR_geq2b_leq1b_btagCSV', 'F', '' ],
    [ 'btag_LR_geq2b_leq1b_btagDeepCSV', 'F', '' ],
    [ 'qg_LR_4b_flavour_3q_0q', 'F', '' ],
    [ 'qg_LR_4b_flavour_4q_0q', 'F', '' ],
    [ 'qg_LR_4b_flavour_5q_0q', 'F', '' ],
    [ 'qg_LR_3b_flavour_4q_0q', 'F', '' ],
    [ 'qg_LR_3b_flavour_5q_0q', 'F', '' ],
    [ 'nBCSVM', 'I', 'Number of good jets that pass the CSV Medium WP' ],
    [ 'nBCSVT', 'I', 'Number of good jets that pass the DeepCSV Tight WP' ],
    [ 'nBCSVL', 'I', 'Number of good jets that pass the DeepCSV Loose WP' ],
    [ 'nBDeepCSVM', 'I', 'Number of good jets that pass the DeepCSV Medium WP' ],
    [ 'nBCMVAM', 'I', 'Number of good jets that pass cMVAv2 Medium WP' ],
    [ 'numJets', 'I', 'Total number of good jets that pass jet ID' ],
    [ 'changes_jet_category', 'I', 'Jet category changed on systematic' ],
    [ 'ht30', 'F', '' ],
        ]


class OutputModule(Module):
    """
    """
    def __init__(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for iVar in listOutputs: self.out.branch( iVar[0], iVar[1], title=iVar[2]);
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        for iVar in listOutputs:
            #try:
            var = getattr( event, iVar[0], -999 )
            self.out.fillBranch( iVar[0], var )
            #except RuntimeError:
            #    self.out.fillBranch( iVar[0], -9999 )

        return True
