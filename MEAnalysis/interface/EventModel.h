#ifndef EVENTMODEL_H // header guards
#define EVENTMODEL_H

#include <iostream>
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH1D.h"
#include "TFile.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"

namespace TTH_MEAnalysis {

class Jet {
public:
    TLorentzVector lv;
    double btag;

    Jet() : lv(TLorentzVector()), btag(0) {}

    Jet(TLorentzVector lv, double btag) :
    lv(lv),
    btag(btag)
    {
    }
};

class Lepton {
public:
    TLorentzVector lv;
    double charge;
    int pdgId;

    Lepton() : lv(TLorentzVector()), charge(0), pdgId(0) {}

    Lepton(TLorentzVector lv, double charge, int pdgId) :
    lv(lv),
    charge(charge),
    pdgId(pdgId)
    {
    }
};

class SampleDescription {
public:
    enum Schema {
        MC,
        DATA
    };

    Schema schema;

    SampleDescription(Schema _schema) : schema(_schema) {};

    bool isMC() const {
        return schema == MC;
    }
};

namespace Systematic {

    enum Event {
        Nominal,
        CMS_scale_j,
        CMS_res_j,
        CMS_scaleSubTotalPileUp_j,
        CMS_scaleAbsoluteStat_j,
        CMS_scaleAbsoluteScale_j,
        CMS_scaleAbsoluteFlavMap_j,
        CMS_scaleAbsoluteMPFBias_j,
        CMS_scaleFragmentation_j,
        CMS_scaleSinglePionECAL_j,
        CMS_scaleSinglePionHCAL_j,
        CMS_scaleFlavorQCD_j,
        CMS_scaleTimePtEta_j,
        CMS_scaleRelativeJEREC1_j,
        CMS_scaleRelativeJEREC2_j,
        CMS_scaleRelativeJERHF_j,
        CMS_scaleRelativePtBB_j,
        CMS_scaleRelativePtEC1_j,
        CMS_scaleRelativePtEC2_j,
        CMS_scaleRelativePtHF_j,
        CMS_scaleRelativeFSR_j,
        CMS_scaleRelativeStatFSR_j,
        CMS_scaleRelativeStatEC_j,
        CMS_scaleRelativeStatHF_j,
        CMS_scalePileUpDataMC_j,
        CMS_scalePileUpPtRef_j,
        CMS_scalePileUpPtBB_j,
        CMS_scalePileUpPtEC1_j,
        CMS_scalePileUpPtEC2_j,
        CMS_scalePileUpPtHF_j,

        CMS_ttH_CSV,
        CMS_ttH_CSVcferr1,
        CMS_ttH_CSVcferr2,
        CMS_ttH_CSVhf,
        CMS_ttH_CSVhfstats1,
        CMS_ttH_CSVhfstats2,
        CMS_ttH_CSVjes,
        CMS_ttH_CSVjesAbsoluteMPFBias,
        CMS_ttH_CSVjesAbsoluteScale,
        CMS_ttH_CSVjesFlavorQCD,
        CMS_ttH_CSVjesPileUpDataMC,
        CMS_ttH_CSVjesPileUpPtBB,
        CMS_ttH_CSVjesPileUpPtEC1,
        CMS_ttH_CSVjesPileUpPtRef,
        CMS_ttH_CSVjesRelativeFSR,
        CMS_ttH_CSVjesSinglePionECAL,
        CMS_ttH_CSVjesSinglePionHCAL,
        CMS_ttH_CSVjesTimePtEta,
        CMS_ttH_CSVlf,
        CMS_ttH_CSVlfstats1,
        CMS_ttH_CSVlfstats2,
        
        CMS_ttH_scaleME,

        CMS_pu,
        gen,
    };

    enum Direction {
        None,
        Up,
        Down
    };

    typedef std::pair<Systematic::Event, Systematic::Direction> SystId;

    bool is_jec(SystId syst_id);
    bool is_jer(SystId syst_id);
    bool is_nominal(SystId syst_id);

    const static auto syst_id_nominal = std::make_pair(Systematic::Nominal, Systematic::None);

