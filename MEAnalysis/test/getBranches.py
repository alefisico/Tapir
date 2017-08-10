import ROOT, sys, os
from TTH.MEAnalysis.samples_base import getSitePrefix

fn = sys.argv[1]
if os.path.isfile(fn):
    tf = ROOT.TFile(fn)
else:
    tf = ROOT.TFile.Open(getSitePrefix(fn))

if not tf:
    raise Exception("Could not open file")
tt = tf.Get(sys.argv[2])

branches = sorted([br.GetName() for br in tt.GetListOfBranches()])
for br in branches:
    print br

