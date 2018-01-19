import ROOT, sys

d = {}
d2 = {}
d3 = {}
for fn in sys.argv[1:]:
    f = ROOT.TFile(fn)
    
    h = f.Get("Count")
    d[fn.split("/")[-1].split(".")[0]] = h.GetBinContent(1)
    
    
    h1 = f.Get("CountPosWeight")
    h2 = f.Get("CountNegWeight")
    d2[fn.split("/")[-1].split(".")[0]] = h1.GetBinContent(1) - h2.GetBinContent(1)
    
    h = f.Get("CountFullWeighted")
    d3[fn.split("/")[-1].split(".")[0]] = h.GetBinContent(1)

for k in sorted(d.keys()):
    print k, d[k], d2[k], d3[k]
