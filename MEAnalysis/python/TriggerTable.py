'''
Some path for testing from the 2017 menu. Move to config?
'''

triggerTable = {
    "ttH_SL_el" : [
        "HLT_Ele27_WPTight_Gsf",
    ],
    "ttH_SL_mu" : [
        "HLT_IsoMu24",
    ],
#    "ttH_DL_mumu" : [
#        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*",
#        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*",
#        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*",
#        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*",
#    ],
#    "ttH_DL_elmu" : [
#        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
#        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*",
#        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*",
#        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*",
#    ],
#    "ttH_DL_elel" : [
#        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*",
#    ],
    "ttH_FH" : [
        "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0",
        "HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2",
    ],
#    "ttH_FH_prescaled" : [
#        "HLT_PFHT450_SixJet40_v*",
#        "HLT_PFHT400_SixJet30_v*",
#    ],
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
