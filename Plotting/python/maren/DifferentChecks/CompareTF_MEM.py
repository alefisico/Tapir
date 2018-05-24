#!/usr/bin/env python
import os
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
import ROOT

genE = 100 #target gen jet pT [GeV]

names = ["TF16","TF17,TTSL", "TF17,TTHad","TF17,ttH"]
MEMFiles = [#os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions.pickle",
                            #"/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/transfer/ttbar/resolved/TFMatrix.dat",
                            #"/mnt/t3nfs01/data01/shome/jpata/tth/tf/V25/resolved/TFMatrix.dat",
                            #"/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/transfer/ttbar/resolved_100/TFMatrix.dat",
                            "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_4/CMSSW/src/TTH/CommonClassifier/crab/output_OldTF.root",
                            #"/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_4/CMSSW/src/TTH/CommonClassifier/crab/output_TTHadLargeSample.root",
                            "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_4/CMSSW/src/TTH/CommonClassifier/crab/output_ttSemiLeptonicTranfer.root",
                            #"/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_4/CMSSW/src/TTH/CommonClassifier/crab/output_ttSemiLeptonicTranfer.root", TTH with old PDFS
                            "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_4/CMSSW/src/TTH/CommonClassifier/crab/output_TTHadLargeSample_NewBTags.root",
                            "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_4/CMSSW/src/TTH/CommonClassifier/crab/output_ttHLargeSample_NewBTags.root"
]


#for fl in ["b", "l"]:
#    for bin in [0, 1]:

tf_formulas = {}
for name, root in zip(names, MEMFiles):

    tf_formulas[name] = ROOT.TH1F("MEM_{}".format(name),"MEM_{}".format(name),50,0,1)

    f1 = ROOT.TFile.Open(root, "READ")

    ttree = f1.Get("tree")

    for event in ttree :
        tf_formulas[name].Fill(event.mem_p)

    print tf_formulas[name].GetMean()
    tf_formulas[name].SetDirectory(0)

    f1.Close()


c1 = ROOT.TCanvas("c1","c1",700,600)
c1.SetGrid() 

tf_formulas[names[0]].SetTitle("")
tf_formulas[names[0]].GetXaxis().SetTitle("MEM")
tf_formulas[names[0]].SetLineColor(ROOT.kRed)
tf_formulas[names[0]].Draw("")
tf_formulas[names[1]].SetLineColor(ROOT.kBlue)    
tf_formulas[names[1]].Draw("SAME")
tf_formulas[names[2]].SetLineColor(ROOT.kGreen)  
tf_formulas[names[2]].Draw("SAME")
tf_formulas[names[3]].SetLineColor(ROOT.kBlack)  
tf_formulas[names[3]].Draw("SAME")

leg = ROOT.TLegend(0.65,0.7,0.85,0.88)
leg.SetBorderSize(0)
leg.AddEntry(tf_formulas[names[0]], names[0], "l")
leg.AddEntry(tf_formulas[names[1]], names[1], "l")
leg.AddEntry(tf_formulas[names[2]], names[2], "l")
leg.AddEntry(tf_formulas[names[3]], names[3], "l")
leg.Draw()

c1.SaveAs("tf_plots/MEM_TF.pdf")


diff = {}
mem = {}
counter = 0
for name, root in zip(names, MEMFiles):

    f1 = ROOT.TFile.Open(root, "READ")

    ttree = f1.Get("tree")

    for event in ttree :
        if counter == 0:
            mem[event.event] = []
        mem[event.event].append(event.mem_p)

    counter = 1

    f1.Close()

for name in names:
    diff[name] = ROOT.TH1F("MEMDiff_{}".format(name),"MEMDiff_{}".format(name),50,-0.6,0.6)
    ind = names.index(name)
    for i in mem:
        diff[name].Fill(mem[i][ind]-mem[i][0])
    print diff[name].GetMean()



c2 = ROOT.TCanvas("c1","c1",700,600)
c2.SetGrid()  

diff[names[1]].SetTitle("")
diff[names[1]].SetStats(00000000)
diff[names[0]].GetXaxis().SetTitle("MEM - MEM16")
diff[names[0]].SetLineColor(ROOT.kRed)
#diff[names[0]].Draw("")
diff[names[1]].SetLineColor(ROOT.kRed)    
diff[names[1]].Draw("SAME")
diff[names[2]].SetLineColor(ROOT.kGreen)  
diff[names[2]].Draw("SAME")
diff[names[3]].SetLineColor(ROOT.kBlack)  
diff[names[3]].Draw("SAME")

leg2 = ROOT.TLegend(0.65,0.7,0.85,0.88)
leg2.SetBorderSize(0)
#leg2.AddEntry(diff[names[0]], names[0], "l")
leg2.AddEntry(diff[names[1]], names[1], "l")
leg2.AddEntry(diff[names[2]], names[2], "l")
leg2.AddEntry(diff[names[3]], names[3], "l")
leg2.Draw()

c2.SaveAs("tf_plots/MEM_Diff_TF.pdf")