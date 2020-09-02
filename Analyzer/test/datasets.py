#!/usr/bin/env python

dictSamples = {

	'ttHTobb' : {
		'2016' : [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 5253482.85, 9972000 ],
		'2017' : [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 4216319.31, 8000000 ],
		'2018' : [ ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_EXT_102X_upgrade2018_realistic_v21-v1/NANOAODSIM' ], 5046714.40, 9580000. ],
        'XS' : 0.2953,
	},
	'THW' : {
		'2016' : [ '/THW_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4989133.86, 4998296  ],
		'2017' : [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 4714331.00, 4719999 ],
		'2018' : [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 14971606.14, 14998988. ],
        'XS' : 0.01517,
	},
        'ttHToNonbb' : {
            '2016' : [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 5248991.57, 9965577 ],
            '2017' : [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 3095197.81, 5499293 ],
            '2018' : [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 3963935.78, 7525991 ],
            'XS' : 0.2118,
        },
	'TTToSemiLeptonic' : {
		'2016' : [  '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 32366940321.33, 107604800 ],
		'2017' : [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 59457024911.66, 197670000 ],
		'2018' : [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext3-v1/NANOAODSIM', 60050384119.23, 199637998  ],
        'XS' : 365.4574,
	},
	'TTTo2L2Nu' : {
		'2016' : [ '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4784620999.11, 66376000 ],
		'2017' : [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 648729877.29, 9000000 ],
		'2018' : [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 4622080044.95, 64120000 ],
        'XS' : 88.3419,
	},
	'TTToHadronic' : {
		'2016' : [ '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 21500086465.24, 68518800 ],
		'2017' : [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 61932449366.28, 197296000 ],
		'2018' : [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM', 62639466237., 199620000 ],
        'XS' : 377.9607,
	},
	'TTZToQQ' : {
		'2016' : [ '/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 396340.93, 749400 ],
		'2017' : [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 4564905.23, 8940000 ],
		'2018' : [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 4534202.12, 8891000 ],
        'XS' : 0.6012,
	},
	'TTZToLLNuNu' : {
		'2016' : [ '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 502198.85, 1992438 ],
		'2017' : [ '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 1838397.29, 7563490 ],
		'2018' : [ '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 3226764.90, 13280000 ],
        'XS' : .2432,       #### 2.432e-01 +- 3.054e-04 pb
	},
	'TTWJetsToQQ' : {
		'2016' : [ '/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 569424.14, 833298 ],
		'2017' : [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 560315.13, 811306 ],
		'2018' : [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 580758.84, 835296 ],
        'XS' : 0.3708,
	},
	'TTWJetsToLNu' : {
		'2016' : [ '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 731877.67, 2160168 ],
		'2017' : [ '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 1654929.98, 4830828 ],
		'2018' : [ '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 1690091.78, 4911941 ],
        'XS' : 0.2181,           #### 2.181e-01 +- 3.838e-04 pb
	},
	'DYJetsToLL' : {
		'2016' : [ '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM', 1897141621849.11, 120777245 ],
		'2017' : [ '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 3251533677930.31, 182217609],
		'2018' : [ '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 17799598587.56, 997561 ],
        'XS' : 6549.,               #### 6.549e+03 +- 1.334e+01 pb
	},
#	'QCD_HT300to500' : {
#		'2016' : [ '', 1, 1 ],
#		'2017' : [ '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 59459614.0, 59569132 ],
#		'2018' : [ '', 1, 1 ],
#        'XS' : 323600.,           #### 3.236e+05 +- 3.074e+02 pb
#	},
	'QCD_HT500to700' : {
		'2016' : [ '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 18560541.0, 18560541 ],
		'2017' : [ '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 55945526.0, 56111970 ],
		'2018' : [ '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 55046821.83, 55152960 ],
        'XS' : 29990.,               #### 2.999e+04 +- 2.871e+01 pb
	},
	'QCD_HT700to1000' : {
		'2016' : [ '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 15629253.0, 15629253 ],
		'2017' : [ '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 47424646.0, 47630084 ],
		'2018' : [ '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 48028221.62, 48158738 ],
        'XS' : 6351.,                   #### 6.351e+03 +- 6.107e+00 pb
	},
	'QCD_HT1000to1500' : {
		'2016' : [ '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4850746.0, 4850746 ],
		'2017' : [ '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 16485296.0, 16595628 ],
		'2018' : [ '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 15403521.91, 15466225 ],
        'XS' : 1094.,               #### 1.094e+03 +- 1.056e+00 pb
	},
	'QCD_HT1500to2000' : {
		'2016' : [ '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 3970819.0, 3970819 ],
		'2017' : [ '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 11508604.0, 11634434 ],
		'2018' : [ '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 10883854.57, 10955087 ],
        'XS' : 101.0,                   ### 1.010e+02 +- 1.514e+00 pb
	},
	'QCD_HT2000toInf' : {
		'2016' : [ '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 1991645.0, 1991645  ],
		'2017' : [ '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 5825566.0, 5941306 ],
		'2018' : [ '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 5412264.53, 5475677 ],
        'XS' : 20.23,                       ### 2.023e+01 +- 1.978e-02 pb
	},
	'TTGJets' : {
		'2016' : [ '/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 67622406.44, 9877942 ],
		'2017' : [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 62364926.69, 8729288 ],
		'2018' : [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 33778755.65, 4691915 ],
        'XS' : 4.103, #3.697,   ### from XSec tool 4.103e+00 +- 1.067e-02 pb
	},
	'WW' : {
		'2016' : [ '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 6988278.14, 6988168 ],
		'2017' : [ '/WW_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 7765891.02, 7765828 ],
		'2018' : [ '/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 7846135.95, 7850000 ],
        'XS' : 118.7,
	},
	'WZ' : {
		'2016' : [ '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 2997571.0, 2997571 ],
		'2017' : [ '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 3928630.0, 3928630.0 ],
		'2018' : [ '/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 3884167.00, 3885000 ],
        'XS' : 65.5443,
	},
	'ZZ' : {
		'2016' : [ '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 998034.0, 998034 ],
		'2017' : [ '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 1949768.0, 1949768.0 ],
		'2018' : [ '/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 1978776.75, 1979000 ],
        'XS' : 15.8274,
	},
#	'WJetsToLNu' : {
#		'2016' : [ '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',  57402435.0, 57402435],
#		'2017' : [ ['/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_ext_102X_mc2017_realistic_v8-v1/NANOAODSIM'], 107612500.0, 107708756 ],
#		'2018' : [ '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 70389866.80, 70454125 ],
#        'XS' : 61526.7,  ### 5279. from GenXSecAnalyzer
#	},
	'WJetsToLNu_HT-200To400' : {
		'2016' : [ '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4963240.0, 4963240 ],
		'2017' : [ '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 21192211.0, 21250517 ],
		'2018' : [ '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 25415129.21, 25468933 ],
        'XS' : 409.3,   ### 4.093e+02 +- 3.834e-01 pb
	},
	'WJetsToLNu_HT-400To600' : {
		'2016' : [ '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 1963464.0, 1963464 ],
		'2017' : [ '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 14250114.0, 14313274 ],
		'2018' : [ '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 5913597.774, 5932701 ],
        'XS' : 57.91,      ### 5.791e+01 +- 5.478e-02 pb
	},
	'WJetsToLNu_HT-600To800' : {
		'2016' : [ '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 3779141.0, 3779141 ],
		'2017' : [ '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 21582309.0, 21709087 ],
		'2018' : [ '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 19690762.31, 19771294 ],
        'XS' : 12.93,          #### 1.293e+01 +- 1.226e-02 pb
	},
	'WJetsToLNu_HT-800To1200' : {
		'2016' : [ '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 1544513.0, 1544513 ],
		'2017' : [ '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 20272990.0,  20432728],
		'2018' : [ '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 8357921.27, 8402687 ],
        'XS' : 5.395,              #### 5.395e+00 +- 5.144e-03 pb
	},
	'WJetsToLNu_HT-1200To2500' : {
		'2016' : [ '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 244532.0, 244532 ],
		'2017' : [ '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 19991892.0, 20258624 ],
		'2018' : [ '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 7567071.14, 7633949 ],
        'XS' : 1.081,              ##### 1.081e+00 +- 1.038e-03 pb
	},
	'WJetsToLNu_HT-2500ToInf' : {
		'2016' : [ '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 253561.0, 253561 ],
		'2017' : [ '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 20629585.0, 21495421],
		'2018' : [ '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 3189396.07, 3273980 ],
        'XS' : 0.008060,            ## 8.060e-03 +- 7.918e-06 pb
	},
	'ST_s-channel_4f_leptonDecays' : {
		'2016' : [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 36768937.25, 9842599 ],
		'2017' : [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 37052021.59, 9914948 ],
		'2018' : [ '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 74634736.73, 19965000  ],
        'XS' : 3.36,
	},
	'ST_t-channel_top' : {
		'2016' : [ '/ST_t-channel_top_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 67975483.38, 68001000  ],
		'2017' : [ '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 5982064.0, 5982064 ],
		'2018' : [ '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 16603455266.97, 154307600 ],
        'XS' : 136.02,
	},
	'ST_t-channel_antitop' : {
		'2016' : [ '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 17771478.65, 17780700  ],
		'2017' : [ '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 64689262.55, 64722800 ],
		'2018' : [ '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 5125996535.38, 79090800 ],
        'XS' : 80.95,
	},
	'ST_tW_top' : {
		'2016' : [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 173908712.95, 4983500 ],
		'2017' : [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 272081073.53, 7794186 ],
		'2018' : [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 334874722.20, 9598000 ],
        'XS' : 35.85,
	},
	'ST_tW_antitop' : {
		'2016' : [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 174109580.67, 4980600  ],
		'2017' : [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',  279005351.85, 7977430 ],
		'2018' : [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 266470421.96, 7623000 ],
        'XS' : 35.85,
	},
	'WJetsToQQ_HT400to600' : {
		#'2016' : [ 'NO SAMPLE IN 2016' ],
		'2017' : [ '/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 9412603.0, 9441439 ],
		'2018' : [ '/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 10046074.61, 10071273  ],
        'XS' : 314.6,       #### 3.146e+02 +- 2.797e-01 pb
	},
	'WJetsToQQ_HT600to800' : {
		'2017' : [ '/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 8761386.0, 8798398 ],
		'2018' : [ '/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 15246402.33, 15298056  ],
        'XS' : 68.60,
	},
	'WJetsToQQ_HT-800toInf' : {
		'2017' : [ '/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 8028207.0, 8081153 ],
		'2018' : [ '/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 14552824.37, 14627242  ],
        'XS' : 34.78,
	},
	'ZJetsToQQ_HT400to600' : {
		#'2016' : [ '/ZJetsToQQ_HT400to600_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM' ],
		'2017' : [ '/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 10285185.0, 10316727 ],
		'2018' : [ '/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 16669536.82, 16704355  ],
        'XS' : 146.1,           #### 1.461e+02 +- 1.380e-01 pb
	},
	'ZJetsToQQ_HT600to800' : {
		#'2016' : [  ],
		'2017' : [ '/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 8845052.0, 8882592 ],
		'2018' : [ '/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 14600689.07, 14642701  ],
        'XS' : 34.01,           #### 3.401e+01 +- 3.225e-02 pb
	},
	'ZJetsToQQ_HT-800toInf' : {
		#'2016' : [ '/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM' ],
		'2017' : [ '/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',  7764804.0, 7818660 ],
		'2018' : [ '/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 10513086.25, 10561192 ],
        'XS' : 18.54,            ##### 1.854e+01 +- 1.772e-02 pb
	},
#	'ZJetsToNuNu_HT-200To400' : {
#		'2016' : [  ],
#		'2017' : [ '/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 21618510.0, 21675916 ],
#		'2018' : [  ],
#        'XS' : 91.83,            #### 9.183e+01 +- 2.437e-01 pb
#	},
#	'ZJetsToNuNu_HT-400To600' : {
#		'2016' : [  ],
#		'2017' : [ '/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 9094890.0, 9134120  ],
#		'2018' : [  ],
#        'XS' : 13.10,            #### 1.310e+01 +- 1.239e-02 pb
#	},
#	'ZJetsToNuNu_HT-600To800' : {
#		'2016' : [  ],
#		'2017' : [ '/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 5615921.0,  5615921.0 ],
#		'2018' : [  ],
#        'XS' : 3.248,            ##### 3.248e+00 +- 3.083e-03 pb
#	},
#	'ZJetsToNuNu_HT-800To1200' : {
#		'2016' : [  ],
#		'2017' : [ '/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 2041779.0, 2058077 ],
#		'2018' : [  ],
#        'XS' : 1.496,            #####  1.496e+00 +- 1.425e-03 pb
#	},
#	'ZJetsToNuNu_HT-1200To2500' : {
#		'2016' : [  ],
#		'2017' : [ '/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 336181.0, 340873 ],
#		'2018' : [  ],
#        'XS' : 0.3425,            #### 3.425e-01 +- 5.603e-04 pb
#	},
#	'ZJetsToNuNu_HT-2500ToInf' : {
#		'2016' : [  ],
#		'2017' : [ '/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 6446.0, 6734  ],
#		'2018' : [  ],
#        'XS' : 0.005264,            #### 5.264e-03 +- 8.654e-06 pb
#	},
#	'QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8' : {
#		'2016' : [ '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v8-v2/NANOAODSIM', 9951232.0 ],
#		'2017' : [ '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v8-v1/NANOAODSIM', 17413568.0 ],
#		'2018' : [ '/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v2/NANOAODSIM', 19464000.0 ],
#        'XS' : 0,
#	},
}

def checkDict( string, dictio ):
    return next(v for k,v in dictio.items() if string in k)