    SystId make_id(Systematic::Event e, Systematic::Direction d);
} // namespace Systematic

template <typename T>
void attachSystematics(TTreeReader& reader, std::map<Systematic::SystId, T*>& values, const char* branch_name, bool add_nominal) {
    if (add_nominal) {
        values[std::make_pair(Systematic::Nominal, Systematic::None)] = new T(reader, branch_name);
    }

    const std::string brname(branch_name);

    //values[std::make_pair(Systematic::CMS_scale_j, Systematic::Up)] = new T(reader, (brname + std::string("_TotalUp")).c_str());
    //values[std::make_pair(Systematic::CMS_res_j, Systematic::Up)] = new T(reader, (brname + std::string("_JERUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleSubTotalPileUp_j, Systematic::Up)] = new T(reader, (brname + std::string("_SubTotalPileUpUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteStat_j, Systematic::Up)] = new T(reader, (brname + std::string("_AbsoluteStatUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteScale_j, Systematic::Up)] = new T(reader, (brname + std::string("_AbsoluteScaleUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteFlavMap_j, Systematic::Up)] = new T(reader, (brname + std::string("_AbsoluteFlavMapUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteMPFBias_j, Systematic::Up)] = new T(reader, (brname + std::string("_AbsoluteMPFBiasUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleFragmentation_j, Systematic::Up)] = new T(reader, (brname + std::string("_FragmentationUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleSinglePionECAL_j, Systematic::Up)] = new T(reader, (brname + std::string("_SinglePionECALUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleSinglePionHCAL_j, Systematic::Up)] = new T(reader, (brname + std::string("_SinglePionHCALUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleFlavorQCD_j, Systematic::Up)] = new T(reader, (brname + std::string("_FlavorQCDUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleTimePtEta_j, Systematic::Up)] = new T(reader, (brname + std::string("_TimePtEtaUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJEREC1_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeJEREC1Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJEREC2_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeJEREC2Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJERHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeJERHFUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtBB_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtBBUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtEC1_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtEC1Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtEC2_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtEC2Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtHFUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeFSR_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeFSRUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatFSR_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeStatFSRUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatEC_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeStatECUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeStatHFUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpDataMC_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpDataMCUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtRef_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtRefUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtBB_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtBBUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtEC1_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtEC1Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtEC2_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtEC2Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtHFUp")).c_str());

    //values[std::make_pair(Systematic::CMS_scale_j, Systematic::Down)] = new T(reader, (brname + std::string("_TotalDown")).c_str());
    //values[std::make_pair(Systematic::CMS_res_j, Systematic::Down)] = new T(reader, (brname + std::string("_JERDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleSubTotalPileUp_j, Systematic::Down)] = new T(reader, (brname + std::string("_SubTotalPileUpDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteStat_j, Systematic::Down)] = new T(reader, (brname + std::string("_AbsoluteStatDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteScale_j, Systematic::Down)] = new T(reader, (brname + std::string("_AbsoluteScaleDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteFlavMap_j, Systematic::Down)] = new T(reader, (brname + std::string("_AbsoluteFlavMapDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleAbsoluteMPFBias_j, Systematic::Down)] = new T(reader, (brname + std::string("_AbsoluteMPFBiasDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleFragmentation_j, Systematic::Down)] = new T(reader, (brname + std::string("_FragmentationDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleSinglePionECAL_j, Systematic::Down)] = new T(reader, (brname + std::string("_SinglePionECALDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleSinglePionHCAL_j, Systematic::Down)] = new T(reader, (brname + std::string("_SinglePionHCALDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleFlavorQCD_j, Systematic::Down)] = new T(reader, (brname + std::string("_FlavorQCDDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleTimePtEta_j, Systematic::Down)] = new T(reader, (brname + std::string("_TimePtEtaDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJEREC1_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeJEREC1Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJEREC2_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeJEREC2Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJERHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeJERHFDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtBB_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtBBDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtEC1_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtEC1Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtEC2_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtEC2Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtHFDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeFSR_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeFSRDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatFSR_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeStatFSRDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatEC_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeStatECDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeStatHFDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpDataMC_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpDataMCDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtRef_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtRefDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtBB_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtBBDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtEC1_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtEC1Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtEC2_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtEC2Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtHFDown")).c_str());
}

template <typename T>
class TTreeReaderValueSystematic {
public:
    std::map<Systematic::SystId, TTreeReaderValue<T>* > values;

