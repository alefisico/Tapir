#!/usr/bin/env python
import os
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
import ROOT

genE = 90 #target gen jet pT [GeV]

names = ["ttH","TTbar","pipeline"]
transferFunctionsPickles = [#os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions.pickle",
                            #"/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/transfer/ttbar/resolved/TFMatrix.dat",
                            #"/mnt/t3nfs01/data01/shome/jpata/tth/tf/V25/resolved/TFMatrix.dat",
                            #"/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/transfer/ttbar/resolved_100/TFMatrix.dat",
                            "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/CMSSW_8_0_25/src/TTH/MEAnalysis/data/transfer_functions.pickle",
                            "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/CMSSW_8_0_25/src/TTH/MEAnalysis/data/transfer_functions_ttbar.pickle",
                            "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/CMSSW_8_0_25/src/TTH/MEIntegratorStandalone/data/transfers.pickle"
]


#for fl in ["b", "l"]:
#    for bin in [0, 1]:

tf_formulas = {}
for name, transferFunctionsPickle in zip(names, transferFunctionsPickles):
    print "Loading TF_matrix for:",name

    pi_file = open(transferFunctionsPickle, 'rb')
    tf_matrix = pickle.load(pi_file)

    #print "matrix", tf_matrix

    eval_gen=False #True: TF[0]=reco, x=gen, False: TF[0]=gen, x=reco
    tf_formula = {}
    for fl in ["b", "l"]:
        tf_formula[fl] = {}
        for bin in [0, 1]:
            tf_formula[fl][bin] = tf_matrix[fl][bin].Make_Formula(eval_gen)

    tf_formulas[name] = tf_formula
    #print "formula", tf_formula

    pi_file.close()

print "General Formula Expression:"
print tf_formulas[names[0]][fl][bin].GetFormula().GetExpFormula()

for fl in ["b", "l"]:
    for bin in [0, 1]:
        print "flavour:", fl, "bin:", bin
        #tf_formula[fl][bin].Draw("L")
        for name in tf_formulas.keys():
            tf_formulas[name][fl][bin].SetParameter(0,genE)
            tf_formulas[name][fl][bin].SetRange(0,2*genE)
            print "\n***",name,"***"
            for i in range(tf_formulas[name][fl][bin].GetNpar()):
                print tf_formulas[name][fl][bin].GetParameter(i)

        c1 = ROOT.TCanvas("c1","c1",700,600)
        c1.SetGrid()  

        tf_formulas[names[0]][fl][bin].SetTitle("")
        tf_formulas[names[0]][fl][bin].GetHistogram().GetXaxis().SetTitle("reco p_{T} [GeV]")
        tf_formulas[names[0]][fl][bin].Draw("L")
        tf_formulas[names[1]][fl][bin].SetLineColor(ROOT.kBlue)    
        tf_formulas[names[1]][fl][bin].Draw("LSAME")
        tf_formulas[names[2]][fl][bin].SetLineColor(ROOT.kGreen)  
        tf_formulas[names[2]][fl][bin].Draw("LSAME")

        leg = ROOT.TLegend(0.65,0.7,0.85,0.88)
        leg.SetBorderSize(0)
        leg.AddEntry(tf_formulas[names[0]][fl][bin], names[0], "l")
        leg.AddEntry(tf_formulas[names[1]][fl][bin], names[1], "l")
        leg.AddEntry(tf_formulas[names[2]][fl][bin], names[2], "l")
        leg.Draw()

        c1.SaveAs("tf_plots/TF_{0}GeV_{1}_eta{2}.pdf".format( genE, fl, bin ))

raw_input ("press Enter to quit")
