import ROOT, sys


for fn in sys.argv[1:]:
    f = ROOT.TFile(fn)
    countw = 0
    tree = f.Get("Runs")
    for ient in range(tree.GetEntries()):
        tree.GetEntry(ient)
        countw += tree.genEventSumw
    print fn, countw
