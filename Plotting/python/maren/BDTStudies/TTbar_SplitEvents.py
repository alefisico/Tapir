#imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
from array import array
import os.path
import argparse

import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf


########################################
# Define helper functions
########################################

def SortEvents(infile,outfile,match):


    print match



    f = ROOT.TFile.Open(infile, "READ")
    ttree = f.Get("t2")
    nentries = ttree.GetEntries()
    #TTHTree tree(oldtree)
    #ttree.set_branch_addresses()

  
    #Create a new file + a clone of old tree in new file
    out = ROOT.TFile("{}".format(outfile),"recreate")
    newtree = ttree.CloneTree(0)
    counter = 0
    for event in ttree :
        #print match, event.fromtop
        if counter%1000==0:
            print counter
        if match == "True" and event.fromtop == 1:
            newtree.Fill()
        elif match == "False" and event.fromtop == 0:
            newtree.Fill()
        counter += 1

        #event->Clear();
    print newtree.GetEntries()
    newtree.Print()
    newtree.AutoSave()
    f.Close()
    out.Close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="collect crab_nano output and make dataset .txt files")
    parser.add_argument("--input", required=True, help="Input root file", type=str)
    parser.add_argument("--output", required=True, help="New output file", type=str)
    parser.add_argument("--match", default=True, help="Whether to get matched to top candidates or not", type=str)
    args = parser.parse_args()

    SortEvents(args.input, args.output, args.match)