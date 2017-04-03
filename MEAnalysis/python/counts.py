import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix


def get_tree_entries(treename, filenames):
    tt = ROOT.TChain(treename)
    for fi in filenames:
        print "adding", fi
        tt.AddFile(fi)
    i = tt.GetEntries()
    return i

def main(filenames, ofname):
    filenames_pref = map(getSitePrefix, filenames)
    of = ROOT.TFile(ofname, "RECREATE")
    good_filenames = []
    count_dict = {}
    count_dict["Count"] = 0

    count_dict["failed"] = []
    count_dict["good_files"] = []
    for infn, lfn in zip(filenames_pref, filenames):
        print "trying to open {0}".format(infn)
        tf = ROOT.TFile.Open(infn)
        
        print "good file", infn, tf
        good_filenames += [lfn]
        vhbb_dir = tf.Get("vhbb")
        if not vhbb_dir:
            vhbb_dir = tf
        for k in vhbb_dir.GetListOfKeys():
            kn = k.GetName()
            if "Count" in kn:
                o = k.ReadObj()
                if not count_dict.has_key(kn):
                    count_dict[kn] = 0
                count_dict[kn] += o.GetBinContent(1)
                if not of.Get(kn):
                    print "first file, creating histogram", kn
                    o2 = o.Clone()
                    of.Add(o2)
                else:
                    of.Get(kn).Add(o)
        of.Write()
        tf.Close()
    count_dict["good_files"] = good_filenames
    
    #hEntries = ROOT.TH1D("numEntries", "numEntries", 3, 0, 3)
    #hEntries.SetDirectory(of)
    #hEntries.SetBinContent(1, get_tree_entries("vhbb/tree", good_filenames))
    #hEntries.SetBinContent(2, get_tree_entries("tree", good_filenames))
    #hEntries.Write()
    
    of.Close()
    return count_dict

if __name__ == "__main__":
    filenames = sys.argv[2:]
    ofname = sys.argv[1]
    main(filenames, ofname)
