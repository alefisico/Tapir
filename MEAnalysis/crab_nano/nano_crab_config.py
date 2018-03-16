###################################################################################################
###################################################################################################
#####################################  nanoAOD production #########################################
###################################################################################################
###################################################################################################
#
# Configure this variables:
setEra = "94X" # Options: 80X, 92X, 94X

#
###################################################################################################
if setEra == "80X":
    eraMC = "Run2_2016,run2_miniAOD_80XLegacy"
    eraData = "Run2_2016,run2_miniAOD_80XLegacy"
    conditionsMC = "auto:run2_mc"
    conditionsData = "auto:run2_data_relval"
    eraBtagSF = "2016"
    print "Using CMSSW 80X"
elif setEra == "92X":
    eraMC = "Run2_2017,run2_nanoAOD_92X"
    eraData = "Run2_2017,run2_nanoAOD_92X"
    conditionsMC = "auto:phase1_2017_realistic"
    conditionsData = "auto:run2_data_relval"
    eraBtagSF = "2017"
    print "Using CMSSW 92X"
elif setEra == "94X":
    eraMC = "Run2_2017"
    eraData = None
    conditionsMC = "auto:phase1_2017_realistic"
    conditionsData = None
    eraBtagSF = "2017"
    print "Using CMSSW 94X"

###################################################################################################
###################################################################################################
################################# nanoAOD postprocessing ##########################################
###################################################################################################
###################################################################################################
#
# Configure this variables:
imports = [('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties', 'jecUncertAll'),
           ('PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer','btagSFProducer')] 
json = None #Intended use: Skimming
cuts = None #Intended use: Skimming
branchsel = None #Intended use: Skimming



#
###################################################################################################
from importlib import import_module
import sys

modules = []
for mod, names in imports: 
    import_module(mod)
    obj = sys.modules[mod]
    selnames = names.split(",")
    for name in dir(obj):
        if name[0] == "_": continue
        if name in selnames:
            print "Loading %s from %s " % (name, mod)
	    if name == "btagSFProducer":
            	modules.append(getattr(obj,name)(eraBtagSF))
	    else:
		modules.append(getattr(obj,name)())
