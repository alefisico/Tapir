from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import *
import numpy as np
from rootpy.tree import Tree
from rootpy.io import root_open

# analyzer to prepare the data for training or prediction
class NNAnalyzer(FilterAnalyzer):

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)

        # define the objects and variables for training/ predictions
        #self.obj = {"good_leptons":2, "good_jets":10}
        #self.obj = {"good_leptons":(2, ["pt", "eta", "phi", "mass"]), "MET": (1, ["pt", "sumEt", "phi"])}
        #self.obj_var = ["pt", "eta", "phi", "mass"]
        self.var = {"leptons":(2,["pt","eta", "phi", "mass"]), "jets":(10, ["pt", "eta", "phi", "mass"]), "met":(0, ["pt", "phi", "sumEt"])}

        self.training = True

        # open output file
        if self.training == True:
            self.output = open("training.csv", "w")

            # make header for file
            for o in ["leptons", "jets", "met"]:
                for var in self.var[o][1]:
                    for i in range(self.var[o][0]):
                        self.output.write(o + "_" + var + "_" + str(i) + " ")

            self.output.write("JLR\n")

    def process(self, event):

        features = []

        #import pdb
        #pdb.set_trace()

        # Leptons
        for var in self.var["leptons"][1]:
            for i in range(self.var["leptons"][0]):
                if i in range(len(getattr(event, "good_leptons"))):
                    io = getattr(event, "good_leptons")[i]
                    features.append(getattr(io,var))
                else:
                    features.append(0.)

        # Jets
        # check if training because otherwise also systematics have to be evaluated
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
            io = getattr(event, "met")
            features.append(getattr(io,var))


        # target: joint likelihood ratio
        if self.training == True:
            features.append(event.jointlikelihood)

        print features

        if self.training == True:
            for f in features:
                self.output.write("%f " %f)
            self.output.write("\n")

        return True
