import ROOT
import rootpy
import numpy as np
import math

import matplotlib
matplotlib.use('PS') #needed on T3
from matplotlib import pyplot as plt
from rootpy.plotting import root2matplotlib as rplt

def compare_hists(files, labels, histo_name):
    hists = []
    tfiles = []
    for fi in files:
        tf = ROOT.TFile(fi)
        h = rootpy.asrootpy(tf.Get(histo_name))
        if not h:
            raise Exception("Could not get histo {0}".format(histo_name))
        tfiles += [tf]
        hists += [h]

    plt.figure(figsize=(5,5))

    a1 = plt.axes([0.0, 0.22, 1.0, 0.8])
    plt.title(histo_name)

    for hi, label in zip(hists, labels):
        color = next(a1._get_lines.prop_cycler)['color']
        hi.color = color
        rplt.step(hi, linewidth=2, label=label + " {0:.1f} ({1:.1f})".format(hi.Integral(), hi.GetEntries()))

    ticks = a1.get_xticks()
    a1.get_xaxis().set_visible(False)
    plt.legend()

    a2 = plt.axes([0.0,0.0, 1.0, 0.18], sharex=a1)

    for hi, label in zip(hists, labels):
        hir = rootpy.asrootpy(hi.Clone())
        hir.Divide(hists[0])
        rplt.step(hir, linewidth=2)

    plt.ylim(0.5, 1.5)
    plt.axhline(1.0, color="black", lw=1)

    plt.savefig(histo_name + ".pdf", bbox_inches="tight")

histos = [
    "ttH_hbb__dl_jge4_tge2__numJets__unweighted",
    "ttH_hbb__dl_jge4_tge2__nBCSVM__unweighted",
    "ttH_hbb__dl_jge4_tge2__ht__unweighted",
    "ttH_hbb__dl_jge4_tge2__mll__unweighted",
    "ttH_hbb__dl_jge4_tge2__nPVs__unweighted",
    "ttH_hbb__dl_jge4_tge2__btag_LR_4b_2b_btagCSV_logit__unweighted",
    "ttH_hbb__dl_jge4_tge2__jetsByPt_0_pt__unweighted",
    "ttH_hbb__dl_jge4_tge2__leps_0_pt__unweighted",
    "ttH_hbb__dl_jge4_tge2__leps_1_pt__unweighted",
    "ttH_hbb__dl_jge4_tge2__met_pt__unweighted",
    
    "ttH_hbb__sl_jge4_tge2__btag_LR_4b_2b_btagCSV_logit__unweighted",
    "ttH_hbb__sl_jge4_tge2__ht__unweighted",
    "ttH_hbb__sl_jge4_tge2__leps_0_pt__unweighted",
    "ttH_hbb__sl_jge4_tge2__met_pt__unweighted",
    "ttH_hbb__sl_jge4_tge2__nBCSVM__unweighted",
    "ttH_hbb__sl_jge4_tge2__nPVs__unweighted",
    "ttH_hbb__sl_jge4_tge2__numJets__unweighted",
]

for histo in histos:
    compare_hists(
        [
            "/mnt/t3nfs01/data01/shome/jpata/tth/gc/sparse/Jan18.root",
            "/mnt/t3nfs01/data01/shome/jpata/tth/gc/sparse/GC08562acc5622/Jan26.root",
        ],
        [
             "Jan18", "Jan26",
        ],
        histo
    )