    TTreeReaderValueSystematic(TTreeReader& reader, const char* branch_name, bool add_nominal = true) {
        attachSystematics<TTreeReaderValue<T>>(reader, values, branch_name, add_nominal); 
    }

    T GetValue(Systematic::SystId syst_id) {
        if (!values.count(syst_id)) {
            std::cerr << "could not find key " << syst_id.first << " " << syst_id.second << std::endl;
            throw std::exception();
        }
        return **values.at(syst_id);
    }

};

template <typename T>
class TTreeReaderArraySystematic {
public:
    std::map<Systematic::SystId, TTreeReaderArray<T>* > values;

    TTreeReaderArraySystematic(TTreeReader& reader, const char* branch_name, bool add_nominal = true) {
        attachSystematics<TTreeReaderArray<T>>(reader, values, branch_name, add_nominal); 
    }

    TTreeReaderArray<T>* GetValue(Systematic::SystId syst_id) {
        return values.at(syst_id);
    }
};

//Static (unchangin) data type that represents the event content
class EventDescription {
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
    int nBCSVM;
    int nPVs;

    int HLT_ttH_SL_mu;
    int HLT_ttH_SL_el;
    int HLT_ttH_DL_mumu;
    int HLT_ttH_DL_elmu;
    int HLT_ttH_DL_elel;
    int HLT_ttH_FH;

    double btag_LR_4b_2b_btagCSV;
    double mem_DL_0w2h2t_p;
    double mem_SL_0w2h2t_p;
    double mem_SL_1w2h2t_p;
    double mem_SL_2w2h2t_p;
    double Wmass;
    double met_pt;

    Systematic::SystId syst_id;
    std::map<Systematic::SystId, double> weights;
};

//Translates a tthbb13 TTree to an EventDescription
template <typename T>
class TreeDescription {
public:

    TTreeReader reader;

    TTreeReaderValue<int> evt;
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
    //TTreeReaderValue<int> HLT_ttH_FH;

    TTreeReaderValue<int> numJets;
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

    TTreeReaderValue<T> btag_LR_4b_2b_btagCSV;
    TTreeReaderValue<T> mem_DL_0w2h2t_p;
    TTreeReaderValue<T> mem_SL_0w2h2t_p;
    TTreeReaderValue<T> mem_SL_1w2h2t_p;
    TTreeReaderValue<T> mem_SL_2w2h2t_p;
    TTreeReaderValue<T> Wmass;
    TTreeReaderValue<T> met_pt;

    std::map<Systematic::SystId, TTreeReaderArray<T>*> correction_branches;

    SampleDescription sample;

    TreeDescription(TFile* file, SampleDescription sample) :
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
        //HLT_ttH_FH(reader, "HLT_ttH_FH"),
        
        numJets(reader, "numJets"),
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

