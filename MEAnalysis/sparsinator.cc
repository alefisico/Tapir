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
#include "TStopwatch.h"

template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

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
            //Add all systematically modified histograms
            auto output_systev = make_unique<OutputNode>(
                fill_func,
                [](Systematic::SystId syst_id, const EventDescription& desc) {return desc.weights.at(Systematic::syst_id_nominal);},
                [](Systematic::SystId syst_id, const EventDescription& desc) {return !Systematic::is_nominal(desc.syst_id) && !Systematic::is_nominal(syst_id);}
            );
            for (auto systematic : systematics_event) {
                output_systev->histograms[systematic] = std::move(make_unique<TH1D>(hist_name.c_str(), hist_name.c_str(), nbins, bin_low, bin_high));
                output_systev->histograms.at(systematic)->SetDirectory(0);
            }

            //Add all systematically reweighted histograms 
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
        "file://./job_0_tree.root"
    };

    SampleDescription sample(SampleDescription::MC);

    auto systematics_event = {
        std::make_pair(Systematic::CMS_scale_j, Systematic::Up),
        std::make_pair(Systematic::CMS_res_j, Systematic::Up),
        std::make_pair(Systematic::CMS_SubTotalPileUp_j, Systematic::Up),
        std::make_pair(Systematic::CMS_AbsoluteStat_j, Systematic::Up),
        std::make_pair(Systematic::CMS_AbsoluteScale_j, Systematic::Up),
        std::make_pair(Systematic::CMS_AbsoluteFlavMap_j, Systematic::Up),
        std::make_pair(Systematic::CMS_AbsoluteMPFBias_j, Systematic::Up),
        std::make_pair(Systematic::CMS_Fragmentation_j, Systematic::Up),
        std::make_pair(Systematic::CMS_SinglePionECAL_j, Systematic::Up),
        std::make_pair(Systematic::CMS_SinglePionHCAL_j, Systematic::Up),
        std::make_pair(Systematic::CMS_FlavorQCD_j, Systematic::Up),
        std::make_pair(Systematic::CMS_TimePtEta_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativeJEREC1_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativeJEREC2_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativeJERHF_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativePtBB_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativePtEC1_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativePtEC2_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativePtHF_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativeFSR_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativeStatFSR_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativeStatEC_j, Systematic::Up),
        std::make_pair(Systematic::CMS_RelativeStatHF_j, Systematic::Up),
        std::make_pair(Systematic::CMS_PileUpDataMC_j, Systematic::Up),
        std::make_pair(Systematic::CMS_PileUpPtRef_j, Systematic::Up),
        std::make_pair(Systematic::CMS_PileUpPtBB_j, Systematic::Up),
        std::make_pair(Systematic::CMS_PileUpPtEC1_j, Systematic::Up),
        std::make_pair(Systematic::CMS_PileUpPtEC2_j, Systematic::Up),
        std::make_pair(Systematic::CMS_PileUpPtHF_j, Systematic::Up),

        std::make_pair(Systematic::CMS_scale_j, Systematic::Down),
        std::make_pair(Systematic::CMS_res_j, Systematic::Down),
        std::make_pair(Systematic::CMS_SubTotalPileUp_j, Systematic::Down),
        std::make_pair(Systematic::CMS_AbsoluteStat_j, Systematic::Down),
        std::make_pair(Systematic::CMS_AbsoluteScale_j, Systematic::Down),
        std::make_pair(Systematic::CMS_AbsoluteFlavMap_j, Systematic::Down),
        std::make_pair(Systematic::CMS_AbsoluteMPFBias_j, Systematic::Down),
        std::make_pair(Systematic::CMS_Fragmentation_j, Systematic::Down),
        std::make_pair(Systematic::CMS_SinglePionECAL_j, Systematic::Down),
        std::make_pair(Systematic::CMS_SinglePionHCAL_j, Systematic::Down),
        std::make_pair(Systematic::CMS_FlavorQCD_j, Systematic::Down),
        std::make_pair(Systematic::CMS_TimePtEta_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativeJEREC1_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativeJEREC2_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativeJERHF_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativePtBB_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativePtEC1_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativePtEC2_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativePtHF_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativeFSR_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativeStatFSR_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativeStatEC_j, Systematic::Down),
        std::make_pair(Systematic::CMS_RelativeStatHF_j, Systematic::Down),
        std::make_pair(Systematic::CMS_PileUpDataMC_j, Systematic::Down),
        std::make_pair(Systematic::CMS_PileUpPtRef_j, Systematic::Down),
        std::make_pair(Systematic::CMS_PileUpPtBB_j, Systematic::Down),
        std::make_pair(Systematic::CMS_PileUpPtEC1_j, Systematic::Down),
        std::make_pair(Systematic::CMS_PileUpPtEC2_j, Systematic::Down),
        std::make_pair(Systematic::CMS_PileUpPtHF_j, Systematic::Down),
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
