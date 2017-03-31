#define RUNONDATA 0
#define LOGSCALE 0
#define POISSON 0
#define SAVEPLOTS 1
#define CAT 12  // 7, 8, 9, 10, 11 or <0 for all
#define METHOD 13 // 11=4w2h2t, 12=3w2h2t, 13=4w2h1t, 14=0w0w2h2t, 15=0w0w2h1t
#define CUT_HT 500.0
#define QCD 0
#define TTSPLIT 1

#include <fstream>

void Probability(){

  TStopwatch* clock = new TStopwatch();
  clock->Start();

  int nbins = 120;
  float xmin  = -60.0;
  float xmax  = 0.0;

  float xbins[nbins+1];
  for(i=0;i<=nbins;i++){
    xbins[i] = xmin + (xmax-xmin)/nbins * i;
  }

  string version = "JoosepFeb_nosyst_v1_v2";

  string folder = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/projectSkimFH/"+version+"/";

  string tag = "_";
  tag += version;
  string method = "";
  if(CUT_HT>0) tag += Form("_HT%.0f",CUT_HT);  
  if(CAT<0) tag += "_catAll";
  else tag += Form("_cat%d",CAT);
  if(TTSPLIT) tag += "_ttsplit";
  if(RUNONDATA) tag += "_data";
  if(LOGSCALE)  tag += "_log"; 

  // load files
  TFile* fsignal = TFile::Open( (folder+"ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root").c_str() );
  if(fsignal==0 || fsignal->IsZombie() ) return;
  
  TFile* fttj = TFile::Open( (folder+"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root").c_str() );
  if(fttj==0 || fttj->IsZombie() ) return;
  
  TFile* fqcd3 = TFile::Open( (folder+"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root").c_str() );
  if(fqcd3==0 || fqcd3->IsZombie() ) return;
  TFile* fqcd5 = TFile::Open( (folder+"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root").c_str() );
  if(fqcd5==0 || fqcd5->IsZombie() ) return;
  TFile* fqcd7 = TFile::Open( (folder+"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root").c_str() );
  if(fqcd7==0 || fqcd7->IsZombie() ) return;
  TFile* fqcd10 = TFile::Open( (folder+"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root").c_str() );
  if(fqcd10==0 || fqcd10->IsZombie() ) return;
  TFile* fqcd15 = TFile::Open( (folder+"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root").c_str() );
  if(fqcd15==0 || fqcd15->IsZombie() ) return;
  TFile* fqcd20 = TFile::Open( (folder+"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root").c_str() );
  if(fqcd20==0 || fqcd20->IsZombie() ) return;
  
  // determine ME method used
  string cat="0";
  if(METHOD==11) method = "_4w2h2t";
  else if(METHOD==12) method = "_3w2h2t";
  else if(METHOD==13) method = "_4w2h1t";
  else if(METHOD==14) method = "_0w0w2h2t";
  else if(METHOD==15) method = "_0w0w2h1t";

  if(CAT==7){
    cat = "cat==7 && btag_LR_4b_2b_btagCSV>0.99 && qg_LR_4b_flavour_3q_0q>0.5";
  }
  else if(CAT==8){
    cat = "cat==8 && btag_LR_4b_2b_btagCSV>0.99 && qg_LR_4b_flavour_4q_0q>0.5";
  }
  else if(CAT==9){
    cat = "cat==9 && btag_LR_4b_2b_btagCSV>0.99 && qg_LR_4b_flavour_4q_0q>0.5"; //5q to come
  }
  else if(CAT==10){
    cat = "cat==10 && btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.83 && qg_LR_3b_flavour_4q_0q>0.5";
  }
  else if(CAT==11){
    cat = "cat==11 && btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.83 && qg_LR_3b_flavour_4q_0q>0.5";
  }
  else if(CAT==12){
    cat = "cat==12 && btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.83 && qg_LR_3b_flavour_4q_0q>0.5";
  }
  if(CAT>=0) tag += method;
  
  // QCD scale factors (xsec/nGen) - scales to 1 pb-1
  // for JoosepFeb_nonsyst_v1_v2
  double scalefacttH = 0.5085*0.577 / 3820351.0;
  double scalefacTTbar = 831.76 / 77206913.0;
  double scalefacQCD3 = 351300.0 / 53992057.0;
  double scalefacQCD5 = 31630.0 / 59204623.0;
  double scalefacQCD7 = 6802.0 / 44868369.0;
  double scalefacQCD10 = 1206.0 / 15127293.0;
  double scalefacQCD15 = 120.4 / 3961038.0;
  double scalefacQCD20 = 25.25 / 1991645.0;

  // load trees
  TTree *tsignal = (TTree*)fsignal->Get("tree");
  TTree *tttj = (TTree*)fttj->Get("tree");
  TTree *tqcd3  = (TTree*)fqcd3->Get("tree");
  TTree *tqcd5  = (TTree*)fqcd5->Get("tree");
  TTree *tqcd7  = (TTree*)fqcd7->Get("tree");
  TTree *tqcd10 = (TTree*)fqcd10->Get("tree");
  TTree *tqcd15 = (TTree*)fqcd15->Get("tree");
  TTree *tqcd20 = (TTree*)fqcd20->Get("tree");
  
  // master histogram
  TH1F* h1 = new TH1F("h1","; log(Ps); Normalized units", nbins, xbins );  
  
  h1->GetXaxis()->SetTitleFont(62);
  h1->GetXaxis()->SetTitleSize(0.04);
  h1->GetXaxis()->SetLabelFont(62);
  h1->GetXaxis()->SetLabelSize(0.038);

  h1->GetYaxis()->SetTitleFont(62);
  h1->GetYaxis()->SetTitleSize(0.039);
  h1->GetYaxis()->SetLabelFont(62);
  h1->GetYaxis()->SetLabelSize(0.038);
  h1->GetYaxis()->SetTitleOffset(1.5);

  htth  = (TH1F*)h1->Clone("htth"); 
  httj  = (TH1F*)h1->Clone("httj");
  httbb = (TH1F*)h1->Clone("httbb");
  htt2b = (TH1F*)h1->Clone("htt2b");
  httb  = (TH1F*)h1->Clone("httb");
  httcc = (TH1F*)h1->Clone("httcc");
  httjj = (TH1F*)h1->Clone("httjj");
  hqcd  = (TH1F*)h1->Clone("hqcd");
  hqcd3  = (TH1F*)h1->Clone("hqcd3");
  hqcd5  = (TH1F*)h1->Clone("hqcd5");
  hqcd7  = (TH1F*)h1->Clone("hqcd7");
  hqcd10 = (TH1F*)h1->Clone("hqcd10");
  hqcd15 = (TH1F*)h1->Clone("hqcd15");
  hqcd20 = (TH1F*)h1->Clone("hqcd20");
  hdata  = (TH1F*)h1->Clone("hdata");
  
  // htth->Sumw2();
  // httj->Sumw2();
  // hqcd->Sumw2();

  string selection = "(ht>";
  selection += Form("%.0f",CUT_HT);
  selection += " && nBCSVM>=2 && ";
  selection += cat;
  //selection += " && HLT_ttH_FH>0";  //TRIGGER SELECTION
  //if(QCD==0) selection += " && mem_tth_FH"+method+"_p>mem_ttbb_FH"+method+"_p";
  //if(QCD==1) selection += " && mem_tth_FH"+method+"_p>mem_qcd_FH"+method+"_p";
  string ttbbsel = selection + " && ttCls>52)";
  string tt2bsel = selection + " && ttCls==52)";
  string ttbsel = selection + " && ttCls==51)";
  string ttccsel = selection + " && ttCls>40 && ttCls<46)";
  string ttjjsel = selection + " && ttCls<40)";
  selection += ")";

  TString drawS = "";
  drawS = ("log10(mem_tth_FH"+method+"_p)").c_str();
  TString drawB = "";
  if(QCD==0) drawB = ("log10(mem_ttbb_FH"+method+"_p)").c_str();
  if(QCD==1) drawB = ("log10(mem_qcd_FH"+method+"_p)").c_str();
  TString draw2D = "";
  if(QCD==0) draw2D = ("log10(mem_ttbb_FH"+method+"_p):log10(mem_tth_FH"+method+"_p)").c_str();
  if(QCD==1) draw2D = ("log10(mem_qcd_FH"+method+"_p):log10(mem_tth_FH"+method+"_p)").c_str();
  TString cut = selection.c_str();
  TString ttbbcut = ttbbsel.c_str();
  TString tt2bcut = tt2bsel.c_str();
  TString ttbcut = ttbsel.c_str();
  TString ttcccut = ttccsel.c_str();
  TString ttjjcut = ttjjsel.c_str();
  
  cout << drawS << endl;
  cout << cut << endl;

  cout << tsignal->Draw(drawS+">>htth",cut) << endl;
  tttj->Draw(drawS+">>httj",cut);
  tttj->Draw(drawS+">>httbb",ttbbcut);
  tttj->Draw(drawS+">>htt2b",tt2bcut);
  tttj->Draw(drawS+">>httb",ttbcut);
  tttj->Draw(drawS+">>httcc",ttcccut);
  tttj->Draw(drawS+">>httjj",ttjjcut);
  tqcd3 ->Draw(drawS+">>hqcd3",cut);
  tqcd5 ->Draw(drawS+">>hqcd5",cut);
  tqcd7 ->Draw(drawS+">>hqcd7",cut);
  tqcd10->Draw(drawS+">>hqcd10",cut);
  tqcd15->Draw(drawS+">>hqcd15",cut);
  tqcd20->Draw(drawS+">>hqcd20",cut);

  //htth->Scale(scalefacttH);
  httj->Scale(scalefacTTbar);
  httbb->Scale(scalefacTTbar);
  htt2b->Scale(scalefacTTbar);
  httb->Scale(scalefacTTbar);
  httcc->Scale(scalefacTTbar);
  httjj->Scale(scalefacTTbar);
  //hqcd->Add(hqcd3,scalefacQCD3); //exclude QCD300 due to large weights
  hqcd->Add(hqcd5,scalefacQCD5); 
  hqcd->Add(hqcd7,scalefacQCD7);
  hqcd->Add(hqcd10,scalefacQCD10);
  hqcd->Add(hqcd15,scalefacQCD15);
  hqcd->Add(hqcd20,scalefacQCD20);

  cout << endl;
  cout << "cat" << CAT << endl;
  cout << "ttH "   << htth->Integral() << endl;
  cout << "TTbar " << httj->Integral() << endl;
  cout << "QCD "   << hqcd->Integral() << endl;  
  cout << endl;

  gStyle->SetOptStat(0);
  gStyle->SetTitleH(0.04);

  TCanvas *c1 = new TCanvas("c1","",5,30,640,580);
  TPad *p1 = new TPad("p1","",0,0,1,1);

  p1->SetGrid(0,0);
  p1->SetFillStyle(4000);
  p1->SetFillColor(10);
  p1->SetTicky();
  p1->SetTicks(0,0);
  p1->SetObjectStat(0);
  p1->Draw();
  p1->cd();

  p1->SetTopMargin(0.05);
  p1->SetLeftMargin(0.11);
  p1->SetRightMargin(0.05);

  TString cmsinfo = "";
  if(RUNONDATA==0) cmsinfo = "CMS Simulation (13 TeV)";
  else cmsinfo = "CMS Preliminary (13 TeV)";

  TPaveText *pt_title = new TPaveText(0.11, 0.952, 0.95, 1.0,"brNDC");
  pt_title->SetFillStyle(1001);
  pt_title->SetBorderSize(0);
  pt_title->SetFillColor(0);
  pt_title->SetTextFont(42); 
  pt_title->SetTextSize(0.04); 
  pt_title->AddText(cmsinfo);

  TLegend* leg = new TLegend(0.15,0.54,0.42,0.91,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04);

  //histrogram colors (index, r, b, g)
  TColor *coltth = new TColor(9001, 44/255., 62/255., 167/255.);
  TColor *colttbb = new TColor(9002, 102/255., 0/255., 0/255.);
  TColor *coltt2b = new TColor(9003, 80/255., 0/255., 0/255.);
  TColor *colttb = new TColor(9004, 153/255., 51/255., 51/255.);
  TColor *colttcc = new TColor(9005, 204/255., 2/255., 0/255.);
  TColor *colttjj = new TColor(9006, 251/255., 102/255., 102/255.);
  TColor *colqcd = new TColor(9007, 102/255., 201/255., 77/255.);

  // set histogram style
  htth->SetLineWidth( 2 );
  htth ->SetLineColor( 9001 );
  htth ->SetFillStyle( 0 );
  htth ->SetMarkerColor( 9001 ); //kBlue+2
  htth ->SetMarkerStyle( 20 );
  htth ->SetMarkerSize( 1.5 );

  hqcd->SetLineWidth( 2 );
  hqcd ->SetLineColor( 9007 ); //kGreen+3
  hqcd ->SetFillStyle( 0 );
  hqcd ->SetMarkerColor( 9007 );
  hqcd ->SetMarkerStyle( 21 );
  hqcd ->SetMarkerSize( 1.5 );

  httj->SetLineWidth( 2 );
  httj ->SetLineColor( kRed+1 );
  httj ->SetFillStyle( 0 );
  httj ->SetMarkerColor( kRed+1 );
  httj ->SetMarkerStyle( 34 );
  httj ->SetMarkerSize( 1.5 );

  httbb->SetLineWidth( 2 );
  httbb ->SetLineColor( 9002 );
  httbb ->SetFillStyle( 0 );
  httbb ->SetMarkerColor( 9002 );
  httbb ->SetMarkerStyle( 22 );
  httbb ->SetMarkerSize( 1.5 );

  htt2b->SetLineWidth( 2 );
  htt2b ->SetLineColor( 9003 );
  htt2b ->SetFillStyle( 0 );
  htt2b ->SetMarkerColor( 9003 );
  htt2b ->SetMarkerStyle( 23 );
  htt2b ->SetMarkerSize( 1.5 );

  httb->SetLineWidth( 2 );
  httb ->SetLineColor( 9004 );
  httb ->SetFillStyle( 0 );
  httb ->SetMarkerColor( 9004 );
  httb ->SetMarkerStyle( 29 );
  httb ->SetMarkerSize( 1.5 );

  httcc->SetLineWidth( 2 );
  httcc ->SetLineColor( 9005 );
  httcc ->SetFillStyle( 0 );
  httcc ->SetMarkerColor( 9005 );
  httcc ->SetMarkerStyle( 33 );
  httcc ->SetMarkerSize( 1.5 );

  httjj->SetLineWidth( 2 );
  httjj ->SetLineColor( 9006 );
  httjj ->SetFillStyle( 0 );
  httjj ->SetMarkerColor( 9006 );
  httjj ->SetMarkerStyle( 34 );
  httjj ->SetMarkerSize( 1.5 );

  hdata->SetMarkerStyle( 20 );
  hdata->SetMarkerSize( 1.5 );
  hdata->SetMarkerColor( kBlack );
  hdata->SetLineColor( kBlack );
  hdata->SetLineWidth( 2 );

  if( RUNONDATA){
    if( POISSON )  hdata->SetBinErrorOption(TH1::kPoisson);
    else hdata->Sumw2();
  }
  
  // add histograms to legend
  leg->AddEntry(htth,  "t#bar{t}H (125)", "P");
  if(TTSPLIT){
    leg->AddEntry(httbb, "t#bar{t} + b#bar{b}", "P");
    leg->AddEntry(htt2b, "t#bar{t} + 2b", "P");
    leg->AddEntry(httb, "t#bar{t} + b", "P");
    leg->AddEntry(httcc, "t#bar{t} + c#bar{c}", "P");
    leg->AddEntry(httjj, "t#bar{t} + jj", "P");
  }
  else leg->AddEntry(httj, "t#bar{t} + jets", "P");
  leg->AddEntry(hqcd,  "QCD Multijet", "P");
  if(RUNONDATA) leg->AddEntry(hdata, "Data", "LPE");
 
  // set y-axis range
  float max =  TMath::Max( hqcd->GetMaximum()*1.8,(hdata!=0&&RUNONDATA ? hdata->GetMaximum()*1.45 : -1.));
  if(LOGSCALE){
    hqcd->GetYaxis()->SetRangeUser(1, max*8.0 );
    p1->SetLogy(1);
  }
  else hqcd->GetYaxis()->SetRangeUser(0, max );
  cout << "max range is " << max << endl;
  // draw histograms
  hqcd ->DrawNormalized("HIST");
  if(TTSPLIT){
    httbb->DrawNormalized("HISTSAME");
    htt2b->DrawNormalized("HISTSAME");
    httb->DrawNormalized("HISTSAME");
    httcc->DrawNormalized("HISTSAME");
    httjj->DrawNormalized("HISTSAME");  
  }
  else httj->DrawNormalized("HISTSAME");
  htth ->DrawNormalized("HISTSAME");
  if(hdata!=0&&RUNONDATA) hdata->DrawNormalized("PESAME");
  leg->Draw();
  pt_title->Draw();

  // save plots
  if( SAVEPLOTS ){
    c1->SaveAs(  ("./MED_plots/AH_logPs"+tag+".pdf").c_str() );
  }


  //////// background probability Ps
  TCanvas *c2 = new TCanvas("c2","",5,30,640,580);
  TPad *p2 = new TPad("p2","",0,0,1,1);

  p2->SetGrid(0,0);
  p2->SetFillStyle(4000);
  p2->SetFillColor(10);
  p2->SetTicky();
  p2->SetTicks(0,0);
  p2->SetObjectStat(0);
  p2->Draw();
  p2->cd();

  p2->SetTopMargin(0.05);
  p2->SetLeftMargin(0.11);
  p2->SetRightMargin(0.05);

  tsignal->Draw(drawB+">>htth",cut);
  tttj->Draw(drawB+">>httj",cut);
  tttj->Draw(drawB+">>httbb",ttbbcut);
  tttj->Draw(drawB+">>htt2b",tt2bcut);
  tttj->Draw(drawB+">>httb",ttbcut);
  tttj->Draw(drawB+">>httcc",ttcccut);
  tttj->Draw(drawB+">>httjj",ttjjcut);
  tqcd3 ->Draw(drawB+">>hqcd3",cut);
  tqcd5 ->Draw(drawB+">>hqcd5",cut);
  tqcd7 ->Draw(drawB+">>hqcd7",cut);
  tqcd10->Draw(drawB+">>hqcd10",cut);
  tqcd15->Draw(drawB+">>hqcd15",cut);
  tqcd20->Draw(drawB+">>hqcd20",cut);

  //htth->Scale(scalefacttH);
  httj->Scale(scalefacTTbar);
  httbb->Scale(scalefacTTbar);
  htt2b->Scale(scalefacTTbar);
  httb->Scale(scalefacTTbar);
  httcc->Scale(scalefacTTbar);
  httjj->Scale(scalefacTTbar);
  //hqcd->Add(hqcd3,scalefacQCD3); //exclude QCD300 due to large weights
  hqcd->Add(hqcd5,scalefacQCD5); 
  hqcd->Add(hqcd7,scalefacQCD7);
  hqcd->Add(hqcd10,scalefacQCD10);
  hqcd->Add(hqcd15,scalefacQCD15);
  hqcd->Add(hqcd20,scalefacQCD20);

  // set y-axis range
  max =  TMath::Max( hqcd->GetMaximum()*1.8,(hdata!=0&&RUNONDATA ? hdata->GetMaximum()*1.45 : -1.));
  if(LOGSCALE){
    hqcd->GetYaxis()->SetRangeUser(1, max*8.0 );
    p2->SetLogy(1);
  }
  else hqcd->GetYaxis()->SetRangeUser(0, max );

  hqcd->GetXaxis()->SetTitle("log(Pb)");
  // draw histograms
  hqcd ->DrawNormalized("HIST");
  if(TTSPLIT){
    httbb->DrawNormalized("HISTSAME");
    htt2b->DrawNormalized("HISTSAME");
    httb->DrawNormalized("HISTSAME");
    httcc->DrawNormalized("HISTSAME");
    httjj->DrawNormalized("HISTSAME");  
  }
  else httj->DrawNormalized("HISTSAME");
  htth ->DrawNormalized("HISTSAME");
  if(hdata!=0&&RUNONDATA) hdata->DrawNormalized("PESAME");
  leg->Draw();
  pt_title->Draw();
  
  // save plots
  if( SAVEPLOTS ){
    c2->SaveAs(  ("./MED_plots/AH_logPb"+tag+".pdf").c_str() );
  }

  // 2D plot
  TCanvas *c3 = new TCanvas("c3","",5,30,640,580);
  TPad *p3 = new TPad("p3","",0,0,1,1);
  
  p3->SetGrid(0,0);
  p3->SetFillStyle(4000);
  p3->SetFillColor(10);
  p3->SetTicky();
  p3->SetTicks(0,0);
  p3->SetObjectStat(0);
  p3->Draw();
  p3->cd();
  
  p3->SetTopMargin(0.05);
  p3->SetLeftMargin(0.11);
  p3->SetRightMargin(0.05);

  // master histogram
  TH2F* h2 = new TH2F("h2","; log(Ps); log(Pb); Normalized units", nbins, xbins, nbins, xbins );  
  
  h2->GetXaxis()->SetTitleFont(62);
  h2->GetXaxis()->SetTitleSize(0.04);
  h2->GetXaxis()->SetLabelFont(62);
  h2->GetXaxis()->SetLabelSize(0.038);

  h2->GetYaxis()->SetTitleFont(62);
  h2->GetYaxis()->SetTitleSize(0.039);
  h2->GetYaxis()->SetLabelFont(62);
  h2->GetYaxis()->SetLabelSize(0.038);
  h2->GetYaxis()->SetTitleOffset(1.5);

  TLegend* leg2 = new TLegend(0.62,0.14,0.87,0.51,NULL,"brNDC");
  leg2->SetFillStyle(0);
  leg2->SetBorderSize(0);
  leg2->SetFillColor(10);
  leg2->SetTextSize(0.04);

  htth_2  = (TH2F*)h2->Clone("htth_2"); 
  httj_2  = (TH2F*)h2->Clone("httj_2");
  httbb_2 = (TH2F*)h2->Clone("httbb_2");
  htt2b_2 = (TH2F*)h2->Clone("htt2b_2");
  httb_2  = (TH2F*)h2->Clone("httb_2");
  httcc_2 = (TH2F*)h2->Clone("httcc_2");
  httjj_2 = (TH2F*)h2->Clone("httjj_2");
  hqcd_2  = (TH2F*)h2->Clone("hqcd_2");
  hqcd3_2  = (TH2F*)h2->Clone("hqcd3_2");
  hqcd5_2  = (TH2F*)h2->Clone("hqcd5_2");
  hqcd7_2  = (TH2F*)h2->Clone("hqcd7_2");
  hqcd10_2 = (TH2F*)h2->Clone("hqcd10_2");
  hqcd15_2 = (TH2F*)h2->Clone("hqcd15_2");
  hqcd20_2 = (TH2F*)h2->Clone("hqcd20_2");
  hdata_2  = (TH2F*)h2->Clone("hdata_2");

  htth_2 ->SetMarkerColor( 9001 );
  htth_2 ->SetMarkerStyle( 20 );
  htth_2 ->SetMarkerSize( 0.6 );

  hqcd_2 ->SetMarkerColor( 9007 );
  hqcd_2 ->SetMarkerStyle( 21 );
  hqcd_2 ->SetMarkerSize( 0.6 );

  httj_2 ->SetMarkerColor( kRed+1 );
  httj_2 ->SetMarkerStyle( 34 );
  httj_2 ->SetMarkerSize( 0.6 );

  httbb_2 ->SetMarkerColor( 9002 );
  httbb_2 ->SetMarkerStyle( 22 );
  httbb_2 ->SetMarkerSize( 0.6 );

  htt2b_2 ->SetMarkerColor( 9003 );
  htt2b_2 ->SetMarkerStyle( 23 );
  htt2b_2 ->SetMarkerSize( 0.6 );

  httb_2 ->SetMarkerColor( 9004 );
  httb_2 ->SetMarkerStyle( 29 );
  httb_2 ->SetMarkerSize( 0.6 );

  httcc_2 ->SetMarkerColor( 9005 );
  httcc_2 ->SetMarkerStyle( 33 );
  httcc_2 ->SetMarkerSize( 0.6 );

  httjj_2 ->SetMarkerColor( 9006 );
  httjj_2 ->SetMarkerStyle( 34 );
  httjj_2 ->SetMarkerSize( 0.6 );

  // add histograms to legend
  leg2->AddEntry(htth,  "t#bar{t}H (125)", "P");
  if(TTSPLIT){
    leg2->AddEntry(httbb, "t#bar{t} + b#bar{b}", "P");
    leg2->AddEntry(htt2b, "t#bar{t} + 2b", "P");
    leg2->AddEntry(httb, "t#bar{t} + b", "P");
    leg2->AddEntry(httcc, "t#bar{t} + c#bar{c}", "P");
    leg2->AddEntry(httjj, "t#bar{t} + jj", "P");
  }
  else leg2->AddEntry(httj, "t#bar{t} + jets", "P");
  leg2->AddEntry(hqcd,  "QCD Multijet", "P");
  if(RUNONDATA) leg2->AddEntry(hdata, "Data", "P");

  tsignal->Draw(draw2D+">>htth_2",cut);
  tttj->Draw(draw2D+">>httj_2",cut);
  tttj->Draw(draw2D+">>httbb_2",ttbbcut);
  tttj->Draw(draw2D+">>htt2b_2",tt2bcut);
  tttj->Draw(draw2D+">>httb_2",ttbcut);
  tttj->Draw(draw2D+">>httcc_2",ttcccut);
  tttj->Draw(draw2D+">>httjj_2",ttjjcut);
  tqcd3 ->Draw(draw2D+">>hqcd3_2",cut);
  tqcd5 ->Draw(draw2D+">>hqcd5_2",cut);
  tqcd7 ->Draw(draw2D+">>hqcd7_2",cut);
  tqcd10->Draw(draw2D+">>hqcd10_2",cut);
  tqcd15->Draw(draw2D+">>hqcd15_2",cut);
  tqcd20->Draw(draw2D+">>hqcd20_2",cut);

  htth_2->Scale(scalefacttH);
  httj_2->Scale(scalefacTTbar);
  httbb_2->Scale(scalefacTTbar);
  htt2b_2->Scale(scalefacTTbar);
  httb_2->Scale(scalefacTTbar);
  httcc_2->Scale(scalefacTTbar);
  httjj_2->Scale(scalefacTTbar);
  //hqcd_2->Add(hqcd3_2,scalefacQCD3); //exclude QCD300 due to large weights
  hqcd_2->Add(hqcd5_2,scalefacQCD5); 
  hqcd_2->Add(hqcd7_2,scalefacQCD7);
  hqcd_2->Add(hqcd10_2,scalefacQCD10);
  hqcd_2->Add(hqcd15_2,scalefacQCD15);
  hqcd_2->Add(hqcd20_2,scalefacQCD20);

  hqcd_2 ->Draw("");
  if(TTSPLIT){
    httbb_2->Draw("SAME");
    htt2b_2->Draw("SAME");
    httb_2->Draw("SAME");
    httcc_2->Draw("SAME");
    httjj_2->Draw("SAME");  
  }
  else httj_2->Draw("SAME");
  htth_2 ->Draw("SAME");
  leg2->Draw();
  pt_title->Draw();
  
  if( SAVEPLOTS ){
    c3->SaveAs(  ("./MED_plots/AH_logPs_v_logPb"+tag+".pdf").c_str() );
  }
  
  return;
}
