#!/usr/bin/env python
from time import sleep
import ROOT, copy
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(0)

saveplots = False
njet = 8 #7, 8, or 9
nbjet = 4 #3 or 4
validation = True #QR=True, BR=False
lumi = 35 #fb-1

#define region cuts
A4 = 0.99 #4b SR/VR
B4 = 0.75 #4b CR/CR2
C4 = 0.88

A3 = 0.83 #3b SR/VR
B3 = 0.6  #3b CR/CR2
C3 = 0.8

QGLR = 0.5 #QR if <QGLR, BR if >

variables = [("jets_pt[0]","(100,0,800)"), ("jets_pt[1]","(100,0,600)"), ("jets_pt[2]","(100,0,400)"),
             ("jets_pt[3]","(100,0,300)"), ("jets_pt[4]","(100,0,200)"), ("jets_pt[5]","(100,0,120)"),
             ("jets_qgl[0]","(100,0,1)"), ("jets_qgl[1]","(100,0,1)"), ("jets_qgl[2]","(100,0,1)"),
             ("jets_qgl[3]","(100,0,1)"), ("jets_qgl[4]","(100,0,1)"), ("jets_qgl[5]","(100,0,1)"),
             ("jets_eta[0]","(100,-2.5,2.5)"), ("ht","(100,0,2000)"), ("min_dr_btag","(100,0,3)") ]

#variables = [("mem","(10,0,1)") ]
#variables = [("jets_pt[0]","(100,0,800)") ]

