from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import *
import numpy as np
from rootpy.tree import Tree
from rootpy.io import root_open

# analyzer to prepare the data for training or prediction
class NNAnalyzer(FilterAnalyzer):

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)

        # defines which information is written to the output files, options = ["GenLevel", "PartLevel", "RecoLevel"]
        self.setup = "RecoLevel"

        # define the objects and variables for training/ predictions
        #self.var = {"leptons":(2,["pt","eta", "phi", "mass"]), "jets":(10, ["pt", "eta", "phi", "mass", "btagDeepCSV"]), "met":(0, ["pt", "phi", "sumEt"]), "high_level_var":(0,["nBDeepCSVM", "mbb_closest", "Wmass", "ht30"])}
        if self.setup == "RecoLevel":
            self.var = {"leptons":(2,["pt","eta", "phi", "mass"]), "jets":(10, ["pt", "eta", "phi", "mass", "btagDeepCSV"]), "met":(0, ["pt", "phi", "sumEt"]), "high_level_var":(0,["nBDeepCSVM", "mbb_closest", "ht30"])}
        elif self.setup == "PartLevel":
            self.var = {"leptons":(2,["pt","eta", "phi", "mass"]), "jets":(10, ["pt", "eta", "phi", "mass"]), "nu":(2, ["pt", "eta", "phi"])}
        else:
            self.var = None

        self.training = True

        # open output file
        if self.training == True:
            self.output = open("training.csv", "w")

            # make header for file
            if self.setup != "PartLevel":

                if self.setup != "GenLevel":
                    l = ["leptons", "jets", "met", "high_level_var"]
                else:
                    l = ["leptons", "jets", "nu"]
                for o in l:
                    if o == "leptons" or o == "jets" or o == "nu":
                        self.output.write("num_" + o + " ")
                    for var in self.var[o][1]:
                        if self.var[o][0] > 0:
                            for i in range(self.var[o][0]):
                                self.output.write(o + "_" + var + "_" + str(i) + " ")
                        else:
                            if o == "high_level_var":
                                self.output.write(var + " ")
                            else:
                                self.output.write(o + "_" + var + " ")
            else:

                for o in ["top", "atop", "bottom", "abottom"]:
                    for var in ["pt", "eta", "phi", "mass"]:
                        self.output.write(o + "_" + var + " ")

            self.output.write("prob_ttH ")
            self.output.write("prob_ttbb ")
            self.output.write("JLR\n")

    def process(self, event):

        features = []


        if self.setup == "RecoLevel":

            # Leptons
            features.append(len(getattr(event.systResults["nominal"], "good_leptons")))
            for var in self.var["leptons"][1]:
                for i in range(self.var["leptons"][0]):
                    if i in range(len(getattr(event.systResults["nominal"], "good_leptons"))):
                        io = event.systResults["nominal"].good_leptons[i]
                        features.append(getattr(io,var))
                    else:
                        features.append(0.)

            # Jets
            # check if training because otherwise also systematics have to be evaluated
            features.append(len(event.systResults["nominal"].good_jets))
            if self.training == True:
                for var in self.var["jets"][1]:
                    for i in range(self.var["jets"][0]):
                        if i in range(len(event.systResults["nominal"].good_jets)):
                            io = event.systResults["nominal"].good_jets[i]
                            features.append(getattr(io,var))
                        else:
                            features.append(0.)

            # MET
            for var in self.var["met"][1]:
                io = getattr(event.systResults["nominal"], "met")
                features.append(getattr(io,var))
        

            # high level variables
            for var in self.var["high_level_var"][1]:
                io = getattr(event.systResults["nominal"], var)
                features.append(float(io))


        if self.setup == "GenLevel":
    
            # Leptons
            features.append(len(event.GenLep))
            for var in self.var["leptons"][1]:
                for i in range(self.var["leptons"][0]):
                    if i in range(len(event.GenLep)):
                        io = event.GenLep[i]
                        features.append(getattr(io,var))
                    else:
                        features.append(0.)

            # Jets
            features.append(len(event.GenJet))
            if self.training == True:
                for var in self.var["jets"][1]:
                    for i in range(self.var["jets"][0]):
                        if i in range(len(event.GenJet)):
                            io = event.GenJet[i]
                            features.append(getattr(io,var))
                        else:
                            features.append(0.)

            # Nu
            features.append(len(event.GenNu))
            for var in self.var["nu"][1]:
                for i in range(self.var["nu"][0]):
                    if i in range(len(event.GenNu)):
                        io = event.GenNu[i]
                        features.append(getattr(io,var))
                    else:
                        features.append(0.)

        if self.setup == "PartLevel":
        
            for p in ["top", "atop", "bottom", "abottom"]:
                LZ = getattr(event, "jlr_" + p)
                features.append(LZ.Pt())
                features.append(LZ.Eta())
                features.append(LZ.Phi())
                features.append(LZ.M())

        # target: joint likelihood ratio
        if self.training == True:
            features.append(np.log10(event.prob_ttHbb))
            features.append(np.log10(event.prob_ttbb))
            features.append(np.log10(event.jointlikelihood))


        print features

        if self.training == True:
            for f in features:
                self.output.write("%f " %f)
            self.output.write("\n")

        return True
