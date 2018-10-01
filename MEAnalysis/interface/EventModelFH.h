#ifndef EVENTMODELFH_H // header guards
#define EVENTMODELFH_H

#include <iostream>
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH1D.h"
#include "TFile.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"
#include "TTH/MEAnalysis/interface/EventModel.h"

namespace TTH_MEAnalysis {

class SampleDescriptionFH {
public:
    enum Schema {
        MC,
        DATA,
        MCBOOSTED,
        DATABOOSTED,
    };

    Schema schema;

    SampleDescriptionFH(Schema _schema) : schema(_schema) {};

    bool isMC() const {
        return schema == MC;
    }
};

//Static (unchangin) data type that represents the event content
class EventDescriptionFH {
public:
    unsigned long long evt;
    unsigned int run;
    unsigned int lumi;
    int json;

    std::vector<Lepton> leptons;
    std::vector<Jet> jets;
    std::vector<int> jets_hadronFlavour;
    
    std::vector<float> leps_superclustereta;

    int ttCls;
    float genTopLep_pt;
    float genTopHad_pt;
    int is_sl;
    int is_dl;
    int is_fh;
    int numJets;
    int nBDeepCSVM;
    int nBCSVM;
    int nPVs;

    int HLT_ttH_SL_mu;
    int HLT_ttH_SL_el;
    int HLT_ttH_DL_mumu;
    int HLT_ttH_DL_elmu;
    int HLT_ttH_DL_elel;
    int HLT_ttH_FH;

    double jetsByPt_5_pt;
    double ht30;
    double min_dr_btag;
    double mass_drpair_btag;
    double mass_drpair_untag;
    double mjjmin;
    double centralitymass;

    double qg_LR_4b_flavour_3q_0q;
    double qg_LR_4b_flavour_4q_0q;
    double qg_LR_4b_flavour_5q_0q;
    double qg_LR_3b_flavour_4q_0q;
    double qg_LR_3b_flavour_5q_0q;
    double btag_LR_4b_2b_btagCSV;

    double mem_FH_3w2h2t_p;
    double mem_FH_4w2h1t_p;
    double mem_FH_4w2h2t_p;
    double mem_tth_FH_3w2h2t_p;
    double mem_tth_FH_4w2h1t_p;
    double mem_tth_FH_4w2h2t_p;
    double mem_ttbb_FH_3w2h2t_p;
    double mem_ttbb_FH_4w2h1t_p;
    double mem_ttbb_FH_4w2h2t_p;

    double mem_DL_0w2h2t_p;
    double mem_SL_0w2h2t_p;
    double mem_SL_1w2h2t_p;
    double mem_SL_2w2h2t_p;

    double Wmass;
    double met_pt;

    Systematic::SystId syst_id;
    std::map<Systematic::SystId, double> weights;


    float n_boosted_bjets;
    float n_boosted_ljets;
    float boosted;

    std::vector<higgsCandidates> higgsCandidate;
    std::vector<topCandidates> topCandidate;

    double mem_FH_3w2h2t_sj_p;
    double mem_DL_0w2h2t_sj_p;
    double mem_SL_0w2h2t_sj_p;
    double mem_SL_1w2h2t_sj_p;
    double mem_SL_2w2h2t_sj_p;
    //double mem_DL_0w2h2t_sj_perm_higgs_p;
    //double mem_SL_0w2h2t_sj_perm_higgs_p;
    //double mem_SL_1w2h2t_sj_perm_higgs_p;
    //double mem_SL_2w2h2t_sj_perm_higgs_p;
    //double mem_SL_2w2h2t_sj_perm_top_p;
    //double mem_SL_2w2h2t_sj_perm_higgstop_p;
};

//Translates a tthbb13 TTree to an EventDescriptionFH
template <typename T>
class TreeDescriptionFH {
public:

    TTreeReader reader;

    TTreeReaderValue<unsigned long long> evt;
    TTreeReaderValue<int> run;
    TTreeReaderValue<int> lumi;
    TTreeReaderValue<int> json;

    TTreeReaderValue<int> is_sl;
    TTreeReaderValue<int> is_dl;
    TTreeReaderValue<int> is_fh;
    
    TTreeReaderValue<int> HLT_ttH_SL_mu;
    TTreeReaderValue<int> HLT_ttH_SL_el;
    TTreeReaderValue<int> HLT_ttH_DL_elmu;
    TTreeReaderValue<int> HLT_ttH_DL_elel;
    TTreeReaderValue<int> HLT_ttH_DL_mumu;
    TTreeReaderValue<int> HLT_ttH_FH;

