#define SAVEPLOTS 1
#define CAT 12
#define CUT_HT 500.0
#define PSB_FAC "0.02" // 2j:4.0e5  3j:1.0e4  4j:5.0e4
#define QCD 0
#define MULTIINT 0

void ROC_curve(){
  
  const int abins = 100; //1000; //100
  const int bbins = 50; //10000; //50
  const int cbins = 20; //1000; //20
  float a = 0.0001;
  float b = 0.9; //0.99999; //0.9

  const int nbins = abins+bbins+cbins;
  float xbins[nbins+1] = {0};
  for(int j=0; j<nbins+1; j++){
    if(j<abins)            xbins[j] = a/abins*j;
    else if(j<abins+bbins) xbins[j] = a + (b-a)/bbins*(j-abins);
    else                   xbins[j] = b + (1.0-b)/cbins*(j-bbins-abins);
    //cout << xbins[j] << " ";
  }
  cout << endl;

  string version = "JoosepFeb_nosyst_v1_v2"; //"test_4bqcdmem"; //"FHwithme_2pcrel_1"; //"test_3jqcdmem_1";  

  string tag = "_"; //"_Psb0pt55";
  tag += version;
  string method = "";
  if(CUT_HT>0) tag += Form("_HT%.0f",CUT_HT);  
  if(CAT<0) tag += "_catAll";
  else tag += Form("_cat%d_",CAT);
  tag += PSB_FAC;

  string folder = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/projectSkimFH/"+version+"/";

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
  if(CAT==7){
    element = "12";
    method = "_3w2h2t";
    cat = "cat==7 && btag_LR_4b_2b_btagCSV>0.99 && qg_LR_4b_flavour_3q_0q>0.5";
  }
  else if(CAT==8){
    element = "11"; //11 or 12 (leave at 11 as 12 hardcoded seperately)
    method = "_4w2h2t"; //4w2h2t or 3w2h2t
    cat = "cat==8 && btag_LR_4b_2b_btagCSV>0.99 && qg_LR_4b_flavour_4q_0q>0.5";
  }
  else if(CAT==9){
    element = "11";
    method = "_4w2h2t";
    cat = "cat==9 && btag_LR_4b_2b_btagCSV>0.99 && qg_LR_4b_flavour_4q_0q>0.5";  //5q to come
  }
  else if(CAT==10){
    element = "13";
    method = "_4w2h1t";
    cat = "cat==10 && btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.83 && qg_LR_3b_flavour_4q_0q>0.5";
  }
  else if(CAT==11){
    element = "13";
    method = "_4w2h1t";
    cat = "cat==11 && btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.83 && qg_LR_3b_flavour_4q_0q>0.5";
  }
  else if(CAT==12){
    element = "13";
    method = "_4w2h1t";
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
  TH1F* h1 = new TH1F("h1","Matrix element discriminant; P_{s/b}; Events", nbins, xbins );  
  
  hsignal  = (TH1F*)h1->Clone("hsignal"); 
  httj  = (TH1F*)h1->Clone("httj");
  hqcd  = (TH1F*)h1->Clone("hqcd");
  hqcd3  = (TH1F*)h1->Clone("hqcd3");
  hqcd5  = (TH1F*)h1->Clone("hqcd5");
  hqcd7  = (TH1F*)h1->Clone("hqcd7");
  hqcd10 = (TH1F*)h1->Clone("hqcd10");
  hqcd15 = (TH1F*)h1->Clone("hqcd15");
  hqcd20 = (TH1F*)h1->Clone("hqcd20");

  hsignal1q = (TH1F*)h1->Clone("hsignal1q");
  httj1q  = (TH1F*)h1->Clone("httj1q");
  hqcd1q  = (TH1F*)h1->Clone("hqcd1q");

  hsignal4q = (TH1F*)h1->Clone("hsignal4q");
  httj4q  = (TH1F*)h1->Clone("httj4q");
  hqcd4q  = (TH1F*)h1->Clone("hqcd4q");

  hsignal4q1b = (TH1F*)h1->Clone("hsignal4q1b");
  httj4q1b  = (TH1F*)h1->Clone("httj4q1b");
  hqcd4q1b  = (TH1F*)h1->Clone("hqcd4q1b");

  hsignal1q1b = (TH1F*)h1->Clone("hsignal1q1b");
  httj1q1b  = (TH1F*)h1->Clone("httj1q1b");
  hqcd1q1b  = (TH1F*)h1->Clone("hqcd1q1b");

  hsignalhb = (TH1F*)h1->Clone("hsignalhb");
  httjhb  = (TH1F*)h1->Clone("httjhb");
  hqcdhb  = (TH1F*)h1->Clone("hqcdhb");

  string me = "(ht>";
  me += Form("%.0f",CUT_HT);
  me += " && nBCSVM>=2 && ";
  me += cat;
  //me += " && HLT_ttH_FH>0";
  me += ")";

  //string oneq="_3w2h2t"; string fourq="_0w0w2h2t"; string fqob="_0w0w2h1t";
  string oneq="_3w2h2t"; string fourq="_0w2w2h2t"; string fqob="_1w1w2h2t"; string oqob="_3w2h1t"; string hb = "_4w1h2t"; string tb = "_4w2h1t";

  TString draw = "";
  if(QCD==0) draw = ("mem_tth_FH"+method+"_p/(mem_tth_FH"+method+"_p+"+PSB_FAC+"*mem_ttbb_FH"+method+"_p)").c_str();
  if(QCD==1) draw = ("mem_tth_FH"+method+"_p/(mem_tth_FH"+method+"_p+"+PSB_FAC+"*mem_qcd_FH"+method+"_p)").c_str();

  TString draw1q = ("mem_tth_FH"+oneq+"_p/(mem_tth_FH"+oneq+"_p+"+PSB_FAC+"*mem_ttbb_FH"+oneq+"_p)").c_str();
  TString draw4q = ("mem_tth_FH"+fourq+"_p/(mem_tth_FH"+fourq+"_p+"+PSB_FAC+"*mem_ttbb_FH"+fourq+"_p)").c_str();
  TString draw4q1b =("mem_tth_FH"+fqob+"_p/(mem_tth_FH"+fqob+"_p+"+PSB_FAC+"*mem_ttbb_FH"+fqob+"_p)").c_str();
  //TString draw1q1b =("mem_tth_FH"+oqob+"_p/(mem_tth_FH"+oqob+"_p+"+PSB_FAC+"*mem_ttbb_FH"+oqob+"_p)").c_str();
  TString drawhb =("mem_tth_FH"+hb+"_p/(mem_tth_FH"+hb+"_p+"+PSB_FAC+"*mem_ttbb_FH"+hb+"_p)").c_str();
  TString draw1q1b =("mem_tth_FH"+hb+"_p/(mem_tth_FH"+hb+"_p+"+PSB_FAC+"*mem_ttbb_FH"+tb+"_p)").c_str();
  TString cut = me.c_str();
  TString weight = "1.0"; //"weight_xs";

  cout << draw << endl;
  cout << cut << endl;
  cout << weight << endl;

  //FILL HISTOGRAMS
  tsignal->Draw(draw+">>hsignal",cut);
  tttj->Draw(draw+">>httj",cut);
  tqcd3 ->Draw(draw+">>hqcd3",cut+"*"+weight);
  tqcd5 ->Draw(draw+">>hqcd5",cut+"*"+weight);
  tqcd7 ->Draw(draw+">>hqcd7",cut+"*"+weight);
  tqcd10->Draw(draw+">>hqcd10",cut+"*"+weight);
  tqcd15->Draw(draw+">>hqcd15",cut+"*"+weight);
  tqcd20->Draw(draw+">>hqcd20",cut+"*"+weight);

  //hqcd->Add(hqcd3,scalefacQCD3); //exclude QCD300 due to large weights
  hqcd->Add(hqcd5,scalefacQCD5); 
  hqcd->Add(hqcd7,scalefacQCD7);
  hqcd->Add(hqcd10,scalefacQCD10);
  hqcd->Add(hqcd15,scalefacQCD15);
  hqcd->Add(hqcd20,scalefacQCD20);

  if(MULTIINT){
    tsignal->Draw(draw1q+">>hsignal1q",cut);
    tttj->Draw(draw1q+">>httj1q",cut);
    tqcd3 ->Draw(draw1q+">>hqcd3",cut+"*"+weight);
    tqcd5 ->Draw(draw1q+">>hqcd5",cut+"*"+weight);
    tqcd7 ->Draw(draw1q+">>hqcd7",cut+"*"+weight);
    tqcd10->Draw(draw1q+">>hqcd10",cut+"*"+weight);
    tqcd15->Draw(draw1q+">>hqcd15",cut+"*"+weight);
    tqcd20->Draw(draw1q+">>hqcd20",cut+"*"+weight);
  
    hqcd1q->Add(hqcd5,scalefacQCD5); 
    hqcd1q->Add(hqcd7,scalefacQCD7);
    hqcd1q->Add(hqcd10,scalefacQCD10);
    hqcd1q->Add(hqcd15,scalefacQCD15);
    hqcd1q->Add(hqcd20,scalefacQCD20);

    tsignal->Draw(draw4q+">>hsignal4q",cut);
    tttj->Draw(draw4q+">>httj4q",cut);
    tqcd3 ->Draw(draw4q+">>hqcd3",cut+"*"+weight);
    tqcd5 ->Draw(draw4q+">>hqcd5",cut+"*"+weight);
    tqcd7 ->Draw(draw4q+">>hqcd7",cut+"*"+weight);
    tqcd10->Draw(draw4q+">>hqcd10",cut+"*"+weight);
    tqcd15->Draw(draw4q+">>hqcd15",cut+"*"+weight);
    tqcd20->Draw(draw4q+">>hqcd20",cut+"*"+weight);
  
    hqcd4q->Add(hqcd5,scalefacQCD5); 
    hqcd4q->Add(hqcd7,scalefacQCD7);
    hqcd4q->Add(hqcd10,scalefacQCD10);
    hqcd4q->Add(hqcd15,scalefacQCD15);
    hqcd4q->Add(hqcd20,scalefacQCD20);

    tsignal->Draw(draw4q1b+">>hsignal4q1b",cut);
    tttj->Draw(draw4q1b+">>httj4q1b",cut);
    tqcd3 ->Draw(draw4q1b+">>hqcd3",cut+"*"+weight);
    tqcd5 ->Draw(draw4q1b+">>hqcd5",cut+"*"+weight);
    tqcd7 ->Draw(draw4q1b+">>hqcd7",cut+"*"+weight);
    tqcd10->Draw(draw4q1b+">>hqcd10",cut+"*"+weight);
    tqcd15->Draw(draw4q1b+">>hqcd15",cut+"*"+weight);
    tqcd20->Draw(draw4q1b+">>hqcd20",cut+"*"+weight);
  
    hqcd4q1b->Add(hqcd5,scalefacQCD5); 
    hqcd4q1b->Add(hqcd7,scalefacQCD7);
    hqcd4q1b->Add(hqcd10,scalefacQCD10);
    hqcd4q1b->Add(hqcd15,scalefacQCD15);
    hqcd4q1b->Add(hqcd20,scalefacQCD20);

    tsignal->Draw(draw1q1b+">>hsignal1q1b",cut);
    tttj->Draw(draw1q1b+">>httj1q1b",cut);
    tqcd3 ->Draw(draw1q1b+">>hqcd3",cut+"*"+weight);
    tqcd5 ->Draw(draw1q1b+">>hqcd5",cut+"*"+weight);
    tqcd7 ->Draw(draw1q1b+">>hqcd7",cut+"*"+weight);
    tqcd10->Draw(draw1q1b+">>hqcd10",cut+"*"+weight);
    tqcd15->Draw(draw1q1b+">>hqcd15",cut+"*"+weight);
    tqcd20->Draw(draw1q1b+">>hqcd20",cut+"*"+weight);
  
    hqcd1q1b->Add(hqcd5,scalefacQCD5); 
    hqcd1q1b->Add(hqcd7,scalefacQCD7);
    hqcd1q1b->Add(hqcd10,scalefacQCD10);
    hqcd1q1b->Add(hqcd15,scalefacQCD15);
    hqcd1q1b->Add(hqcd20,scalefacQCD20);

    tsignal->Draw(drawhb+">>hsignalhb",cut);
    tttj->Draw(drawhb+">>httjhb",cut);
    tqcd3 ->Draw(drawhb+">>hqcd3",cut+"*"+weight);
    tqcd5 ->Draw(drawhb+">>hqcd5",cut+"*"+weight);
    tqcd7 ->Draw(drawhb+">>hqcd7",cut+"*"+weight);
    tqcd10->Draw(drawhb+">>hqcd10",cut+"*"+weight);
    tqcd15->Draw(drawhb+">>hqcd15",cut+"*"+weight);
    tqcd20->Draw(drawhb+">>hqcd20",cut+"*"+weight);
  
    hqcdhb->Add(hqcd5,scalefacQCD5); 
    hqcdhb->Add(hqcd7,scalefacQCD7);
    hqcdhb->Add(hqcd10,scalefacQCD10);
    hqcdhb->Add(hqcd15,scalefacQCD15);
    hqcdhb->Add(hqcd20,scalefacQCD20);
  }
  else if(CAT==8){
    tsignal->Draw(draw1q+">>hsignal1q",cut);
    tttj->Draw(draw1q+">>httj1q",cut);
    tqcd3 ->Draw(draw1q+">>hqcd3",cut+"*"+weight);
    tqcd5 ->Draw(draw1q+">>hqcd5",cut+"*"+weight);
    tqcd7 ->Draw(draw1q+">>hqcd7",cut+"*"+weight);
    tqcd10->Draw(draw1q+">>hqcd10",cut+"*"+weight);
    tqcd15->Draw(draw1q+">>hqcd15",cut+"*"+weight);
    tqcd20->Draw(draw1q+">>hqcd20",cut+"*"+weight);
  
    hqcd1q->Add(hqcd5,scalefacQCD5); 
    hqcd1q->Add(hqcd7,scalefacQCD7);
    hqcd1q->Add(hqcd10,scalefacQCD10);
    hqcd1q->Add(hqcd15,scalefacQCD15);
    hqcd1q->Add(hqcd20,scalefacQCD20);
  }  

  //GET COUNTS
  float totalsignal = hsignal->Integral();
  float totalttj = httj->Integral();
  float totalqcd = hqcd->Integral();

  float totalsignal1q, totalttj1q, totalqcd1q;
  float totalsignal4q, totalttj4q,  totalqcd4q;
  float totalsignal4q1b, totalttj4q1b, totalqcd4q1b;
  float totalsignal1q1b, totalttj1q1b, totalqcd1q1b;
  float totalsignalhb, totalttjhb, totalqcdhb;

  if(MULTIINT){
    totalsignal1q = hsignal1q->Integral();
    totalttj1q = httj1q->Integral();
    totalqcd1q = hqcd1q->Integral();
    
    totalsignal4q = hsignal4q->Integral();
    totalttj4q = httj4q->Integral();
    totalqcd4q = hqcd4q->Integral();

    totalsignal4q1b = hsignal4q1b->Integral();
    totalttj4q1b = httj4q1b->Integral();
    totalqcd4q1b = hqcd4q1b->Integral();

    totalsignal1q1b = hsignal1q1b->Integral();
    totalttj1q1b = httj1q1b->Integral();
    totalqcd1q1b = hqcd1q1b->Integral();

    totalsignalhb = hsignalhb->Integral();
    totalttjhb = httjhb->Integral();
    totalqcdhb = hqcdhb->Integral();
  }
  else if(CAT==8){
    totalsignal1q = hsignal1q->Integral();
    totalttj1q = httj1q->Integral();
    totalqcd1q = hqcd1q->Integral();
  }

  //DECLARE COUNT VARIABLES
  float nsignal = 0.0;
  float nttj = 0.0;
  float nqcd = 0.0;

  float nsignal1q = 0.0;
  float nttj1q = 0.0;
  float nqcd1q = 0.0;

  float nsignal4q = 0.0;
  float nttj4q = 0.0;
  float nqcd4q = 0.0;

  float nsignal4q1b = 0.0;
  float nttj4q1b = 0.0;
  float nqcd4q1b = 0.0;

  float nsignal1q1b = 0.0;
  float nttj1q1b = 0.0;
  float nqcd1q1b = 0.0;

  float nsignalhb = 0.0;
  float nttjhb = 0.0;
  float nqcdhb = 0.0;

  //DECLARE EFFICIENCY VARIABLES
  vector<float> esignal;
  vector<float> ettj;
  vector<float> eqcd;  

  vector<float> esignal1q;
  vector<float> ettj1q;
  vector<float> eqcd1q;

  vector<float> esignal4q;
  vector<float> ettj4q;
  vector<float> eqcd4q;

  vector<float> esignal4q1b;
  vector<float> ettj4q1b;
  vector<float> eqcd4q1b;

  vector<float> esignal1q1b;
  vector<float> ettj1q1b;
  vector<float> eqcd1q1b;

  vector<float> esignalhb;
  vector<float> ettjhb;
  vector<float> eqcdhb;

  //FILL EFFICIENCY VARIABLES
  for(int i=0; i<nbins; i++){

    nsignal += hsignal->GetBinContent(i);
    nttj += httj->GetBinContent(i);
    nqcd += hqcd->GetBinContent(i);

    esignal.push_back( 1.0-nsignal/totalsignal );
    ettj.push_back( 1.0-nttj/totalttj );
    eqcd.push_back( 1.0-nqcd/totalqcd );

    if(MULTIINT){
      nsignal1q += hsignal1q->GetBinContent(i);
      nttj1q += httj1q->GetBinContent(i);
      nqcd1q += hqcd1q->GetBinContent(i);
    
      esignal1q.push_back( 1.0-nsignal1q/totalsignal1q );
      ettj1q.push_back( 1.0-nttj1q/totalttj1q );
      eqcd1q.push_back( 1.0-nqcd1q/totalqcd1q );

      nsignal4q += hsignal4q->GetBinContent(i);
      nttj4q += httj4q->GetBinContent(i);
      nqcd4q += hqcd4q->GetBinContent(i);
    
      esignal4q.push_back( 1.0-nsignal4q/totalsignal4q );
      ettj4q.push_back( 1.0-nttj4q/totalttj4q );
      eqcd4q.push_back( 1.0-nqcd4q/totalqcd4q );

      nsignal4q1b += hsignal4q1b->GetBinContent(i);
      nttj4q1b += httj4q1b->GetBinContent(i);
      nqcd4q1b += hqcd4q1b->GetBinContent(i);
    
      esignal4q1b.push_back( 1.0-nsignal4q1b/totalsignal4q1b );
      ettj4q1b.push_back( 1.0-nttj4q1b/totalttj4q1b );
      eqcd4q1b.push_back( 1.0-nqcd4q1b/totalqcd4q1b );

      nsignal1q1b += hsignal1q1b->GetBinContent(i);
      nttj1q1b += httj1q1b->GetBinContent(i);
      nqcd1q1b += hqcd1q1b->GetBinContent(i);
    
      esignal1q1b.push_back( 1.0-nsignal1q1b/totalsignal1q1b );
      ettj1q1b.push_back( 1.0-nttj1q1b/totalttj1q1b );
      eqcd1q1b.push_back( 1.0-nqcd1q1b/totalqcd1q1b );

      nsignalhb += hsignalhb->GetBinContent(i);
      nttjhb += httjhb->GetBinContent(i);
      nqcdhb += hqcdhb->GetBinContent(i);

      esignalhb.push_back( 1.0-nsignalhb/totalsignalhb );
      ettjhb.push_back( 1.0-nttjhb/totalttjhb );
      eqcdhb.push_back( 1.0-nqcdhb/totalqcdhb );
    }
    else if(CAT==8){
      nsignal1q += hsignal1q->GetBinContent(i);
      nttj1q += httj1q->GetBinContent(i);
      nqcd1q += hqcd1q->GetBinContent(i);
      
      esignal1q.push_back( 1.0-nsignal1q/totalsignal1q );
      ettj1q.push_back( 1.0-nttj1q/totalttj1q );
      eqcd1q.push_back( 1.0-nqcd1q/totalqcd1q );
    }
  }

  //CREATE CURVES 
  TF1* line = new TF1("line","x",0.0,1.0);

  TGraph* gttj = new TGraph(nbins);
  TGraph* gqcd = new TGraph(nbins);

  TGraph* gttj1q = new TGraph(nbins);
  TGraph* gqcd1q = new TGraph(nbins);

  TGraph* gttj4q = new TGraph(nbins);
  TGraph* gqcd4q = new TGraph(nbins);

  TGraph* gttj4q1b = new TGraph(nbins);
  TGraph* gqcd4q1b = new TGraph(nbins);

  TGraph* gttj1q1b = new TGraph(nbins);
  TGraph* gqcd1q1b = new TGraph(nbins);

  TGraph* gttjhb = new TGraph(nbins);
  TGraph* gqcdhb = new TGraph(nbins);

  //FILL GRAPHS
  cout << "esignal.size() " << esignal.size() << endl;
  cout << "i esignal ettj eqcd" << endl;
  for(int i=0; i<(int)esignal.size(); i++){
    gttj->SetPoint(i, esignal[i], ettj[i]);
    gqcd->SetPoint(i, esignal[i], eqcd[i]);
    if(MULTIINT){
      gttj1q->SetPoint(i, esignal1q[i], ettj1q[i]);
      gqcd1q->SetPoint(i, esignal1q[i], eqcd1q[i]);
      gttj4q->SetPoint(i, esignal4q[i], ettj4q[i]);
      gqcd4q->SetPoint(i, esignal4q[i], eqcd4q[i]);
      gttj4q1b->SetPoint(i, esignal4q1b[i], ettj4q1b[i]);
      gqcd4q1b->SetPoint(i, esignal4q1b[i], eqcd4q1b[i]);
      gttj1q1b->SetPoint(i, esignal1q1b[i], ettj1q1b[i]);
      gqcd1q1b->SetPoint(i, esignal1q1b[i], eqcd1q1b[i]);
      gttjhb->SetPoint(i, esignalhb[i], ettjhb[i]);
      gqcdhb->SetPoint(i, esignalhb[i], eqcdhb[i]);
    }
    else if(CAT==8){
      gttj1q->SetPoint(i, esignal1q[i], ettj1q[i]);
      gqcd1q->SetPoint(i, esignal1q[i], eqcd1q[i]);
    }
    if(i<11 || (i>abins && i<abins+11 ) || (i>(abins+bbins) && i<(abins+bbins+11)) ) cout << i << " " << esignal[i] << " " << ettj[i] << " " << eqcd[i] << endl;
  }

  //AREA UNDER CURVES
  float attj = 0.0;
  float aqcd = 0.0;
  float attj1q = 0.0;
  float aqcd1q = 0.0;
  for(int i=0; i<(int)esignal.size()-1; i++){
    attj += (esignal[i]-esignal[i+1])*ettj[i];
    aqcd += (esignal[i]-esignal[i+1])*eqcd[i];
    if(CAT==8){
      attj1q += (esignal1q[i]-esignal1q[i+1])*ettj1q[i];
      aqcd1q += (esignal1q[i]-esignal1q[i+1])*eqcd1q[i];
    }
  }

  cout << "area under curve:" << endl;
  cout << "ttj " << attj << endl;
  cout << "QCD " << aqcd << endl;
  if(CAT==8){
    cout << "ttj(1q) " << attj1q << endl;
    cout << "QCD(1q) " << aqcd1q << endl;
  }

  TCanvas *c2 = new TCanvas("c2","",5,30,640,580);

  TLegend* leg = new TLegend(0.15,0.6,0.50,0.9,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(kYellow);
  leg->SetTextSize(0.035);

  //SET GRAPH STYLES
  gttj->SetTitle("Matrix element discriminant");
  gttj->GetXaxis()->SetLimits(0.0,1.0); 
  gttj->GetXaxis()->SetTitle("Signal efficiency");
  gttj->GetYaxis()->SetTitle("Background efficiency");
  gttj->SetLineColor(kRed);
  gttj->SetLineWidth(2);
  gttj->SetMaximum(1.0);
  gttj->Draw("AL");
  leg->AddEntry(gttj, Form("ttH vs tt+jets AUC=%.4f",attj), "L");

  //gqcd->SetTitle("Matrix element discriminant");
  //gqcd->GetXaxis()->SetLimits(0.0,1.0); 
  //gqcd->GetXaxis()->SetTitle("Signal efficiency");
  //gqcd->GetYaxis()->SetTitle("Background efficiency");
  gqcd->SetLineColor(kGreen+3);
  gqcd->SetLineWidth(2);
  gqcd->SetMaximum(1.0);
  gqcd->Draw("LSAME");
  leg->AddEntry(gqcd, Form("ttH vs QCD AUC=%.4f",aqcd), "L");

  gttj1q->SetLineColor(kRed);
  gttj1q->SetLineStyle(7);
  gttj1q->SetLineWidth(2);
  gttj1q->SetMaximum(1.0);

  gqcd1q->SetLineColor(kGreen+3);
  gqcd1q->SetLineStyle(7);
  gqcd1q->SetLineWidth(2);
  gqcd1q->SetMaximum(1.0);

  gttj4q->SetLineColor(kRed);
  gttj4q->SetLineStyle(3);
  gttj4q->SetLineWidth(2);
  gttj4q->SetMaximum(1.0);

  gqcd4q->SetLineColor(kGreen+3);
  gqcd4q->SetLineStyle(3);
  gqcd4q->SetLineWidth(2);
  gqcd4q->SetMaximum(1.0);

  gttj4q1b->SetLineColor(kRed);
  gttj4q1b->SetLineStyle(5);
  gttj4q1b->SetLineWidth(2);
  gttj4q1b->SetMaximum(1.0);

  gqcd4q1b->SetLineColor(kGreen+3);
  gqcd4q1b->SetLineStyle(5);
  gqcd4q1b->SetLineWidth(2);
  gqcd4q1b->SetMaximum(1.0);

  gttj1q1b->SetLineColor(kRed);
  gttj1q1b->SetLineStyle(7);
  gttj1q1b->SetLineWidth(2);
  gttj1q1b->SetMaximum(1.0);

  gqcd1q1b->SetLineColor(kGreen+3);
  gqcd1q1b->SetLineStyle(7);
  gqcd1q1b->SetLineWidth(2);
  gqcd1q1b->SetMaximum(1.0);

  gttjhb->SetLineColor(kRed);
  gttjhb->SetLineStyle(3);
  gttjhb->SetLineWidth(2);
  gttjhb->SetMaximum(1.0);

  gqcdhb->SetLineColor(kGreen+3);
  gqcdhb->SetLineStyle(3);
  gqcdhb->SetLineWidth(2);
  gqcdhb->SetMaximum(1.0);

  if(MULTIINT){
    if(CAT==8 || CAT==9){
      gttj1q->Draw("LSAME");
      leg->AddEntry(gttj1q, "ttH vs tt+jets (int. 1q)", "L");
      gqcd1q->Draw("LSAME");
      leg->AddEntry(gqcd1q, "ttH vs QCD (int. 1q)", "L");
    }
    if(CAT==8 || CAT==7 || CAT==9){
      gttj4q->Draw("LSAME");
      //leg->AddEntry(gttj4q, "ttH vs tt+jets (int. 4q)", "L");
      leg->AddEntry(gttj4q, "ttH vs tt+jets (int. 1W)", "L");
      gqcd4q->Draw("LSAME");
      //leg->AddEntry(gqcd4q, "ttH vs QCD (int. 4q)", "L");
      leg->AddEntry(gqcd4q, "ttH vs QCD (int. 1W)", "L");
      
      gttj4q1b->Draw("LSAME");
      leg->AddEntry(gttj4q1b, "ttH vs tt+jets (int. 2q)", "L");
      gqcd4q1b->Draw("LSAME");
      leg->AddEntry(gqcd4q1b, "ttH vs QCD (int. 2q)", "L");
    }
    if(CAT==10 || CAT==11 || CAT==12){
      gttj1q1b->Draw("LSAME");
      gttjhb->Draw("LSAME");
      //leg->AddEntry(gttj4q1b, "ttH vs tt+jets (int. 4q,1b)", "L");
      leg->AddEntry(gttj1q1b, "ttH vs tt+jets (int. 1hb/1tb)", "L");
      leg->AddEntry(gttjhb, "ttH vs tt+jets (int. 1hb)", "L");
      gqcd1q1b->Draw("LSAME");
      gqcdhb->Draw("LSAME");
      //leg->AddEntry(gqcd4q1b, "ttH vs QCD (int. 4q,1b)", "L");
      leg->AddEntry(gqcd1q1b, "ttH vs QCD (int. 1hb/1tb)", "L");
      leg->AddEntry(gqcdhb, "ttH vs QCD (int. 1hb)", "L");
    }
  }
  else if(CAT==8){
    gttj1q->Draw("LSAME");
    leg->AddEntry(gttj1q, Form("ttH vs tt+jets (int. 1q) AUC=%.4f",attj1q), "L");
    gqcd1q->Draw("LSAME");
    leg->AddEntry(gqcd1q, Form("ttH vs QCD (int. 1q) AUC=%.4f",aqcd1q), "L");
  } 
  
  line->SetLineColor(kBlack);
  line->SetLineWidth(1);
  line->Draw("SAME");
  
  leg->Draw();

  // save plots
  if( SAVEPLOTS ){
    c2->SaveAs(  ("./MED_plots/ROC"+tag+".pdf").c_str() ); 
  }

}
