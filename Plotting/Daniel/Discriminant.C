#define RUNONDATA 0
#define LOGSCALE 0
#define RATIO 0
#define NORMALIZE 1
#define POISSON 0
#define SAVEPLOTS 1
#define CAT 12  // 7, 8, 9, 10, 11 or <0 for all
#define METHOD 13 // 11=4w2h2t, 12=3w2h2t, 13=4w2h1t, 14=3w2h1t, 15=0w2w2h2t, 16=1w1w2h2t, 17=4w1h2t, 18=4w1h2t/4w2h1t
#define CUT_HT 500.0
#define PSB_FAC "0.02" //"2.0e-10" // 2j:4.0e5  3j:1.0e4  4j:5.0e4
#define QCD 0
#define LUMI 36.8
#define TTSPLIT 1

#include <fstream>

void Discriminant(){

  TStopwatch* clock = new TStopwatch();
  clock->Start();

  int nbins = 6;
  //float xbins[nbins+1] = {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0};
  float xbins[nbins+1];
  for(i=0;i<=nbins;i++){
    xbins[i] = 1.0/nbins * i;
  }

  float xmin  = 0.0;
  float xmax  = 1.0;

  string version = "JoosepFeb_nosyst_v1_v2";

  string folder = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/projectSkimFH/"+version+"/";

  string variable;
  variable = "Psb";

  string tag = "_"; //"_Psb0pt55";
  tag += version;
  string method = "";
  if(CUT_HT>0) tag += Form("_HT%.0f",CUT_HT);  
  if(CAT<0) tag += "_catAll_";
  else tag += Form("_cat%d_",CAT);
  tag += PSB_FAC;
  if(TTSPLIT) tag += "_ttsplit";
  if(RUNONDATA) tag += "_data";
  if(LOGSCALE)  tag += "_log";
  if(RATIO)  tag += "_ratio";  

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
  string element="";
  string cat="0";
  if(METHOD==11) {method = "_4w2h2t"; element="11";}
  else if(METHOD==12) {method = "_3w2h2t";  element="12";}
  else if(METHOD==13) {method = "_4w2h1t";  element="13";}
  else if(METHOD==14) {method = "_3w2h1t";  element="14";}
  else if(METHOD==15) {method = "_0w2w2h2t";  element="15";}
  else if(METHOD==16) {method = "_1w1w2h2t";  element="16";}
  else if(METHOD==17) {method = "_4w1h2t";  element="17";}
  else if(METHOD==18) {method = "_4w1h2t_2h1t";  element="18";}

  if(CAT==7){
    cat = "cat==7 &&  btag_LR_4b_2b_btagCSV>0.99 && qg_LR_4b_flavour_3q_0q>0.5";
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
  
  //scale to luminosity (pb-1 --> fb-1)
  double lumi = 1000.0 * LUMI;

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
  TH1F* h1 = new TH1F("h1","; P_{s/b}; Events", nbins, xbins );  
  
  h1->GetXaxis()->SetTitleFont(62);
  h1->GetXaxis()->SetTitleSize(0.04);
  h1->GetXaxis()->SetLabelFont(62);
  h1->GetXaxis()->SetLabelSize(0.038);

  h1->GetYaxis()->SetTitleFont(62);
  h1->GetYaxis()->SetTitleSize(0.039);
  h1->GetYaxis()->SetLabelFont(62);
  h1->GetYaxis()->SetLabelSize(0.038);
  h1->GetYaxis()->SetTitleOffset(1.5);

  hsignal  = (TH1F*)h1->Clone("hsignal");
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
  herr  = (TH1F*)h1->Clone("herr");
  hdata  = (TH1F*)h1->Clone("hdata");
  
  hsignal->Sumw2();
  htth->Sumw2();
  httj->Sumw2();
  httbb->Sumw2();
  htt2b->Sumw2();
  httb->Sumw2();
  httcc->Sumw2();
  httjj->Sumw2();
  hqcd->Sumw2();

  string selection = "(ht>";
  selection += Form("%.0f",CUT_HT);
  selection += " && nBCSVM>=2 && ";
  selection += cat;
  //selection += " && HLT_ttH_FH>0";  //TRIGGER SELECTION
  string ttbbsel = selection + " && ttCls>52)";
  string tt2bsel = selection + " && ttCls==52)";
  string ttbsel = selection + " && ttCls==51)";
  string ttccsel = selection + " && ttCls>40 && ttCls<46)";
  string ttjjsel = selection + " && ttCls<40)";
  selection += ")";

  TString draw = "";
  if(QCD==0) draw = ("mem_tth_FH"+method+"_p/(mem_tth_FH"+method+"_p+"+PSB_FAC+"*mem_ttbb_FH"+method+"_p)").c_str();
  method = "_4w1h2t";
  if(METHOD==18) draw = ("mem_tth_FH"+method+"_p/(mem_tth_FH"+method+"_p+"+PSB_FAC+"*mem_ttbb_FH_4w2h1t_p)").c_str();
  if(QCD==1) draw = ("mem_tth_FH"+method+"_p/(mem_tth_FH"+method+"_p+"+PSB_FAC+"*mem_qcd_FH"+method+"_p)").c_str();
  //TString draw = "1.0*numJets/(2.0*numJets)";
  TString cut = selection.c_str();
  TString ttbbcut = ttbbsel.c_str();
  TString tt2bcut = tt2bsel.c_str();
  TString ttbcut = ttbsel.c_str();
  TString ttcccut = ttccsel.c_str();
  TString ttjjcut = ttjjsel.c_str();
  
  cout << draw << endl;
  cout << cut << endl;

  tsignal->Draw(draw+">>hsignal",cut);
  tsignal->Draw(draw+">>htth",cut);
  tttj->Draw(draw+">>httj",cut);
  tttj->Draw(draw+">>httbb",ttbbcut);
  tttj->Draw(draw+">>htt2b",tt2bcut);
  tttj->Draw(draw+">>httb",ttbcut);
  tttj->Draw(draw+">>httcc",ttcccut);
  tttj->Draw(draw+">>httjj",ttjjcut);
  tqcd3 ->Draw(draw+">>hqcd3",cut);
  tqcd5 ->Draw(draw+">>hqcd5",cut);
  tqcd7 ->Draw(draw+">>hqcd7",cut);
  tqcd10->Draw(draw+">>hqcd10",cut);
  tqcd15->Draw(draw+">>hqcd15",cut);
  tqcd20->Draw(draw+">>hqcd20",cut);

  hsignal->Scale(lumi*scalefacttH*10.0);
  htth->Scale(lumi*scalefacttH);
  httj->Scale(lumi*scalefacTTbar);
  httbb->Scale(lumi*scalefacTTbar);
  htt2b->Scale(lumi*scalefacTTbar);
  httb->Scale(lumi*scalefacTTbar);
  httcc->Scale(lumi*scalefacTTbar);
  httjj->Scale(lumi*scalefacTTbar);
  //hqcd->Add(hqcd3,lumi*scalefacQCD3); //exclude QCD300 due to large weights
  hqcd->Add(hqcd5,lumi*scalefacQCD5); 
  hqcd->Add(hqcd7,lumi*scalefacQCD7);
  hqcd->Add(hqcd10,lumi*scalefacQCD10);
  hqcd->Add(hqcd15,lumi*scalefacQCD15);
  hqcd->Add(hqcd20,lumi*scalefacQCD20);

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
  
  if( RATIO ){
    c1 = new TCanvas("c1","",5,30,640,580/0.85);
    p1 = new TPad("p1","",0,0.155,1,1);
  }

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
  if(RUNONDATA==0) cmsinfo = Form("Simulation                                               %.1f fb^{-1} (13 TeV)",LUMI);
  else cmsinfo =             Form("CMS Preliminary                                     %.1f fb^{-1} (13 TeV)",LUMI);

  TPaveText *pt_title = new TPaveText(0.11, 0.952, 0.95, 1.0,"brNDC");
  pt_title->SetFillStyle(1001);
  pt_title->SetBorderSize(0);
  pt_title->SetFillColor(0);
  pt_title->SetTextFont(42); 
  pt_title->SetTextSize(0.04); 
  pt_title->AddText(cmsinfo);

  TPaveText *pt_lumi = new TPaveText(0.68, 0.951, 0.95, 1.0,"brNDC");
  pt_lumi->SetFillStyle(1001);
  pt_lumi->SetBorderSize(0);
  pt_lumi->SetFillColor(0);
  pt_lumi->SetTextFont(42); 
  pt_lumi->SetTextSize(0.04);
  pt_lumi->SetTextAlign(12); //left, centre 
  pt_lumi->AddText( Form("%.1f fb^{-1} (13 TeV)",LUMI) );

  //TPaveText *pt_CMS = new TPaveText(0.15, 0.84, 0.30, 0.90,"brNDC"); //inside
  TPaveText *pt_CMS = new TPaveText(0.11, 0.951, 0.21, 1.0,"brNDC"); //top
  pt_CMS->SetFillStyle(1001);
  pt_CMS->SetBorderSize(0);
  pt_CMS->SetFillColor(0);
  pt_CMS->SetTextFont(61); 
  pt_CMS->SetTextSize(0.05);
  pt_CMS->SetTextAlign(12); 
  pt_CMS->AddText("CMS");

  //TPaveText *pt_Prelim = new TPaveText(0.15, 0.78, 0.35, 0.84,"brNDC"); //inside
  TPaveText *pt_Prelim = new TPaveText(0.205, 0.951, 0.41, 1.0,"brNDC"); //top
  pt_Prelim->SetFillStyle(0);
  pt_Prelim->SetBorderSize(0);
  pt_Prelim->SetFillColor(0);
  pt_Prelim->SetTextFont(52); 
  pt_Prelim->SetTextSize(0.05*0.76);
  pt_Prelim->SetTextAlign(12); 
  pt_Prelim->AddText("Simulation");

  TLegend* leg = new TLegend(0.42,0.54,0.67,0.91,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04);

  THStack* hStack = new THStack("hStack","Title; x-axis ; events ");

  //histrogram colors (index, r, b, g)
  TColor *coltth = new TColor(9001, 44/255., 62/255., 167/255.);
  TColor *colttbb = new TColor(9002, 102/255., 0/255., 0/255.);
  TColor *coltt2b = new TColor(9003, 80/255., 0/255., 0/255.);
  TColor *colttb = new TColor(9004, 153/255., 51/255., 51/255.);
  TColor *colttcc = new TColor(9005, 204/255., 2/255., 0/255.);
  TColor *colttjj = new TColor(9006, 251/255., 102/255., 102/255.);
  TColor *colqcd = new TColor(9007, 102/255., 201/255., 77/255.);

  // set histogram styles
  hsignal->SetLineWidth( 4 );
  hsignal->SetLineColor( 9001 ); //kBlue+2
  //hsignal->Sumw2();
  htth ->SetLineColor( 9001 ); //kBlue+2
  htth ->SetFillColor( 9001 );
  htth ->SetFillStyle( 3002 );
  htth ->SetMarkerColor( 9001 );
  htth ->SetMarkerStyle( 20 );
  htth ->SetMarkerSize( 1.5 );
  //htth ->Sumw2();
  hqcd ->SetLineColor( 9007 ); //kGreen+3
  hqcd ->SetFillColor( 9007 );
  hqcd ->SetMarkerColor( 9007 );
  hqcd ->SetMarkerStyle( 21 );
  hqcd ->SetMarkerSize( 1.5 );
  //hqcd ->Sumw2();
  httj ->SetLineColor( kRed+1 );
  httj ->SetFillColor( kRed+1 );
  httj ->SetMarkerColor( kRed+1 );
  httj ->SetMarkerStyle( 34 );
  httj ->SetMarkerSize( 1.5 );
  //httj ->Sumw2();
  httbb ->SetLineColor( 9002 );
  httbb ->SetFillColor( 9002 );
  httbb ->SetMarkerColor( 9002 );
  httbb ->SetMarkerStyle( 22 );
  httbb ->SetMarkerSize( 1.5 );

  htt2b ->SetLineColor( 9003 );
  htt2b ->SetFillColor( 9003 );
  htt2b ->SetMarkerColor( 9003 );
  htt2b ->SetMarkerStyle( 23 );
  htt2b ->SetMarkerSize( 1.5 );

  httb ->SetLineColor( 9004 );
  httb ->SetFillColor( 9004 );
  httb ->SetMarkerColor( 9004 );
  httb ->SetMarkerStyle( 29 );
  httb ->SetMarkerSize( 1.5 );

  httcc ->SetLineColor( 9005 );
  httcc ->SetFillColor( 9005 );
  httcc ->SetMarkerColor( 9005 );
  httcc ->SetMarkerStyle( 33 );
  httcc ->SetMarkerSize( 1.5 );

  httjj ->SetLineColor( 9006 );
  httjj ->SetFillColor( 9006 );
  httjj ->SetMarkerColor( 9006 );
  httjj ->SetMarkerStyle( 34 );
  httjj ->SetMarkerSize( 1.5 );

  herr ->SetLineColor( kBlack );
  herr ->SetFillColor( kBlack );
  herr ->SetFillStyle( 3654 );
  hdata->SetMarkerStyle( 20 );
  hdata->SetMarkerSize( 1.5 );
  hdata->SetMarkerColor( kBlack );
  hdata->SetLineColor( kBlack );
  hdata->SetLineWidth( 2 );

  if( RUNONDATA){
    if( POISSON ) hdata->SetBinErrorOption(TH1::kPoisson);
    else hdata->Sumw2();
  }
  
  // add histrograms to background error
  herr->Add(hqcd, 1.0);
  herr->Add(httj, 1.0);
  
  // add histrograms to stack
  hStack->Add(hqcd);
  if(TTSPLIT){
    hStack->Add(httjj);
    hStack->Add(httcc);
    hStack->Add(httb);
    hStack->Add(htt2b);
    hStack->Add(httbb);
  }
  else hStack->Add(httj);
  hStack->Add(htth);
  
  // add histograms to legend
  leg->AddEntry(htth,  "t#bar{t}H (125)", "F");
  if(TTSPLIT){
    leg->AddEntry(httbb, "t#bar{t} + b#bar{b}", "P");
    leg->AddEntry(htt2b, "t#bar{t} + 2b", "P");
    leg->AddEntry(httb, "t#bar{t} + b", "P");
    leg->AddEntry(httcc, "t#bar{t} + c#bar{c}", "P");
    leg->AddEntry(httjj, "t#bar{t} + jj", "P");
  }
  else leg->AddEntry(httj, "t#bar{t} + jets", "F");
  leg->AddEntry(hqcd,  "QCD Multijet", "F");
  if(RUNONDATA) leg->AddEntry(hdata, "Data", "LPE");
  leg->AddEntry(herr,  "Bkg. Unc.", "F");
  leg->AddEntry(hsignal,"t#bar{t}H (125) x 10", "L");
 
  // set y-axis range
  float max =  TMath::Max( herr->GetMaximum()*1.15,(hdata!=0 ? hdata->GetMaximum()*1.45 : -1.));
  if(LOGSCALE){
    herr->GetYaxis()->SetRangeUser(1, max*8.0 );
    p1->SetLogy(1);
  }
  else herr->GetYaxis()->SetRangeUser(0, max );
  cout << "max range is " << max << endl;
  // draw histograms
  herr  ->Draw("HIST");
  hStack->Draw("HISTSAME");
  hsignal->Draw("HISTSAME");
  herr  ->Draw("E2SAME");
  if(hdata!=0) hdata->Draw("PE1SAME");
  leg->Draw();

  //pt_title->Draw();
  pt_lumi->Draw();
  pt_CMS->Draw();
  pt_Prelim->Draw();

    
  //-----------------------ratio plot-------------------
  if( RATIO ){
    
    c1->cd();
    TPad *p2 = new TPad("p1","",0,0,1,0.175);
    // p2->SetTopMargin(0.1);
    // p2->SetBottomMargin(0.3);
    // p2->SetLeftMargin(0.10);
    // p2->SetRightMargin(0.03);
    p2->SetGrid(0,0);
    p2->SetFillStyle(4000);
    p2->SetFillColor(10);
    p2->SetTicky();
    p2->SetObjectStat(0);
    p2->Draw();
    p2->cd();
    
    TF1* one = new TF1("one","1",0,1);

    TH1F* one_error = 0;
    one_error = (TH1F*)h1->Clone("one_error");
    
    TH1F* h_ratio = 0;
    h_ratio = (TH1F*)h1->Clone("h_ratio");

    TGraphAsymmErrors* g_ratio = new TGraphAsymmErrors(h1);
    if( g_ratio->GetN() != h_ratio->GetNbinsX() ){
      cout << "g_ratio has different number of bins to h_ratio. return!" << endl;
      return;
    }

    // loop over bins
    for(int b=1; b<= h_ratio->GetNbinsX() ; b++){

      float nbkg     = herr->GetBinContent(b);
      float nbkg_up  = herr->GetBinContent(b) + herr->GetBinError(b);
      float nbkg_low = herr->GetBinContent(b) - herr->GetBinError(b);
    
      float ndata      = herr->GetBinContent(b);
      float ndataErr   = herr->GetBinError(b);  
      if(RUNONDATA){
	ndata      = hdata->GetBinContent(b);
	ndataErr   = hdata->GetBinError(b);
      }

      float r       = nbkg>0 ? ndata/nbkg      : 0;
      float rErr    = nbkg>0 ? ndataErr/nbkg   : 0;

      float one_up  = nbkg_low >0 ? nbkg/nbkg_low : 0;
      float one_low = nbkg_up  >0 ? nbkg/nbkg_up  : 0;

      float xPoint  = h1->GetBinCenter(b);
      float xWidth  = 0.5*h1->GetBinWidth(b);

      h_ratio->SetBinContent(b, r);
      h_ratio->SetBinError(b,rErr);

      if(RUNONDATA && POISSON){

	float dataErrLow = hdata->GetBinErrorLow(b);
	float dataErrUp  = hdata->GetBinErrorUp(b);
	float rErrUp     = nbkg>0 ? dataErrUp/nbkg  : 0;
	float rErrLow    = nbkg>0 ? dataErrLow/nbkg : 0;

	g_ratio->SetPoint(b-1, xPoint, r);
	g_ratio->SetPointEYlow(b-1, rErrLow);
	g_ratio->SetPointEYhigh(b-1, rErrUp);
	g_ratio->SetPointEXlow(b-1, xWidth);
	g_ratio->SetPointEXhigh(b-1, xWidth);
      }

      one_error->SetBinContent(b, 1.0);
      one_error->SetBinError(b, (one_up-one_low)/2 );
    
    } //end loop over bins

    // set ratio histogram styles
    one_error->SetTitle(0);
    one_error->GetYaxis()->SetRangeUser(0.0,2.0);

    one_error->GetXaxis()->SetTitle(0);
    one_error->GetXaxis()->SetLabelSize(0);
    one_error->GetXaxis()->SetNdivisions(0);
    one_error->GetXaxis()->SetTickLength(0.1);

    one_error->GetYaxis()->SetTitleSize(0.18);
    one_error->GetYaxis()->SetTitleOffset(0.24);
    one_error->GetYaxis()->SetTitle("Data/MC  ");
    one_error->GetYaxis()->SetNdivisions(202);
    one_error->GetYaxis()->SetLabelSize(0.16);

    one_error->SetFillColor(kGreen);

    h_ratio->SetMarkerStyle(20);
    h_ratio->SetMarkerSize(1.5);
    h_ratio->SetMarkerColor(kBlack);
    h_ratio->SetLineColor(kBlack);
    h_ratio->SetLineWidth(2);

    g_ratio->SetMarkerStyle(20);
    g_ratio->SetMarkerSize(1.5);
    g_ratio->SetMarkerColor(kBlack);
    g_ratio->SetLineColor(kBlack);
    g_ratio->SetLineWidth(2);

    one->SetLineColor(kBlack);
    one->SetLineStyle(kDashed);
    one->SetLineWidth(1);

    one_error->Draw("E2");
    one->Draw("SAME");
    if(RUNONDATA && POISSON) g_ratio->Draw("PE1SAME");
    else h_ratio->Draw("PE1SAME");

  } //end ratio plot
  
  
  // save plots
  if( SAVEPLOTS ){
    c1->SaveAs(  ("./MED_plots/AH_"+variable+tag+".pdf").c_str() ); 
  }

  // Normalized plot
  if( NORMALIZE ){
    TCanvas *c2 = new TCanvas("c2","",5,30,640,580);
    TPad *p3 = new TPad("p2","",0,0,1,1);
  
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

    int lw = 4;

    htth ->SetLineWidth( lw );
    //htth ->SetFillStyle( 0 );

    hqcd ->SetLineWidth( lw );
    //hqcd ->SetFillStyle( 0 );

    httj ->SetLineWidth( lw );
    //httj ->SetFillStyle( 0 );
    httbb ->SetLineWidth( lw );
    htt2b ->SetLineWidth( lw );
    httb ->SetLineWidth( lw );
    httcc ->SetLineWidth( lw );
    httjj ->SetLineWidth( lw );


    hqcd ->GetYaxis()->SetTitle("Normalized units");
    hqcd ->SetMinimum( 0.0 );
    float normmax = TMath::Max( hqcd->GetMaximum(), htth->GetMaximum()*hqcd->Integral()/htth->Integral() );
    hqcd ->SetMaximum( normmax*1.2 );   //CHANGE HERE
    hqcd ->DrawNormalized("PE");
    if(TTSPLIT){
      httbb->DrawNormalized("PESAME");
      htt2b->DrawNormalized("PESAME");
      httb->DrawNormalized("PESAME");
      httcc->DrawNormalized("PESAME");
      httjj->DrawNormalized("PESAME");  
    }
    else httj->DrawNormalized("PESAME");
    htth ->DrawNormalized("PESAME");
    leg->Draw();
    pt_title->Draw();

    if( SAVEPLOTS ){
      c2->SaveAs(  ("./MED_plots/AH_"+variable+tag+"_norm.pdf").c_str() ); 
    }
  }
  
  return;
}
