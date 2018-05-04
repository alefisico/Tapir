import os
import os.path
import argparse
import ROOT

def makeDatacards(fpath, opath, prefix):

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
                tree = rf.Get("nanoAOD/Events")
                nevt = tree.GetEntries()  
              
                print prefix + cf + " = %i" % nevt
                dataset.write(prefix + cf + " = %i\n" % nevt)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="collect crab_nano output and make datacards")
    parser.add_argument("--path", required=True, help="path of crab output", type=str)
    parser.add_argument("--outpath", default="/mnt/t3nfs01/data01/shome/creissel/tth/2017/sw/CMSSW_9_4_5_cand1/src/TTH/MEAnalysis/gc/datasets", help="path to store datasets", type=str)                     
    parser.add_argument("--prefix", default="root://t3dcachedb03.psi.ch", help="prefix to add to rootfiles", type=str)
    args = parser.parse_args()

    makeDatacards(args.path, args.outpath, args.prefix)
