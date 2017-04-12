#include <sstream>
#include <iostream>
#include <string>
#include <functional>
#include <memory>

#include "TH1.h"
#include "TH1D.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"
#include "TLorentzVector.h"
#include "TStopwatch.h"

template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

class Jet {
public:
    TLorentzVector lv;
    double btagCSV;

    Jet(TLorentzVector _lv, double _btagCSV) :
    lv(_lv),
    btagCSV(_btagCSV)
    {
    }
};


namespace Systematic {

enum Event {
    Nominal,
    CMS_scale_j,
    CMS_res_j,
    CMS_SubTotalPileUp_j,
    CMS_AbsoluteStat_j,
    CMS_AbsoluteScale_j,
    CMS_AbsoluteFlavMap_j,
    CMS_AbsoluteMPFBias_j,
    CMS_Fragmentation_j,
    CMS_SinglePionECAL_j,
    CMS_SinglePionHCAL_j,
    CMS_FlavorQCD_j,
    CMS_TimePtEta_j,
    CMS_RelativeJEREC1_j,
    CMS_RelativeJEREC2_j,
    CMS_RelativeJERHF_j,
    CMS_RelativePtBB_j,
    CMS_RelativePtEC1_j,
    CMS_RelativePtEC2_j,
    CMS_RelativePtHF_j,
    CMS_RelativeFSR_j,
    CMS_RelativeStatFSR_j,
    CMS_RelativeStatEC_j,
    CMS_RelativeStatHF_j,
    CMS_PileUpDataMC_j,
    CMS_PileUpPtRef_j,
    CMS_PileUpPtBB_j,
    CMS_PileUpPtEC1_j,
    CMS_PileUpPtEC2_j,
    CMS_PileUpPtHF_j,
    CMS_ttH_CSVcferr1,
    CMS_ttH_CSVcferr2,
    CMS_ttH_CSVhf,
    CMS_ttH_CSVhfstats1,
    CMS_ttH_CSVhfstats2,
    CMS_ttH_CSVjes,
    CMS_ttH_CSVlf,
    CMS_ttH_CSVlfstats1,
    CMS_ttH_CSVlfstats2,
    CMS_pu,
};

enum Direction {
    None,
    Up,
    Down
};

typedef std::pair<Systematic::Event, Systematic::Direction> SystId;

bool is_jec(SystId syst_id) {
    return syst_id.first != CMS_res_j;
}

bool is_jer(SystId syst_id) {
    return syst_id.first == CMS_res_j;
}

bool is_nominal(SystId syst_id) {
    return syst_id.first == Nominal;
}

const static auto syst_id_nominal = std::make_pair(Systematic::Nominal, Systematic::None);
} // namespace Systematic

class EventDescription {
public:
    std::vector<Jet> jets;
    std::vector<int> leps_pdgId;
    int is_sl;
    int numJets;
    int nBCSVM;
    Systematic::SystId syst_id;
    std::map<Systematic::SystId, double> weights;
};

