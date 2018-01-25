import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix


def main(filenames, ofname):
    filenames_pref = map(getSitePrefix, filenames)
    of = ROOT.TFile(ofname, "RECREATE")
    tree_list = ROOT.TList()

    #keep tfiles open for the duration of the merge
    tfiles = []
    for infn, lfn in zip(filenames_pref, filenames):
        tf = ROOT.TFile.Open(infn)
        tfiles += [tf]

        run_tree = tf.Get("Runs")
        tree_list.Add(run_tree)

    of.cd()
    out_tree = ROOT.TTree.MergeTrees(tree_list)
    out_tree.Write()
    of.Close()
    return ofname

if __name__ == "__main__":
    filenames = sys.argv[2:]
    ofname = sys.argv[1]
    print main(filenames, ofname)
