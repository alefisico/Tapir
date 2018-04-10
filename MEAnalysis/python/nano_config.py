#Creates the era-dependent configuration for the NanoAOD postprocessor

class NanoConfig:
    def __init__(self, setEra, jec=False, btag=False, pu=False):
        ###################################################################################################
        if setEra == "80X":
            self.eraMC = "Run2_2016,run2_miniAOD_80XLegacy"
            self.eraData = "Run2_2016,run2_miniAOD_80XLegacy"
            self.conditionsMC = "auto:run2_mc"
            self.conditionsData = "auto:run2_data_relval"
            self.eraBtagSF = "csvv2"
            print "Using CMSSW 80X"
        elif setEra == "92X":
            self.eraMC = "Run2_2017,run2_nanoAOD_92X"
            self.eraData = "Run2_2017,run2_nanoAOD_92X"
            self.conditionsMC = "auto:phase1_2017_realistic"
            self.conditionsData = "auto:run2_data_relval"
            self.eraBtagSF = "csvv2"
            print "Using CMSSW 92X"
        elif setEra == "94X":
            self.eraMC = "Run2_2017"
            self.eraData = None
            self.conditionsMC = "auto:phase1_2017_realistic"
            self.conditionsData = None
            self.eraBtagSF = "csvv2"
            print "Using CMSSW 94X"
        
        imports = []
        if jec:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties', 'jecUncertAll')
            ]

        if btag:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer','btagSFProducer')
            ]
        if pu:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer','puWeight')
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
                        self.modules.append(getattr(obj,name)(self.eraBtagSF))
                    else:
                        self.modules.append(getattr(obj,name)())
