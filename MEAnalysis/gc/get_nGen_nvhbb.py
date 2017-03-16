#!/usr/bin/env python
from TTH.MEAnalysis.ParHadd import par_hadd
import ROOT
import glob
import sys
import os, fnmatch

filenames = {
    "datasets/FHwithme_2pcrel_1_T3/ttHTobb_M125_13TeV_powheg_pythia8.txt",
    "datasets/FHwithme_2pcrel_1_T3/ttHToNonbb_M125_13TeV_powheg_pythia8.txt",
    "datasets/FHwithme_2pcrel_1_T3/TT_TuneCUETP8M1_13TeV-powheg-pythia8.txt",
    "datasets/FHwithme_2pcrel_1_T3/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",  
    "datasets/FHwithme_2pcrel_1_T3/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",
    "datasets/FHwithme_2pcrel_1_T3/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",
    "datasets/FHwithme_2pcrel_1_T3/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",
    "datasets/FHwithme_2pcrel_1_T3/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",
    "datasets/FHwithme_2pcrel_1_T3/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt"
}

prefix = "root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat"

print "sample nvhbb nGen %"
for fname in filenames:
    nGen = 0
    nvhbb = 0
    sample = fname.split("/")[2].split("_13TeV")[0]
    print sample
    continue
    f = open(fname)
    lines = f.readlines()
    for l in lines:
        if not (l.find('.root')>0):
            continue
        rootfile = l.split()[0]
        longfile = prefix+rootfile
        #print longfile
        file_ = ROOT.TFile.Open(longfile)
        count_gen = file_.Get("vhbb/Count")
        count_vhbb = file_.Get("CounterAnalyzer_count")
        #print l
        #print type( count_gen)
        #print type( count_vhbb)
        nGen += count_gen.GetBinContent(1)
        nvhbb += count_vhbb.GetBinContent(1)

    print sample,nvhbb,nGen,(100.0*nvhbb/nGen)
