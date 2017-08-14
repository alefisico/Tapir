#include "TTH/MEAnalysis/interface/EventModel.h"


namespace TTH_MEAnalysis {

template <typename T> int sgn(T val) {
    return (T(0) < val) - (val < T(0));
}

bool Systematic::is_jec(Systematic::SystId syst_id) {
    return syst_id.first == CMS_scale_j;
}

bool Systematic::is_jer(Systematic::SystId syst_id) {
    return syst_id.first == CMS_res_j;
}

bool Systematic::is_nominal(Systematic::SystId syst_id) {
    return syst_id.first == Nominal;
}

Systematic::SystId Systematic::make_id(Systematic::Event e, Systematic::Direction d) {
    return std::make_pair(e, d);
}

EventDescription TreeDescriptionMC::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescription::create_event(syst_id);

    std::vector<int> jets_hadronflavour;
    for (auto njet=0; njet < *njets; njet++) {
        jets_hadronflavour.push_back(this->jets_hadronFlavour[njet]);
    }

    event.ttCls = *ttCls;
    event.numJets = numJets.GetValue(syst_id);
    event.nBCSVM = nBCSVM.GetValue(syst_id);

    event.weights[std::make_pair(Systematic::CMS_ttH_CSV, Systematic::None)] = (*btagWeightCSV);
    event.weights[std::make_pair(Systematic::CMS_pu, Systematic::None)] = (*puWeight);

    if (Systematic::is_nominal(syst_id)) {

        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Up)] = (*btagWeightCSV_CSVcferr1Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr2, Systematic::Up)] = (*btagWeightCSV_CSVcferr2Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhf, Systematic::Up)] = (*btagWeightCSV_CSVhfUp);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats1, Systematic::Up)] = (*btagWeightCSV_CSVhfstats1Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats2, Systematic::Up)] = (*btagWeightCSV_CSVhfstats2Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVjes, Systematic::Up)] = (*btagWeightCSV_CSVjesUp);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlf, Systematic::Up)] = (*btagWeightCSV_CSVlfUp);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats1, Systematic::Up)] = (*btagWeightCSV_CSVlfstats1Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats2, Systematic::Up)] = (*btagWeightCSV_CSVlfstats2Up);

        event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Up)] = (*puWeightUp);

        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Down)] = (*btagWeightCSV_CSVcferr1Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr2, Systematic::Down)] = (*btagWeightCSV_CSVcferr2Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhf, Systematic::Down)] = (*btagWeightCSV_CSVhfDown);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats1, Systematic::Down)] = (*btagWeightCSV_CSVhfstats1Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats2, Systematic::Down)] = (*btagWeightCSV_CSVhfstats2Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVjes, Systematic::Down)] = (*btagWeightCSV_CSVjesDown);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlf, Systematic::Down)] = (*btagWeightCSV_CSVlfDown);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats1, Systematic::Down)] = (*btagWeightCSV_CSVlfstats1Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats2, Systematic::Down)] = (*btagWeightCSV_CSVlfstats2Down);

        event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Down)] = (*puWeightDown);


    }
    return event;
}

EventDescription TreeDescription::create_event(Systematic::SystId syst_id) {
    std::vector<Jet> jets(build_jets(syst_id));
    
    EventDescription event;

    event.run = *run;
    event.lumi = *lumi;
    event.evt = *evt;

    event.is_sl = *is_sl;
    event.is_dl = *is_dl;
    event.is_fh = *is_fh;

    event.HLT_ttH_SL_mu = 1;
    event.HLT_ttH_SL_el = 1;
    event.HLT_ttH_DL_mumu = 1;
    event.HLT_ttH_DL_elmu = 1;
    event.HLT_ttH_DL_elel = 1;
    event.HLT_ttH_FH = 1;
    
    event.numJets = *numJets;
    event.nBCSVM = *nBCSVM;
    event.jets = jets;
    event.syst_id = syst_id;
    event.leptons = build_leptons(syst_id);

    event.btag_LR_4b_2b_btagCSV = *btag_LR_4b_2b_btagCSV;
    event.mem_DL_0w2h2t_p = *mem_DL_0w2h2t_p;
    event.mem_SL_0w2h2t_p = *mem_SL_0w2h2t_p;
    event.mem_SL_1w2h2t_p = *mem_SL_1w2h2t_p;
    event.mem_SL_2w2h2t_p = *mem_SL_2w2h2t_p;
    event.Wmass = *Wmass;

    event.weights[Systematic::syst_id_nominal] = 1.0;
    return event;
}

std::vector<Lepton> TreeDescription::build_leptons(Systematic::SystId syst_id) {
    std::vector<Lepton> leps;

    for (int ilep = 0; ilep < *nleps; ilep++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            leps_pt[ilep],
            leps_eta[ilep],
            leps_phi[ilep],
            leps_mass[ilep]
        );
        leps.push_back(Lepton(lv, sgn(leps_pdgId[ilep]), leps_pdgId[ilep]));
    }
    return leps;
}

std::vector<Jet> TreeDescription::build_jets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *njets; njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;

        lv.SetPtEtaPhiM(jets_pt[njet] * corr/base_corr, jets_eta[njet], jets_phi[njet], jets_mass[njet]);
        Jet jet(lv, jets_btagCSV[njet]);
        jets.push_back(jet);
    }
    return jets;
}

std::vector<Jet> TreeDescriptionMC::build_jets(Systematic::SystId syst_id) {
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
            base_corr = jets_corr_JER[njet];
        }

        lv.SetPtEtaPhiM(jets_pt[njet] * corr/base_corr, jets_eta[njet], jets_phi[njet], jets_mass[njet]);
        Jet jet(lv, jets_btagCSV[njet]);
        jets.push_back(jet);
    }
    return jets;
}

TTreeReaderArray<double>* TreeDescriptionMC::get_correction_branch(Systematic::SystId syst_id) {
    return jets_corr.GetValue(syst_id);
}

} //namespace TTH_MEAnalysis
