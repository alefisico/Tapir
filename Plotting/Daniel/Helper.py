import ROOT
import collections

luminosity = 41.29
lumi_Trigger = 35.336

topPTrewt = "exp(0.5*(Sum$(0.0843616-0.000743051*genTopLep_pt)+Sum$(0.0843616-0.000743051*genTopHad_pt)))"
topPTrewtUp = "exp(0.5*(Sum$(0.00160296-0.000411375*genTopLep_pt)+Sum$(0.00160296-0.000411375*genTopHad_pt)))"
topPTrewtDown = "exp(0.5*(Sum$(0.16712-0.00107473*genTopLep_pt)+Sum$(0.16712-0.00107473*genTopHad_pt)))"

colors = { "ddQCD": 9007, "qcd": 9007,
           "ttH_hbb": 9001, "ttH": 9001, "total_signal":9001,
           "ttbarPlusBBbar": 9002,
           "ttbarPlus2B": 9003,
           "ttbarPlusB" : 9004, "ttb":9004,
           "ttbarPlusCCbar": 9005,
           "ttbarOther": 9006,
           "ttH_nonhbb": 9008, "ttH_hcc": 9008, "ttH_hww": 9008, "ttH_hzz": 9008, "ttH_htt": 9008, "ttH_hgg": 9008, "ttH_hgluglu": 9008, "ttH_hzg": 9008,
           "wjets": 9009, "vjets":9009,
           "zjets":9010,
           "diboson":9011, "EWK":9011,
           "stop":9012,
           "ttv":9013, "ttw":9013, "ttz":9013, "tOther":9013,
           "JetHT": 1,
           "TTbar_inc": ROOT.kRed+2,
           "Minor": ROOT.kAzure+8}
#histogram colors (index, r, b, g)
col_tth     = ROOT.TColor(colors["ttH_hbb"], 44/255., 62/255., 167/255.)
col_qcd     = ROOT.TColor(colors["ddQCD"], 102/255., 201/255., 77/255.)
col_ttbarBB = ROOT.TColor(colors["ttbarPlusBBbar"], 102/255., 0/255., 0/255.)
col_ttbar2B = ROOT.TColor(colors["ttbarPlus2B"], 80/255., 0/255., 0/255.)
col_ttbarB  = ROOT.TColor(colors["ttbarPlusB"], 153/255., 51/255., 51/255.)
col_ttbarCC = ROOT.TColor(colors["ttbarPlusCCbar"], 204/255., 2/255., 0/255.) 
col_ttbarJJ = ROOT.TColor(colors["ttbarOther"], 251/255., 102/255., 102/255.)
col_tthnon  = ROOT.TColor(colors["ttH_nonhbb"], 90/255., 115/255., 203/255.)
col_wjets   = ROOT.TColor(colors["wjets"], 254/255., 195/255., 8/255.)
col_zjets   = ROOT.TColor(colors["zjets"], 191/255., 193/255., 222/255.)
col_diboson = ROOT.TColor(colors["diboson"], 229/255., 198/255., 218/255.)
col_stop    = ROOT.TColor(colors["stop"], 235/255., 73/255., 247/255.)
col_ttv     = ROOT.TColor(colors["ttv"], 246/255., 236/255., 145/255.)

legnames = { "ddQCD": "Multijet",
             "qcd": "Multijet",
             "ttH_hbb": "t#bar{t}H(bb)",
             "ttH": "t#bar{t}H",
             "total_signal": "t#bar{t}H",
             "ttH_nonhbb": "t#bar{t}H(non)",
             "ttbarPlusBBbar": "t#bar{t}+b#bar{b}",
             "ttbarPlus2B": "t#bar{t}+2b",
             "ttbarPlusB" : "t#bar{t}+b",
             "ttb": "t#bar{t}+b#bar{b}",
             "ttbarPlusCCbar": "t#bar{t}+c#bar{c}",
             "ttbarOther": "t#bar{t}+lf",
             "wjets": "W+jets",
             "zjets": "Z+jets",
             "vjets": "V+jets",
             "diboson": "Diboson",
             "EWK":"EWK",
             "stop": "Single t",
             "ttv": "t#bar{t}+V",
             "ttz": "t#bar{t}+V",
             "tOther":"Other t",
             "JetHT": "Data",
             "TTbar_inc": "t#bar{t}+jets"}

