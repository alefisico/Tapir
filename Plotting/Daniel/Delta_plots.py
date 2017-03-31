#!/usr/bin/env python
from time import sleep
import ROOT, copy
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(0)

saveplots = True
njet = 6
njexact = False
nbjet = 0
nbexact = False
htcut = 450
trigger = False

# variables = [("DR1j","(100,0.4,2.0)"), ("DR2j","(100,0.5,2.6)"), ("DR3j","(100,0.8,3.5)"), ("DR4j","(100,1.0,4.0)"), ("DR5j","(100,1.5,4.5)"), ("DR6j","(100,1.8,4.5)"),
# ("DR1j2","(100,0.0,1.6)"), ("DR2j3","(100,0.2,2.4)"), ("DR3j4","(100,0.5,3.2)"), ("DR4j5","(100,0.8,3.8)"), ("DR5j6","(100,1.2,4.5)"), ("DR6j7","(100,1.6,4.6)"),
# ("Deta1j","(100,0.0,0.8)"), ("Deta2j","(100,0.0,1.6)"), ("Deta3j","(100,0.0,2.2)"), ("Deta4j","(100,0.0,3.2)"), ("Deta5j","(100,0.0,4.0)"), ("Deta6j","(100,0.2,4.0)"),
# ("Deta1j2","(100,0.0,1.4)"), ("Deta2j3","(100,0.0,2.0)"), ("Deta3j4","(100,0.0,2.6)"), ("Deta4j5","(100,0.0,3.5)"), ("Deta5j6","(100,0.0,4.0)"), ("Deta6j7","(100,0.2,4.0)"),
# ("Dphi1j","(100,0.0,1.0)"), ("Dphi2j","(100,0.2,2.0)"), ("Dphi3j","(100,0.4,2.8)"), ("Dphi4j","(100,0.6,3.2)"), ("Dphi5j","(100,0.8,3.2)"), ("Dphi6j","(100,1.0,3.2)"),
# ("Dphi1j2","(100,0.0,1.2)"), ("Dphi2j3","(100,0.0,1.8)"), ("Dphi3j4","(100,0.4,2.2)"), ("Dphi4j5","(100,0.7,2.7)"), ("Dphi5j6","(100,1.0,3.2)"), ("Dphi6j7","(100,1.4,3.2)"),
# ("DD1j[12]","(100,0.1,1.2)"), ("DD2j[12]","(100,0.0,2.2)"), ("DD3j[12]","(100,0.0,3.2)"), ("DD4j[12]","(100,0.2,4.2)"), ("DD5j[12]","(100,0.3,4.6)"), ("DD6j[12]","(100,0.6,4.6)"),
# ("DD1j2[12]","(100,0.0,5.0)"), ("DD2j3[12]","(100,0.0,5.0)"), ("DD3j4[12]","(100,0.0,4.8)"), ("DD4j5[12]","(100,0.0,4.8)"), ("DD5j6[12]","(100,0.2,4.8)"), ("DD6j7[12]","(100,0.6,4.6)"),
# ("DW1j","(100,0.2,1.4)"), ("DW2j","(100,0.3,2.1)"), ("DW3j","(100,0.4,2.6)"), ("DW4j","(100,0.5,3.3)"), ("DW5j","(100,0.6,4.0)"), ("DW6j","(100,0.8,4.0)"),
# ("DW1j2","(100,0.0,1.4)"), ("DW2j3","(100,0.1,2.1)"), ("DW3j4","(100,0.2,2.6)"), ("DW4j5","(100,0.4,3.4)"), ("DW5j6","(100,0.5,4.0)"), ("DW6j7","(100,0.8,4.0)")
# ]

