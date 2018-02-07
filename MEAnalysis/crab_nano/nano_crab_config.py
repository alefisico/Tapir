###################################################################################################
###################################################################################################
#####################################  nanoAOD production #########################################
###################################################################################################
###################################################################################################
#
# Configure this variables:
setEra = "80X" # Options: 80X, 92X, 94X



#
###################################################################################################
if setEra == "80X":
    eraMC = "Run2_2016,run2_miniAOD_80XLegacy"
    eraData = "Run2_2016,run2_miniAOD_80XLegacy"
    conditionsMC = "auto:run2_mc"
    conditionsData = "auto:run2_data_relval"
elif setEra == "92X":
    eraMC = "Run2_2017,run2_nanoAOD_92X"
    eraData = "Run2_2017,run2_nanoAOD_92X"
    conditionsMC = "auto:phase1_2017_realistic"
    conditionsData = "auto:run2_data_relval"
elif setEra == "94X":
    eraMC = "Run2_2017"
    eraData = None
    conditionsMC = "auto:phase1_2017_realistic"
    conditionsData = None
    print "Not working yet"
    exit()
###################################################################################################
###################################################################################################
################################# nanoAOD postprocessing ##########################################
###################################################################################################
###################################################################################################
#
# Configure this variables:
imports = [('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties', 'jecUncertAll')] 
json = None
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
            modules.append(getattr(obj,name)())
