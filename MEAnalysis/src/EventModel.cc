#include "TTH/MEAnalysis/interface/EventModel.h"


namespace TTH_MEAnalysis {

template <typename T> int sgn(T val) {
    return (T(0) < val) - (val < T(0));
}

bool Systematic::is_jec(Systematic::SystId syst_id) {
    bool ret = false;
    ret = (syst_id.first == CMS_scale_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtHF_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtEC2_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtEC1_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtBB_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtRef_j ) | ret;
    ret = (syst_id.first == CMS_scalePileUpDataMC_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeStatHF_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeStatEC_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeStatFSR_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeFSR_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativePtHF_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativePtEC2_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativePtEC1_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativePtBB_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeJERHF_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeJEREC2_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeJEREC1_j) | ret;
    ret = (syst_id.first == CMS_scaleTimePtEta_j) | ret;
    ret = (syst_id.first == CMS_scaleFlavorQCD_j) | ret;
    ret = (syst_id.first == CMS_scaleSinglePionHCAL_j) | ret;
    ret = (syst_id.first == CMS_scaleSinglePionECAL_j) | ret;
    ret = (syst_id.first == CMS_scaleFragmentation_j) | ret;
    ret = (syst_id.first == CMS_scaleAbsoluteMPFBias_j) | ret;
    ret = (syst_id.first == CMS_scaleAbsoluteFlavMap_j) | ret;
    ret = (syst_id.first == CMS_scaleAbsoluteScale_j) | ret;
    ret = (syst_id.first == CMS_scaleAbsoluteStat_j) | ret;
    ret = (syst_id.first == CMS_scaleSubTotalPileUp_j) | ret;
    return ret;
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

template <typename T>
EventDescription TreeDescriptionMCSystematic<T>::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescription<T>::create_event(syst_id);
    event.ttCls = *ttCls;
    event.genTopHad_pt = *genTopHad_pt;
    event.genTopLep_pt = *genTopLep_pt;
    event.weights[std::make_pair(Systematic::CMS_ttH_CSV, Systematic::None)] = 1.0;
    event.weights[std::make_pair(Systematic::CMS_pu, Systematic::None)] = 1.0;
    event.weights[std::make_pair(Systematic::gen, Systematic::None)] = (*genWeight);
    return event;
}

float recomputeMem(float p0, float p1, float sf=0.1) {
    if (p0 == 0 && p1 == 0) {
        return 0.0;
    }
    return p0/(p0+sf*p1);
}

template <typename T>
EventDescription TreeDescriptionMC<T>::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescription<T>::create_event(syst_id);

    for (auto njet=0; njet < *(this->njets); njet++) {
        event.jets_hadronFlavour.push_back(this->jets_hadronFlavour[njet]);
    }

    event.ttCls = *ttCls;
    event.numJets = numJets.GetValue(syst_id);
    event.nBCSVM = nBCSVM.GetValue(syst_id);

    event.weights[std::make_pair(Systematic::gen, Systematic::None)] = (*genWeight);
    event.weights[std::make_pair(Systematic::CMS_ttH_CSV, Systematic::None)] = 1.0;
    event.weights[std::make_pair(Systematic::CMS_pu, Systematic::None)] = 1.0;

    if (Systematic::is_nominal(syst_id)) {

        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Up)] = (*btagWeightCSV_CSVcferr1Up);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr2, Systematic::Up)] = (*btagWeightCSV_CSVcferr2Up);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVhf, Systematic::Up)] = (*btagWeightCSV_CSVhfUp);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats1, Systematic::Up)] = (*btagWeightCSV_CSVhfstats1Up);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats2, Systematic::Up)] = (*btagWeightCSV_CSVhfstats2Up);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVjes, Systematic::Up)] = (*btagWeightCSV_CSVjesUp);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVlf, Systematic::Up)] = (*btagWeightCSV_CSVlfUp);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats1, Systematic::Up)] = (*btagWeightCSV_CSVlfstats1Up);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats2, Systematic::Up)] = (*btagWeightCSV_CSVlfstats2Up);

        //event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Up)] = (*puWeightUp);

        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Down)] = (*btagWeightCSV_CSVcferr1Down);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr2, Systematic::Down)] = (*btagWeightCSV_CSVcferr2Down);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVhf, Systematic::Down)] = (*btagWeightCSV_CSVhfDown);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats1, Systematic::Down)] = (*btagWeightCSV_CSVhfstats1Down);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats2, Systematic::Down)] = (*btagWeightCSV_CSVhfstats2Down);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVjes, Systematic::Down)] = (*btagWeightCSV_CSVjesDown);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVlf, Systematic::Down)] = (*btagWeightCSV_CSVlfDown);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats1, Systematic::Down)] = (*btagWeightCSV_CSVlfstats1Down);
        //event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats2, Systematic::Down)] = (*btagWeightCSV_CSVlfstats2Down);

        //event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Down)] = (*puWeightDown);
    }

    if (Systematic::is_jec(syst_id) || Systematic::is_jer(syst_id)) {

        event.mem_DL_0w2h2t_p = this->mem_DL_0w2h2t_p.GetValue(syst_id);
        event.mem_SL_0w2h2t_p = this->mem_SL_0w2h2t_p.GetValue(syst_id);
        event.mem_SL_1w2h2t_p = this->mem_SL_1w2h2t_p.GetValue(syst_id);
        event.mem_SL_2w2h2t_p = this->mem_SL_2w2h2t_p.GetValue(syst_id);
    }
    
    event.genTopHad_pt = *genTopHad_pt;
    event.genTopLep_pt = *genTopLep_pt;

    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Up)] = LHE_weights_scale_wgt[4];
    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Down)] = LHE_weights_scale_wgt[5];
    return event;
}

