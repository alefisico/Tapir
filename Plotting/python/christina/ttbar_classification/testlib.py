import matplotlib
matplotlib.use("Agg")
import numpy as np
import ROOT
from root_numpy import fill_hist
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier 
from sklearn.metrics import roc_curve, auc
from sklearn.externals import joblib
import sys
import os
import glob
import pandas as pd

# calculate naive discriminator
def CSVM(btags, d, proc):

    d = pd.read_csv(d)

# cut on events from special process 
    if proc == "ttbarOther":
        d_cut = d[d["ttCls"] == 0] 
    elif proc == "ttbarPlusBBbar":
        d_cut = d[d["ttCls"] == 53] 
    else:
        d_cut = d
    nevt = d_cut.shape[0]

# use nBCSVM as discriminant
    d_cut = d_cut[d_cut["nBCSVM"] == btags]
    nevt_nBCSVM = d_cut.shape[0]

    eff = nevt_nBCSVM/float(nevt)

    print eff
    return eff
    

# calculate fpr, tpr for roc curve
def fpr_tpr(y_true, y_score, unc = False , weight = None):

# fill histo to calculate tpr, fpr
    h = {}
    c_histo = {}

    nbin = len(y_true)
    hmin = np.amin(y_score)
    hmax = np.amax(y_score)

    if hmin == -9999:
        hmin = 0

    process = ["4b", "2b"]
    for p in process:
        h[p] = ROOT.TH1F(p, "x", nbin, hmin, hmax)
        if p == "4b":
            y_filtered = y_score[y_true == 53]
            if unc == True:
                weights = weight[y_true == 53] 
        elif p == "2b":
            y_filtered = y_score[y_true == 0]
            if unc == True:
                weights = weight[y_true == 0]
        if unc == True:
            fill_hist(h[p], y_filtered, weights=weights)
        else:
            fill_hist(h[p], y_filtered)
        N = h[p].Integral()
        if N == 0:
            raise ValueError("Integral of histogram equals zero, normalization not possible")
        else:
            h[p].Scale(1/N)
        c_histo[p] = h[p].GetCumulative()

    nbin = h[process[0]].GetSize()-2
    tpr = []
    fpr = []
    for j in range(0, nbin + 1):
        tpr.append(1 - c_histo[process[0]].GetBinContent(j))
        fpr.append(1 - c_histo[process[1]].GetBinContent(j))

    return tpr, fpr

# define sample containing ttH evt
def make_ttH_sample(fpath):

    

     


# plot roc curves
def plot_roc(classifier, test, plot_blr = None, unc = False):

    clf = joblib.load(classifier)

    test = pd.read_csv("test.csv")
    numJets = 6
    var = ["jets_btagCSV_" + str(x) for x in range(numJets)]
    X_test = np.array(test[var])
    X_test = np.sort(X_test)
    y_test = np.array(test["ttCls"]) 
    y_score = clf.decision_function(X_test)


    fig = plt.figure()
    if unc == True:
        tpr_up, fpr_up = fpr_tpr(y_test, y_score, unc = unc,  weight = test["btagWeightCSV_up_lf"])
        tpr_down, fpr_down = fpr_tpr(y_test, y_score, unc = unc, weight = test["btagWeightCSV_down_lf"])
        tpr_nom, fpr_nom = fpr_tpr(y_test, y_score, unc = unc, weight = test["btagWeightCSV"])
        
        #plt.plot(tpr_nom, fpr_nom, "r-", label='BDT output')
        #plt.plot(tpr_up, fpr_up, "r-", alpha = 0.5 )
        #plt.plot(tpr_down, fpr_down, "r-", alpha = 0.5)
        plt.semilogy(tpr_nom, fpr_nom, "r-", label='BDT output', zorder=4)
        plt.semilogy(tpr_up, fpr_up, "r-", alpha = 0.5 )
        plt.semilogy(tpr_down, fpr_down, "r-", alpha = 0.5)
 
    else:
        tpr_test, fpr_test = fpr_tpr(y_test, y_score)
        plt.semilogy(tpr_test, fpr_test, "r-", label='BDT output')
        #plt.plot(tpr_test, fpr_test, "r-", label='BDT output')
    
    if plot_blr != None:
        d = pd.read_csv(plot_blr)
        blr = d["btag_LR_4b_2b_btagCSV"]
        ttCls = d["ttCls"]
        if unc == True:
            tpr_blr_up, fpr_blr_up = fpr_tpr(ttCls, blr, unc = unc,  weight = test["btagWeightCSV_up_lf"])
            tpr_blr_down, fpr_blr_down = fpr_tpr(ttCls, blr, unc = unc, weight = test["btagWeightCSV_down_lf"])
            tpr_blr_nom, fpr_blr_nom = fpr_tpr(ttCls, blr, unc = unc, weight = test["btagWeightCSV"])
         
            #plt.plot(tpr_blr_nom, fpr_blr_nom, "g-", label='BLR')
            #plt.plot(tpr_blr_up, fpr_blr_up, "g-", alpha = 0.5 )
            #plt.plot(tpr_blr_down, fpr_blr_down, "g-", alpha = 0.5)
            plt.semilogy(tpr_blr_nom, fpr_blr_nom, "g-", label='BLR', zorder=4)
            plt.semilogy(tpr_blr_up, fpr_blr_up, "g-", alpha = 0.5 )
            plt.semilogy(tpr_blr_down, fpr_blr_down, "g-", alpha = 0.5)
        else:
            tpr_blr, fpr_blr = fpr_tpr(ttCls, blr)    
            #plt.plot(tpr_blr, fpr_blr, "g-", label="BLR")
            plt.semilogy(tpr_blr, fpr_blr, "g-", label='BLR')

    eff_sig = CSVM(4, "dataframe.csv", "ttbarPlusBBbar") 
    eff_bkg = CSVM(4, "dataframe.csv", "ttbarOther")
    plt.scatter([eff_sig], [eff_bkg], c="k", marker = "^", label = "4x BCSVM", zorder = 1) 

    eff_sig = CSVM(3, "dataframe.csv", "ttbarPlusBBbar") 
    eff_bkg = CSVM(3, "dataframe.csv", "ttbarOther")
    plt.scatter([eff_sig], [eff_bkg], c="k", marker = "o", label = "3x BCSVM", zorder = 1) 



    plt.xlim([0.0, .5])
    #plt.ylim([0.0, 1.05])
    plt.ylabel('tt+jets (light) efficiency', fontsize=16)
    plt.xlabel('tt+bb efficiency', fontsize=16)
    plt.title(r"SL/DL, $N_j = 6$", fontsize=16)
    plt.legend(loc="upper left")
    os.chdir(sys.path[0])
    fig.savefig("roc.pdf")

if __name__ == "__main__":

    plot_roc("classifier.pkl", "test.csv", plot_blr = "test.csv", unc = True)
    #CSVM(4,"dataframe.csv", "ttbarOther")

