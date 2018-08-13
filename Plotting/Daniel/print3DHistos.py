import sys
import ROOT

def getBinEdgeLine(histo, axis = "x"):
    if axis == "x":
        axis = histo.GetXaxis()
    elif axis == "y":
        axis = histo.GetYaxis()
    else:
        axis = histo.GetZaxis()

    bins = ""
    for ib in range(1, axis.GetNbins()+1):
        bins += str(axis.GetBinLowEdge(ib))
        if not ib == axis.GetNbins():
            bins += "\t"

    return bins

def getBinEdgeList(histo, axis = "x"):
    if axis == "x":
        axis = histo.GetXaxis()
    elif axis == "y":
        axis = histo.GetYaxis()
    else:
        axis = histo.GetZaxis()

    bins = []
    for ib in range(axis.GetNbins()+1):
        bins.append(axis.GetBinLowEdge(ib))
    return bins

def printTH3F(th3f, error = False):
    ptbins = getBinEdgeList(th3f, "y")
    for b in range(1,th3f.GetNbinsZ()+1):
        print "nBCSVM=={0}".format(th3f.GetZaxis().GetBinLowEdge(b))
        print "ht>\t",getBinEdgeLine(th3f)
        for p in range(1,th3f.GetNbinsY()+1):
            line = ""
            line += "6jpt>{0}\t".format(ptbins[p])
            for h in range(1,th3f.GetNbinsX()+1):
                if not error:
                    line += str(th3f.GetBinContent(h,p,b))
                else:
                    line += str(th3f.GetBinError(h,p,b))
                if h != th3f.GetNbinsX():
                    line += "\t"
            print line


if __name__ == "__main__":
    SFFile = sys.argv[1]
    rSFFile = ROOT.TFile(SFFile, "OPEN")
    SFHisto = rSFFile.Get("h3SF_tot")
    DataEffhisto = rSFFile.Get("h3Data_eff")
    MCEffhisto = rSFFile.Get("h3MC_eff")
    #DataDenomhisto =
    #MCDenomhisto =
    #DataNumhisto =
    #MCNumhisto =

    print "----------------------"
    print "*** Data Efficieny ***"
    printTH3F(DataEffhisto)
    print "----------------------"
    print "***  MC  Efficieny ***"
    printTH3F(MCEffhisto)
    
    print "---------------------"
    print "*** Scale factors ***"
    printTH3F(SFHisto)
    print "---------------------"
    print "*** SF errors ***"
    printTH3F(SFHisto, error = True)
    
