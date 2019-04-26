#Creates the era-dependent configuration for the NanoAOD postprocessor

class NanoConfig:
    def __init__(self, setEra, jec=False, btag=False, pu=False):
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
        if jec:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties', 'jetmetUncertaintiesProducer')
            ]

        if btag:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer','btagSFProducer')
            ]
        if pu:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer','puAutoWeight_2018')
            ]

        self.json = None #Intended use: Skimming
        self.cuts = None #Intended use: Skimming
        self.branchsel = None #Intended use: Skimming

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
