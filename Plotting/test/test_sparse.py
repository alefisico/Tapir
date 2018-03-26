import ROOT
import TTH.Plotting.Datacards.sparse as sparse

h = ROOT.TH1D("h", "h", 100, 0, 300)

d = {}
d["a/b/c/bla"] = h

sparse.save_hdict(ofn="out.root", hdict=d)