# variables = [("DD1j[0]","(100,0.0,5.)"), ("DD2j[0]","(100,0.0,11.)"), ("DD3j[0]","(100,0.0,22.)"), ("DD4j[0]","(100,0.0,30.)"), ("DD5j[0]","(100,0.0,40.)"), ("DD6j[0]","(100,0.1,40.)"),
# ("DD1j[1]","(100,0.0,2.5)"), ("DD2j[1]","(100,0.0,5.)"), ("DD3j[1]","(100,0.0,10.)"), ("DD4j[1]","(100,0.0,15.)"), ("DD5j[1]","(100,0.0,20.)"), ("DD6j[1]","(100,0.1,20.)"),
# ("DD1j[2]","(100,0.0,1.5)"), ("DD2j[2]","(100,0.0,4.)"), ("DD3j[2]","(100,0.0,6.)"), ("DD4j[2]","(100,0.0,10.)"), ("DD5j[2]","(100,0.0,12.)"), ("DD6j[2]","(100,0.1,12.)"),
# ("DD1j[3]","(100,0.0,1.4)"), ("DD2j[3]","(100,0.0,2.5)"), ("DD3j[3]","(100,0.0,4.)"), ("DD4j[3]","(100,0.0,6.)"), ("DD5j[3]","(100,0.0,8.)"), ("DD6j[3]","(100,0.1,8.)"),
# ("DD1j[4]","(100,0.0,1.2)"), ("DD2j[4]","(100,0.0,2.2)"), ("DD3j[4]","(100,0.0,3.2)"), ("DD4j[4]","(100,0.0,4.2)"), ("DD5j[4]","(100,0.0,5.0)"), ("DD6j[4]","(100,0.1,5.0)"),
# ("DD1j[5]","(100,0.0,1.2)"), ("DD2j[5]","(100,0.0,2.2)"), ("DD3j[5]","(100,0.0,3.2)"), ("DD4j[5]","(100,0.0,4.2)"), ("DD5j[5]","(100,0.0,5.0)"), ("DD6j[5]","(100,0.1,5.0)"),
# ("DD1j[6]","(100,0.0,1.2)"), ("DD2j[6]","(100,0.0,2.2)"), ("DD3j[6]","(100,0.0,3.2)"), ("DD4j[6]","(100,0.0,4.2)"), ("DD5j[6]","(100,0.0,5.0)"), ("DD6j[6]","(100,0.1,5.0)"),
# ("DD1j[7]","(100,0.0,1.2)"), ("DD2j[7]","(100,0.0,2.2)"), ("DD3j[7]","(100,0.0,3.2)"), ("DD4j[7]","(100,0.0,4.2)"), ("DD5j[7]","(100,0.0,5.0)"), ("DD6j[7]","(100,0.1,5.0)"),
# ("DD1j[8]","(100,0.0,1.2)"), ("DD2j[8]","(100,0.0,2.2)"), ("DD3j[8]","(100,0.0,3.2)"), ("DD4j[8]","(100,0.0,4.2)"), ("DD5j[8]","(100,0.0,5.0)"), ("DD6j[8]","(100,0.1,5.0)"),
# ("DD1j[9]","(100,0.0,1.2)"), ("DD2j[9]","(100,0.0,2.2)"), ("DD3j[9]","(100,0.0,3.2)"), ("DD4j[9]","(100,0.0,4.2)"), ("DD5j[9]","(100,0.0,5.0)"), ("DD6j[9]","(100,0.1,5.0)"),
# ("DD1j[10]","(100,0.0,1.2)"), ("DD2j[10]","(100,0.0,2.2)"), ("DD3j[10]","(100,0.0,3.2)"), ("DD4j[10]","(100,0.0,4.2)"), ("DD5j[10]","(100,0.0,5.0)"), ("DD6j[10]","(100,0.1,5.0)"),
# ("DD1j[11]","(100,0.0,1.2)"), ("DD2j[11]","(100,0.0,2.2)"), ("DD3j[11]","(100,0.0,3.2)"), ("DD4j[11]","(100,0.0,4.2)"), ("DD5j[11]","(100,0.0,5.0)"), ("DD6j[11]","(100,0.1,5.0)") ]

