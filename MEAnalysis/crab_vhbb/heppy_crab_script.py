#!/usr/bin/env python
import os, time, sys, re, imp
import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg
cfg.Analyzer.nosubdir=True
import PSet
args = sys.argv
if "--test" in sys.argv:
    import PSet_test as PSet

import copy
import json
from PhysicsTools.HeppyCore.framework.looper import Looper

def getLumisProcessed(vlumiblock): 
    lumidict = {}
    print vlumiblock
    for ll in vlumiblock:
        runs_lumis = map(lambda x: map(int, x.split(":")), ll.split("-"))
        print runs_lumis 
        if len(runs_lumis) == 1:
            run, lumi1 = tuple(runs_lumis[0])
            lumi2 = lumi1
        elif len(runs_lumis) == 2:
            rl1, rl2 = runs_lumis
            if rl1[0] != rl2[0]:
                raise Exception("run not equal: {0} {1}".format(rl1, rl2))
            run = rl1[0]
            lumi1 = rl1[1]
            lumi2 = rl2[1]
        else:
            raise Exception("unknown lumilist: {0}".format(ll))
        
        if not lumidict.has_key(run):
            lumidict[run] = []
        
        lumidict[run] += [i for i in range(lumi1, lumi2 + 1)]
    return lumidict

dumpfile = open("dump.txt", "w")

dumpfile.write(PSet.process.dumpPython())
dumpfile.write("\n")

t0 = time.time()
print "ARGV:",sys.argv

me_conf_name = "MEAnalysis_cfg_heppy.py"
for arg in sys.argv:
    if arg.startswith("ME_CONF="):
        me_conf_name = arg.split("=")[1]

crabFiles=PSet.process.source.fileNames
crabFiles_pfn = copy.deepcopy(PSet.process.source.fileNames)

###
### Convert LFN to PFN
###
##in case of ignoreLocality = True
#for i in xrange(0, len(crabFiles)) :
#    crabFiles[i]="root://cms-xrd-global.cern.ch/"+crabFiles[i]
print "--------------- using edmFileUtil to convert PFN to LFN -------------------------"
for i in xrange(0,len(crabFiles)) :
    if "file://" in crabFiles[i] or "root://" in crabFiles[i]:
        continue
    if (os.getenv("GLIDECLIENT_Group","") != "overflow" and
        os.getenv("GLIDECLIENT_Group","") != "overflow_conservative"):
        pfn=os.popen("edmFileUtil -d %s"%(crabFiles[i])).read()
        pfn=re.sub("\n","",pfn)
        print "replaced", crabFiles[i],"->",pfn
        crabFiles_pfn[i]=pfn
    else:
        print "data is not local" 
        crabFiles_pfn[i]="root://cms-xrd-global.cern.ch/"+crabFiles[i]

###
### VHBB code
###
handle = open("heppy_config.py", 'r')
cfo = imp.load_source("heppy_config", "heppy_config.py", handle)
config = cfo.config

#Setting lumis in file
lumisToProcess = None
lumidict = {}
if hasattr(PSet.process.source, "lumisToProcess"):
    lumisToProcess = PSet.process.source.lumisToProcess
    config.preprocessor.options["lumisToProcess"] = PSet.process.source.lumisToProcess
    lumidict = getLumisProcessed(lumisToProcess)
handle.close()

#replace files with crab ones
config.components[0].files=crabFiles_pfn

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

###
### tthbb13 code
###
if not "--nostep2" in args:
    print "Running tth code"
    
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    from TTH.MEAnalysis.MEAnalysis_heppy import main as tth_main
    from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str
    an = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default.cfg")
    an.mem_python_config = "$CMSSW_BASE/src/TTH/MEAnalysis/python/" + me_conf_name
    mem_python_conf = tth_main(
        an,
        schema="mc" if cfo.sample.isMC else "data",
        output_name="Output_tth",
        files="Output/tree.root"
    )
    dumpfile.write(conf_to_str(mem_python_conf))
    dumpfile.write("\n")
    print "timeto_doMEM ",(time.time()-t0)

#Now we need to copy both the vhbb and tth outputs to the same file
inf1 = ROOT.TFile("Output/tree.root")
inf2 = ROOT.TFile("Output_tth/tree.root")
tof = ROOT.TFile("tree.root", "RECREATE")
vhbb_dir = tof.mkdir("vhbb")
def copyTo(src, dst, keys=[]):
    #copy ttjets output
    dst.cd()
    if len(keys) == 0:
        keys = list(set([k.GetName() for k in src.GetListOfKeys()]))
    for k in keys:
        o = src.Get(k)
        if o.ClassName() == "TTree":
            o = o.CloneTree()
        else:
            o = o.Clone()
        print "copying", k, o
        dst.Add(o)
        o.Write("", ROOT.TObject.kOverwrite)