for variable, binning in variables:

    if variable == "mem":
        if (njet >= 8 and nbjet==4):
            variable = "mem_tth_FH_4w2h2t_p/(mem_tth_FH_4w2h2t_p+0.02*mem_ttbb_FH_4w2h2t_p)"
        if (njet == 7 and nbjet==4):
            variable = "mem_tth_FH_3w2h2t_p/(mem_tth_FH_3w2h2t_p+0.02*mem_ttbb_FH_3w2h2t_p)"
        if (njet >= 7 and nbjet==3):
            variable = "mem_tth_FH_4w2h1t_p/(mem_tth_FH_4w2h1t_p+0.02*mem_ttbb_FH_4w2h1t_p)"

    if (njet >=9):
        WmassCut = "Wmass>72 && Wmass<94"
    else:
        WmassCut = "Wmass>60 && Wmass<100"        

    #variable = "jets_pt[5]"
    #binning = "(100,0,120)"

    var = variable.translate(None,"[]")

    data = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/projectSkimFH/JoosepFeb_nosyst_v1_v2/JetHT.root"
    ttbar = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/projectSkimFH/JoosepFeb_nosyst_v1_v2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root"

    cut = ""
    cutSR = ""
    cutCR = ""
    if validation: #QR, VR, CR2 (qglr<0.5)
        if nbjet == 4: 
            cut = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q<"+str(QGLR)+")"
            cutSR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q<"+str(QGLR)+" && btag_LR_4b_2b_btagCSV>"+str(A4)+")"
            cutCR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q<"+str(QGLR)+" && btag_LR_3b_2b_btagCSV<"+str(A3)+" && btag_LR_4b_2b_btagCSV>"+str(B4)+" && btag_LR_4b_2b_btagCSV<"+str(C4)+")"
        elif nbjet ==3:
            cut = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q<"+str(QGLR)+" && btag_LR_4b_2b_btagCSV<"+str(A4)+")"
            cutSR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q<"+str(QGLR)+" && btag_LR_4b_2b_btagCSV<"+str(A4)+" && btag_LR_3b_2b_btagCSV>"+str(A3)+")"
            cutCR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q<"+str(QGLR)+" && btag_LR_4b_2b_btagCSV<"+str(B4)+" && btag_LR_3b_2b_btagCSV>"+str(B3)+" && btag_LR_3b_2b_btagCSV<"+str(C3)+")"

    else: #BR, SR, CR
        if nbjet == 4:
            cut = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q>"+str(QGLR)+")"
            cutSR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q>"+str(QGLR)+" && btag_LR_4b_2b_btagCSV>"+str(A4)+")"
            cutCR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q>"+str(QGLR)+" && btag_LR_3b_2b_btagCSV<"+str(A3)+" && btag_LR_4b_2b_btagCSV>"+str(B4)+" && btag_LR_4b_2b_btagCSV<"+str(C4)+")"
        elif nbjet ==3:
            cut = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q>"+str(QGLR)+" && btag_LR_4b_2b_btagCSV<"+str(A4)+")"
            cutSR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q>"+str(QGLR)+" && btag_LR_4b_2b_btagCSV<"+str(A4)+" && btag_LR_3b_2b_btagCSV>"+str(A3)+")"
            cutCR = "(ht>450 && HLT_ttH_FH && nBCSVM>=2 && numJets=="+str(njet)+" && "+WmassCut+" && qg_LR_4b_flavour_4q_0q>"+str(QGLR)+" && btag_LR_4b_2b_btagCSV<"+str(B4)+" && btag_LR_3b_2b_btagCSV>"+str(B3)+" && btag_LR_3b_2b_btagCSV<"+str(C3)+")"

    bLR3 = "btag_LR_3b_2b_btagCSV"
    bLR4 = "btag_LR_4b_2b_btagCSV"
    bLR = bLR3 if (nbjet==3) else bLR4

    cat = str(njet)+"j_"+str(nbjet)+"b"
    BR = "QR" if validation else "BR"
    SR = "VR" if validation else "SR"
    CR = "CR2" if validation else "CR"
    print "plotregion",cat+"_"+BR

    # open files
    fdata = ROOT.TFile.Open(data)
    tdata = fdata.Get("tree")
    fttbar = ROOT.TFile.Open(ttbar)
    tttbar = fttbar.Get("tree")

    tt_total = tttbar.Draw("",cut)
    tt_pos = tttbar.Draw("",cut+"&&"+bLR+">-1")
    tt_scalefac = 831.76 / 92667118.0 * float(tt_total) / float(tt_pos) * 1000.0 * lumi

    c1 = ROOT.TCanvas("c1","",5,30,640,580)
    p1 = ROOT.TPad("p1","",0,0,1,1)

    p1.SetGrid(0,0)
    p1.SetFillStyle(4000)
    p1.SetFillColor(10)
    p1.SetTicky()
    p1.SetTicks(0,0)
    p1.SetObjectStat(0)
    p1.Draw()
    p1.cd()

    p1.SetTopMargin(0.08)
    p1.SetLeftMargin(0.11)
    p1.SetRightMargin(0.05)

    ydataBR = tdata.Draw(bLR+">>hdata(100,0,1)",cut)
    hdata = ROOT.gDirectory.Get("hdata")
    hdata.SetLineColor(1)
    hdata.SetMarkerColor(1)
    hdata.SetMarkerStyle(20)
    hdata.SetMarkerSize(1)
    hdata.Sumw2()

    if saveplots: c1.SaveAs("./QCD_estimate_plots/data_"+cat+"_"+BR+"_bLR.pdf")

    #raw_input('done data: press any key to continue')

    yttbarBR = tttbar.Draw(bLR+">>httbar(100,0,1)",cut+" && "+bLR+">-1")
    httbar = ROOT.gDirectory.Get("httbar")
    httbar.Scale(tt_scalefac)
    yttbarBR *= tt_scalefac
    httbar.SetFillColor(2)
    httbar.SetLineColor(0)
    p1.Update()

    if saveplots: c1.SaveAs("./QCD_estimate_plots/ttbar_"+cat+"_"+BR+"_bLR.pdf")

    #raw_input('done ttbar: press any key to continue')

    yqcdBR = ydataBR - yttbarBR
    hqcd = hdata - httbar
    hqcd.SetTitle(("QCD bLR Region (QR);" if validation else "bLR Region (BR);")+"bLR_"+str(nbjet)+"b_2b;Events" )
    hqcd.SetFillColor(8)
    hqcd.SetLineColor(0)
    hqcd.Draw("hist")
    p1.Update()

    if saveplots: c1.SaveAs("./QCD_estimate_plots/qcd_"+cat+"_"+BR+"_bLR.pdf")

    #raw_input('done qcd: press any key to continue')

    hstack = ROOT.THStack ("hstack",("QCD bLR Region (QR);" if validation else "bLR Region (BR);")+"bLR_"+str(nbjet)+"b_2b;Events")
    hstack.Add(hqcd)
    hstack.Add(httbar)
    hstack.Draw("hist")
    hdata.Draw("pesame")
    p1.Update()

    if saveplots: c1.SaveAs("./QCD_estimate_plots/stack_"+cat+"_"+BR+"_bLR.pdf")

    #print "tt_scalefac =",tt_scalefac
    #print cut+" && "+bLR+">-1"

    c2 = ROOT.TCanvas("c2","",5,30,640,580)
    p2 = ROOT.TPad("p2","",0,0,1,1)
    p2.SetTopMargin(0.08)
    p2.SetRightMargin(0.05)
    p2.Draw()
    p2.cd()

    ydataCR = tdata.Draw(variable+">>hdataCR"+binning,cutCR)
    hdataCR = ROOT.gDirectory.Get("hdataCR")
    hdataCR.SetLineColor(1)
    hdataCR.SetMarkerColor(1)
    hdataCR.SetMarkerStyle(20)
    hdataCR.SetMarkerSize(1)
    hdataCR.Sumw2()

    if saveplots: c2.SaveAs("./QCD_estimate_plots/data_"+cat+"_"+CR+"_"+var+".pdf")

    #raw_input('done dataCR: press any key to continue')

    yttbarCR = tttbar.Draw(variable+">>httbarCR"+binning,cutCR+" && "+bLR+">-1")
    httbarCR = ROOT.gDirectory.Get("httbarCR")
    #print "Integral",httbar.Integral()
    httbarCR.Scale(tt_scalefac)
    yttbarCR *= tt_scalefac
    httbarCR.SetFillColor(2)
    httbarCR.SetLineColor(0)
    p2.Update()

    if saveplots: c2.SaveAs("./QCD_estimate_plots/ttbar_"+cat+"_"+CR+"_"+var+".pdf")

    #raw_input('done ttbarCR: press any key to continue')

    yqcdCR = ydataCR - yttbarCR
    hqcdCR = hdataCR - httbarCR
    hqcdCR.SetTitle(("Control Region 2 (CR2);" if validation else "Control region (CR);")+variable+";Events" )
    hqcdCR.SetFillColor(8)
    hqcdCR.SetLineColor(0)
    hqcdCR.Draw("hist")
    p2.Update()

    if saveplots: c2.SaveAs("./QCD_estimate_plots/qcd_"+cat+"_"+CR+"_"+var+".pdf")

    #raw_input('done qcdCR: press any key to continue')

    hstackCR = ROOT.THStack ("hstackCR",("Control Region 2 (CR2);" if validation else "Control region (CR);")+variable+";Events")
    hstackCR.Add(hqcdCR)
    hstackCR.Add(httbarCR)
    hstackCR.Draw("hist")
    hdataCR.Draw("pesame")
    p2.Update()

    if saveplots: c2.SaveAs("./QCD_estimate_plots/stack_"+cat+"_"+CR+"_"+var+".pdf")

    c3 = ROOT.TCanvas("c3","",5,30,640,580)
    p3 = ROOT.TPad("p3","",0,0,1,1)
    p3.SetTopMargin(0.08)
    p3.SetRightMargin(0.05)
    p3.Draw()
    p3.cd()

    ydataSR = tdata.Draw(variable+">>hdataSR"+binning,cutSR)
    hdataSR = ROOT.gDirectory.Get("hdataSR")
    hdataSR.SetLineColor(1)
    hdataSR.SetMarkerColor(1)
    hdataSR.SetMarkerStyle(20)
    hdataSR.SetMarkerSize(1)
    hdataSR.Sumw2()

    if saveplots: c3.SaveAs("./QCD_estimate_plots/data_"+cat+"_"+SR+"_"+var+".pdf")

    #raw_input('done dataSR: press any key to continue')

    yttbarSR = tttbar.Draw(variable+">>httbarSR"+binning,cutSR+" && "+bLR+">-1")
    httbarSR = ROOT.gDirectory.Get("httbarSR")
    httbarSR.Scale(tt_scalefac)
    yttbarSR *= tt_scalefac
    httbarSR.SetFillColor(2)
    httbarSR.SetLineColor(0)
    p3.Update()

    if saveplots: c3.SaveAs("./QCD_estimate_plots/ttbar_"+cat+"_"+SR+"_"+var+".pdf")

    #raw_input('done ttbarSR: press any key to continue')

    yqcdSR = ydataSR - yttbarSR
    hqcdSR = hdataSR - httbarSR
    hqcdSR.SetTitle(("Validation Region (VR);" if validation else "Signal region (SR);")+var+";Events")
    hqcdSR.SetTitle
    hqcdSR.SetFillColor(8)
    hqcdSR.SetLineColor(0)
    hqcdSR.Draw("hist")
    p3.Update()

    #hQCD = hdata - httbar
    #hQCD.SetLineColor(8)
    #hQCD.Draw("hist")

    if saveplots: c3.SaveAs("./QCD_estimate_plots/qcd_"+cat+"_"+SR+"_"+var+".pdf")

    hstackSR = ROOT.THStack ("hstackSR",("Validation Region (VR);" if validation else "Signal region (SR);")+variable+";Events")
    hstackSR.Add(hqcdSR)
    hstackSR.Add(httbarSR)
    hstackSR.Draw("hist")
    hdataSR.Draw("pesame")
    p3.Update()

    if saveplots: c3.SaveAs("./QCD_estimate_plots/stack_"+cat+"_"+SR+"_"+var+".pdf")

    ########## closure test #########

    c4 = ROOT.TCanvas("c4","",5,30,640,580)
    p4 = ROOT.TPad("p4","",0,0.155,1,1)
    p4.SetTopMargin(0.08)
    p4.SetRightMargin(0.05)
    p4.Draw()
    p4.cd()

    hqcd_check = hqcdCR.Clone()
    hqcd_check.Scale(yqcdSR/yqcdCR)

    herr_check = hqcd_check.Clone()
    herr_check.Add(httbarSR)

    hstack_check = ROOT.THStack ("hstack_check",("Validation Region (VR) check;" if validation else "Signal region (SR) check;")+variable+";Events")
    hstack_check.Add(hqcd_check)
    hstack_check.Add(httbarSR)
    hstack_check.SetMaximum( max(hstack_check.GetMaximum(),hdataSR.GetMaximum())*1.1 )
    hstack_check.Draw("hist")
    hdataSR.Draw("pesame")
    p4.Update()

    c4.cd()
    p4r = ROOT.TPad("p4","",0,0,1,0.175)
    p4r.SetRightMargin(0.05)
    p4r.Draw()
    p4r.cd()

    xmin = float(binning.split(",")[1])
    xmax = float(binning.split(",")[2].split(")")[0])
    one = ROOT.TF1("one","1",xmin,xmax)
    one.SetLineColor(1)
    one.SetLineStyle(2)
    one.SetLineWidth(1)

    nxbins = herr_check.GetNbinsX()
    hratio = hdataSR.Clone()

    for b in range(nxbins):

        nbkg = herr_check.GetBinContent(b+1)
        ndata = hdataSR.GetBinContent(b+1)
        edata = hdataSR.GetBinError(b+1)

        r = ndata / nbkg if nbkg>0 else 0
        rerr = edata / nbkg if nbkg>0 else 0

        hratio.SetBinContent(b+1, r);
        hratio.SetBinError(b+1,rerr);

    hratio.SetTitle("")
    hratio.GetYaxis().SetRangeUser(0.0,3.0)
    hratio.GetYaxis().SetTitleSize(0.18)
    hratio.GetYaxis().SetTitleOffset(0.24)
    hratio.GetYaxis().SetTitle("Data/MC  ")
    hratio.GetYaxis().SetNdivisions(202);
    hratio.GetYaxis().SetLabelSize(0.16)

    hratio.Draw("pe")
    one.Draw("SAME")
    #hratio.Draw("pesame")
    #p4r.Update()

    if saveplots: c4.SaveAs("./QCD_estimate_plots/check_"+cat+"_"+SR+"_"+var+".pdf")

    print "Region data ttbar qcd"
    print "QR" if validation else "BR",ydataBR,yttbarBR,yqcdBR
    print "CR2" if validation else"CR",ydataCR,yttbarCR,yqcdCR
    print "VR" if validation else"SR",ydataSR,yttbarSR,yqcdSR

    #raw_input('done qcdSR: press Enter to quit')
    sleep(5)

#end loop over variables
raw_input('done: press Enter to quit')