# variables = [("DD1j2[0]","(100,0.0,30.)"), ("DD2j3[0]","(100,0.0,40.)"), ("DD3j4[0]","(100,0.0,40.)"), ("DD4j5[0]","(100,0.0,40.)"), ("DD5j6[0]","(100,0.0,40.)"), ("DD6j7[0]","(100,0.1,40.)"),
# ("DD1j2[1]","(100,0.0,20.)"), ("DD2j3[1]","(100,0.0,20.)"), ("DD3j4[1]","(100,0.0,20.)"), ("DD4j5[1]","(100,0.0,20.)"), ("DD5j6[1]","(100,0.0,20.)"), ("DD6j7[1]","(100,0.1,20.)"),
# ("DD1j2[2]","(100,0.0,10.)"), ("DD2j3[2]","(100,0.0,10.)"), ("DD3j4[2]","(100,0.0,10.)"), ("DD4j5[2]","(100,0.0,10.)"), ("DD5j6[2]","(100,0.0,10.)"), ("DD6j7[2]","(100,0.1,10.)"),
# ("DD1j2[3]","(100,0.0,8.)"), ("DD2j3[3]","(100,0.0,8.)"), ("DD3j4[3]","(100,0.0,8.)"), ("DD4j5[3]","(100,0.0,8.)"), ("DD5j6[3]","(100,0.0,8.)"), ("DD6j7[3]","(100,0.1,8.)"),
# ("DD1j2[4]","(100,0.0,6.)"), ("DD2j3[4]","(100,0.0,6.)"), ("DD3j4[4]","(100,0.0,6.)"), ("DD4j5[4]","(100,0.0,6.)"), ("DD5j6[4]","(100,0.0,6.0)"), ("DD6j7[4]","(100,0.1,5.0)"),
# ("DD1j2[5]","(100,0.0,5.)"), ("DD2j3[5]","(100,0.0,5.)"), ("DD3j4[5]","(100,0.0,5.)"), ("DD4j5[5]","(100,0.0,5.)"), ("DD5j6[5]","(100,0.0,5.0)"), ("DD6j7[5]","(100,0.1,5.0)"),
# ("DD1j2[6]","(100,0.0,5.)"), ("DD2j3[6]","(100,0.0,5.)"), ("DD3j4[6]","(100,0.0,5.)"), ("DD4j5[6]","(100,0.0,5.)"), ("DD5j6[6]","(100,0.0,5.0)"), ("DD6j7[6]","(100,0.1,5.0)"),
# ("DD1j2[7]","(100,0.0,5.)"), ("DD2j3[7]","(100,0.0,5.)"), ("DD3j4[7]","(100,0.0,5.)"), ("DD4j5[7]","(100,0.0,5.)"), ("DD5j6[7]","(100,0.0,5.0)"), ("DD6j7[7]","(100,0.1,5.0)"),
# ("DD1j2[8]","(100,0.0,5.)"), ("DD2j3[8]","(100,0.0,5.)"), ("DD3j4[8]","(100,0.0,5.)"), ("DD4j5[8]","(100,0.0,5.)"), ("DD5j6[8]","(100,0.0,5.0)"), ("DD6j7[8]","(100,0.1,5.0)"),
# ("DD1j2[9]","(100,0.0,5.)"), ("DD2j3[9]","(100,0.0,5.)"), ("DD3j4[9]","(100,0.0,5.)"), ("DD4j5[9]","(100,0.0,5.)"), ("DD5j6[9]","(100,0.0,5.0)"), ("DD6j7[9]","(100,0.1,5.0)"),
# ("DD1j2[10]","(100,0.0,5.)"), ("DD2j3[10]","(100,0.0,5.)"), ("DD3j4[10]","(100,0.0,5.)"), ("DD4j5[10]","(100,0.0,5.)"), ("DD5j6[10]","(100,0.0,5.0)"), ("DD6j7[10]","(100,0.1,5.0)"),
# ("DD1j2[11]","(100,0.0,5.)"), ("DD2j3[11]","(100,0.0,5.)"), ("DD3j4[11]","(100,0.0,5.)"), ("DD4j5[11]","(100,0.0,5.)"), ("DD5j6[11]","(100,0.0,5.0)"), ("DD6j7[11]","(100,0.1,5.0)") ]

variables = [ ("DD5j[12]","(100,0.0,5.0)"), ("DD3j4[12]","(100,0.0,5.)") ]

# list files
directory = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_test2/mini_trees/"
file_tth = "ttHTobb_M125_13TeV_powheg_pythia8.root"
file_ttbar = "TT_TuneCUETP8M1_13TeV-powheg-pythia8.root"
file_qcd3 = "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
file_qcd5 = "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
file_qcd7 = "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
file_qcd10 = "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
file_qcd15 = "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
file_qcd20 = "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"

# scale factor (xSec / nGen)
scalefac = {"tth": 0.5085*0.577 / 3413232.0,
            "ttbar": 831.76 / 76610800.0,
            "qcd3": 351300.0 / 38222596.0,
            "qcd5": 31630.0 / 56596792.0,
            "qcd7": 6802.0 / 41236680.0,
            "qcd10": 1206.0 / 10024439.0,
            "qcd15": 120.4 / 7479181.0,
            "qcd20": 25.25 / 3951574.0 }