template <typename T>
EventDescription TreeDescription<T>::create_event(Systematic::SystId syst_id) {
    std::vector<Jet> jets(this->build_jets(syst_id));
    
    EventDescription event;

    event.run = *(this->run);
    event.lumi = *(this->lumi);
    event.evt = *(this->evt);
    event.json = *(this->json);

    event.is_sl = *(this->is_sl);
    event.is_dl = *(this->is_dl);
    event.is_fh = *(this->is_fh);

    event.HLT_ttH_SL_mu = *(this->HLT_ttH_SL_mu);
    event.HLT_ttH_SL_el = *(this->HLT_ttH_SL_el);
    event.HLT_ttH_DL_mumu = *(this->HLT_ttH_DL_mumu);
    event.HLT_ttH_DL_elmu = *(this->HLT_ttH_DL_elmu);
    event.HLT_ttH_DL_elel = *(this->HLT_ttH_DL_elel);
    event.HLT_ttH_FH = *(this->HLT_ttH_FH);
    
    event.numJets = *(this->numJets);
    event.nBCSVM = *(this->nBCSVM);
    event.jets = jets;
    event.syst_id = syst_id;
    event.leptons = build_leptons(syst_id);
    
    event.nPVs = *(this->nPVs);
    
    for (int ilep=0; ilep < *(this->nleps); ilep++) {
        event.leps_superclustereta.push_back(this->leps_scEta[ilep]);
    }

    event.btag_LR_4b_2b_btagCSV = *(this->btag_LR_4b_2b_btagCSV);
    event.mem_DL_0w2h2t_p = *(this->mem_DL_0w2h2t_p);
    event.mem_SL_0w2h2t_p = *(this->mem_SL_0w2h2t_p);
    event.mem_SL_1w2h2t_p = *(this->mem_SL_1w2h2t_p);
    event.mem_SL_2w2h2t_p = *(this->mem_SL_2w2h2t_p);
    event.Wmass = *(this->Wmass);
    event.met_pt = *(this->met_pt);

    event.weights[Systematic::syst_id_nominal] = 1.0;
    return event;
}

template <typename T>
std::vector<Lepton> TreeDescription<T>::build_leptons(Systematic::SystId syst_id) {
    std::vector<Lepton> leps;

    for (int ilep = 0; ilep < *(this->nleps); ilep++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->leps_pt[ilep],
            this->leps_eta[ilep],
            this->leps_phi[ilep],
            this->leps_mass[ilep]
        );
        leps.push_back(Lepton(lv, sgn(this->leps_pdgId[ilep]), this->leps_pdgId[ilep]));
    }
    return leps;
}

template <typename T>
std::vector<Jet> TreeDescription<T>::build_jets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->njets); njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;

        lv.SetPtEtaPhiM(this->jets_pt[njet] * corr/base_corr, this->jets_eta[njet], this->jets_phi[njet], this->jets_mass[njet]);
        Jet jet(lv, this->jets_btagCSV[njet]);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T>
std::vector<Jet> TreeDescriptionMC<T>::build_jets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->njets); njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;
        
        
        //if (Systematic::is_jec(syst_id)) {
        //    auto* correction_branch = get_correction_branch(syst_id);
        //    corr = (*correction_branch)[njet];
        //    base_corr = this->jets_corr_JEC[njet];
        //} else if (Systematic::is_jer(syst_id)) {
        //    auto* correction_branch = get_correction_branch(syst_id);
        //    corr = (*correction_branch)[njet];
        //    base_corr = this->jets_corr_JER[njet];
        //}

        lv.SetPtEtaPhiM(this->jets_pt[njet] * corr/base_corr, this->jets_eta[njet], this->jets_phi[njet], this->jets_mass[njet]);
        Jet jet(lv, this->jets_btagCSV[njet]);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T>
TTreeReaderArray<T>* TreeDescriptionMC<T>::get_correction_branch(Systematic::SystId syst_id) {
    return this->jets_corr.GetValue(syst_id);
}

template class TreeDescription<float>;
template class TreeDescription<double>;

template class TreeDescriptionMC<float>;
template class TreeDescriptionMC<double>;

template class TreeDescriptionMCSystematic<float>;
template class TreeDescriptionMCSystematic<double>;

} //namespace TTH_MEAnalysis