    TTreeReaderValue<int> numJets;
    TTreeReaderValue<int> nBDeepCSVM;
    TTreeReaderValue<int> nBCSVM;
    TTreeReaderValue<T> nPVs;
    
    TTreeReaderValue<int> nleps;
    TTreeReaderArray<T> leps_pdgId;
    TTreeReaderArray<T> leps_pt;
    TTreeReaderArray<T> leps_eta;
    TTreeReaderArray<T> leps_phi;
    TTreeReaderArray<T> leps_mass;
    TTreeReaderArray<T> leps_scEta;

    TTreeReaderValue<int> njets;
    TTreeReaderArray<T> jets_pt;
    TTreeReaderArray<T> jets_eta;
    TTreeReaderArray<T> jets_phi;
    TTreeReaderArray<T> jets_mass;
    TTreeReaderArray<T> jets_btagCSV;

    TTreeReaderValue<T> ht30;
    TTreeReaderValue<T> min_dr_btag;
    TTreeReaderValue<T> mass_drpair_btag;
    TTreeReaderValue<T> mass_drpair_untag;
    TTreeReaderValue<T> mjjmin;
    TTreeReaderValue<T> centralitymass;

    TTreeReaderValue<T> qg_LR_4b_flavour_3q_0q;
    TTreeReaderValue<T> qg_LR_4b_flavour_4q_0q;
    TTreeReaderValue<T> qg_LR_4b_flavour_5q_0q;
    TTreeReaderValue<T> qg_LR_3b_flavour_4q_0q;
    TTreeReaderValue<T> qg_LR_3b_flavour_5q_0q;
    TTreeReaderValue<T> btag_LR_4b_2b_btagCSV;

    TTreeReaderValue<T> mem_FH_3w2h2t_p;
    TTreeReaderValue<T> mem_FH_4w2h1t_p;
    TTreeReaderValue<T> mem_FH_4w2h2t_p;
    TTreeReaderValue<T> mem_tth_FH_3w2h2t_p;
    TTreeReaderValue<T> mem_tth_FH_4w2h1t_p;
    TTreeReaderValue<T> mem_tth_FH_4w2h2t_p;
    TTreeReaderValue<T> mem_ttbb_FH_3w2h2t_p;
    TTreeReaderValue<T> mem_ttbb_FH_4w2h1t_p;
    TTreeReaderValue<T> mem_ttbb_FH_4w2h2t_p;

    //TTreeReaderValue<T> mem_DL_0w2h2t_p;
    //TTreeReaderValue<T> mem_SL_0w2h2t_p;
    //TTreeReaderValue<T> mem_SL_1w2h2t_p;
    //TTreeReaderValue<T> mem_SL_2w2h2t_p;

    TTreeReaderValue<T> Wmass;
    TTreeReaderValue<T> met_pt;

    std::map<Systematic::SystId, TTreeReaderArray<T>*> correction_branches;

    SampleDescriptionFH sample;

    TreeDescriptionFH(TFile* file, SampleDescriptionFH sample) :
        reader("tree", file),
        evt(reader, "evt"),
        run(reader, "run"),
        lumi(reader, "lumi"),
        json(reader, "json"),

        is_sl(reader, "is_sl"),
        is_dl(reader, "is_dl"),
        is_fh(reader, "is_fh"),
       
        HLT_ttH_SL_mu(reader, "HLT_ttH_SL_mu"),
        HLT_ttH_SL_el(reader, "HLT_ttH_SL_el"),
        HLT_ttH_DL_elmu(reader, "HLT_ttH_DL_elmu"),
        HLT_ttH_DL_elel(reader, "HLT_ttH_DL_elel"),
        HLT_ttH_DL_mumu(reader, "HLT_ttH_DL_mumu"),
        HLT_ttH_FH(reader, "HLT_ttH_FH"),
        
        numJets(reader, "numJets"),
        nBDeepCSVM(reader, "nBDeepCSVM"),
        nBCSVM(reader, "nBCSVM"),
        nPVs(reader, "nPVs"),
        
        nleps(reader, "nleps"),
        leps_pdgId(reader, "leps_pdgId"),
        leps_pt(reader, "leps_pt"),
        leps_eta(reader, "leps_eta"),
        leps_phi(reader, "leps_phi"),
        leps_mass(reader, "leps_mass"),
        //FIXME: add scEta to tthbb13 tree
        leps_scEta(reader, "leps_eta"),

        njets(reader, "njets"),
        jets_pt(reader, "jets_pt"),
        jets_eta(reader, "jets_eta"),
        jets_phi(reader, "jets_phi"),
        jets_mass(reader, "jets_mass"),
        jets_btagCSV(reader, "jets_btagCSV"),

