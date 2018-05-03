'''
Trigger defintions:

Set different trigger configurations containing one or more HLT paths. If more than on is given 
for a configuration the or of all is used.

Possibility to define dataset sprecific configurations. Define configuration with name [ttH_configname]
that is used as default. For dataset specific variatitions add element to dict with [ttH_configname]:[datasetname].
The [datasetname] sould be true for the comparison of [datasetname] in cfg_comp.name (the name set in e.g. in 
default.cfg). For this dataset the default configuration will be replaced.
'''

triggerTable = {
    "ttH_SL_el" : [
        "HLT_Ele35_WPTight_Gsf",
        "HLT_Ele28_eta2p1_WPTight_Gsf_HT150",
    ],
    "ttH_SL_mu" : [
        "HLT_IsoMu24_eta2p1",
        "HLT_IsoMu27",
    ],
    "ttH_DL_mumu" : [
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
    ],
    "ttH_DL_elmu" : [
        "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
    "ttH_DL_elel" : [
        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
   "ttH_FH" : [
       "HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5",
       "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0",
       "HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2",
   ],
   "ttH_FH:JetHT" : [
       "HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5",
       "HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2",
       ("and not","HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0")
   ],
   "ttH_FH:BTagCSV" : [
       "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0"
   ],
#   "ttH_FH_prescaled" : [
#       "HLT_PFHT450_SixJet40_v",
#       "HLT_PFHT400_SixJet30_v",
#   ],
}



'''
ttH paths from https://github.com/jpata/cmssw/blob/vhbbHeppy80X_july31/VHbbAnalysis/Heppy/python/TriggerTable.py#L218-L247
'''

triggerTable2016 = {

    "ttH_SL_el" : [
        "HLT_Ele27_WPTight_Gsf",
    ],
    "ttH_SL_mu" : [
        "HLT_IsoMu24",
        "HLT_IsoTkMu24",
    ],
    "ttH_DL_mumu" : [
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",
        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",
    ],
    "ttH_DL_elmu" : [
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
#Disabled as not there in nanoAOD for data
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
    "ttH_DL_elel" : [
        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
    "ttH_FH" : [
        "HLT_PFHT450_SixJet40_BTagCSV_p056",
        "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056",
    ],
    "ttH_FH_prescaled" : [
        "HLT_PFHT450_SixJet40",
        "HLT_PFHT400_SixJet30",
    ],

}