template <typename T>
void attachSystematics(TTreeReader& reader, std::map<Systematic::SystId, T*>& values, const char* branch_name) {
    values[std::make_pair(Systematic::Nominal, Systematic::None)] = new T(reader, branch_name);
    
    values[std::make_pair(Systematic::CMS_scale_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_TotalUp")).c_str());
    values[std::make_pair(Systematic::CMS_res_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_JERUp")).c_str());
    values[std::make_pair(Systematic::CMS_SubTotalPileUp_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_SubTotalPileUpUp")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteStat_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteStatUp")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteScale_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteScaleUp")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteFlavMap_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteFlavMapUp")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteMPFBias_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteMPFBiasUp")).c_str());
    values[std::make_pair(Systematic::CMS_Fragmentation_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_FragmentationUp")).c_str());
    values[std::make_pair(Systematic::CMS_SinglePionECAL_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_SinglePionECALUp")).c_str());
    values[std::make_pair(Systematic::CMS_SinglePionHCAL_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_SinglePionHCALUp")).c_str());
    values[std::make_pair(Systematic::CMS_FlavorQCD_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_FlavorQCDUp")).c_str());
    values[std::make_pair(Systematic::CMS_TimePtEta_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_TimePtEtaUp")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeJEREC1_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativeJEREC1Up")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeJEREC2_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativeJEREC2Up")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeJERHF_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativeJERHFUp")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtBB_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtBBUp")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtEC1_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtEC1Up")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtEC2_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtEC2Up")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtHF_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtHFUp")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeFSR_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativeFSRUp")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeStatFSR_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativeStatFSRUp")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeStatEC_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativeStatECUp")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeStatHF_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_RelativeStatHFUp")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpDataMC_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_PileUpDataMCUp")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtRef_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtRefUp")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtBB_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtBBUp")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtEC1_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtEC1Up")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtEC2_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtEC2Up")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtHF_j, Systematic::Up)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtHFUp")).c_str());

    values[std::make_pair(Systematic::CMS_scale_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_TotalDown")).c_str());
    values[std::make_pair(Systematic::CMS_res_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_JERDown")).c_str());
    values[std::make_pair(Systematic::CMS_SubTotalPileUp_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_SubTotalPileUpDown")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteStat_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteStatDown")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteScale_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteScaleDown")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteFlavMap_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteFlavMapDown")).c_str());
    values[std::make_pair(Systematic::CMS_AbsoluteMPFBias_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_AbsoluteMPFBiasDown")).c_str());
    values[std::make_pair(Systematic::CMS_Fragmentation_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_FragmentationDown")).c_str());
    values[std::make_pair(Systematic::CMS_SinglePionECAL_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_SinglePionECALDown")).c_str());
    values[std::make_pair(Systematic::CMS_SinglePionHCAL_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_SinglePionHCALDown")).c_str());
    values[std::make_pair(Systematic::CMS_FlavorQCD_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_FlavorQCDDown")).c_str());
    values[std::make_pair(Systematic::CMS_TimePtEta_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_TimePtEtaDown")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeJEREC1_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativeJEREC1Down")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeJEREC2_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativeJEREC2Down")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeJERHF_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativeJERHFDown")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtBB_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtBBDown")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtEC1_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtEC1Down")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtEC2_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtEC2Down")).c_str());
    values[std::make_pair(Systematic::CMS_RelativePtHF_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativePtHFDown")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeFSR_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativeFSRDown")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeStatFSR_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativeStatFSRDown")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeStatEC_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativeStatECDown")).c_str());
    values[std::make_pair(Systematic::CMS_RelativeStatHF_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_RelativeStatHFDown")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpDataMC_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_PileUpDataMCDown")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtRef_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtRefDown")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtBB_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtBBDown")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtEC1_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtEC1Down")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtEC2_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtEC2Down")).c_str());
    values[std::make_pair(Systematic::CMS_PileUpPtHF_j, Systematic::Down)] = new T(reader, (std::string(branch_name) + std::string("_PileUpPtHFDown")).c_str());
}

template <typename T>
class TTreeReaderValueSystematic {
public:
    std::map<Systematic::SystId, TTreeReaderValue<T>* > values;

    TTreeReaderValueSystematic(TTreeReader& reader, const char* branch_name) {
        attachSystematics<TTreeReaderValue<T>>(reader, values, branch_name); 
    }

    T GetValue(Systematic::SystId syst_id) {
        return **values.at(syst_id);
    }
};

template <typename T>
class TTreeReaderArraySystematic {
public:
    std::map<Systematic::SystId, TTreeReaderArray<T>* > values;

    TTreeReaderArraySystematic(TTreeReader& reader, const char* branch_name) {
        attachSystematics<TTreeReaderArray<T>>(reader, values, branch_name); 
    }

    TTreeReaderArray<T>* GetValue(Systematic::SystId syst_id) {
        return values.at(syst_id);
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

class TreeDescription {
public:

    TTreeReader reader;

    TTreeReaderValue<unsigned long long> evt;
    TTreeReaderValue<unsigned int> run;
    TTreeReaderValue<unsigned int> lumi;

    TTreeReaderValue<int> is_sl;
    TTreeReaderValue<int> is_dl;
    TTreeReaderValue<int> is_fh;

    TTreeReaderValueSystematic<int> numJets;
    TTreeReaderValueSystematic<int> nBCSVM;
    
    TTreeReaderValue<int> nleps;
    TTreeReaderArray<double> leps_pdgId;
    
    TTreeReaderValue<int> njets;
    TTreeReaderArray<double> jets_pt;
    TTreeReaderArray<double> jets_eta;
    TTreeReaderArray<double> jets_phi;
    TTreeReaderArray<double> jets_mass;
    TTreeReaderArray<double> jets_btagCSV;
    TTreeReaderArraySystematic<double> jets_corr;
    
    TTreeReaderValue<double> btagWeightCSV;
    TTreeReaderValue<double> btagWeightCSV_CSVcferr1Down;
    TTreeReaderValue<double> btagWeightCSV_CSVcferr1Up;

    std::map<Systematic::SystId, TTreeReaderArray<double>*> correction_branches;

    SampleDescription sample;

    TreeDescription(TFile* file, SampleDescription _sample) :
        reader("tree", file),
        evt(reader, "evt"),
        run(reader, "run"),
        lumi(reader, "lumi"),

        is_sl(reader, "is_sl"),
        is_dl(reader, "is_dl"),
        is_fh(reader, "is_fh"),
        
        numJets(reader, "numJets"),
        nBCSVM(reader, "nBCSVM"),
        
        nleps(reader, "nleps"),
        leps_pdgId(reader, "leps_pdgId"),
        
        njets(reader, "njets"),
        jets_pt(reader, "jets_pt"),
        jets_eta(reader, "jets_eta"),
        jets_phi(reader, "jets_phi"),
        jets_mass(reader, "jets_mass"),
        jets_btagCSV(reader, "jets_btagCSV"),
        jets_corr(reader, "jets_corr"),
        
        btagWeightCSV(reader, "btagWeightCSV"),
        btagWeightCSV_CSVcferr1Down(reader, "btagWeightCSV_down_cferr1"),
        btagWeightCSV_CSVcferr1Up(reader, "btagWeightCSV_up_cferr1"),
        sample(_sample)
    {
    }

    TTreeReaderArray<double>* get_correction_branch(Systematic::SystId syst_id) {
        return jets_corr.GetValue(syst_id);
    };

    std::vector<Jet> build_jets(Systematic::SystId syst_id) {
        auto* correction_branch = get_correction_branch(syst_id);
        std::vector<Jet> jets;
        for (auto njet=0; njet < *njets; njet++) {
            TLorentzVector lv;

            double corr = 1.0;
            double base_corr = 1.0;
            
            if (Systematic::is_jec(syst_id)) {
                corr = (*correction_branch)[njet];
                base_corr = (*jets_corr.GetValue(std::make_pair(Systematic::Nominal, Systematic::None)))[njet];
            } else if (Systematic::is_jer(syst_id)) {
                corr = (*correction_branch)[njet];
                base_corr = (*jets_corr.GetValue(std::make_pair(Systematic::Nominal, Systematic::None)))[njet];
            }

            lv.SetPtEtaPhiM(jets_pt[njet] * corr/base_corr, jets_eta[njet], jets_phi[njet], jets_mass[njet]);
            Jet jet(lv, jets_btagCSV[njet]);
            jets.push_back(jet);
        }
        return jets;
    }

    EventDescription create_event(Systematic::SystId syst_id) {
        std::vector<Jet> jets(build_jets(syst_id));
        EventDescription event;
        event.is_sl = *is_sl;
        event.numJets = numJets.GetValue(syst_id);
        event.nBCSVM = nBCSVM.GetValue(syst_id);
        event.jets = jets;
        event.syst_id = syst_id;
        for (int ilep = 0; ilep < *nleps; ilep++) {
            event.leps_pdgId.push_back((int)leps_pdgId[ilep]);
        }

        if (sample.isMC()) {
            event.weights[Systematic::syst_id_nominal] = *btagWeightCSV;
            if (Systematic::is_nominal(syst_id)) {
                event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Up)] = *btagWeightCSV_CSVcferr1Up;
                event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Down)] = *btagWeightCSV_CSVcferr1Down;
            }
        } else {
            event.weights[Systematic::syst_id_nominal] = 1.0;
        }
        return event;
    }
};

class OutputNode {
public:
    std::map<Systematic::SystId, std::unique_ptr<TH1D>> histograms;
   
    std::function<double(const EventDescription&)> value;
    std::function<double(Systematic::SystId, const EventDescription&)> weight;
    std::function<bool(Systematic::SystId, const EventDescription&)> cut;

    void fill(Systematic::SystId syst_id, const EventDescription& desc) {
        if (cut(syst_id, desc)) {
            histograms.at(syst_id)->Fill(value(desc), weight(syst_id, desc));
        }
    }

    OutputNode(
        std::function<double(const EventDescription&)> _value,
        std::function<double(Systematic::SystId, const EventDescription&)> _weight = [](Systematic::SystId syst_id, const EventDescription& desc) { return 1.0; },
        std::function<bool(Systematic::SystId, const EventDescription&)> _cut = [](Systematic::SystId syst_id, const EventDescription& desc) { return true; }
    ) :
        value(_value),
        weight(_weight),
        cut(_cut)
    {
    }
};

double weight_systematic_map(Systematic::SystId syst_id, const EventDescription& desc) {
    if (desc.weights.count(desc.syst_id) > 0) {
        auto w = desc.weights.at(syst_id);
        return w;
    }
    std::ostringstream ss;
    ss << "could not get weight: syst_id=" << desc.syst_id.first << ":" << desc.syst_id.second;
    throw std::runtime_error(ss.str().c_str());
    return 0.0;
}

class CategoryTree {
public:
    std::vector<std::unique_ptr<CategoryTree>> children;
    std::vector<std::unique_ptr<OutputNode>> outputs;
    
    std::function<bool(const EventDescription&)> cut;

    const std::string name;
    CategoryTree(
        std::string _name,
        std::function<bool(const EventDescription&)> _cut = [](const EventDescription& desc) { return true;}
    ) : cut(_cut), name(_name) {
    }

    void addOutput(
        const SampleDescription& sample,
        std::vector<Systematic::SystId> systematics_event,
        std::vector<Systematic::SystId> systematics_weight,
        std::string hist_name,
        std::function<double(const EventDescription& desc)> fill_func,
        int nbins, double bin_low, double bin_high
        ) {
        auto output = make_unique<OutputNode>(
            fill_func,
            [](Systematic::SystId syst_id, const EventDescription& desc) {return desc.weights.at(Systematic::syst_id_nominal);},
            [](Systematic::SystId syst_id, const EventDescription& desc) {return Systematic::is_nominal(desc.syst_id) && Systematic::is_nominal(syst_id);}
        );
        output->histograms[Systematic::syst_id_nominal] = std::move(make_unique<TH1D>(hist_name.c_str(), hist_name.c_str(), nbins, bin_low, bin_high));
        outputs.push_back(std::move(output));
    
        if (sample.isMC()) {
            auto output_systev = make_unique<OutputNode>(
                fill_func,
                [](Systematic::SystId syst_id, const EventDescription& desc) {return desc.weights.at(Systematic::syst_id_nominal);},
                [](Systematic::SystId syst_id, const EventDescription& desc) {return !Systematic::is_nominal(desc.syst_id) && !Systematic::is_nominal(syst_id);}
            );
            for (auto systematic : systematics_event) {
                output_systev->histograms[systematic] = std::move(make_unique<TH1D>(hist_name.c_str(), hist_name.c_str(), nbins, bin_low, bin_high));
                output_systev->histograms.at(systematic)->SetDirectory(0);
            }

            auto output_systw = make_unique<OutputNode>(
                fill_func,
                weight_systematic_map,
                [](Systematic::SystId syst_id, const EventDescription& desc) {return Systematic::is_nominal(desc.syst_id) && !Systematic::is_nominal(syst_id);}
            );
            for (auto systematic : systematics_weight) {
                output_systw->histograms[systematic] = std::move(make_unique<TH1D>("h", "h", nbins, bin_low, bin_high));
                output_systw->histograms.at(systematic)->SetDirectory(0);
            }
            outputs.push_back(std::move(output_systev));
            outputs.push_back(std::move(output_systw));
        }
    }

    void apply(Systematic::SystId syst_id, const EventDescription& desc) {
        if(cut(desc)) {
            for (const auto& output : outputs) {
                output->fill(syst_id, desc);
            }
            for (const auto& child : children) {
                child->apply(syst_id, desc);
            }
        }
    }

    void saveOutputs(TFile* outfile) {
        for (const auto& output : outputs) {
            for (auto& syst_histo : output->histograms) {
                auto systematic = syst_histo.first;
                auto histogram = std::move(syst_histo.second);
                std::ostringstream ss;
                ss << (int)systematic.first << "_" << (int)systematic.second;
                std::string syst_name = ss.str();
                histogram->SetName((name + std::string("__") + syst_name).c_str());
                histogram->SetDirectory(outfile);
                //histogram->AddDirectory(&outfile); 
                //outfile.Append(histogram.get());
                histogram->Write();
                std::cout << histogram->GetName() << " " << histogram->Integral() << " " << histogram->GetEntries() << std::endl;
            }
        }
        for (const auto& child : children) {
            child->saveOutputs(outfile);
        }
    }
};


int main(int argc, const char** argv) {
    
    TH1::AddDirectory(false);
    TFile outfile("out.root", "RECREATE");
    auto filenames = {
        "file:///mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GC4e85405795b1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_245_tree.root",
        "file:///mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GC4e85405795b1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_246_tree.root",
        "file:///mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GC4e85405795b1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_248_tree.root",
        "file:///mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GC4e85405795b1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_249_tree.root",
        "file:///mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GC4e85405795b1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_250_tree.root",
        "file:///mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GC4e85405795b1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_251_tree.root",
        "file:///mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GC4e85405795b1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_252_tree.root"
    };

    SampleDescription sample(SampleDescription::MC);

    auto systematics_event = {
        std::make_pair(Systematic::CMS_scale_j, Systematic::Up),
        std::make_pair(Systematic::CMS_res_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_SubTotalPileUp_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_AbsoluteStat_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_AbsoluteScale_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_AbsoluteFlavMap_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_AbsoluteMPFBias_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_Fragmentation_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_SinglePionECAL_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_SinglePionHCAL_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_FlavorQCD_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_TimePtEta_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativeJEREC1_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativeJEREC2_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativeJERHF_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativePtBB_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativePtEC1_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativePtEC2_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativePtHF_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativeFSR_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativeStatFSR_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativeStatEC_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_RelativeStatHF_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_PileUpDataMC_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_PileUpPtRef_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_PileUpPtBB_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_PileUpPtEC1_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_PileUpPtEC2_j, Systematic::Up),
//        std::make_pair(Systematic::CMS_PileUpPtHF_j, Systematic::Up),

        std::make_pair(Systematic::CMS_scale_j, Systematic::Down),
        std::make_pair(Systematic::CMS_res_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_SubTotalPileUp_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_AbsoluteStat_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_AbsoluteScale_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_AbsoluteFlavMap_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_AbsoluteMPFBias_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_Fragmentation_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_SinglePionECAL_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_SinglePionHCAL_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_FlavorQCD_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_TimePtEta_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativeJEREC1_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativeJEREC2_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativeJERHF_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativePtBB_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativePtEC1_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativePtEC2_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativePtHF_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativeFSR_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativeStatFSR_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativeStatEC_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_RelativeStatHF_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_PileUpDataMC_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_PileUpPtRef_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_PileUpPtBB_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_PileUpPtEC1_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_PileUpPtEC2_j, Systematic::Down),
//        std::make_pair(Systematic::CMS_PileUpPtHF_j, Systematic::Down),
    };
    auto systematics_weight = {
        std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Up),
        std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Down)
    };

    CategoryTree cat_root("sl_jge4", [](const EventDescription& desc) { return desc.is_sl && desc.numJets>=4; });
    cat_root.addOutput(
        sample, systematics_event, systematics_weight,
        "numJets",
        [](const EventDescription& desc) { return desc.numJets; },
        15, 0, 15 
    );
    auto cat_sl_jge6_tge4 = make_unique<CategoryTree>(
        "sl_jge6_tge4",
        [](const EventDescription& desc) { return desc.is_sl && desc.numJets>=6 && desc.nBCSVM>=4; }
    );
    cat_sl_jge6_tge4->addOutput(
        sample, systematics_event, systematics_weight,
        "jets_pt0",
        [](const EventDescription& desc) { return desc.jets.at(0).lv.Pt(); },
        100, 0, 300
    );
    cat_root.children.push_back(std::move(cat_sl_jge6_tge4));
    
    TStopwatch timer;
    unsigned int iEv = 0;
    for (auto filename : filenames) {
        std::cout << "opening " << filename << std::endl;
        TFile* fi = TFile::Open(filename);
        TreeDescription tree_desc(fi, sample);

        while (tree_desc.reader.Next()) {
           
            //Fill nominal
            auto event_nominal = tree_desc.create_event(Systematic::syst_id_nominal);
            cat_root.apply(Systematic::syst_id_nominal, event_nominal);

            //Fill systematic weights
            for (auto systematic_weight : systematics_weight) {
                cat_root.apply(systematic_weight, event_nominal);
            }

            //Fill systematic events
            for (auto systematic_event : systematics_event) {
                auto event = tree_desc.create_event(systematic_event);
                cat_root.apply(systematic_event, event);
            }

            iEv += 1;
            if (iEv % 10000 == 0) {
                std::cout << iEv << std::endl;
            }
        }
    }
    std::cout << (float)iEv / timer.RealTime() << std::endl;

    outfile.cd();
    cat_root.saveOutputs(&outfile);
    outfile.Write();
    outfile.Close();
    return 0;
}