        ht30(reader, "ht30"),
	min_dr_btag(reader, "min_dr_btag"),
	mass_drpair_btag(reader, "mass_drpair_btag"),
	mass_drpair_untag(reader, "mass_drpair_untag"),
	mjjmin(reader, "mjjmin"),
	centralitymass(reader, "centralitymass"),

	qg_LR_4b_flavour_3q_0q(reader, "qg_LR_4b_flavour_3q_0q"),
	qg_LR_4b_flavour_4q_0q(reader, "qg_LR_4b_flavour_4q_0q"),
	qg_LR_4b_flavour_5q_0q(reader, "qg_LR_4b_flavour_5q_0q"),
	qg_LR_3b_flavour_4q_0q(reader, "qg_LR_3b_flavour_4q_0q"),
	qg_LR_3b_flavour_5q_0q(reader, "qg_LR_3b_flavour_5q_0q"),
        btag_LR_4b_2b_btagCSV(reader, "btag_LR_4b_2b_btagCSV"),

        mem_FH_3w2h2t_p(reader, "mem_FH_3w2h2t_p"),
        mem_FH_4w2h1t_p(reader, "mem_FH_4w2h1t_p"),
        mem_FH_4w2h2t_p(reader, "mem_FH_4w2h2t_p"),
        mem_tth_FH_3w2h2t_p(reader, "mem_tth_FH_3w2h2t_p"),
        mem_tth_FH_4w2h1t_p(reader, "mem_tth_FH_4w2h1t_p"),
        mem_tth_FH_4w2h2t_p(reader, "mem_tth_FH_4w2h2t_p"),
        mem_ttbb_FH_3w2h2t_p(reader, "mem_ttbb_FH_3w2h2t_p"),
        mem_ttbb_FH_4w2h1t_p(reader, "mem_ttbb_FH_4w2h1t_p"),
        mem_ttbb_FH_4w2h2t_p(reader, "mem_ttbb_FH_4w2h2t_p"),

	  //mem_DL_0w2h2t_p(reader, "mem_DL_0w2h2t_p"),
	  //mem_SL_0w2h2t_p(reader, "mem_SL_0w2h2t_p"),
	  //mem_SL_1w2h2t_p(reader, "mem_SL_1w2h2t_p"),
	  //mem_SL_2w2h2t_p(reader, "mem_SL_2w2h2t_p"),
 
        Wmass(reader, "Wmass"),
        met_pt(reader, "met_pt"),


        sample(sample) {
    }
    virtual ~TreeDescriptionFH() {}

