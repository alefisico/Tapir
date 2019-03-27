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
    //event.ttCls = *ttCls;
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
EventDescription TreeDescriptionMCBOOSTED<T>::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescriptionMC<T>::create_event(syst_id);

    event.n_boosted_bjets = n_boosted_bjets.GetValue(syst_id);
    event.n_boosted_ljets = n_boosted_ljets.GetValue(syst_id);
    event.boosted = boosted.GetValue(syst_id);

    event.higgsCandidate = build_higgsCandidate(syst_id);
    event.topCandidate = build_topCandidate(syst_id);


    if (Systematic::is_nominal(syst_id) || Systematic::is_jec(syst_id) || Systematic::is_jer(syst_id)) {
        event.mem_DL_0w2h2t_sj_p = this->mem_DL_0w2h2t_sj_p.GetValue(syst_id);
        event.mem_SL_0w2h2t_sj_p = this->mem_SL_0w2h2t_sj_p.GetValue(syst_id);
        event.mem_SL_1w2h2t_sj_p = this->mem_SL_1w2h2t_sj_p.GetValue(syst_id);
        event.mem_SL_2w2h2t_sj_p = this->mem_SL_2w2h2t_sj_p.GetValue(syst_id);
    }
    
    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Up)] = LHE_weights_scale_wgt[4];
    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Down)] = LHE_weights_scale_wgt[5];
    return event;
}

template <typename T>
EventDescription TreeDescriptionMC<T>::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescription<T>::create_event(syst_id);

    for (auto njet=0; njet < *(this->njets); njet++) {
        event.jets_hadronFlavour.push_back(this->jets_hadronFlavour[njet]);
    }

    //event.ttCls = *ttCls;
    event.numJets = numJets.GetValue(syst_id);
    event.nBDeepCSVM = nBDeepCSVM.GetValue(syst_id);
    event.nBCSVM = nBCSVM.GetValue(syst_id);

    event.weights[std::make_pair(Systematic::gen, Systematic::None)] = (*genWeight);
    event.weights[std::make_pair(Systematic::CMS_ttH_CSV, Systematic::None)] = (*btagWeight_shape);
    event.weights[std::make_pair(Systematic::CMS_pu, Systematic::None)] = (*puWeight);

    if (Systematic::is_nominal(syst_id)) {

        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Up)] = (*btagWeight_shape_cferr1Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr2, Systematic::Up)] = (*btagWeight_shape_cferr2Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhf, Systematic::Up)] = (*btagWeight_shape_hfUp);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats1, Systematic::Up)] = (*btagWeight_shape_hfstats1Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats2, Systematic::Up)] = (*btagWeight_shape_hfstats2Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVjes, Systematic::Up)] = (*btagWeight_shape_jesUp);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlf, Systematic::Up)] = (*btagWeight_shape_lfUp);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats1, Systematic::Up)] = (*btagWeight_shape_lfstats1Up);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats2, Systematic::Up)] = (*btagWeight_shape_lfstats2Up);

        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr1, Systematic::Down)] = (*btagWeight_shape_cferr1Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVcferr2, Systematic::Down)] = (*btagWeight_shape_cferr2Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhf, Systematic::Down)] = (*btagWeight_shape_hfDown);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats1, Systematic::Down)] = (*btagWeight_shape_hfstats1Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVhfstats2, Systematic::Down)] = (*btagWeight_shape_hfstats2Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVjes, Systematic::Down)] = (*btagWeight_shape_jesDown);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlf, Systematic::Down)] = (*btagWeight_shape_lfDown);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats1, Systematic::Down)] = (*btagWeight_shape_lfstats1Down);
        event.weights[std::make_pair(Systematic::CMS_ttH_CSVlfstats2, Systematic::Down)] = (*btagWeight_shape_lfstats2Down);
        
        event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Up)] = (*puWeightUp);
        event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Down)] = (*puWeightDown);
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
    event.event = *(this->event);
    event.json = *(this->json);

    event.is_sl = *(this->is_sl);
    event.is_dl = *(this->is_dl);
    event.is_fh = *(this->is_fh);

    event.HLT_ttH_SL_mu = *(this->HLT_ttH_SL_mu);
    event.HLT_ttH_SL_el = *(this->HLT_ttH_SL_el);
    event.HLT_ttH_DL_mumu = *(this->HLT_ttH_DL_mumu);
    event.HLT_ttH_DL_elmu = *(this->HLT_ttH_DL_elmu);
    event.HLT_ttH_DL_elel = *(this->HLT_ttH_DL_elel);
    //disabled in May1-2 
    //event.HLT_ttH_FH = *(this->HLT_ttH_FH);
    event.HLT_ttH_FH = 1;
    
    event.numJets = *(this->numJets);
    event.nBDeepCSVM = *(this->nBDeepCSVM);
    event.nBCSVM = *(this->nBCSVM);
    event.ttCls = *(this->ttCls);
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
EventDescription TreeDescriptionBOOSTED<T>::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescription<T>::create_event(syst_id);

    event.n_boosted_bjets = *(this->n_boosted_bjets);
    event.n_boosted_ljets = *(this->n_boosted_ljets);
    event.boosted = *(this->boosted);

    event.higgsCandidate = build_higgsCandidate(syst_id);
    event.topCandidate = build_topCandidate(syst_id);

    event.mem_DL_0w2h2t_sj_p = *(this->mem_DL_0w2h2t_sj_p);
    event.mem_SL_0w2h2t_sj_p = *(this->mem_SL_0w2h2t_sj_p);
    event.mem_SL_1w2h2t_sj_p = *(this->mem_SL_1w2h2t_sj_p);
    event.mem_SL_2w2h2t_sj_p = *(this->mem_SL_2w2h2t_sj_p);

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
std::vector<higgsCandidates> TreeDescriptionBOOSTED<T>::build_higgsCandidate(Systematic::SystId syst_id) {
    std::vector<higgsCandidates> hc;

    for (int ih = 0; ih < *(this->nhiggsCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->higgsCandidate_pt[ih],
            this->higgsCandidate_eta[ih],
            this->higgsCandidate_phi[ih],
            this->higgsCandidate_mass[ih]
        );

        float m_softdrop = this->higgsCandidate_msoftdrop[ih];
        float tau21 = this->higgsCandidate_tau21[ih];
        float bbtag = this->higgsCandidate_bbtag[ih];
        float sj1btag = this->higgsCandidate_sj1btag[ih];
        float sj2btag = this->higgsCandidate_sj2btag[ih];
        float sj1pt = this->higgsCandidate_sj1pt[ih];
        float sj2pt = this->higgsCandidate_sj2pt[ih];
        hc.push_back(higgsCandidates(lv, m_softdrop,tau21,bbtag,sj1btag,sj2btag,sj1pt,sj2pt));
    }
    return hc;
}

