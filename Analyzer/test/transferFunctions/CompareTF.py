#!/usr/bin/env python
import os
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
import ROOT
from ROOT import *

gROOT.SetBatch()


#names = ['2016_old', '2016_ttHTobb', '2016_TTToSemiLeptonic', '2017_ttHTobb', '2017_TTToSemiLeptonic', '2018_ttHTobb', '2018_TTToSemiLeptonic']
names = [ 'Old 2016 campaing', '2016 campaign', '2017 campaign', '2018 campaign' ]
transferFunctionsPickles = [
        "../../../MEAnalysis/data/transfer_functions.pickle",
        "2016_ttHTobb_ttToSemiLep/TFMatrix.dat",
        #"2016_TTToSemiLeptonic/TFMatrix.dat",
        "2017_ttHTobb_ttToSemiLep/TFMatrix.dat",
        #"2017_TTToSemiLeptonic/TFMatrix.dat",
        "2018_ttHTobb_ttToSemiLep/TFMatrix.dat",
        #"2018_TTToSemiLeptonic/TFMatrix.dat"
]


#for fl in ["b", "l"]:
#    for bin in [0, 1]:

for genE in range(30,200, 10): #target gen jet pT [GeV]
    tf_formulas = {}
    for name, transferFunctionsPickle in zip(names, transferFunctionsPickles):
        print "Loading TF_matrix for:", name

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
        print "formula", tf_formula

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

            tf_formulas[names[0]][fl][bin].SetTitle("{} quarks, eta bin {}".format(fl,bin))
            tf_formulas[names[0]][fl][bin].GetHistogram().GetXaxis().SetTitle("reco p_{T} [GeV]")
            tf_formulas[names[0]][fl][bin].Draw("L")
            tf_formulas[names[1]][fl][bin].SetLineColor(ROOT.kBlue)
            tf_formulas[names[1]][fl][bin].Draw("LSAME")
            tf_formulas[names[2]][fl][bin].SetLineColor(ROOT.kGreen)
            tf_formulas[names[2]][fl][bin].Draw("LSAME")
            tf_formulas[names[3]][fl][bin].SetLineColor(ROOT.kBlack)
#            tf_formulas[names[3]][fl][bin].Draw("LSAME")
#            tf_formulas[names[4]][fl][bin].SetLineColor(ROOT.kMagenta)
#            tf_formulas[names[4]][fl][bin].Draw("LSAME")
#            tf_formulas[names[5]][fl][bin].SetLineColor(ROOT.kCyan)
#            tf_formulas[names[5]][fl][bin].Draw("LSAME")
#            tf_formulas[names[6]][fl][bin].SetLineColor(ROOT.kPink)
#            tf_formulas[names[6]][fl][bin].Draw("LSAME")

            leg = ROOT.TLegend(0.65,0.7,0.85,0.88)
            leg.SetBorderSize(0)
            leg.AddEntry(tf_formulas[names[0]][fl][bin], names[0], "l")
            leg.AddEntry(tf_formulas[names[1]][fl][bin], names[1], "l")
            leg.AddEntry(tf_formulas[names[2]][fl][bin], names[2], "l")
            leg.AddEntry(tf_formulas[names[3]][fl][bin], names[3], "l")
#            leg.AddEntry(tf_formulas[names[4]][fl][bin], names[4], "l")
#            leg.AddEntry(tf_formulas[names[5]][fl][bin], names[5], "l")
#            leg.AddEntry(tf_formulas[names[6]][fl][bin], names[6], "l")
            leg.Draw()

            c1.SaveAs("Plots/TF_{0}GeV_{1}_eta{2}.png".format( genE, fl, bin ))

