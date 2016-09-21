
import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt


import ROOT
import TTH.MEAnalysis.counts as counts
import TTH.Plotting.joosep.sparsinator as sparsinator
import tempfile, os
from shutil import copyfile

import sys, os, copy
from collections import OrderedDict
import TTH.Plotting.joosep.plotlib as plotlib #heplot, 


import rootpy
from rootpy.plotting import Hist
from rootpy.plotting import root2matplotlib as rplt




def count(filenames):
    ofname = tempfile.mktemp() 
    ret = counts.main(filenames, ofname)
    os.remove(ofname)
    return ret

def sparse(analysis, filenames, sample, outfile):
    ofname = tempfile.mktemp()
    sparsinator.main(analysis, filenames, sample, ofname)

    basepath = os.path.dirname(outfile)
    if not os.path.isdir(basepath):
        os.makedirs(basepath)

    copyfile(ofname, outfile)
    os.remove(ofname)
    return outfile



def blind(h):
    hc = h.Clone()
    for i in range(h.GetNbinsX()+1):
        hc.SetBinContent(i, 0)
        hc.SetBinError(i, 0)
    return hc

#def plot_syst_updown(nominal, up, down):
#    plt.figure(figsize=(6,6))
#    heplot.barhist(nominal, color="black")
#    heplot.barhist(up, color="red")
#    heplot.barhist(down, color="blue")




def plot_worker(kwargs):
    inf = rootpy.io.File(kwargs.pop("infile"))
    outname = kwargs.pop("outname")
    histname = kwargs.pop("histname")
    procs = kwargs.pop("procs")
    signal_procs = kwargs.pop("signal_procs")
    do_syst = kwargs.pop("do_syst")

    fig = plt.figure(figsize=(6,6))
    ret = plotlib.draw_data_mc(
        inf,
        histname,
        procs,
        signal_procs,
        **kwargs
    )
    
    path = os.path.dirname(outname)
    if not os.path.isdir(path):
        os.makedirs(path)
    plotlib.svfg(outname + ".pdf")
    plt.clf()    
    inf.Close()
