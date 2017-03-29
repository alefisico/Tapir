#!/usr/bin/env python
"""
Run the combine limit setting tool
"""

########################################
# Imports
########################################

import os, sys
import shutil
import datetime
import subprocess
import ROOT
import numpy as np

from EnvForCombine import PATH, LD_LIBRARY_PATH, PYTHONPATH, GENREFLEX, ROOTSYS, ROOT_INCLUDE_PATH, CMSSW_BASE

def get_limits_asymptotic(fn):
    """
    Returns a length 6 vector with the expected limits and quantiles based on the
    combine root file.
    """
    f = ROOT.TFile(fn)

    #No root file created, fit failed
    if f==None or f.IsZombie():
        lims = np.zeros(6)
        quantiles = np.zeros(6)
        lims[:] = 99999
        return lims, quantiles
    tt = f.Get("limit")
    if tt==None or tt.IsZombie():
        lims = np.zeros(6)
        quantiles = np.zeros(6)
        lims[:] = 99999
        return lims, quantiles
    lims = np.zeros(6)
    quantiles = np.zeros(6)
    for i in range(tt.GetEntries()):
        tt.GetEntry(i)
        lims[i] = tt.limit
        quantiles[i] = tt.quantileExpected
    f.Close()
    return lims, quantiles

def get_limits_mlfit(fn):
    f = ROOT.TFile(fn)
    tt = f.Get("tree_fit_sb")
    tt.GetEntry(0)
    return tt.mu, 0.0

class LimitGetter(object):
    
    def __init__(self, output_path = "."):
        self.output_path = output_path

    def __call__(self,
            datacard,
            name_extended="",
            opts=["-M", "Asymptotic"],
            output_format="higgsCombine{process_name}.Asymptotic.mH120.root",
            get_limits=get_limits_asymptotic
        ):

        datacard_path, datacard_name = os.path.split(datacard)

        # Add a timestamp to the name
        process_name = "{0}".format(
            os.path.splitext(datacard_name)[0]
        ) + name_extended

        # Run combine
        combine_command = ["combine", 
                           "-n", process_name,
                           "-t", "-1"
        ] + opts + [datacard_name]
        
        print "running combine"
        print " ".join(combine_command)
        
        process = subprocess.Popen(combine_command,
                                   stdout=subprocess.PIPE,
                                   cwd=datacard_path,
                                   env=dict(os.environ, 
                                            PATH=PATH,
                                            LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                            PYTHONPATH=PYTHONPATH,
                                            ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                                            ROOTSYS = ROOTSYS,
                                            GENREFLEX = GENREFLEX
                                        ))
        
        output, stderr = process.communicate()
        if process.returncode != 0:
            print "error running limit", stderr
        print output

        # Put the output file in the correct place..
        # ..root file
        output_rootfile_name = output_format.format(process_name=process_name)
        targetpath = os.path.join(self.output_path, output_rootfile_name)
        shutil.move(os.path.join(datacard_path, output_rootfile_name),
                   targetpath)
        # ..text file
        output_textfile_name = "out_{0}.log".format(process_name)
        of = open(os.path.join(self.output_path, output_textfile_name), "w")
        of.write(output)
        
        # And extact the limit
        lims, quantiles = get_limits(targetpath)
        return lims, quantiles
    # End of get_limit

    def runSignalInjection(self, datacard):
        limits = []
        for sig in [0.0, 1.0, 2.0, 3.0]:
            res = self(
                datacard,
                name_extended="_sig_{0:.2f}".format(sig).replace(".", "_"),
                opts=["-M", "MaxLikelihoodFit",
                "--expectSignal", str(sig)],
                output_format="mlfit{process_name}.root",
                get_limits=get_limits_mlfit
            )[0]
            limits += [res]
        return limits

class ConstraintGetter(object):
    def __init__(self, output_path = "."):
        self.output_path = output_path

    def __call__(self, datacard, signal_coef):

        datacard_path, datacard_name = os.path.split(datacard)
       
        process_name = "_sig_{0:.2f}".format(signal_coef).replace(".", "_")

        # Run combine
        combine_command = ["combine", 
                           "-n", process_name,
                           "-M", "MaxLikelihoodFit",
                           "-t", "-1",
                           "--expectSignal", str(signal_coef),
                           datacard_name]
        
        print "running combine with "
        print " ".join(combine_command)
        
        process = subprocess.Popen(combine_command,
                                   stdout=subprocess.PIPE,
                                   cwd=datacard_path,
                                   env=dict(os.environ, 
                                            PATH=PATH,
                                            LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                            PYTHONPATH=PYTHONPATH,
                                            ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                                            ROOTSYS = ROOTSYS,
                                            GENREFLEX = GENREFLEX
                                        ))
        
        output, stderr = process.communicate()
        if process.returncode != 0:
            print "error running limit", stderr
        print output

        diff_cmd = "python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py --format text -a mlfit{0}.root -g plots{0}.root".format(process_name)
        print diff_cmd
        process = subprocess.Popen(diff_cmd,
                                   stdout=subprocess.PIPE,
                                   cwd=datacard_path,
                                   env=dict(os.environ,
                                           CMSSW_BASE=CMSSW_BASE,
                                           PATH=PATH,
                                           LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                           PYTHONPATH=PYTHONPATH,
                                           ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                                           ROOTSYS = ROOTSYS,
                                           GENREFLEX = GENREFLEX
                                   ),
                                   shell=True
        )
        
        output, stderr = process.communicate()
        print output
        return output

class DummyLimitGetter(object):
    
    def __init__(self, output_path = "."):
        self.output_path = output_path

    def __call__(self, datacard):
        print "calling limit on datacard", datacard
        return np.array([0,0,0,0,0,0]), None
    # End of get_limit

if __name__ == "__main__":
    datacard = sys.argv[1]
    workdir = os.path.dirname(datacard)
    lg = LimitGetter(workdir)
    lg.runSignalInjection(datacard)