tree = {}
# open files
f_tth = ROOT.TFile.Open(directory+file_tth)
tree["tth"] = f_tth.Get("tree")
f_ttbar = ROOT.TFile.Open(directory+file_ttbar)
tree["ttbar"] = f_ttbar.Get("tree")
f_qcd3 = ROOT.TFile.Open(directory+file_qcd3)
tree["qcd3"] = f_qcd3.Get("tree")
f_qcd5 = ROOT.TFile.Open(directory+file_qcd5)
tree["qcd5"] = f_qcd5.Get("tree")
f_qcd7 = ROOT.TFile.Open(directory+file_qcd7)
tree["qcd7"]= f_qcd7.Get("tree")
f_qcd10 = ROOT.TFile.Open(directory+file_qcd10)
tree["qcd10"] = f_qcd10.Get("tree")
f_qcd15 = ROOT.TFile.Open(directory+file_qcd15)
tree["qcd15"] = f_qcd15.Get("tree")
f_qcd20 = ROOT.TFile.Open(directory+file_qcd20)
tree["qcd20"] = f_qcd20.Get("tree")

cut = "njets"+("==" if njexact else ">=")+str(njet) + " && nBCSVM"+("==" if nbexact else ">=")+str(nbjet) + " && ht>"+str(htcut)+(" && HLT_ttH_FH" if trigger else "")
print cut

cat = ("e" if njexact else "ge")+str(njet)+"j_"+("e" if nbexact else "ge")+str(nbjet)+"b_ht"+str(htcut)+("_withtrig" if trigger else "_notrig")
print cat

can = 0
for variable, binning in variables:
    
    can += 1
    var = variable.translate(None,"[]") #remove [] for saving

    y_tth = tree["tth"].Draw(variable+">>h_tth"+binning,cut)
    h_tth = ROOT.gDirectory.Get("h_tth")
    h_tth.SetLineColor(4) #4=blue
    h_tth.SetLineWidth(2)

    y_ttbar = tree["ttbar"].Draw(variable+">>h_ttbar"+binning,cut)
    h_ttbar = ROOT.gDirectory.Get("h_ttbar")
    h_ttbar.SetLineColor(2) #2=red
    h_ttbar.SetLineWidth(2)

    y_qcd = 0.0
    h_qcd = h_tth.Clone("h_qcd")
    h_qcd.Reset("M")

    for key in ["qcd5","qcd7","qcd10","qcd15","qcd20"]:
        weight = scalefac[key]
        y_qcd += tree[key].Draw(variable+">>hist"+binning,cut)
        hist = ROOT.gDirectory.Get("hist")
        h_qcd.Add(hist,weight)

    h_qcd.SetLineColor(8) #8=green
    h_qcd.SetLineWidth(2)
    
    cn = ROOT.TCanvas("c"+str(can+1),"",5,30,640,580)
    pd = ROOT.TPad("p"+str(can+1),"",0,0,1,1)

    pd.SetGrid(0,0)
    pd.SetFillStyle(4000)
    pd.SetFillColor(10)
    pd.SetTicky()
    pd.SetTicks(0,0)
    pd.SetObjectStat(0)
    pd.Draw()
    pd.cd()

    pd.SetTopMargin(0.08)
    pd.SetLeftMargin(0.11)
    pd.SetRightMargin(0.05)

    leg = ROOT.TLegend(0.75,0.72,0.95,0.90)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetTextSize(0.04)

    leg.AddEntry(h_tth,  "t#bar{t}H (125)", "L")
    leg.AddEntry(h_ttbar,  "t#bar{t}+jets", "L")
    leg.AddEntry(h_qcd,  "QCD MC", "L")
    
    ymax = max(h_tth.GetMaximum() * h_qcd.Integral() / h_tth.Integral(),
               h_ttbar.GetMaximum() * h_qcd.Integral() / h_ttbar.Integral(),
               h_qcd.GetMaximum() )

    h_qcd.SetMaximum(ymax*1.1)

    h_qcd.GetXaxis().SetTitle(variable)

    h_qcd.DrawNormalized("hist")
    h_ttbar.DrawNormalized("histsame")
    h_tth.DrawNormalized("histsame")
    leg.Draw()

    if saveplots: cn.SaveAs("./Delta_plots/DDnjm_test/"+var+"_"+cat+".pdf")

    # text = raw_input('end variable: press any key to continue ')
    # if text=="q":
    #     break

    sleep(1)
    #end loop over variables

raw_input('end file: press any key to exit ')