        btag_LR_4b_2b_btagCSV(reader, "btag_LR_4b_2b_btagCSV"),
        mem_DL_0w2h2t_p(reader, "mem_DL_0w2h2t_p"),
        mem_SL_0w2h2t_p(reader, "mem_SL_0w2h2t_p"),
        mem_SL_1w2h2t_p(reader, "mem_SL_1w2h2t_p"),
        mem_SL_2w2h2t_p(reader, "mem_SL_2w2h2t_p"),
        Wmass(reader, "Wmass"),
        met_pt(reader, "met_pt"),
        sample(sample) {
    }
    virtual ~TreeDescription() {}

    
    std::vector<Lepton> build_leptons(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_jets(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

template <typename T>
class TreeDescriptionMCSystematic : public TreeDescription<T> {
public:

    TTreeReaderValue<int> ttCls;
    TTreeReaderValue<T> genTopHad_pt;
    TTreeReaderValue<T> genTopLep_pt;
    
    TTreeReaderValue<T> genWeight;
    TTreeReaderValue<T> puWeight;
    TTreeReaderValue<T> btagWeight_shape;
    
    TreeDescriptionMCSystematic(TFile* file, SampleDescription sample) :
        TreeDescription<T>(file, sample),
        ttCls(TreeDescription<T>::reader, "ttCls"),
        genTopHad_pt(TreeDescription<T>::reader, "genTopHad_pt"),
        genTopLep_pt(TreeDescription<T>::reader, "genTopLep_pt"),
        genWeight(TreeDescription<T>::reader, "genWeight"),
        puWeight(TreeDescription<T>::reader, "puWeight"),
        btagWeight_shape(TreeDescription<T>::reader, "btagWeight_shape")
    {}
    
    ~TreeDescriptionMCSystematic() {}
    
    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

template <typename T>
class TreeDescriptionMC : public TreeDescription<T> {
public:

    TTreeReaderValue<int> ttCls;
    TTreeReaderValue<T> genTopHad_pt;
    TTreeReaderValue<T> genTopLep_pt;

    TTreeReaderValueSystematic<int> numJets;
    TTreeReaderValueSystematic<int> nBCSVM;

    TTreeReaderArray<int> jets_hadronFlavour;
    TTreeReaderArraySystematic<T> jets_corr;
    //TTreeReaderArray<T> jets_corr_JEC;
    //TTreeReaderArray<T> jets_corr_JER;

    TTreeReaderValueSystematic<T> mem_DL_0w2h2t_p;
    TTreeReaderValueSystematic<T> mem_SL_0w2h2t_p;
    TTreeReaderValueSystematic<T> mem_SL_1w2h2t_p;
    TTreeReaderValueSystematic<T> mem_SL_2w2h2t_p;

    TTreeReaderValue<T> genWeight;
    
    TTreeReaderValue<T> puWeight;
    TTreeReaderValue<T> puWeightUp;
    TTreeReaderValue<T> puWeightDown;
    
    TTreeReaderValue<T> btagWeight_shape;
    //TTreeReaderValue<T> btagWeightCSV_CSVcferr1Up;
    //TTreeReaderValue<T> btagWeightCSV_CSVcferr2Up;
    //TTreeReaderValue<T> btagWeightCSV_CSVhfUp;
    //TTreeReaderValue<T> btagWeightCSV_CSVhfstats1Up;
    //TTreeReaderValue<T> btagWeightCSV_CSVhfstats2Up;
    //TTreeReaderValue<T> btagWeightCSV_CSVjesUp;
    //TTreeReaderValue<T> btagWeightCSV_CSVlfUp;
    //TTreeReaderValue<T> btagWeightCSV_CSVlfstats1Up;
    //TTreeReaderValue<T> btagWeightCSV_CSVlfstats2Up;

    //TTreeReaderValue<T> btagWeightCSV_CSVcferr1Down;
    //TTreeReaderValue<T> btagWeightCSV_CSVcferr2Down;
    //TTreeReaderValue<T> btagWeightCSV_CSVhfDown;
    //TTreeReaderValue<T> btagWeightCSV_CSVhfstats1Down;
    //TTreeReaderValue<T> btagWeightCSV_CSVhfstats2Down;
    //TTreeReaderValue<T> btagWeightCSV_CSVjesDown;
    //TTreeReaderValue<T> btagWeightCSV_CSVlfDown;
    //TTreeReaderValue<T> btagWeightCSV_CSVlfstats1Down;
    //TTreeReaderValue<T> btagWeightCSV_CSVlfstats2Down;
    //
    //TTreeReaderArray<T> LHE_weights_scale_wgt;
    
    TreeDescriptionMC(TFile* file, SampleDescription sample) :
        TreeDescription<T>(file, sample),
        ttCls(TreeDescription<T>::reader, "ttCls"),
        genTopHad_pt(TreeDescription<T>::reader, "genTopHad_pt"),
        genTopLep_pt(TreeDescription<T>::reader, "genTopLep_pt"),
        
        numJets(TreeDescription<T>::reader, "numJets"),
        nBCSVM(TreeDescription<T>::reader, "nBCSVM"),

        jets_hadronFlavour(TreeDescription<T>::reader, "jets_hadronFlavour"),
        jets_corr(TreeDescription<T>::reader, "jets_corr", false),
        //jets_corr_JEC(TreeDescription<T>::reader, "jets_corr_JEC"),
        //jets_corr_JER(TreeDescription<T>::reader, "jets_corr_JER"),

        mem_DL_0w2h2t_p(TreeDescription<T>::reader, "mem_DL_0w2h2t_p"),
        mem_SL_0w2h2t_p(TreeDescription<T>::reader, "mem_SL_0w2h2t_p"),
        mem_SL_1w2h2t_p(TreeDescription<T>::reader, "mem_SL_1w2h2t_p"),
        mem_SL_2w2h2t_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_p"),

        genWeight(TreeDescription<T>::reader, "genWeight"),
        
        puWeight(TreeDescription<T>::reader, "puWeight"),
        puWeightUp(TreeDescription<T>::reader, "puWeightUp"),
        puWeightDown(TreeDescription<T>::reader, "puWeightDown"),

        btagWeight_shape(TreeDescription<T>::reader, "btagWeight_shape")

        //btagWeightCSV_CSVcferr1Up(TreeDescription<T>::reader, "btagWeightCSV_up_cferr1"),
        //btagWeightCSV_CSVcferr2Up(TreeDescription<T>::reader, "btagWeightCSV_up_cferr2"),
        //btagWeightCSV_CSVhfUp(TreeDescription<T>::reader, "btagWeightCSV_up_hf"),
        //btagWeightCSV_CSVhfstats1Up(TreeDescription<T>::reader, "btagWeightCSV_up_hfstats1"),
        //btagWeightCSV_CSVhfstats2Up(TreeDescription<T>::reader, "btagWeightCSV_up_hfstats2"),
        //btagWeightCSV_CSVjesUp(TreeDescription<T>::reader, "btagWeightCSV_up_jes"),
        //btagWeightCSV_CSVlfUp(TreeDescription<T>::reader, "btagWeightCSV_up_lf"),
        //btagWeightCSV_CSVlfstats1Up(TreeDescription<T>::reader, "btagWeightCSV_up_lfstats1"),
        //btagWeightCSV_CSVlfstats2Up(TreeDescription<T>::reader, "btagWeightCSV_up_lfstats2"),

        //btagWeightCSV_CSVcferr1Down(TreeDescription<T>::reader, "btagWeightCSV_down_cferr1"),
        //btagWeightCSV_CSVcferr2Down(TreeDescription<T>::reader, "btagWeightCSV_down_cferr2"),
        //btagWeightCSV_CSVhfDown(TreeDescription<T>::reader, "btagWeightCSV_down_hf"),
        //btagWeightCSV_CSVhfstats1Down(TreeDescription<T>::reader, "btagWeightCSV_down_hfstats1"),
        //btagWeightCSV_CSVhfstats2Down(TreeDescription<T>::reader, "btagWeightCSV_down_hfstats2"),
        //btagWeightCSV_CSVjesDown(TreeDescription<T>::reader, "btagWeightCSV_down_jes"),
        //btagWeightCSV_CSVlfDown(TreeDescription<T>::reader, "btagWeightCSV_down_lf"),
        //btagWeightCSV_CSVlfstats1Down(TreeDescription<T>::reader, "btagWeightCSV_down_lfstats1"),
        //btagWeightCSV_CSVlfstats2Down(TreeDescription<T>::reader, "btagWeightCSV_down_lfstats2"),
        //
        //LHE_weights_scale_wgt(TreeDescription<T>::reader, "LHE_weights_scale_wgt")
    {}
    
    ~TreeDescriptionMC() {}

    TTreeReaderArray<T>* get_correction_branch(Systematic::SystId syst_id = Systematic::syst_id_nominal);

    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_jets(Systematic::SystId syst_id = Systematic::syst_id_nominal);

};

typedef TreeDescription<float> TreeDescriptionFloat;
typedef TreeDescriptionMC<float> TreeDescriptionMCFloat;
typedef TreeDescriptionMCSystematic<float> TreeDescriptionMCSystematicFloat;

typedef TreeDescription<double> TreeDescriptionDouble;
typedef TreeDescriptionMC<double> TreeDescriptionMCDouble;
typedef TreeDescriptionMCSystematic<double> TreeDescriptionMCSystematicDouble;

} //namespace TTH_MEAnalysis
#endif
