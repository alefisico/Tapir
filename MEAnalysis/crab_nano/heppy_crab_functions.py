#!/usr/bin/env python
import os, re
import ROOT

def updateJetGT(config, crabFiles):
    print "Setting Data GT if needed"
    mm=re.match('.*(Run2016.).*',crabFiles[0])
    gtmap={}
    gtmap["Run2016B"]='Summer16_23Sep2016BCDV4_DATA'
    gtmap["Run2016C"]='Summer16_23Sep2016BCDV4_DATA'
    gtmap["Run2016D"]='Summer16_23Sep2016BCDV4_DATA'
    gtmap["Run2016E"]='Summer16_23Sep2016EFV4_DATA'
    gtmap["Run2016F"]='Summer16_23Sep2016EFV4_DATA'
    gtmap["Run2016G"]='Summer16_23Sep2016GV4_DATA'
    gtmap["Run2016H"]='Summer16_23Sep2016HV4_DATA'
    
    for x in config.sequence :
      if x.name == "PhysicsTools.Heppy.analyzers.objects.JetAnalyzer.JetAnalyzer_1" :
        JetAna=x
    if mm :
      JetAna.dataGT=gtmap[mm.group(1)]
      print "Updated data GT: ", JetAna.dataGT
    
def convertLFN(crabFiles,crabFiles_pfn):
    print "--------------- using edmFileUtil to convert PFN to LFN -------------------------"
    for i in xrange(0,len(crabFiles)) :
        if "file:/" in crabFiles[i] or "root://" in crabFiles[i]:
            continue
        if not ("overflow" in os.getenv("GLIDECLIENT_Group","overflow")):
            pfn=os.popen("edmFileUtil -d %s"%(crabFiles[i])).read()
            pfn=re.sub("\n","",pfn)
            print "replaced", crabFiles[i],"->",pfn
            crabFiles_pfn[i]=pfn
        else:
            print "data is not local" 
            crabFiles_pfn[i]="root://cms-xrd-global.cern.ch/"+crabFiles[i]


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

def getEntries(inf, tree):
    tf = ROOT.TFile(inf)
    tt = tf.Get(tree)
    n = tt.GetEntries()
    tf.Close()
    return n

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
