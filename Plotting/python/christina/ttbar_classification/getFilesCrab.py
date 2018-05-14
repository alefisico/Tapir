import os
import os.path
import argparse
import ROOT

def makeDatacards(fpath, opath, prefix, treename):
   
    #need /-terminated string
    if not fpath.endswith("/"):
        fpath += "/"

    dirs = os.listdir(fpath)
    tag = os.path.split(os.path.dirname(fpath))[1]
    print tag

    outpath = opath + "/" + tag + "/" 

    out = os.path.dirname(outpath)
    if not os.path.exists(out):
        os.makedirs(outpath)


    for d in dirs:

        dataset = open(outpath + d + ".txt", "w")
        print ("[" + d + "]")
        dataset.write("[" + d + "]\n")

        for dirpath, dirnames, filenames in os.walk(fpath+d):
            for filename in [f for f in filenames if f.endswith(".root")]:
                cf = os.path.join(dirpath, filename)
                rootfile = prefix +cf

                # get number of entries
                rf = ROOT.TFile.Open(rootfile)
                tree = rf.Get(treename)
                nevt = tree.GetEntries()  
              
                print prefix + cf + " = %i" % nevt
                dataset.write(prefix + cf + " = %i\n" % nevt)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="collect crab_nano output and make dataset .txt files")
    parser.add_argument("--path", required=True, help="path of crab output, e.g. /pnfs/psi.ch/cms/trivcat/store/user/algomez/tth/May08_t1/", type=str)
    parser.add_argument("--outpath", default="/mnt/t3nfs01/data01/shome/creissel/tth/2017/sw/CMSSW_9_4_5_cand1/src/TTH/MEAnalysis/gc/datasets", help="path to store dataset .txt files", type=str)
    parser.add_argument("--prefix", default="root://t3dcachedb.psi.ch", help="server prefix to add to rootfiles", type=str)
    parser.add_argument("--treename", default="nanoAOD/Events", help="Name of the TTree to retrieve the number of events from", type=str)
    args = parser.parse_args()

    makeDatacards(args.path, args.outpath, args.prefix, args.treename)
