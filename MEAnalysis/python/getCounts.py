import ROOT, sys
from glob import glob

if len(sys.argv) == 2 and not sys.argv[1].endswith(".root"):
    files = glob(sys.argv[1]+"/*.root")
    sys.argv = [sys.argv[0]] + files


for fn in sys.argv[1:]:
    f = ROOT.TFile(fn)
    countw = 0
    countgen = 0
    tree = f.Get("Runs")
    for ient in range(tree.GetEntries()):
        tree.GetEntry(ient)
        countw += tree.genEventSumw
        countgen += tree.genEventCount
    print fn, countw, countgen
