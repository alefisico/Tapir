#!/usr/bin/env python
"""
Retrieves the number of generated MC events from the input files and saves it
into an output file.
In nanoAOD, this number is stored in a separate TTree "Runs", which can simply
be added up from all the input files.
"""
import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix


def main(filenames, ofname):
    """
    Retrieves counts from input files and saves to output file.

    Args:
        filenames (list of strings): Input ROOT file names
        ofname (string): Output ROOT file name, will be created
    
    Returns:
        Output file name
    """
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
