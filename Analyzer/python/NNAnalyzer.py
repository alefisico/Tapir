import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from TTH.Analyzer.utils import *
import numpy as np
from rootpy.tree import Tree
from rootpy.io import root_open
import os

import tensorflow as tf
from tensorflow.contrib import predictor

# analyzer to prepare the data for training or prediction
class NNAnalyzer(Module):

    def __init__(self, tag):
        self.tag = tag

    def beginJob(self):

        # load models for SL, DL, FH
        tag = self.tag
        self.model = {}
        # for tests: load model only for DL -> replace later when all training available
        #for i in ["sl", "dl", "fh"]:
        for i in ["dl"]:
            path = os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/dnn/" + i + "/" + tag
            self.model[i] = predictor.from_saved_model(path)

    def make_array(self, evt_info, feats, dim):
        arr = np.zeros(dim)

        for obj in evt_info:
            if evt_info.index(obj) < dim[1]:
                for f in feats:
                    if f == "en":
                        attr = np.sqrt(obj.mass**2 + (1+np.sinh(obj.eta)**2)*obj.pt**2)
                    elif f == "px":
                        attr = obj.pt * np.cos(obj.phi)
                    elif f == "py":
                        attr = obj.pt * np.sin(obj.phi)
                    elif f == "pz":
                        attr = obj.pt * np.sinh(obj.eta)
                    else:
                        attr = getattr(obj, f)
                    arr[0, evt_info.index(obj), feats.index(f)] = attr

        return arr

    def analyze(self, event):

        event.dnn_ttH = -1.

        # get numpy arrays for jets, leps, met
        # todo: load features from DNN code automatically by tag
        met_feats = ["phi", "pt", "px", "py"]
        jet_feats = ["pt","eta","phi","en","px","py","pz","btagCSV"]
        lep_feats = ["pt","eta","phi","en","px","py","pz"]

        leps = self.make_array(event.good_leptons, lep_feats, (1,2,len(lep_feats)))
        jets = self.make_array(event.systResults["nominal"].good_jets, jet_feats, (1,10,len(jet_feats)))

        met = np.array([getattr(event.MET, feat) for feat in met_feats])
        met = met.reshape([-1, len(met)])

        # get prediction from DNN model
        # todo: update for multiclassification
        if event.is_dl:
            pred = self.model["dl"]({"cmb_jet_inp:0" : jets, "cmb_lep_inp:0" : leps, "cmb_met_inp:0" : met})
            p = float(pred['cmb_out/Sigmoid:0'][0])
            event.dnn_ttH = p

        return True