#!/usr/bin/env python
import os, time, sys, re, imp
import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg
cfg.Analyzer.nosubdir=True
import PSet
args = sys.argv
if "--test" in sys.argv:
    import PSet_test as PSet
elif "--local" in sys.argv:
    import PSet_local as PSet
    print PSet

if "--isMC" in sys.argv:
    isMC = True
elif "--isData" in sys.argv:
    isMC = False
else:
    print "No MC flag in scirpt --> falling back to isMC = True"
    isMC = True
    
import copy
import json
import nano_crab_config as nanoCFG


import heppy_crab_functions as fn

dumpfile = open("dump.txt", "w") #new file created here

dumpfile.write(PSet.process.dumpPython())
dumpfile.write("\n")

t0 = time.time()
print "ARGV:",sys.argv


#Load necessary variables from PSet:
crabFiles=PSet.process.source.fileNames
crabFiles_pfn = copy.deepcopy(PSet.process.source.fileNames)
crabnfirst = int(PSet.process.source.skipEvents.value())
crabMaxEvents = PSet.process.maxEvents.input.value()


print crabFiles
fn.convertLFN(crabFiles,crabFiles_pfn)
print "-------------------------",crabFiles_pfn


#Setting lumis in file
#TODO!!! Figure out how to tell cmsDriver the lumi sections!
# ---> --lumiToProcess= specify a certification json file in input to run on
#                       certified data
lumisToProcess = None
lumidict = {}
"""
if hasattr(PSet.process.source, "lumisToProcess"):
    lumisToProcess = PSet.process.source.lumisToProcess
    config.preprocessor.options["lumisToProcess"] = PSet.process.source.lumisToProcess
    lumidict = fn.getLumisProcessed(lumisToProcess)
"""

os.system("mkdir Output")

### nanoAOD code
if not "--nostep1" in args:
    
    driverCommand = "cmsDriver.py {0} --fileout=Output/nanoAOD.root  -s NANO --filein {1} -n {2}" .format("", crabFiles.value()[0], crabMaxEvents)
    if isMC:
        conditions = nanoCFG.conditionsMC
        era = nanoCFG.eraMC
        eventcontent = "NANOAODSIM"
        driverCommand = "{0} --eventcontent {1} --datatier {1} --mc --conditions {2} --era {3}".format(driverCommand, eventcontent, conditions, era)
    else:
        conditions = nanoCFG.conditionsData
        era = nanoCFG.eraData
        eventcontent = "NANOAOD"
        driverCommand = "{0} --eventcontent {1} --datatier {1} --data --conditions {2} --era {3}".format(driverCommand, eventcontent, conditions, era)

    print "Running cmsDriver command:"
    print driverCommand

    #Run cmsDriver
    os.system(driverCommand+" &> Output/cmsRun.log")
    #This produdes file named: [name]_NANO.root                                       

    
    tf = ROOT.TFile("Output/nanoAOD.root")
    if not tf or tf.IsZombie():
        raise Exception("Error occurred in processing step1")
    tt = tf.Get("Events")
    print "step1 tree={0}".format(tt.GetEntries())
    tf.Close()
    
    print "timeto_donanoAOD ",(time.time()-t0)

t1 = time.time()
    
### Run nanoAOD postprocessing
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor



outdir = "Output"
if "--nostep1" in args:
    infiles = inputfiles #Use the inputdataset as input for postprocessing -> Check if DS is really nanoAOD?
else:
    infiles = ["Output/nanoAOD.root"] #Use nanoAOD output as input for postprocessing
cuts = nanoCFG.cuts
branchsel = nanoCFG.branchsel
json = nanoCFG.json
if isMC:
    json = None
modules = nanoCFG.modules

print "Starting postprocessor:"
p=PostProcessor(outdir, infiles, cuts, branchsel, modules, "LZMA:9", False, "_postprocessed", json, False, False)
p.run()

print "timeto_donanoAODpostprocessing", (time.time() - t1)
### run tthbb13 code separately
tf = ROOT.TFile("Output/nanoAOD_postprocessed.root")
if not tf or tf.IsZombie():
    raise Exception("Error occurred in processing step1")
tt = tf.Get("Events")
print "step1.5 tree={0}".format(tt.GetEntries())
tf.Close()
#Write the FWKJobReport after the mem step

print "timeto_FirstHalf ",(time.time()-t0)
dumpfile.close() #will reopen in append mode later
