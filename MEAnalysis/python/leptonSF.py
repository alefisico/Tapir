import ROOT, os, sys
ROOT.gSystem.Load("libTTHMEAnalysis")
import ROOT.TTH_MEAnalysis
dummy = ROOT.TTH_MEAnalysis.TreeDescription
import logging
LOG_MODULE_NAME = logging.getLogger("leptonSF")

tfile_ele_trig = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/ele_trig_sf.root")
hist_ele_trig = tfile_ele_trig.Get("Ele27_WPTight_Gsf")

def calcTriggerSF_el(pt, eta, hist=hist_ele_trig):
    if pt < 25:
        pt = 25
    if pt > 200:
        pt = 199
    b = hist.FindBin(pt, eta)
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("el trig sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_ee_trig = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/triggerSummary_ee_ReReco2016_ttH.root")
hist_ee_trig = tfile_ee_trig.Get("scalefactor_eta2d_with_syst") 
tfile_em_trig = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/triggerSummary_emu_ReReco2016_ttH.root")
hist_em_trig = tfile_em_trig.Get("scalefactor_eta2d_with_syst") 
tfile_mm_trig = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/triggerSummary_mumu_ReReco2016_ttH.root")
hist_mm_trig = tfile_mm_trig.Get("scalefactor_eta2d_with_syst") 

def calcDileptonSF(eta1, eta2, hist):
    b = hist.FindBin(eta1, eta2)
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    return w, wup, wdown

def calcTriggerSF_dilepton(eta1, eta2, hlt_ee, hlt_em, hlt_mm):
    if hlt_ee:
        return calcDileptonSF(eta1, eta2, hist_ee_trig)
    elif hlt_em:
        return calcDileptonSF(eta1, eta2, hist_em_trig)
    elif hlt_mm:
        return calcDileptonSF(eta1, eta2, hist_mm_trig)
    else:
        return (1.0, 1.0, 1.0)

tfile_ele_id = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/el_id_bcdef.root")
hist_ele_id = tfile_ele_id.Get("EGamma_SF2D")