template <typename T>
std::vector<topCandidates> TreeDescriptionBOOSTED<T>::build_topCandidate(Systematic::SystId syst_id) {
    std::vector<topCandidates> hc;

    for (int ih = 0; ih < *(this->ntopCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->topCandidate_pt[ih],
            this->topCandidate_eta[ih],
            this->topCandidate_phi[ih],
            this->topCandidate_mass[ih]
        );

        float tau32SD = this->topCandidate_tau32SD[ih];
        float fRec = this->topCandidate_fRec[ih];
        float delRopt = this->topCandidate_delRopt[ih];
        float sj1btag = this->topCandidate_sj1btag[ih];
        float sj2btag = this->topCandidate_sj2btag[ih];
        float sj3btag = this->topCandidate_sj3btag[ih];
        float sj1pt = this->topCandidate_sj1pt[ih];
        float sj2pt = this->topCandidate_sj2pt[ih];
        float sj3pt = this->topCandidate_sj3pt[ih];
        hc.push_back(topCandidates(lv, tau32SD,fRec,delRopt,sj1btag,sj2btag,sj3btag,sj1pt,sj2pt,sj3pt));
    }
    return hc;
}

template <typename T>
std::vector<higgsCandidates> TreeDescriptionMCBOOSTED<T>::build_higgsCandidate(Systematic::SystId syst_id) {
    std::vector<higgsCandidates> hc;

    for (int ih = 0; ih < *(this->nhiggsCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->higgsCandidate_pt[ih],
            this->higgsCandidate_eta[ih],
            this->higgsCandidate_phi[ih],
            this->higgsCandidate_mass[ih]
        );

        float m_softdrop = this->higgsCandidate_msoftdrop[ih];
        float tau21 = this->higgsCandidate_tau21[ih];
        float bbtag = this->higgsCandidate_bbtag[ih];
        float sj1btag = this->higgsCandidate_sj1btag[ih];
        float sj2btag = this->higgsCandidate_sj2btag[ih];
        float sj1pt = this->higgsCandidate_sj1pt[ih];
        float sj2pt = this->higgsCandidate_sj2pt[ih];
        hc.push_back(higgsCandidates(lv, m_softdrop,tau21,bbtag,sj1btag,sj2btag,sj1pt,sj2pt));
    }
    return hc;
}

template <typename T>
std::vector<topCandidates> TreeDescriptionMCBOOSTED<T>::build_topCandidate(Systematic::SystId syst_id) {
    std::vector<topCandidates> hc;

    for (int ih = 0; ih < *(this->ntopCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->topCandidate_pt[ih],
            this->topCandidate_eta[ih],
            this->topCandidate_phi[ih],
            this->topCandidate_mass[ih]
        );

        float tau32SD = this->topCandidate_tau32SD[ih];
        float fRec = this->topCandidate_fRec[ih];
        float delRopt = this->topCandidate_delRopt[ih];
        float sj1btag = this->topCandidate_sj1btag[ih];
        float sj2btag = this->topCandidate_sj2btag[ih];
        float sj3btag = this->topCandidate_sj3btag[ih];
        float sj1pt = this->topCandidate_sj1pt[ih];
        float sj2pt = this->topCandidate_sj2pt[ih];
        float sj3pt = this->topCandidate_sj3pt[ih];
        hc.push_back(topCandidates(lv, tau32SD,fRec,delRopt,sj1btag,sj2btag,sj3btag,sj1pt,sj2pt,sj3pt));
    }
    return hc;
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

        double pt = this->jets_pt[njet];
        if (Systematic::is_jec(syst_id) || Systematic::is_jer(syst_id)) {
            pt = (*get_correction_branch(syst_id))[njet];
        }

        lv.SetPtEtaPhiM(pt, this->jets_eta[njet], this->jets_phi[njet], this->jets_mass[njet]);
        Jet jet(lv, this->jets_btagCSV[njet]);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T>
TTreeReaderArray<T>* TreeDescriptionMC<T>::get_correction_branch(Systematic::SystId syst_id) {
    return this->jets_pt_corr.GetValue(syst_id);
}

template class TreeDescription<float>;
template class TreeDescription<double>;

template class TreeDescriptionMC<float>;
template class TreeDescriptionMC<double>;

template class TreeDescriptionMCSystematic<float>;
template class TreeDescriptionMCSystematic<double>;

template class TreeDescriptionMCBOOSTED<float>;
template class TreeDescriptionMCBOOSTED<double>;

template class TreeDescriptionBOOSTED<float>;
template class TreeDescriptionBOOSTED<double>;

} //namespace TTH_MEAnalysis
