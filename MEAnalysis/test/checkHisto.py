import ROOT, sys

tf = ROOT.TFile(sys.argv[1])

for k in tf.GetListOfKeys():
    o = k.ReadObj()
    cn = o.__class__.__name__
    if cn.startswith("TH"):
        print o.GetName(), o.Integral(), o.GetEntries()