def calcIDSF_el(pt, eta, hist=hist_ele_id):
    if pt > 150:
        pt = 149 
    b = hist.FindBin(eta, pt)
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("el ID sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_ele_reco = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/el_reco.root")
hist_ele_reco = tfile_ele_reco.Get("EGamma_SF2D")
def calcRecoSF_el(pt, eta, hist=hist_ele_reco):
    if pt < 25:
        pt = 25
    if pt > 150:
        pt = 149
    b = hist.FindBin(eta, pt)
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("el reco sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

#https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults#Results_on_the_full_2016_data
tfile_mu_trig1 = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/mu_trig_sf_btof.root")
hist_mu_trig1 = tfile_mu_trig1.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio")

def calcTriggerSF_mu(pt, eta, hist=hist_mu_trig1):
    if pt < 26:
        pt = 26
    if pt > 500:
        pt = 499
    b = hist.FindBin(pt, abs(eta))
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("mu trig sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_mu_id = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/mu_id_bcdef.root")
hist_mu_id = tfile_mu_id.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio")

def calcIDSF_mu(pt, eta, hist=hist_mu_id):
    if pt < 26:
        pt = 26
    if pt > 120:
        pt = 119
    b = hist.FindBin(pt, abs(eta))
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("mu ID sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_mu_iso = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/mu_iso_bcdef.root")
hist_mu_iso = tfile_mu_iso.Get("TightISO_TightID_pt_eta/pt_abseta_ratio")
hist_mu_iso_loose = tfile_mu_iso.Get("LooseISO_TightID_pt_eta/pt_abseta_ratio")

def calcIsoSF_mu(pt, eta, hist=hist_mu_iso):
    if pt < 26:
        pt = 26
    if pt > 120:
        pt = 119
    b = hist.FindBin(pt, abs(eta))
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("mu iso sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_mu_track = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/mu_tracking_bcdef.root")
hist_mu_track = tfile_mu_track.Get("ratio_eff_aeta_dr030e030_corr")

# helper function to find the first occurance of a point whose x-error bars cover a certain value
def findGraphPoint(tgraph, x):
    x_, y_ = ROOT.Double(), ROOT.Double()
    for i in range(0, tgraph.GetN()):
        tgraph.GetPoint(i, x_, y_)
        # use same edge treatment as root histograms use, so inclusive at the left edge
        # and exclusive at the right edge
        l, r = x_ - tgraph.GetErrorXlow(i), x_ + tgraph.GetErrorXhigh(i)
        if float(l) <= x < float(r):
            return i
    return -1

# helper function to get the y-value of a point defined by it's x-value with optional error handling
def getGraphValue(tgraph, x, err="nominal"):
    assert(err in ("nominal", "up", "down"))

    i = findGraphPoint(tgraph, x)
    if i < 0:
        raise Exception("x-value %f cannot be assigned to a valid point" % x)

    x_, y_ = ROOT.Double(), ROOT.Double()
    tgraph.GetPoint(i, x_, y_)
    y = float(y_)

    if err == "up":
        return y + tgraph.GetErrorYhigh(i)
    elif err == "down":
        return y - tgraph.GetErrorYlow(i)
    else:
        return y

def calc_lepton_SF_mu(ev, syst="nominal"):
   
    ilep = 0
    pt = ev.leptons.at(ilep).lv.Pt()
    aeta = abs(ev.leptons.at(ilep).lv.Eta())
   
    w = 1.0
    weights_trigger = calcTriggerSF_mu(pt, aeta)
    if syst == "CMS_effTrigger_mUp":
        w *= weights_trigger[1]
    elif syst == "CMS_effTrigger_mDown":
        w *= weights_trigger[2]
    else:
        w *= weights_trigger[0]

    weights_id = calcIDSF_mu(pt, aeta)
    if syst == "CMS_effID_mUp":
        w *= weights_id[1]
    elif syst == "CMS_effID_mDown":
        w *= weights_id[2]
    else:
        w *= weights_id[0]

    weights_track = getGraphValue(hist_mu_track, aeta), getGraphValue(hist_mu_track, aeta, "up"), getGraphValue(hist_mu_track, aeta, "down")
    if syst == "CMS_effTracking_mUp":
        w *= weights_track[1]
    elif syst == "CMS_effTracking_mDown":
        w *= weights_track[2]
    else:
        w *= weights_track[0]

    weights_iso = calcIsoSF_mu(pt, aeta)
    if syst == "CMS_effIso_mUp":
        w *= weights_iso[1]
    elif syst == "CMS_effIso_mDown":
        w *= weights_iso[2]
    else:
        w *= weights_iso[0]
    
    return w

def calc_lepton_SF_el(ev, syst="nominal"):
   
    ilep = 0
    pt = ev.leptons.at(ilep).lv.Pt()
    eta = ev.leps_superclustereta.at(ilep)

    w = 1.0
    weights_trigger = calcTriggerSF_el(pt, eta)
    if syst == "CMS_effTrigger_eUp":
        w *= weights_trigger[1]
    elif syst == "CMS_effTrigger_eDown":
        w *= weights_trigger[2]
    else:
        w *= weights_trigger[0]

    weights_id = calcIDSF_el(pt, eta)
    if syst == "CMS_effID_eUp":
        w *= weights_id[1]
    elif syst == "CMS_effID_eDown":
        w *= weights_id[2]
    else:
        w *= weights_id[0]

    weights_reco = calcRecoSF_el(pt, eta)
    if syst == "CMS_effReco_eUp":
        w *= weights_reco[1]
    elif syst == "CMS_effReco_eDown":
        w *= weights_reco[2]
    else:
        w *= weights_reco[0]
    return w

def calc_lepton_SF_dilepton(event, syst="nominal"):
    w = 1.0
    
    weights_trigger = calcTriggerSF_dilepton(
        abs(event.leptons.at(0).lv.Eta()),
        abs(event.leptons.at(1).lv.Eta()),
        event.HLT_ttH_DL_elel,
        event.HLT_ttH_DL_elmu,
        event.HLT_ttH_DL_mumu
    )

    if event.HLT_ttH_DL_elel:
        if syst == "CMS_effTrigger_eeUp":
            w *= weights_trigger[1]
        elif syst == "CMS_effTrigger_eeDown":
            w *= weights_trigger[2]
        else:
            w *= weights_trigger[0]
    elif event.HLT_ttH_DL_elmu:
        if syst == "CMS_effTrigger_emUp":
            w *= weights_trigger[1]
        elif syst == "CMS_effTrigger_emDown":
            w *= weights_trigger[2]
        else:
            w *= weights_trigger[0]
    elif event.HLT_ttH_DL_mumu:
        if syst == "CMS_effTrigger_mmUp":
            w *= weights_trigger[1]
        elif syst == "CMS_effTrigger_mmDown":
            w *= weights_trigger[2]
        else:
            w *= weights_trigger[0]
    else:
        w *= weights_trigger[0]
    
    for ilep in range(2):
        pt = event.leptons.at(ilep).lv.Pt()
        if abs(event.leps_pdgId[ilep]) == 11:
            eta = event.leps_superclustereta.at(ilep)
            weights_id = calcIDSF_el(pt, eta)
            if syst == "CMS_effID_eUp":
                w *= weights_id[1]
            elif syst == "CMS_effID_eDown":
                w *= weights_id[2]
            else:
                w *= weights_id[0]

            weights_reco = calcRecoSF_el(pt, eta)
            if syst == "CMS_effReco_eUp":
                w *= weights_reco[1]
            elif syst == "CMS_effReco_eDown":
                w *= weights_reco[2]
            else:
                w *= weights_reco[0]

        elif abs(event.leps_pdgId[ilep]) == 13:
            aeta = abs(event.leptons.at(ilep).lv.Eta())
            weights_id = calcIDSF_mu(pt, aeta)
            if syst == "CMS_effID_mUp":
                w *= weights_id[1]
            elif syst == "CMS_effID_mDown":
                w *= weights_id[2]
            else:
                w *= weights_id[0]

            weights_track = getGraphValue(hist_mu_track, aeta), getGraphValue(hist_mu_track, aeta, "up"), getGraphValue(hist_mu_track, aeta, "down")
            if syst == "CMS_effTracking_mUp":
                w *= weights_track[1]
            elif syst == "CMS_effTracking_mDown":
                w *= weights_track[2]
            else:
                w *= weights_track[0]

            weights_iso = calcIsoSF_mu(pt, aeta, hist_mu_iso_loose)
            if syst == "CMS_effIso_mUp":
                w *= weights_iso[1]
            elif syst == "CMS_effIso_mDown":
                w *= weights_iso[2]
            else:
                w *= weights_iso[0]
    return w

def calc_lepton_SF(event, syst="nominal"):
    if event.is_sl:
        if abs(event.leps_pdgId[0]) == 13:
            w = calc_lepton_SF_mu(event, syst)
        elif abs(event.leps_pdgId[0]) == 11:
            w = calc_lepton_SF_el(event, syst)
    elif event.is_dl:
        w = calc_lepton_SF_dilepton(event, syst)
    return w

from PhysicsTools.HeppyCore.statistics.tree import Tree
if __name__ == "__main__":
    dummy = ROOT.TTH_MEAnalysis.TreeDescription
    
    tf = ROOT.TFile.Open(sys.argv[1])
    events = ROOT.TTH_MEAnalysis.TreeDescriptionMCFloat(
        tf,
        ROOT.TTH_MEAnalysis.SampleDescription(
            ROOT.TTH_MEAnalysis.SampleDescription.MC
        )
    )
    nom = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.Nominal, ROOT.TTH_MEAnalysis.Systematic.None)
   
    
    outfile = ROOT.TFile('out.root', 'recreate')
    tree = Tree('tree', 'MEM tree')
    tree.var('is_sl', the_type=int)
    tree.var('is_dl', the_type=int)
    tree.var('numJets', the_type=int)
    tree.var('nBCSVM', the_type=int)
    tree.var('lep0_pdgId', the_type=int)
    tree.var('lep1_pdgId', the_type=int)
    tree.var('lep0_pt', the_type=float)
    tree.var('lep1_pt', the_type=float)
    tree.var('lep_trigger', the_type=float)
    tree.var('lep_id', the_type=float)
    tree.var('lep_track', the_type=float)
    tree.var('lep_iso', the_type=float)
    tree.var('lep_reco', the_type=float)
    
    iEv = 0
    systs = [
        "nominal",
        "CMS_effTrigger_eUp",
        "CMS_effTrigger_mUp",
        "CMS_effTrigger_eeUp",
        "CMS_effTrigger_emUp",
        "CMS_effTrigger_mmUp",

        "CMS_effID_eUp",
        "CMS_effReco_eUp",

        "CMS_effID_mUp",
        "CMS_effIso_mUp",
        "CMS_effTracking_mUp",
        
        "CMS_effTrigger_eDown",
        "CMS_effTrigger_mDown",
        "CMS_effTrigger_eeDown",
        "CMS_effTrigger_emDown",
        "CMS_effTrigger_mmDown",

        "CMS_effID_eDown",
        "CMS_effReco_eDown",

        "CMS_effID_mDown",
        "CMS_effIso_mDown",
        "CMS_effTracking_mDown",
    ]

    for syst in systs:
        tree.var('lep_weight_'+syst, the_type=float)

    while events.reader.Next():
        print iEv
        event = events.create_event(nom)
        event.leps_pdgId = [x.pdgId for x in event.leptons]

        w_trigger = 1.0
        w_id = 1.0
        w_track = 1.0
        w_iso = 1.0
        w_reco = 1.0
        lep0_pdgId = 0
        lep1_pdgId = 0
        lep0_pt = 0
        lep1_pt = 0
        
        for syst in systs:
            tree.fill('lep_weight_' + syst, 0)

        if event.is_sl or event.is_dl:
            if event.is_sl:
                lep0_pdgId = event.leps_pdgId[0]
                lep0_pt = event.leptons.at(0).lv.Pt()
            elif event.is_dl:
                lep0_pdgId = event.leps_pdgId[0]
                lep0_pt = event.leptons.at(0).lv.Pt()
                lep1_pdgId = event.leps_pdgId[1]
                lep1_pt = event.leptons.at(1).lv.Pt()

            for syst in systs:
                w = calc_lepton_SF(event, syst)
                tree.fill('lep_weight_' + syst, w)

        tree.fill('is_sl', event.is_sl)
        tree.fill('is_dl', event.is_dl)
        tree.fill('numJets', event.numJets)
        tree.fill('nBCSVM', event.nBCSVM)
        tree.fill('lep0_pdgId', lep0_pdgId)
        tree.fill('lep1_pdgId', lep1_pdgId)
        tree.fill('lep0_pt', lep0_pt)
        tree.fill('lep1_pt', lep1_pt)
        tree.tree.Fill()
        iEv += 1

    outfile.Write()
    outfile.Close()
