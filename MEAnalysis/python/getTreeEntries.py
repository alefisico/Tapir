import ROOT, sys

for fn in sys.stdin.readlines():
    f = ROOT.TFile.Open("root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/" + fn.strip())
    
    t = f.Get("vhbb/tree")
    print "{0} = {1}".format(fn, t.GetEntries())
    
    f.Close()