    std::vector<Lepton> build_leptons(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_jets(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual EventDescriptionFH create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

template <typename T>
class TreeDescriptionFHBOOSTED : public TreeDescriptionFH<T> {
public:


    TTreeReaderValue<float>  n_boosted_bjets;
    TTreeReaderValue<float>  n_boosted_ljets;
    TTreeReaderValue<float>  boosted;

    TTreeReaderValue<int> nhiggsCandidate;
    TTreeReaderArray<T> higgsCandidate_pt;
    TTreeReaderArray<T> higgsCandidate_eta;
    TTreeReaderArray<T> higgsCandidate_phi;
    TTreeReaderArray<T> higgsCandidate_mass;
    TTreeReaderArray<T> higgsCandidate_msoftdrop; 
    TTreeReaderArray<T> higgsCandidate_tau21;
    TTreeReaderArray<T> higgsCandidate_bbtag;
    TTreeReaderArray<T> higgsCandidate_sj1btag;
    TTreeReaderArray<T> higgsCandidate_sj2btag;
    TTreeReaderArray<T> higgsCandidate_sj1pt;
    TTreeReaderArray<T> higgsCandidate_sj2pt;

    TTreeReaderValue<int> ntopCandidate;
    TTreeReaderArray<T> topCandidate_pt;
    TTreeReaderArray<T> topCandidate_eta;
    TTreeReaderArray<T> topCandidate_phi;
    TTreeReaderArray<T> topCandidate_mass;
    TTreeReaderArray<T> topCandidate_tau32SD;
    TTreeReaderArray<T> topCandidate_fRec;
    TTreeReaderArray<T> topCandidate_delRopt; 
    TTreeReaderArray<T> topCandidate_sj1btag;
    TTreeReaderArray<T> topCandidate_sj2btag;
    TTreeReaderArray<T> topCandidate_sj3btag;
    TTreeReaderArray<T> topCandidate_sj1pt;
    TTreeReaderArray<T> topCandidate_sj2pt;
    TTreeReaderArray<T> topCandidate_sj3pt;

    TTreeReaderValue<T> mem_FH_3w2h2t_sj_p;
    //TTreeReaderValue<T> mem_DL_0w2h2t_sj_p;
    //TTreeReaderValue<T> mem_SL_0w2h2t_sj_p;
    //TTreeReaderValue<T> mem_SL_1w2h2t_sj_p;
    //TTreeReaderValue<T> mem_SL_2w2h2t_sj_p;
    //TTreeReaderValue<T> mem_DL_0w2h2t_sj_perm_higgs_p;
    //TTreeReaderValue<T> mem_SL_0w2h2t_sj_perm_higgs_p;
    //TTreeReaderValue<T> mem_SL_1w2h2t_sj_perm_higgs_p;
    //TTreeReaderValue<T> mem_SL_2w2h2t_sj_perm_higgs_p;
    //TTreeReaderValue<T> mem_SL_2w2h2t_sj_perm_top_p;
    //TTreeReaderValue<T> mem_SL_2w2h2t_sj_perm_higgstop_p;


    TreeDescriptionFHBOOSTED(TFile* file, SampleDescriptionFH sample) :
        TreeDescriptionFH<T>(file, sample),
        n_boosted_bjets(TreeDescriptionFH<T>::reader, "n_boosted_bjets"),
        n_boosted_ljets(TreeDescriptionFH<T>::reader, "n_boosted_ljets"),
        boosted(TreeDescriptionFH<T>::reader, "boosted"),

        nhiggsCandidate(TreeDescriptionFH<T>::reader, "nhiggsCandidate"),
        higgsCandidate_pt(TreeDescriptionFH<T>::reader, "higgsCandidate_pt"),
        higgsCandidate_eta(TreeDescriptionFH<T>::reader, "higgsCandidate_eta"),
        higgsCandidate_phi(TreeDescriptionFH<T>::reader, "higgsCandidate_phi"),
        higgsCandidate_mass(TreeDescriptionFH<T>::reader, "higgsCandidate_mass"),
        higgsCandidate_msoftdrop(TreeDescriptionFH<T>::reader, "higgsCandidate_msoftdrop"),
        higgsCandidate_tau21(TreeDescriptionFH<T>::reader, "higgsCandidate_tau21"),
        higgsCandidate_bbtag(TreeDescriptionFH<T>::reader, "higgsCandidate_bbtag"),
        higgsCandidate_sj1btag(TreeDescriptionFH<T>::reader, "higgsCandidate_sj1btag"),
        higgsCandidate_sj2btag(TreeDescriptionFH<T>::reader, "higgsCandidate_sj2btag"),
        higgsCandidate_sj1pt(TreeDescriptionFH<T>::reader, "higgsCandidate_sj1pt"),
        higgsCandidate_sj2pt(TreeDescriptionFH<T>::reader, "higgsCandidate_sj2pt"),

        ntopCandidate(TreeDescriptionFH<T>::reader, "ntopCandidate"),
        topCandidate_pt(TreeDescriptionFH<T>::reader, "topCandidate_pt"),
        topCandidate_eta(TreeDescriptionFH<T>::reader, "topCandidate_eta"),
        topCandidate_phi(TreeDescriptionFH<T>::reader, "topCandidate_phi"),
        topCandidate_mass(TreeDescriptionFH<T>::reader, "topCandidate_mass"),
        topCandidate_tau32SD(TreeDescriptionFH<T>::reader, "topCandidate_tau32SD"),
        topCandidate_fRec(TreeDescriptionFH<T>::reader, "topCandidate_fRec"),
        topCandidate_delRopt(TreeDescriptionFH<T>::reader, "topCandidate_delRopt"),
        topCandidate_sj1btag(TreeDescriptionFH<T>::reader, "topCandidate_sj1btag"),
        topCandidate_sj2btag(TreeDescriptionFH<T>::reader, "topCandidate_sj2btag"),
        topCandidate_sj3btag(TreeDescriptionFH<T>::reader, "topCandidate_sj3btag"),
        topCandidate_sj1pt(TreeDescriptionFH<T>::reader, "topCandidate_sj1pt"),
        topCandidate_sj2pt(TreeDescriptionFH<T>::reader, "topCandidate_sj2pt"),
        topCandidate_sj3pt(TreeDescriptionFH<T>::reader, "topCandidate_sj3pt"),

        mem_FH_3w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_FH_3w2h2t_sj_p")
	  //mem_DL_0w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_DL_0w2h2t_sj_p"),
	  //mem_SL_0w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_SL_0w2h2t_sj_p"),
	  //mem_SL_1w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_SL_1w2h2t_sj_p"),
	  //mem_SL_2w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_p")
        //mem_DL_0w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_DL_0w2h2t_sj_perm_higgs_p"),
        //mem_SL_0w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_SL_0w2h2t_sj_perm_higgs_p"),
        //mem_SL_1w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_SL_1w2h2t_sj_perm_higgs_p"),
        //mem_SL_2w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_perm_higgs_p"),
        //mem_SL_2w2h2t_sj_perm_top_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_perm_top_p"),
        //mem_SL_2w2h2t_sj_perm_higgstop_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_perm_higgstop_p")
    {}
    ~TreeDescriptionFHBOOSTED() {}

    virtual EventDescriptionFH create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    std::vector<higgsCandidates> build_higgsCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    std::vector<topCandidates> build_topCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
 };

template <typename T>
class TreeDescriptionFHMCSystematic : public TreeDescriptionFH<T> {
public:

    TTreeReaderValue<int> ttCls;
    TTreeReaderValue<T> genTopHad_pt;
    TTreeReaderValue<T> genTopLep_pt;
    
    TTreeReaderValue<T> genWeight;
    TTreeReaderValue<T> puWeight;
    TTreeReaderValue<T> btagWeight_shape;
    
    TreeDescriptionFHMCSystematic(TFile* file, SampleDescriptionFH sample) :
        TreeDescriptionFH<T>(file, sample),
        ttCls(TreeDescriptionFH<T>::reader, "ttCls"),
        genTopHad_pt(TreeDescriptionFH<T>::reader, "genTopHad_pt"),
        genTopLep_pt(TreeDescriptionFH<T>::reader, "genTopLep_pt"),
        genWeight(TreeDescriptionFH<T>::reader, "genWeight"),
        puWeight(TreeDescriptionFH<T>::reader, "puWeight"),
        btagWeight_shape(TreeDescriptionFH<T>::reader, "btagWeight_shape")
    {}
    
    ~TreeDescriptionFHMCSystematic() {}
    
    virtual EventDescriptionFH create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

template <typename T>
class TreeDescriptionFHMC : public TreeDescriptionFH<T> {
public:

    TTreeReaderValue<int> ttCls;
    TTreeReaderValue<T> genTopHad_pt;
    TTreeReaderValue<T> genTopLep_pt;

    TTreeReaderValueSystematic<int> numJets;
    TTreeReaderValueSystematic<int> nBDeepCSVM;
    TTreeReaderValueSystematic<int> nBCSVM;

    TTreeReaderArray<int> jets_hadronFlavour;
    TTreeReaderArraySystematic<T> jets_pt_corr;

    TTreeReaderValueSystematic<T> mem_FH_3w2h2t_p;
    //TTreeReaderValueSystematic<T> mem_DL_0w2h2t_p;
    //TTreeReaderValueSystematic<T> mem_SL_0w2h2t_p;
    //TTreeReaderValueSystematic<T> mem_SL_1w2h2t_p;
    //TTreeReaderValueSystematic<T> mem_SL_2w2h2t_p;

    TTreeReaderValue<T> genWeight;
    
    TTreeReaderValue<T> puWeight;
    TTreeReaderValue<T> puWeightUp;
    TTreeReaderValue<T> puWeightDown;
    
    TTreeReaderValue<T> btagWeight_shape;
    TTreeReaderValue<T> btagWeight_shape_cferr1Up;
    TTreeReaderValue<T> btagWeight_shape_cferr2Up;
    TTreeReaderValue<T> btagWeight_shape_hfUp;
    TTreeReaderValue<T> btagWeight_shape_hfstats1Up;
    TTreeReaderValue<T> btagWeight_shape_hfstats2Up;
    TTreeReaderValue<T> btagWeight_shape_jesUp;
    TTreeReaderValue<T> btagWeight_shape_lfUp;
    TTreeReaderValue<T> btagWeight_shape_lfstats1Up;
    TTreeReaderValue<T> btagWeight_shape_lfstats2Up;
    
    TTreeReaderValue<T> btagWeight_shape_cferr1Down;
    TTreeReaderValue<T> btagWeight_shape_cferr2Down;
    TTreeReaderValue<T> btagWeight_shape_hfDown;
    TTreeReaderValue<T> btagWeight_shape_hfstats1Down;
    TTreeReaderValue<T> btagWeight_shape_hfstats2Down;
    TTreeReaderValue<T> btagWeight_shape_jesDown;
    TTreeReaderValue<T> btagWeight_shape_lfDown;
    TTreeReaderValue<T> btagWeight_shape_lfstats1Down;
    TTreeReaderValue<T> btagWeight_shape_lfstats2Down;

    //TTreeReaderArray<T> LHE_weights_scale_wgt;
    
    TreeDescriptionFHMC(TFile* file, SampleDescriptionFH sample) :
        TreeDescriptionFH<T>(file, sample),
        ttCls(TreeDescriptionFH<T>::reader, "ttCls"),
        genTopHad_pt(TreeDescriptionFH<T>::reader, "genTopHad_pt"),
        genTopLep_pt(TreeDescriptionFH<T>::reader, "genTopLep_pt"),
        
        numJets(TreeDescriptionFH<T>::reader, "numJets"),
        nBDeepCSVM(TreeDescriptionFH<T>::reader, "nBDeepCSVM"),
        nBCSVM(TreeDescriptionFH<T>::reader, "nBCSVM"),

        jets_hadronFlavour(TreeDescriptionFH<T>::reader, "jets_hadronFlavour"),
        jets_pt_corr(TreeDescriptionFH<T>::reader, "jets_pt_corr", false),

        mem_FH_3w2h2t_p(TreeDescriptionFH<T>::reader, "mem_FH_3w2h2t_p"),
	//mem_DL_0w2h2t_p(TreeDescriptionFH<T>::reader, "mem_DL_0w2h2t_p"),
	//mem_SL_0w2h2t_p(TreeDescriptionFH<T>::reader, "mem_SL_0w2h2t_p"),
	//mem_SL_1w2h2t_p(TreeDescriptionFH<T>::reader, "mem_SL_1w2h2t_p"),
	//mem_SL_2w2h2t_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_p"),

        genWeight(TreeDescriptionFH<T>::reader, "genWeight"),
        
        puWeight(TreeDescriptionFH<T>::reader, "puWeight"),
        puWeightUp(TreeDescriptionFH<T>::reader, "puWeightUp"),
        puWeightDown(TreeDescriptionFH<T>::reader, "puWeightDown"),

        btagWeight_shape(TreeDescriptionFH<T>::reader, "btagWeight_shape"),

        btagWeight_shape_cferr1Up(TreeDescriptionFH<T>::reader, "btagWeight_shapeCFERR1Up"),
        btagWeight_shape_cferr2Up(TreeDescriptionFH<T>::reader, "btagWeight_shapeCFERR2Up"),
        btagWeight_shape_hfUp(TreeDescriptionFH<T>::reader, "btagWeight_shapeHFUp"),
        btagWeight_shape_hfstats1Up(TreeDescriptionFH<T>::reader, "btagWeight_shapeHFSTATS1Up"),
        btagWeight_shape_hfstats2Up(TreeDescriptionFH<T>::reader, "btagWeight_shapeHFSTATS2Up"),
        btagWeight_shape_jesUp(TreeDescriptionFH<T>::reader, "btagWeight_shapeJESUp"),
        btagWeight_shape_lfUp(TreeDescriptionFH<T>::reader, "btagWeight_shapeLFUp"),
        btagWeight_shape_lfstats1Up(TreeDescriptionFH<T>::reader, "btagWeight_shapeLFSTATS1Up"),
        btagWeight_shape_lfstats2Up(TreeDescriptionFH<T>::reader, "btagWeight_shapeLFSTATS2Up"),
        
        btagWeight_shape_cferr1Down(TreeDescriptionFH<T>::reader, "btagWeight_shapeCFERR1Down"),
        btagWeight_shape_cferr2Down(TreeDescriptionFH<T>::reader, "btagWeight_shapeCFERR2Down"),
        btagWeight_shape_hfDown(TreeDescriptionFH<T>::reader, "btagWeight_shapeHFDown"),
        btagWeight_shape_hfstats1Down(TreeDescriptionFH<T>::reader, "btagWeight_shapeHFSTATS1Down"),
        btagWeight_shape_hfstats2Down(TreeDescriptionFH<T>::reader, "btagWeight_shapeHFSTATS2Down"),
        btagWeight_shape_jesDown(TreeDescriptionFH<T>::reader, "btagWeight_shapeJESDown"),
        btagWeight_shape_lfDown(TreeDescriptionFH<T>::reader, "btagWeight_shapeLFDown"),
        btagWeight_shape_lfstats1Down(TreeDescriptionFH<T>::reader, "btagWeight_shapeLFSTATS1Down"),
        btagWeight_shape_lfstats2Down(TreeDescriptionFH<T>::reader, "btagWeight_shapeLFSTATS2Down")


        //LHE_weights_scale_wgt(TreeDescriptionFH<T>::reader, "LHE_weights_scale_wgt")
    {}
    
    ~TreeDescriptionFHMC() {}

    TTreeReaderArray<T>* get_correction_branch(Systematic::SystId syst_id = Systematic::syst_id_nominal);

    virtual EventDescriptionFH create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_jets(Systematic::SystId syst_id = Systematic::syst_id_nominal);

};

template <typename T>
class TreeDescriptionFHMCBOOSTED : public TreeDescriptionFHMC<T> {
public:

    TTreeReaderValueSystematic<float>  n_boosted_bjets;
    TTreeReaderValueSystematic<float>  n_boosted_ljets;
    TTreeReaderValueSystematic<float>  boosted;

    TTreeReaderValue<int> nhiggsCandidate;
    TTreeReaderArray<T> higgsCandidate_pt;
    TTreeReaderArray<T> higgsCandidate_eta;
    TTreeReaderArray<T> higgsCandidate_phi;
    TTreeReaderArray<T> higgsCandidate_mass;
    TTreeReaderArray<T> higgsCandidate_msoftdrop; 
    TTreeReaderArray<T> higgsCandidate_tau21;
    TTreeReaderArray<T> higgsCandidate_bbtag;
    TTreeReaderArray<T> higgsCandidate_sj1btag;
    TTreeReaderArray<T> higgsCandidate_sj2btag;
    TTreeReaderArray<T> higgsCandidate_sj1pt;
    TTreeReaderArray<T> higgsCandidate_sj2pt;

    TTreeReaderValue<int> ntopCandidate;
    TTreeReaderArray<T> topCandidate_pt;
    TTreeReaderArray<T> topCandidate_eta;
    TTreeReaderArray<T> topCandidate_phi;
    TTreeReaderArray<T> topCandidate_mass;
    TTreeReaderArray<T> topCandidate_tau32SD;
    TTreeReaderArray<T> topCandidate_fRec;
    TTreeReaderArray<T> topCandidate_delRopt; 
    TTreeReaderArray<T> topCandidate_sj1btag;
    TTreeReaderArray<T> topCandidate_sj2btag;
    TTreeReaderArray<T> topCandidate_sj3btag;
    TTreeReaderArray<T> topCandidate_sj1pt;
    TTreeReaderArray<T> topCandidate_sj2pt;
    TTreeReaderArray<T> topCandidate_sj3pt;

    TTreeReaderValueSystematic<T> mem_FH_3w2h2t_sj_p;
    //TTreeReaderValueSystematic<T> mem_DL_0w2h2t_sj_p;
    //TTreeReaderValueSystematic<T> mem_SL_0w2h2t_sj_p;
    //TTreeReaderValueSystematic<T> mem_SL_1w2h2t_sj_p;
    //TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_p;
    //TTreeReaderValueSystematic<T> mem_DL_0w2h2t_sj_perm_higgs_p;
    //TTreeReaderValueSystematic<T> mem_SL_0w2h2t_sj_perm_higgs_p;
    //TTreeReaderValueSystematic<T> mem_SL_1w2h2t_sj_perm_higgs_p;
    //TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_perm_higgs_p;
    //TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_perm_top_p;
    //TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_perm_higgstop_p;
    
    TreeDescriptionFHMCBOOSTED(TFile* file, SampleDescriptionFH sample) :
        TreeDescriptionFHMC<T>(file, sample),

        n_boosted_bjets(TreeDescriptionFH<T>::reader, "n_boosted_bjets"),
        n_boosted_ljets(TreeDescriptionFH<T>::reader, "n_boosted_ljets"),
        boosted(TreeDescriptionFH<T>::reader, "boosted"),

        nhiggsCandidate(TreeDescriptionFH<T>::reader, "nhiggsCandidate"),
        higgsCandidate_pt(TreeDescriptionFH<T>::reader, "higgsCandidate_pt"),
        higgsCandidate_eta(TreeDescriptionFH<T>::reader, "higgsCandidate_eta"),
        higgsCandidate_phi(TreeDescriptionFH<T>::reader, "higgsCandidate_phi"),
        higgsCandidate_mass(TreeDescriptionFH<T>::reader, "higgsCandidate_mass"),
        higgsCandidate_msoftdrop(TreeDescriptionFH<T>::reader, "higgsCandidate_msoftdrop"),
        higgsCandidate_tau21(TreeDescriptionFH<T>::reader, "higgsCandidate_tau21"),
        higgsCandidate_bbtag(TreeDescriptionFH<T>::reader, "higgsCandidate_bbtag"),
        higgsCandidate_sj1btag(TreeDescriptionFH<T>::reader, "higgsCandidate_sj1btag"),
        higgsCandidate_sj2btag(TreeDescriptionFH<T>::reader, "higgsCandidate_sj2btag"),
        higgsCandidate_sj1pt(TreeDescriptionFH<T>::reader, "higgsCandidate_sj1pt"),
        higgsCandidate_sj2pt(TreeDescriptionFH<T>::reader, "higgsCandidate_sj2pt"),

        ntopCandidate(TreeDescriptionFH<T>::reader, "ntopCandidate"),
        topCandidate_pt(TreeDescriptionFH<T>::reader, "topCandidate_pt"),
        topCandidate_eta(TreeDescriptionFH<T>::reader, "topCandidate_eta"),
        topCandidate_phi(TreeDescriptionFH<T>::reader, "topCandidate_phi"),
        topCandidate_mass(TreeDescriptionFH<T>::reader, "topCandidate_mass"),
        topCandidate_tau32SD(TreeDescriptionFH<T>::reader, "topCandidate_tau32SD"),
        topCandidate_fRec(TreeDescriptionFH<T>::reader, "topCandidate_fRec"),
        topCandidate_delRopt(TreeDescriptionFH<T>::reader, "topCandidate_delRopt"),
        topCandidate_sj1btag(TreeDescriptionFH<T>::reader, "topCandidate_sj1btag"),
        topCandidate_sj2btag(TreeDescriptionFH<T>::reader, "topCandidate_sj2btag"),
        topCandidate_sj3btag(TreeDescriptionFH<T>::reader, "topCandidate_sj3btag"),
        topCandidate_sj1pt(TreeDescriptionFH<T>::reader, "topCandidate_sj1pt"),
        topCandidate_sj2pt(TreeDescriptionFH<T>::reader, "topCandidate_sj2pt"),
        topCandidate_sj3pt(TreeDescriptionFH<T>::reader, "topCandidate_sj3pt"),

        mem_FH_3w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_FH_3w2h2t_sj_p")
	  //mem_DL_0w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_DL_0w2h2t_sj_p"),
	  //mem_SL_0w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_SL_0w2h2t_sj_p"),
	  //mem_SL_1w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_SL_1w2h2t_sj_p"),
	  //mem_SL_2w2h2t_sj_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_p")
        //mem_DL_0w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_DL_0w2h2t_sj_perm_higgs_p"),
        //mem_SL_0w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_SL_0w2h2t_sj_perm_higgs_p"),
        //mem_SL_1w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_SL_1w2h2t_sj_perm_higgs_p"),
        //mem_SL_2w2h2t_sj_perm_higgs_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_perm_higgs_p"),
        //mem_SL_2w2h2t_sj_perm_top_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_perm_top_p"),
        //mem_SL_2w2h2t_sj_perm_higgstop_p(TreeDescriptionFH<T>::reader, "mem_SL_2w2h2t_sj_perm_higgstop_p")


        //LHE_weights_scale_wgt(TreeDescriptionFH<T>::reader, "LHE_weights_scale_wgt")
    {}
    
    ~TreeDescriptionFHMCBOOSTED() {}

    //TTreeReaderArray<T>* get_correction_branch(Systematic::SystId syst_id = Systematic::syst_id_nominal);

    std::vector<higgsCandidates> build_higgsCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    std::vector<topCandidates> build_topCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual EventDescriptionFH create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

typedef TreeDescriptionFH<float> TreeDescriptionFHFloat;
typedef TreeDescriptionFHBOOSTED<float> TreeDescriptionFHBOOSTEDFloat;
typedef TreeDescriptionFHMC<float> TreeDescriptionFHMCFloat;
typedef TreeDescriptionFHMCBOOSTED<float> TreeDescriptionFHMCBOOSTEDFloat;
typedef TreeDescriptionFHMCSystematic<float> TreeDescriptionFHMCSystematicFloat;

typedef TreeDescriptionFH<double> TreeDescriptionFHDouble;
typedef TreeDescriptionFHBOOSTED<double> TreeDescriptionFHBOOSTEDDouble;
typedef TreeDescriptionFHMC<double> TreeDescriptionFHMCDouble;
typedef TreeDescriptionFHMCBOOSTED<double> TreeDescriptionFHMCBOOSTEDDouble;
typedef TreeDescriptionFHMCSystematic<double> TreeDescriptionFHMCSystematicDouble;

} //namespace TTH_MEAnalysis
#endif
