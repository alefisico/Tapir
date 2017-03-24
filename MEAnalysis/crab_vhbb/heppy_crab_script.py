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

import copy
import json
from PhysicsTools.HeppyCore.framework.looper import Looper

import heppy_crab_functions as fn

dumpfile = open("dump.txt", "w") #new file created here

dumpfile.write(PSet.process.dumpPython())
dumpfile.write("\n")

t0 = time.time()
print "ARGV:",sys.argv

crabFiles=PSet.process.source.fileNames
crabFiles_pfn = copy.deepcopy(PSet.process.source.fileNames)

fn.convertLFN(crabFiles,crabFiles_pfn)

### setup crab info
handle = open("heppy_config.py", 'r')
cfo = imp.load_source("heppy_config", "heppy_config.py", handle)
config = cfo.config

#Setting lumis in file
lumisToProcess = None
lumidict = {}
if hasattr(PSet.process.source, "lumisToProcess"):
    lumisToProcess = PSet.process.source.lumisToProcess
    config.preprocessor.options["lumisToProcess"] = PSet.process.source.lumisToProcess
    lumidict = fn.getLumisProcessed(lumisToProcess)
handle.close()

#replace files with crab ones
config.components[0].files=crabFiles_pfn

### vhbb code
if not "--nostep1" in args:
    print "heppy_config", config
    if hasattr(PSet.process.source, "skipEvents") and PSet.process.source.skipEvents.value()>=0:
        nfirst = int(PSet.process.source.skipEvents.value())
        nmax = int(PSet.process.maxEvents.input.value())
        looper = Looper( 'Output', config, nPrint=0, nEvents=nmax, firstEvent=nfirst)
    else:
        looper = Looper( 'Output', config, nPrint=0)
    looper.loop()
    looper.write()
    
    tf = ROOT.TFile("Output/tree.root")
    if not tf or tf.IsZombie():
        raise Exception("Error occurred in processing step1")
    tt = tf.Get("tree")
    print "step1 tree={0}".format(tt.GetEntries())
    tf.Close()
    
    print "timeto_doVHbb ",(time.time()-t0)

### run tthbb13 code separately

#Write the FWKJobReport after the mem step

print "timeto_FirstHalf ",(time.time()-t0)
dumpfile.close() #will reopen in append mode later