copyTo(inf1, vhbb_dir)
copyTo(inf2, tof)
tof.Close()


def getEntries(inf, tree):
    tf = ROOT.TFile(inf)
    tt = tf.Get(tree)
    n = tt.GetEntries()
    tf.Close()
    return n

assert(getEntries("Output/tree.root", "tree") == getEntries("tree.root", "vhbb/tree"))
assert(getEntries("Output_tth/tree.root", "tree") == getEntries("tree.root", "tree"))

def getEventsLumisInFile(infile):
    from DataFormats.FWLite import Lumis, Handle, Events
    events = Events(infile)
    lumis = Lumis(infile)

    ret = {}
    for lum in lumis:
        run = lum.aux().run()
        if not ret.has_key(run):
            ret[run] = []
        ret[run] += [lum.aux().id().luminosityBlock()]
    return events.size(), ret

def getFJR(lumidict, inputfiles_lfn, inputfiles_pfn, outputfile):

    fwkreport="""<FrameworkJobReport>
    <ReadBranches>
    </ReadBranches>
    <PerformanceReport>
      <PerformanceSummary Metric="StorageStatistics">
        <Metric Name="Parameter-untracked-bool-enabled" Value="true"/>
        <Metric Name="Parameter-untracked-bool-stats" Value="true"/>
        <Metric Name="Parameter-untracked-string-cacheHint" Value="application-only"/>
        <Metric Name="Parameter-untracked-string-readHint" Value="auto-detect"/>
        <Metric Name="ROOT-tfile-read-totalMegabytes" Value="0"/>
        <Metric Name="ROOT-tfile-write-totalMegabytes" Value="0"/>
      </PerformanceSummary>
    </PerformanceReport>
    
    <GeneratorInfo>
    </GeneratorInfo>
"""
    allruns = {}
    for infile_lfn, infile_pfn in zip(inputfiles_lfn, inputfiles_pfn):
        events, runs = getEventsLumisInFile(infile_pfn)
        for run, lumis in lumidict.items():
            if not allruns.has_key(run):
                allruns[run] = []
            allruns[run] += lumis

        allruns.update(runs)
        inf = """
        <InputFile>
        <LFN>%s</LFN>
        <PFN></PFN>
        <Catalog></Catalog>
        <InputType>primaryFiles</InputType>
        <ModuleLabel>source</ModuleLabel>
        <GUID></GUID>
        <InputSourceClass>PoolSource</InputSourceClass>
        <EventsRead>%d</EventsRead>
        <Runs>
        """ % (infile_lfn, events)
        for run, lumis in lumidict.items():
            inf += """<Run ID="%d">
            """ % run
            for lumisection in lumis:
                print run, lumisection
                inf += """<LumiSection ID="%d"/>
                """ % lumisection
            inf += """</Run>"""
        inf += """
        </Runs>
        </InputFile>
        """
        fwkreport += inf
    
    output_entries = 0
    tf = ROOT.TFile(outputfile)
    output_entries = tf.Get("vhbb/tree").GetEntries()

    fwkreport += """
    <File>
    <LFN></LFN>
    <PFN>%s</PFN>
    <Catalog></Catalog>
    <ModuleLabel>HEPPY</ModuleLabel>
    <Runs>
    """ % (outputfile)
    for run, lumis in lumidict.items():
        fwkreport += """<Run ID="%d">
        """ % run
        for lumisection in lumis:
            fwkreport += """<LumiSection ID="%d"/>
            """ % lumisection
        fwkreport += """</Run>"""

    fwkreport += """
    </Runs>
    <GUID></GUID>
    <OutputModuleClass>PoolOutputModule</OutputModuleClass>
    <TotalEvents>%d</TotalEvents>
    <BranchHash>dc90308e392b2fa1e0eff46acbfa24bc</BranchHash>
    </File>
    
    </FrameworkJobReport>""" % (output_entries)
    return fwkreport

#Now write the FWKJobReport

report=open('./FrameworkJobReport.xml', 'w+')
report.write(getFJR(lumidict, crabFiles, crabFiles_pfn, "tree.root"))
report.close()
print "timeto_totalJob ",(time.time()-t0)
dumpfile.close()