datasets = collections.OrderedDict([
    ("JetHT","JetHT"),
    ("SingleMuon","SingleMuon"),
    ("ttH_hbb","ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"),
    ("ttH_nonhbb","ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"),
    ("TTbar_inc","TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"),
    ("QCD300","QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD500","QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD700","QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD1000","QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD1500","QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD2000","QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("ww","WW_TuneCUETP8M1_13TeV-pythia8"),
    ("wz","WZ_TuneCUETP8M1_13TeV-pythia8"),
    ("zz","ZZ_TuneCUETP8M1_13TeV-pythia8"),
    ("st_t","ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin"),
    ("stbar_t","ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin"),
    ("st_s_inc","ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8"),
    ("st_tw","ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4"),
    ("stbar_tw","ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4"),
    ("ttw_wqq","TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"),
    ("ttz_zqq","TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8"),
    ("WJetsToQQ600","WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("WJetsToQQ180","WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8"),
    ("WJetsToQQ180_gencut","WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8"), #gencut, lheHT>400
    ("ZJetsToQQ600","ZJetsToQQ_HT600toInf_13TeV-madgraph"),
    ("WWTo4Q","WWTo4Q_13TeV-powheg"),
    ("ZZTo4Q","ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8"),
    ("st_s_lep","ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"),
    ("ttw_wlnu","TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"),
    ("ttz_zllnunu","TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8"),
    ("wjets100","WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("wjets200","WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("wjets400","WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("wjets600","WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("wjets800","WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("wjets1200","WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("wjets2500","WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m5_100","DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m5_200","DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m5_400","DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m5_600","DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m50_100","DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m50_200","DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m50_400","DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m50_600","DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m50_800","DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m50_1200","DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("zjets_m50_2500","DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")
    ])

xsecs = { "ttH_hbb": 0.29533504, #0.2934045,
    "ttH_nonhbb": 0.21176496, #0.2150955,
    "TTbar_inc": 831.76,
    "QCD300": 351300.0, #+- 1682
    "QCD500": 31630.0, #+- 937
    "QCD700": 6802.0, #+- 43
    "QCD1000": 1206.0, #+- 6,5
    "QCD1500": 0.9*120.4, #+- 0.64 #TEMP
    "QCD2000": 0.9*25.25, #+- 0.15 #TEMP
    "ww": 118.7,
    "wz": 47.13,
    "zz": 16.523,
    "st_t": 136.02,
    "stbar_t": 80.95,
    "st_s_inc": 10.32,
    "st_tw": 35.85,
    "stbar_tw": 35.85,
    "ttw_wqq": 0.4062,
    "ttz_zqq": 0.5297,
    "WJetsToQQ600": 95.14,
    "WJetsToQQ180": 2788,
    "WJetsToQQ180_gencut": 343.05, #gencut, lheHT>400
    "ZJetsToQQ600": 5.67,
    "WWTo4Q": 51.723,
    "ZZTo4Q": 7.487,
    "st_s_lep": 3.702,
    "ttw_wlnu": 0.2043,
    "ttz_zllnunu": 0.2529,
    "wjets100": 1345,
    "wjets200": 359.7,
    "wjets400": 48.91,
    "wjets600": 12.05,
    "wjets800": 5.501,
    "wjets1200": 1.329,
    "wjets2500": 0.03216,
    "zjets_m5_100": 224.2,
    "zjets_m5_200": 37.2,
    "zjets_m5_400": 3.581,
    "zjets_m5_600": 1.124,
    "zjets_m50_100": 147.4,
    "zjets_m50_200": 40.99,
    "zjets_m50_400": 5.678,
    "zjets_m50_600": 1.367,
    "zjets_m50_800": 0.6304,
    "zjets_m50_1200": 0.1514,
    "zjets_m50_2500": 0.003565
    }

nGen = { "ttH_hbb": 3737487,
         "ttH_nonhbb": 3873929,
         "TTbar_inc": 76972929,
         "QCD300": 54500812,
         "QCD500": 62178097,
         "QCD700": 45018815,
         "QCD1000": 15112403,
         "QCD1500": 3970702,
         "QCD2000": 1979791,
         "ww": 7981534,
         "wz": 3995503,
         "zz": 1988503,
         "st_t": 5993152,
         "stbar_t": 3928406,
         "st_s_inc": 1872411,
         "st_tw": 991587,
         "stbar_tw": 998630,
         "ttw_wqq": 428932,
         "ttz_zqq": 346702,
         "WJetsToQQ600": 1026513,
         "WJetsToQQ180": 22370989,
         "WJetsToQQ180_gencut": 2749933,
         "ZJetsToQQ600": 996052,
         "WWTo4Q": 1997858,
         "ZZTo4Q": 3170864,
         "st_s_lep": 591362,
         "ttw_wlnu": 2713793,
         "ttz_zllnunu": 3710207,
         "wjets100": 68636273,
         "wjets200": 34646997,
         "wjets400": 7759448,
         "wjets600": 14782163,
         "wjets800": 6174210,
         "wjets1200": 6615199,
         "wjets2500": 2384767,
         "zjets_m5_100": 8583409,
         "zjets_m5_200": 2066660,
         "zjets_m5_400": 2065540,
         "zjets_m5_600": 2006840,
         "zjets_m50_100": 2981058, #partial ~35%
         "zjets_m50_200": 8486735,
         "zjets_m50_400": 2330322, #partial ~25%
         "zjets_m50_600": 8239835,
         "zjets_m50_800": 2249549, #partial ~80%
         "zjets_m50_1200": 593783,
         "zjets_m50_2500": 399753
         }

qgWtFac = { "ttH_hbb": 0.954,
            "ttH_nonhbb": 0.938,
            "ttH_hcc": 0.955,
            "ttH_hgg": 0.818,
            "ttH_hzz": 0.944,
            "ttH_hgluglu": 0.992,
            "ttH_hww": 0.930,
            "ttH_hss": 0.908,
            "ttH_hmm": 1.033,
            "ttH_htt": 0.858,
            "ttH_hzg": 0.867,
            "TTbar_inc": 0.912,
            "ttbarPlusBBbar": 0.940,
            "ttbarPlusCCbar": 0.931,
            "ttbarPlus2B": 0.928,
            "ttbarPlusB": 0.927,
            "ttbarOther": 0.902,
            "QCD300": 0.966,
            "QCD500": 1.000,
            "QCD700": 1.002,
            "QCD1000": 0.979,
            "QCD1500": 0.931,
            "QCD2000": 0.924,
            "ww": 0.871,
            "wz": 0.913,
            "zz": 0.896,
            "st_t": 0.912,
            "stbar_t": 0.910,
            "st_s_inc": 0.914,
            "st_tw": 0.873,
            "stbar_tw": 0.882,
            "ttw_wqq": 0.894,
            "ttz_zqq": 0.916,
            "WJetsToQQ600": 0.902,
            "WJetsToQQ180": 0.891,
            "WJetsToQQ180_gencut": 0.892, #gencut, lheHT>400
            "ZJetsToQQ600": 0.949,
            "WWTo4Q": 0.902,
            "ZZTo4Q": 0.910,
            "st_s_lep": 1,
            "ttw_wlnu": 1,
            "ttz_zllnunu": 1,
            "wjets100": 1,
            "wjets200": 1,
            "wjets400": 1,
            "wjets600": 1,
            "wjets800": 1,
            "wjets1200": 1,
            "wjets2500": 1,
            "zjets_m5_100": 1,
            "zjets_m5_200": 1,
            "zjets_m5_400": 1,
            "zjets_m5_600": 1,
            "zjets_m50_100": 1,
            "zjets_m50_200": 1,
            "zjets_m50_400": 1,
            "zjets_m50_600": 1,
            "zjets_m50_800": 1,
            "zjets_m50_1200": 1,
            "zjets_m50_2500": 1
            }

qgWtFacSL = {"ttH_hbb": 0.982,
             "TTbar_inc": 0.953,
             "ttbarPlusBBbar": 0.977,
             "ttbarPlusCCbar": 0.970,
             "ttbarPlus2B": 0.970,
             "ttbarPlusB": 0.969,
             "ttbarOther": 0.948,
             "QCD300": 0.602,
             "QCD500": 0.944,
             "QCD700": 0.908,
             "QCD1000": 1.071,
             "QCD1500": 0.934,
             "QCD2000": 1.031,
             "ww": 0.909,
             "wz": 0.928,
             "zz": 0.920,
             "st_t": 0.948,
             "stbar_t": 0.948,
             "st_s_inc": 0.961,
             "st_tw": 0.947,
             "stbar_tw": 0.946,
             "ttw_wqq": 0.941,
             "ttz_zqq": 0.958,
             "WJetsToQQ180": 0.958,
             "WJetsToQQ180_gencut": 0.958,
             "ZJetsToQQ600": 1.033,
             "st_s_lep": 0.961,
             "ttw_wlnu": 0.936,
             "ttz_zllnunu": 0.946,
             "wjets100": 0.936,
             "wjets200": 0.941,
             "wjets400": 0.934,
             "wjets600": 0.930,
             "wjets800": 0.920,
             "wjets1200": 0.892,
             "wjets2500": 0.833,
             "zjets_m5_100": 0.952,
             "zjets_m5_200": 0.948,
             "zjets_m5_400": 0.933,
             "zjets_m5_600": 0.940,
             "zjets_m50_100": 0.906,
             "zjets_m50_200": 0.917,
             "zjets_m50_400": 0.911,
             "zjets_m50_600": 0.903,
             "zjets_m50_800": 0.904,
             "zjets_m50_1200": 0.879,
             "zjets_m50_2500": 0.825,
             }

qgWtFacSL5j = {"ttH_hbb": 0.977,
               "TTbar_inc": 0.941,
               "ttbarPlusBBbar": 0.970,
               "ttbarPlusCCbar": 0.961,
               "ttbarPlus2B": 0.959,
               "ttbarPlusB": 0.958,
               "ttbarOther": 0.933,
               "QCD300": 0.513,
               "QCD500": 0.952,
               "QCD700": 0.995,
               "QCD1000": 1.076,
               "QCD1500": 0.982,
               "QCD2000": 1.031,
               "ww": 0.858,
               "wz": 0.918,
               "zz": 0.968,
               "st_t": 0.928,
               "stbar_t": 0.945,
               "st_s_inc": 0.952,
               "st_tw": 0.936,
               "stbar_tw": 0.928,
               "ttw_wqq": 0.931,
               "ttz_zqq": 0.948,
               "WJetsToQQ180": 0.958,
               "WJetsToQQ180_gencut": 0.958,
               "ZJetsToQQ600": 1.033,
               "st_s_lep": 0.968,
               "ttw_wlnu": 0.923,
               "ttz_zllnunu": 0.931,
               "wjets100": 0.931,
               "wjets200": 0.924,
               "wjets400": 0.928,
               "wjets600": 0.930,
               "wjets800": 0.922,
               "wjets1200": 0.899,
               "wjets2500": 0.833,
               "zjets_m5_100": 0.878,
               "zjets_m5_200": 0.935,
               "zjets_m5_400": 0.927,
               "zjets_m5_600": 0.954,
               "zjets_m50_100": 0.985,
               "zjets_m50_200": 0.904,
               "zjets_m50_400": 0.901,
               "zjets_m50_600": 0.899,
               "zjets_m50_800": 0.894,
               "zjets_m50_1200": 0.884,
               "zjets_m50_2500": 0.827,
               }

qgWtFacSL6j = {"ttH_hbb": 0.970,
               "TTbar_inc": 0.934,
               "ttbarPlusBBbar": 0.966,
               "ttbarPlusCCbar": 0.952,
               "ttbarPlus2B": 0.949,
               "ttbarPlusB": 0.948,
               "ttbarOther": 0.923,
               "QCD300": 0.400,
               "QCD500": 1.004,
               "QCD700": 0.963,
               "QCD1000": 1.321,
               "QCD1500": 0.987,
               "QCD2000": 1.031,
               "ww": 0.803,
               "wz": 0.814,
               "zz": 0.777,
               "st_t": 0.896,
               "stbar_t": 0.958,
               "st_s_inc": 0.961,
               "st_tw": 0.935,
               "stbar_tw": 0.908,
               "ttw_wqq": 0.915,
               "ttz_zqq": 0.937,
               "WJetsToQQ180": 1,
               "WJetsToQQ180_gencut": 1,
               "ZJetsToQQ600": 1.034,
               "st_s_lep": 0.941,
               "ttw_wlnu": 0.909,
               "ttz_zllnunu": 0.919,
               "wjets100": 1.041,
               "wjets200": 0.910,
               "wjets400": 0.918,
               "wjets600": 0.937,
               "wjets800": 0.917,
               "wjets1200": 0.900,
               "wjets2500": 0.839,
               "zjets_m5_100": 1,
               "zjets_m5_200": 1.046,
               "zjets_m5_400": 0.879,
               "zjets_m5_600": 0.926,
               "zjets_m50_100": 1.601,
               "zjets_m50_200": 0.941,
               "zjets_m50_400": 0.867,
               "zjets_m50_600": 0.892,
               "zjets_m50_800": 0.905,
               "zjets_m50_1200": 0.890,
               "zjets_m50_2500": 0.812,
               }

preselection = "json && (HLT_ttH_FH || HLT_BIT_HLT_PFJet450_v) && ht>500 && jets_pt[5]>40"
preselSL = "json && (HLT_BIT_HLT_IsoMu24_v || HLT_BIT_HLT_IsoTkMu24_v) && Sum$(abs(leps_pdgId)==13)==1 && leps_pt[0]>26 && numJets>=4"

def get_cuts(systematic=""):
    cuts = {"6j":"numJets{0}==6".format(systematic),
            "ge6j":"numJets{0}>=6".format(systematic),
            "ge7j":"numJets{0}>=7 && Wmass{0}>60 && Wmass{0}<100".format(systematic),
            "7j":"numJets{0}==7 && Wmass{0}>60 && Wmass{0}<100".format(systematic),
            "8j":"numJets{0}==8 && Wmass{0}>60 && Wmass{0}<100".format(systematic),
            "9j":"numJets{0}>=9 && Wmass{0}>70 && Wmass{0}<92".format(systematic),
            "3bSR":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.5".format(systematic),
            "4bSR":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.5".format(systematic),
            "3bCR":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.5".format(systematic),
            "4bCR":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.5".format(systematic),
            "3bVR":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bVR":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.5".format(systematic),
            "3bCR2":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bCR2":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.5".format(systematic),

            "3bSRx":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==3 && qg_LR_3b_flavour_5q_0q>0.5",
            "4bSRx":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)>=4 && qg_LR_4b_flavour_5q_0q>0.5",
            "3bCRx":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_3b_flavour_5q_0q>0.5",
            "4bCRx":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_4b_flavour_5q_0q>0.5",
            "3bVRx":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==3 && qg_LR_3b_flavour_5q_0q<0.5",
            "4bVRx":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)>=4 && qg_LR_4b_flavour_5q_0q<0.5",
            "3bCR2x":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_3b_flavour_5q_0q<0.5",
            "4bCR2x":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_4b_flavour_5q_0q<0.5",

            "3bSRy":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bSRy":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "3bCRy":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bCRy":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "3bVRy":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.3".format(systematic),
            "4bVRy":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.3".format(systematic),
            "3bCR2y":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.3".format(systematic),
            "4bCR2y":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.3".format(systematic),

            "2bPresel":"nBCSVM>=2",
            "3bPresel":"nBCSVM>=2",
            "4bPresel":"nBCSVM>=2",
            "ge4j":"numJets>=4",
            "ge5j":"numJets>=5",

}
    return cuts

ttCuts = {"ttbarPlusBBbar": "ttCls>52",
          "ttbarPlus2B": "ttCls==52",
          "ttbarPlusB": "ttCls==51",
          "ttbarPlusCCbar": "ttCls>40 && ttCls<46",
          "ttbarOther": "ttCls<40"}

ttHcuts = { "ttH_hcc": "genHiggsDecayMode==4", 
            "ttH_hww": "genHiggsDecayMode==24",
            "ttH_hzz": "genHiggsDecayMode==23",
            "ttH_htt": "genHiggsDecayMode==15",
            "ttH_hgg": "genHiggsDecayMode==22",
            "ttH_hgluglu": "genHiggsDecayMode==21",
            "ttH_hzg": "genHiggsDecayMode==230022",
            "ttH_hss": "genHiggsDecayMode==3",
            "ttH_hmm": "genHiggsDecayMode==13"}

systematics = ["CMS_res_j",
               #"CMS_scale_j",
               "CMS_scaleAbsoluteStat_j",
               "CMS_scaleAbsoluteScale_j",
               ###"CMS_scaleAbsoluteFlavMap_j", #obsolete (1 anyway)
               "CMS_scaleAbsoluteMPFBias_j",
               "CMS_scaleFragmentation_j",
               "CMS_scaleSinglePionECAL_j",
               "CMS_scaleSinglePionHCAL_j",
               "CMS_scaleFlavorQCD_j",
               "CMS_scaleTimePtEta_j",
               "CMS_scaleRelativeJEREC1_j",
               "CMS_scaleRelativeJEREC2_j",
               "CMS_scaleRelativeJERHF_j",
               "CMS_scaleRelativePtBB_j",
               "CMS_scaleRelativePtEC1_j",
               "CMS_scaleRelativePtEC2_j",
               "CMS_scaleRelativePtHF_j",
               "CMS_scaleRelativeBal_j", #added this one for Moriond 2016/80X
               "CMS_scaleRelativeFSR_j",
               "CMS_scaleRelativeStatFSR_j",
               "CMS_scaleRelativeStatEC_j",
               "CMS_scaleRelativeStatHF_j",
               "CMS_scalePileUpDataMC_j",
               "CMS_scalePileUpPtRef_j",
               "CMS_scalePileUpPtBB_j",
               "CMS_scalePileUpPtEC1_j",
               ###"CMS_scalePileUpPtEC2_j", #always 1
               "CMS_scalePileUpPtHF_j",
               "CMS_ttH_CSVcferr1",
               "CMS_ttH_CSVcferr2",
               "CMS_ttH_CSVhf",
               "CMS_ttH_CSVhfstats1",
               "CMS_ttH_CSVhfstats2",
               "CMS_ttH_CSVjes", ##NEED to include in normal JES!!!
               "CMS_ttH_CSVlf",
               "CMS_ttH_CSVlfstats1",
               "CMS_ttH_CSVlfstats2",
               "CMS_ttH_FHtrigger",
               "CMS_pu",
               #"CMS_ttjetsfsr", #ignore for now
               #"CMS_ttjetsisr"
               "ddQCD_3b", #don't need 1st bin unc. for 3b cats. anymore, but keep as conservative 
               "ddQCD_4b",
               #should be able to add normalisation systematics that are added in Add_ddQCD.py
               "lumi_13TeV",
               "pdf_Higgs_ttH",
               "pdf_gg",
               "pdf_qqbar",
               "pdf_qg",
               "QCDscale_ttH",
               "QCDscale_tt",
               "QCDscale_t",
               "QCDscale_V",
               "QCDscale_VV",
               "bgnorm_ttbarPlus2B",
               "bgnorm_ttbarPlusB",
               "bgnorm_ttbarPlusBBbar",
               "bgnorm_ttbarPlusCCbar",
               #added in sparsinator
               "CMS_ttH_ddQCD",
               "HTreweight3b", #this is only 7j3b
               "HTreweight4b",
               "CMS_ttH_qgWeight",
               "CMS_ttH_topPt",
               ]

normsys = ["lumi_13TeV",
           "pdf_Higgs_ttH",
           "pdf_gg",
           "pdf_qqbar",
           "pdf_qg",
           "QCDscale_ttH",
           "QCDscale_tt",
           "QCDscale_t",
           "QCDscale_V",
           "QCDscale_VV",
           "bgnorm_ttbarPlus2B",
           "bgnorm_ttbarPlusB",
           "bgnorm_ttbarPlusBBbar",
           "bgnorm_ttbarPlusCCbar"]

#Plotting size guides
#Canvas Width: 600, Height: 500
#Margin top: 0.08, right: 0.04, bottom: 0.12, left: 0.12 
#axis titles: 0.055 (0.06 recommended)
#axis labels: 0.048 (0.05 recommended)
#legend: 0.045

#def create_paves(lumi, data, CMSpos=1, PrelimPos=1, xlo=0.11, ylo=0.951, xhi=0.95, yhi=1.0):
def create_paves(lumi, label, CMSposX=0.11, CMSposY=0.9, prelimPosX=0.11, prelimPosY=0.85, lumiPosX=0.95, lumiPosY=0.951, alignRight=False, CMSsize=0.75*0.08, prelimSize=0.75*0.08*0.76, lumiSize=0.6*0.08):

    #pt_lumi = ROOT.TPaveText(xhi-0.25, ylo, xhi, yhi,"brNDC")
    pt_lumi = ROOT.TPaveText(lumiPosX-0.25, lumiPosY, lumiPosX, 1.0,"brNDC")
    pt_lumi.SetFillStyle(0)
    pt_lumi.SetBorderSize(0)
    pt_lumi.SetFillColor(0)
    pt_lumi.SetTextFont(42) 
    pt_lumi.SetTextSize(lumiSize)
    pt_lumi.SetTextAlign(31) #left=10, bottom=1, centre=2 
    pt_lumi.AddText( "{0:.1f}".format(lumi)+" fb^{-1} (13 TeV)" )
    
    # if CMSpos == 0: #outside frame
    #     pt_CMS = ROOT.TPaveText(xlo, ylo, xlo+0.1, yhi,"brNDC")
    # elif CMSpos == 1: #left
    #     pt_CMS = ROOT.TPaveText(xlo+0.04, ylo-0.09, xlo+0.14, ylo-0.04,"brNDC")
    # elif CMSpos == 2: #center 
    #     pt_CMS = ROOT.TPaveText(xlo+0.4, ylo-0.09, xlo+0.5, ylo-0.04,"brNDC")
    # elif CMSpos == 3: #right
    #     pt_CMS = ROOT.TPaveText(xhi-0.2, ylo-0.09, xhi-0.1, ylo-0.04,"brNDC")
    if alignRight:
        pt_CMS = ROOT.TPaveText(CMSposX-0.1, CMSposY, CMSposX, CMSposY+0.05,"brNDC")
    else:
        pt_CMS = ROOT.TPaveText(CMSposX, CMSposY, CMSposX+0.1, CMSposY+0.05,"brNDC") 
    pt_CMS.SetFillStyle(0)
    pt_CMS.SetBorderSize(0)
    pt_CMS.SetFillColor(0)
    pt_CMS.SetTextFont(61)
    pt_CMS.SetTextSize(CMSsize)
    #pt_CMS.SetTextAlign(31 if CMSpos==3 else 11)
    pt_CMS.SetTextAlign(31 if alignRight else 11 )
    pt_CMS.AddText("CMS")
    
    # if PrelimPos == 0: #outside frame
    #     pt_prelim = ROOT.TPaveText(xlo+0.09, ylo, xlo+0.3, yhi,"brNDC")
    # elif PrelimPos == 1: #left beside CMS
    #     pt_prelim = ROOT.TPaveText(xlo+0.13, ylo-0.09, xlo+0.34, ylo-0.04,"brNDC")
    # elif PrelimPos == 2: #left under CMS
    #     pt_prelim = ROOT.TPaveText(xlo+0.04, ylo-0.15, xlo+0.14, ylo-0.10,"brNDC")
    # elif PrelimPos == 3: #right under CMS
    #     pt_prelim = ROOT.TPaveText(xhi-0.2, ylo-0.15, xhi-0.1, ylo-0.10,"brNDC")
    if alignRight:
        pt_prelim = ROOT.TPaveText(prelimPosX-0.2, prelimPosY, prelimPosX, prelimPosY+0.05,"brNDC")
    else:
        pt_prelim = ROOT.TPaveText(prelimPosX, prelimPosY, prelimPosX+0.2, prelimPosY+0.05,"brNDC")
    pt_prelim.SetFillStyle(0)
    pt_prelim.SetBorderSize(0)
    pt_prelim.SetFillColor(0)
    pt_prelim.SetTextFont(52) 
    pt_prelim.SetTextSize(prelimSize)
    #pt_prelim.SetTextAlign(31 if PrelimPos==3 else 11)
    pt_prelim.SetTextAlign(31 if alignRight else 11 )    
    if label == "SimPAS":
        pt_prelim.AddText("Simulation Preliminary")
    elif label == "DataPAS":
        pt_prelim.AddText("Preliminary")
    elif label == "Sim":
        pt_prelim.AddText("Simulation")
    elif label == "Data":
        pt_prelim.AddText("")
    elif label == "SimSupp":
        pt_prelim.AddText("Simulation Supplementary")
    elif label == "DataSupp":
        pt_prelim.AddText("Supplementary")
    elif label == "DataWiP":
        pt_prelim.AddText("Work in Progress")
    
    return {"lumi":pt_lumi, "CMS":pt_CMS, "label":pt_prelim}

