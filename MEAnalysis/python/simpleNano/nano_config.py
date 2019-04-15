#Creates the era-dependent configuration for the NanoAOD postprocessor

class ModulesConfig:
    def __init__(self, setEra, isMC, sample, jec=False, btag=False, pu=False):
        ###################################################################################################
        if setEra == "80X":
            self.eraMC = "Run2_2016,run2_miniAOD_80XLegacy"
            self.eraData = "Run2_2016,run2_miniAOD_80XLegacy"
            self.conditionsMC = "auto:run2_mc"
            self.conditionsData = "auto:run2_data_relval"
            self.eraBtagSF = "2016"
            self.algoBtag = "csvv2"
            print "Using CMSSW 80X"
        elif setEra == "92X":
            self.eraMC = "Run2_2017,run2_nanoAOD_92X"
            self.eraData = "Run2_2017,run2_nanoAOD_92X"
            self.conditionsMC = "auto:phase1_2017_realistic"
            self.conditionsData = "auto:run2_data_relval"
            self.eraBtagSF = "2017"
            self.algoBtag = "csvv2"
            print "Using CMSSW 92X"
        #For RunIIFall17MiniAOD we need v1
        elif setEra == "94Xv1":
            self.eraMC = "Run2_2017,run2_nanoAOD_94XMiniAODv1"
            self.eraData = "Run2_2017,run2_nanoAOD_94XMiniAODv1"
            self.conditionsMC = "94X_mc2017_realistic_v13"
            self.conditionsData = "94X_dataRun2_ReReco_EOY17_v6"
            self.eraBtagSF = "2017"
            self.algoBtag = "deepcsv"
            print "Using CMSSW 94X with v1 era"
        elif setEra == "94Xv2":
            self.eraMC = "Run2_2017,run2_nanoAOD_94XMiniAODv2"
            self.eraData = "Run2_2017,run2_nanoAOD_94XMiniAODv2"
            self.conditionsMC = "94X_mc2017_realistic_v13"
            self.conditionsData = "94X_dataRun2_ReReco_EOY17_v6"
            self.eraBtagSF = "2017"
            self.algoBtag = "deepcsv"
            print "Using CMSSW 94X with v2 era"
        elif setEra == "102Xv1":
            self.eraMC = "Run2_2018,run2_nanoAOD_102Xv1"
            self.eraData = "Run2_2018,run2_nanoAOD_102Xv1"
            self.conditionsMC = "102X_upgrade2018_realistic_v12"
            self.conditionsData = "102X_dataRun2_Sep2018Rereco_v1"
            self.jecMC = "Autumn18_V8_MC"
            self.eraBtagSF = "2018"
            self.algoBtag = "deepcsv"
            print "Using CMSSW 102X with v2 era"

        imports = []
        if jec: imports += [ ('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties', 'jetmetUncertaintiesProducer') ]
        #if btag: imports += [ ('PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer','btagSFProducer') ]
        if pu: imports += [ ('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer','puAutoWeight2018') ]


        from importlib import import_module
        import sys

        #Imports the various nanoAOD postprocessor modules
        self.modules = []
        for mod, names in imports:
            import_module(mod)
            obj = sys.modules[mod]
            selnames = names.split(",")
            for name in dir(obj):
                if name[0] == "_": continue
                if name in selnames:
                    print "Loading %s from %s " % (name, mod)
                    if name == "btagSFProducer":
                        self.modules.append(getattr(obj,name)(self.eraBtagSF, self.algoBtag))
                    elif name == "jetmetUncertaintiesProducer":
                        for itypeJet in ['AK4PFchs', 'AK4PFPuppi', 'AK8PFPuppi']:
                            self.modules.append(getattr(obj,name)(self.eraBtagSF, self.jecMC, jesUncertainties=['All'], jetType=itypeJet, redoJEC=True))
                    else:
                        self.modules.append(getattr(obj,name)())

        ### load event content from nadoAOD trees #### this can be replaced with nanoaodTools Object and Collection
        from TTH.MEAnalysis.simpleNano.nanoTree import EventAnalyzer
        print "Loading %s from %s " % ('EventAnalyzer', EventAnalyzer)
        self.modules.append(EventAnalyzer(isMC))

        ### Importing selections/definitions
        from TTH.MEAnalysis.simpleNano.MEAnalysis_cfg_heppy import Conf

        ############################################################################
        #### Load Transfer functions     .... should be move to somewhere else

        import cPickle as pickle
        import TTH.MEAnalysis.TFClasses as TFClasses
        sys.modules["TFClasses"] = TFClasses
        #Load transfer functions from pickle file
        pi_file = open(Conf.general["transferFunctionsPickle"] , 'rb')
        Conf.tf_matrix = pickle.load(pi_file)
        #Pre-compute the TF formulae
        # eval_gen:specifies how the transfer functions are interpreted
        #     If True, TF [0] - reco, x - gen
        #     If False, TF [0] - gen, x - reco
        #FIXME!!!: remove this flag in future versions!
        eval_gen=False
        Conf.tf_formula = {}
        for fl in ["b", "l"]:
            Conf.tf_formula[fl] = {}
            for bin in [0, 1]:
                    Conf.tf_formula[fl][bin] = Conf.tf_matrix[fl][bin].Make_Formula(eval_gen)
        pi_file.close()

        #Load the subjet transfer functions from pickle file
        #For Top subjets
        pi_file = open(Conf.general["transferFunctions_htt_Pickle"] , 'rb')
        Conf.tf_htt_matrix = pickle.load(pi_file)
        pi_file.close()

        #For Higgs subjets
        pi_file = open(Conf.general["transferFunctions_higgs_Pickle"] , 'rb')
        Conf.tf_higgs_matrix = pickle.load(pi_file)
        pi_file.close()
        ############################################################################

        ### Memory filter
        from TTH.MEAnalysis.simpleNano.MemoryAnalyzer import MemoryAnalyzer
        print "Loading %s from %s " % ('MemoryAnalyzer', MemoryAnalyzer)
        self.modules.append(MemoryAnalyzer())

        ### MET filter
        from TTH.MEAnalysis.simpleNano.METFilterAnalyzer import METFilterAnalyzer
        print "Loading %s from %s " % ('METFilterAnalyzer', METFilterAnalyzer)
        self.modules.append(METFilterAnalyzer(Conf, isMC))

        ### Gen definitions for ttH, takes content calculated in genrad and create event content
        from TTH.MEAnalysis.simpleNano.GenTTHAnalyzer import GenTTHAnalyzerPre
        print "Loading %s from %s " % ('GenTTHAnalyzerPre', GenTTHAnalyzerPre)
        self.modules.append(GenTTHAnalyzerPre(Conf, isMC))

        ### PV analyzer
        from TTH.MEAnalysis.simpleNano.PrimaryVertexAnalyzer import PrimaryVertexAnalyzer
        print "Loading %s from %s " % ('PrimaryVertexAnalyzer', PrimaryVertexAnalyzer)
        self.modules.append(PrimaryVertexAnalyzer(Conf))

        ### Trigger: checks OR of triggers  ##### needs doublecheck
        from TTH.MEAnalysis.simpleNano.TriggerAnalyzer import TriggerAnalyzer
        print "Loading %s from %s " % ('TriggerAnalyzer', TriggerAnalyzer)
        self.modules.append(TriggerAnalyzer(Conf, isMC, sample))

        ### Lepton analyzer
        from TTH.MEAnalysis.simpleNano.LeptonAnalyzer import LeptonAnalyzer
        print "Loading %s from %s " % ('LeptonAnalyzer', LeptonAnalyzer)
        self.modules.append(LeptonAnalyzer(Conf, isMC))

        ### Jet analyzer
        from TTH.MEAnalysis.simpleNano.JetAnalyzer import JetAnalyzer
        print "Loading %s from %s " % ('JetAnalyzer', JetAnalyzer)
        self.modules.append(JetAnalyzer(Conf, isMC))

        ### Btag weight analyzer: Stores btag weights
        #from TTH.MEAnalysis.simpleNano.BtagWeightAnalyzer import BtagWeightAnalyzer
        #print "Loading %s from %s " % ('BtagWeightAnalyzer', BtagWeightAnalyzer)
        #self.modules.append(BtagWeightAnalyzer(isMC))

        ## Computes trigger weight from root files containing the SF (2018/10/25 is not doing anything because calcFHSF is False in MEAnalysis/python/MEAnalysis_cfg_heppy.py)
        from TTH.MEAnalysis.simpleNano.TriggerWeightAnalyzer import TriggerWeightAnalyzer
        print "Loading %s from %s " % ('TriggerWeightAnalyzer', TriggerWeightAnalyzer)
        self.modules.append(TriggerWeightAnalyzer(Conf, isMC))

        ## calculates the b-tag likelihood ratio
        from TTH.MEAnalysis.simpleNano.BTagLRAnalyzer import BTagLRAnalyzer
        print "Loading %s from %s " % ('BTagLRAnalyzer', BTagLRAnalyzer)
        self.modules.append(BTagLRAnalyzer(Conf, isMC, sample))

        ### QG likelihood ratio calculations
        from TTH.MEAnalysis.simpleNano.QGLRAnalyzer import QGLRAnalyzer
        print "Loading %s from %s " % ('QGLRAnalyzer', QGLRAnalyzer)
        self.modules.append(QGLRAnalyzer(Conf))

        ### performs W-tag calculation on pairs of untagged jets
        from TTH.MEAnalysis.simpleNano.WTagAnalyzer import WTagAnalyzer
        print "Loading %s from %s " % ('WTagAnalyzer', WTagAnalyzer)
        self.modules.append(WTagAnalyzer(Conf))

        ### assigns the ME category based on leptons, jets and the bLR
        from TTH.MEAnalysis.simpleNano.MECategoryAnalyzer import MECategoryAnalyzer
        print "Loading %s from %s " % ('MECategoryAnalyzer', MECategoryAnalyzer)
        self.modules.append(MECategoryAnalyzer(Conf))

        ## calculates the number of matched simulated B, C quarks for tt+XY matching
        from TTH.MEAnalysis.simpleNano.GenRadiationModeAnalyzer import GenRadiationModeAnalyzer
        print "Loading %s from %s " % ('GenRadiationModeAnalyzer', GenRadiationModeAnalyzer)
        self.modules.append(GenRadiationModeAnalyzer(Conf, isMC))

        ### Find the best possible match for each individual jet. Store for each jet, specified by it's index in the jet vector, if it is matched to any gen-level quarks
        from TTH.MEAnalysis.simpleNano.GenTTHAnalyzer import GenTTHAnalyzer
        print "Loading %s from %s " % ('GenTTHAnalyzer', GenTTHAnalyzer)
        self.modules.append(GenTTHAnalyzer(Conf, isMC))

        ### Calls the C++ MEM integrator with good_jets, good_leptons and the ME category
        from TTH.MEAnalysis.simpleNano.MEMAnalyzer import MEMAnalyzer
        print "Loading %s from %s " % ('MEMAnalyzer', MEMAnalyzer)
        self.modules.append(MEMAnalyzer(Conf, isMC))

        ### inference of ETH DNN
        #from TTH.MEAnalysis.simpleNano.NNAnalyzer import NNAnalyzer
        #print "Loading %s from %s " % ('NNAnalyzer', NNAnalyzer)
        #tag = "0"
        #self.modules.append(NNAnalyzer(tag))

        ###
        #from TTH.MEAnalysis.simpleNano.MVAVarAnalyzer import MVAVarAnalyzer
        #print "Loading %s from %s " % ('MVAVarAnalyzer', MVAVarAnalyzer)
        #self.modules.append(MVAVarAnalyzer(Conf))

        ###
        from TTH.MEAnalysis.simpleNano.TreeVarAnalyzer import TreeVarAnalyzer
        print "Loading %s from %s " % ('TreeVarAnalyzer', TreeVarAnalyzer)
        self.modules.append(TreeVarAnalyzer())

#        #Make the final output tree producer
#        #from TTH.MEAnalysis.simpleNano.metree import getTreeProducer
#        #treeProducer = getTreeProducer(Conf)
