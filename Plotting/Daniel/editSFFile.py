import ROOT

def editSFFile(inputFile, outputFile, xyzVar, histoname, findbyValue, draw = False):
    editing = True
    print "+-----------------------------------------------------------------+"
    print "| With this script BinContents of a TH3F can be edited. This will |"
    print "| only effect the content while the error stays unchnaged. When   |"
    print "| prompted please input three ints (for the three dimentions)     |"
    print "| separated by whitespace.                                        |"
    print "+-----------------------------------------------------------------+"
    print "Using input file: "+inputFile
    print "Using output file: "+outputFile
    xVar = xyzVar[0]
    yVar = xyzVar[1]
    zVar = xyzVar[2]
    print "Following variable configuration set: x|{0} - y|{1} - z|{2}".format(xVar, yVar, zVar)
    if not findbyValue:
        print "Will use bin numbers instead of values to find the bin!"
    rFile = ROOT.TFile(inputFile, "OPEN")
    inHisto = rFile.Get(histoname)
    h2mod = inHisto.Clone(inHisto.GetName()+"_mod")
    if draw:
        c1 = ROOT.TCanvas("c1","c1",600,600)
        c1.cd()
        h2mod.Draw("LEGO2")
        c1.Update()
    xLowerBound = h2mod.GetXaxis().GetBinLowEdge(1)
    xUpperBound = h2mod.GetXaxis().GetBinUpEdge(h2mod.GetXaxis().GetNbins())
    yLowerBound = h2mod.GetYaxis().GetBinLowEdge(1)
    yUpperBound = h2mod.GetYaxis().GetBinUpEdge(h2mod.GetYaxis().GetNbins())
    zLowerBound = h2mod.GetZaxis().GetBinLowEdge(1)
    zUpperBound = h2mod.GetZaxis().GetBinUpEdge(h2mod.GetZaxis().GetNbins())
    while editing:
        intuple = raw_input("Enter tuple of {0}, {1}, {2}: ".format(xVar, yVar, zVar))
        if intuple == "":
            print "-----> Please enter something"
            continue
        intuple = intuple.split(" ")
        intuple = [int(i) for i in intuple]
        if len(intuple) != 3:
            print "-----> Please enter exactly three numbers"
            continue
        x,y,z = intuple
        if findbyValue:
            if x > xUpperBound or x < xLowerBound:
                print "-----> x Variable outside bin boundries"
                continue
            if y > yUpperBound or y < yLowerBound:
                print "-----> y Variable outside bin boundries"
                continue
            if z > zUpperBound or z < zLowerBound:
                print "-----> z Variable outside bin boundries"
                continue
            selectedBin = h2mod.FindBin(x,y,z)
        else:
            if x > h2mod.GetXaxis().GetNbins() or x < 0:
                print "-----> x Bin outside bin boundries"
                continue
            if y > h2mod.GetYaxis().GetNbins() or y < 0:
                print "-----> y Bin outside bin boundries"
                continue
            if z > h2mod.GetZaxis().GetNbins() or z < 0:
                print "-----> z Bin outside bin boundries"
                continue
            selectedBin = h2mod.GetBin(x,y,z)
        print "Selected bin {0} with value {1}".format(selectedBin, h2mod.GetBinContent(selectedBin))
        newValue = float(raw_input("Please enter the new value for this bin: "))
        print "Will replace {0} with {1}".format(h2mod.GetBinContent(selectedBin), newValue)
        h2mod.SetBinContent(selectedBin, newValue)
        if draw:
            h2mod.Draw("LEGO2")
            c1.Update()
        validanswer = False
        while not validanswer:
            answer = raw_input("Continue editing bins? Enter y or n: ")
            if answer.lower() in ["y","n"]:
                validanswer = True
        if answer == "n":
            editing = False

    print "Saving output file:",outputFile
    rOutput = ROOT.TFile(outputFile, "RECREATE")
    rOutput.cd()
    h2mod.Write()
    rOutput.Close()
    
        
if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Description'
    )
    argumentparser.add_argument(
        "--input",
        action = "store",
        required = True,
        type = str,
        help = "Path to input file",
    )
    argumentparser.add_argument(
        "--output",
        action = "store",
        required = True,
        type = str,
        help = "Path to output file",
    )
    argumentparser.add_argument(
        "--histoName",
        action = "store",
        required = False,
        type = str,
        default = "h3SF_tot",
        help = "Name of the TH3F to be edited",
    )
    argumentparser.add_argument(
        "--vars",
        nargs='3',
        action = "store",
        required = False,
        type = tuple,
        default = ("HT", "pt6", "nBCSVM"),
        help = "x,y,z variables",
    )
    argumentparser.add_argument(
        "--useBinNumbers",
        action = "store_false",
        help = "If this is set, bin numbers instead of values are used to find the 3d Bin",
    )
    argumentparser.add_argument(
        "--drawprogress",
        action = "store_true",
        help = "If this is set, the histogram will be displayed between steps",
    )
    args = argumentparser.parse_args()    
    editSFFile(inputFile = args.input, outputFile = args.output, xyzVar = args.vars, histoname = args.histoName, findbyValue = args.useBinNumbers, draw = args.drawprogress)
