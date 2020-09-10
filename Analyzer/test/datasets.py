#!/usr/bin/env python

dictSamples = {

	'ttHTobb' : {
		'2016' : {
			'nanoAOD' : [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 5253482.85, 9972000 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 4216319.31, 8000000 ],
			'nanoAODPost' : [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-ttHTobb2017_nanoAODPostProcessor_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_EXT_102X_upgrade2018_realistic_v21-v1/NANOAODSIM' ], 5046714.40, 9580000. ],
			'nanoAODPost' : [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-ttHTobb2018ext_nanoAODPostProcessor_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 0.2953,
	},
	'THW' : {
		'2016' : {
			'nanoAOD' : [ '/THW_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4989133.86, 4998296  ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 4714331.00, 4719999 ],
			'nanoAODPost' : [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/algomez-THW2017_nanoAODPostProcessor_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 14971606.14, 14998988. ],
			'nanoAODPost' : [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/algomez-THW2018_nanoAODPostProcessor_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 0.01517,
	},
        'ttHToNonbb' : {
            '2016' : {
			'nanoAOD' : [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 5248991.57, 9965577 ],
			'nanoAODPost' : [ '',   ],
		},
            '2017' : {
			'nanoAOD' : [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 3095197.81, 5499293 ],
			'nanoAODPost' : [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-ttHToNonbb_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
            '2018' : {
			'nanoAOD' : [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 3963935.78, 7525991 ],
			'nanoAODPost' : [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-ttHTobb2018_nanoAODPostProcessor_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
            'XS' : 0.2118,
        },
	'TTToSemiLeptonic' : {
		'2016' : {
			'nanoAOD' : [  '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 32366940321.33, 107604800 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 59457024911.66, 197670000 ],
			'nanoAODPost' : [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/algomez-TTToSemiLeptonic_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext3-v1/NANOAODSIM', 60050384119.23, 199637998  ],
			'nanoAODPost' : [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/algomez-TTToSemiLeptonic_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 365.4574,
	},
	'TTTo2L2Nu' : {
		'2016' : {
			'nanoAOD' : [ '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4784620999.11, 66376000 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 648729877.29, 9000000 ],
			'nanoAODPost' : [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/algomez-TTTo2L2Nu_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 4622080044.95, 64120000 ],
			'nanoAODPost' : [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/algomez-TTTo2L2Nu_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 88.3419,
	},
	'TTToHadronic' : {
		'2016' : {
			'nanoAOD' : [ '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 21500086465.24, 68518800 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 61932449366.28, 197296000 ],
			'nanoAODPost' : [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/algomez-TTToHadronic_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM', 62639466237., 199620000 ],
			'nanoAODPost' : [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/algomez-TTToHadronic_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 377.9607,
	},
	'TTZToQQ' : {
		'2016' : {
			'nanoAOD' : [ '/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 396340.93, 749400 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 4564905.23, 8940000 ],
			'nanoAODPost' : [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/algomez-TTZToQQ_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 4534202.12, 8891000 ],
			'nanoAODPost' : [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/algomez-TTZToQQ_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 0.6012,
	},
	'TTZToLLNuNu' : {
		'2016' : {
			'nanoAOD' : [ '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 502198.85, 1992438 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 1838397.29, 7563490 ],
			'nanoAODPost' : [ '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/algomez-TTZToLLNuNu_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 3226764.90, 13280000 ],
			'nanoAODPost' : [ '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/algomez-TTZToLLNuNu_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : .2432,       #### 2.432e-01 +- 3.054e-04 pb
	},
	'TTWJetsToQQ' : {
		'2016' : {
			'nanoAOD' : [ '/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 569424.14, 833298 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 560315.13, 811306 ],
			'nanoAODPost' : [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-TTWJetsToQQ_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 580758.84, 835296 ],
			'nanoAODPost' : [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-TTWJetsToQQ_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 0.3708,
	},
	'TTWJetsToLNu' : {
		'2016' : {
			'nanoAOD' : [ '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 731877.67, 2160168 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 1654929.98, 4830828 ],
			'nanoAODPost' : [ '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-TTWJetsToLNu_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 1690091.78, 4911941 ],
			'nanoAODPost' : [ '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-TTWJetsToLNu_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 0.2181,           #### 2.181e-01 +- 3.838e-04 pb
	},
	'DYJetsToLL' : {
		'2016' : {
			'nanoAOD' : [ '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM', 1897141621849.11, 120777245 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 3251533677930.31, 182217609],
			'nanoAODPost' : [ '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/algomez-DYJetsToLL_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 17799598587.56, 997561 ],
			'nanoAODPost' : [ '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/algomez-DYJetsToLL_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 6549.,               #### 6.549e+03 +- 1.334e+01 pb
	},
	'QCD_HT500to700' : {
		'2016' : {
			'nanoAOD' : [ '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 18560541.0, 18560541 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 55945526.0, 56111970 ],
			'nanoAODPost' : [ '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/algomez-QCD_HT500to700_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 55046821.83, 55152960 ],
			'nanoAODPost' : [ '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-QCD_HT500to700_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 29990.,               #### 2.999e+04 +- 2.871e+01 pb
	},
	'QCD_HT700to1000' : {
		'2016' : {
			'nanoAOD' : [ '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 15629253.0, 15629253 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 47424646.0, 47630084 ],
			'nanoAODPost' : [ '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/algomez-QCD_HT700to1000_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 48028221.62, 48158738 ],
			'nanoAODPost' : [ '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-QCD_HT700to1000_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 6351.,                   #### 6.351e+03 +- 6.107e+00 pb
	},
	'QCD_HT1000to1500' : {
		'2016' : {
			'nanoAOD' : [ '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4850746.0, 4850746 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 16485296.0, 16595628 ],
			'nanoAODPost' : [ '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/algomez-QCD_HT1000to1500_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 15403521.91, 15466225 ],
			'nanoAODPost' : [ '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-QCD_HT1000to1500_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 1094.,               #### 1.094e+03 +- 1.056e+00 pb
	},
	'QCD_HT1500to2000' : {
		'2016' : {
			'nanoAOD' : [ '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 3970819.0, 3970819 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 11508604.0, 11634434 ],
			'nanoAODPost' : [ '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/algomez-QCD_HT1500to2000_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 10883854.57, 10955087 ],
			'nanoAODPost' : [ '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-QCD_HT1500to2000_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 101.0,                   ### 1.010e+02 +- 1.514e+00 pb
	},
	'QCD_HT2000toInf' : {
		'2016' : {
			'nanoAOD' : [ '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 1991645.0, 1991645  ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 5825566.0, 5941306 ],
			'nanoAODPost' : [ '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/algomez-QCD_HT2000toInf_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 5412264.53, 5475677 ],
			'nanoAODPost' : [ '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-QCD_HT2000toInf_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 20.23,                       ### 2.023e+01 +- 1.978e-02 pb
	},
	'TTGJets' : {
		'2016' : {
			'nanoAOD' : [ '/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 67622406.44, 9877942 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM', 62364926.69, 8729288 ],
			'nanoAODPost' : [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-TTGJets_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 33778755.65, 4691915 ],
			'nanoAODPost' : [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-TTGJets_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 4.103, #3.697,   ### from XSec tool 4.103e+00 +- 1.067e-02 pb
	},
	'WW' : {
		'2016' : {
			'nanoAOD' : [ '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 6988278.14, 6988168 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WW_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 7765891.02, 7765828 ],
			'nanoAODPost' : [ '/WW_TuneCP5_13TeV-pythia8/algomez-WW_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 7846135.95, 7850000 ],
			'nanoAODPost' : [ '/WW_TuneCP5_13TeV-pythia8/algomez-WW_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 118.7,
	},
	'WZ' : {
		'2016' : {
			'nanoAOD' : [ '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 2997571.0, 2997571 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 3928630.0, 3928630.0 ],
			'nanoAODPost' : [ '/WZ_TuneCP5_13TeV-pythia8/algomez-WZ_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 3884167.00, 3885000 ],
			'nanoAODPost' : [ '/WZ_TuneCP5_13TeV-pythia8/algomez-WZ_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 65.5443,
	},
	'ZZ' : {
		'2016' : {
			'nanoAOD' : [ '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM', 998034.0, 998034 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 1949768.0, 1949768.0 ],
			'nanoAODPost' : [ '/ZZ_TuneCP5_13TeV-pythia8/algomez-ZZ_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 1978776.75, 1979000 ],
			'nanoAODPost' : [ '/ZZ_TuneCP5_13TeV-pythia8/algomez-ZZ_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 15.8274,
	},
	'WJetsToLNu_HT-200To400' : {
		'2016' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 4963240.0, 4963240 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 21192211.0, 21250517 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-200To400_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 25415129.21, 25468933 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-200To400_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 409.3,   ### 4.093e+02 +- 3.834e-01 pb
	},
	'WJetsToLNu_HT-400To600' : {
		'2016' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 1963464.0, 1963464 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 14250114.0, 14313274 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-400To600_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 5913597.774, 5932701 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-400To600_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 57.91,      ### 5.791e+01 +- 5.478e-02 pb
	},
	'WJetsToLNu_HT-600To800' : {
		'2016' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 3779141.0, 3779141 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 21582309.0, 21709087 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-600To800_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 19690762.31, 19771294 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-600To800_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 12.93,          #### 1.293e+01 +- 1.226e-02 pb
	},
	'WJetsToLNu_HT-800To1200' : {
		'2016' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 1544513.0, 1544513 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 20272990.0,  20432728],
			'nanoAODPost' : [ '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-800To1200_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 8357921.27, 8402687 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-800To1200_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 5.395,              #### 5.395e+00 +- 5.144e-03 pb
	},
	'WJetsToLNu_HT-1200To2500' : {
		'2016' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 244532.0, 244532 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 19991892.0, 20258624 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-1200To2500_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 7567071.14, 7633949 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-1200To2500_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 1.081,              ##### 1.081e+00 +- 1.038e-03 pb
	},
	'WJetsToLNu_HT-2500ToInf' : {
		'2016' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 253561.0, 253561 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 20629585.0, 21495421],
			'nanoAODPost' : [ '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-2500ToInf_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 3189396.07, 3273980 ],
			'nanoAODPost' : [ '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToLNu_HT-2500ToInf_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 0.008060,            ## 8.060e-03 +- 7.918e-06 pb
	},
	'ST_s-channel_4f_leptonDecays' : {
		'2016' : {
			'nanoAOD' : [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 36768937.25, 9842599 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 37052021.59, 9914948 ],
			'nanoAODPost' : [ '',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 74634736.73, 19965000  ],
			'nanoAODPost' : [ '',   ],
		},
        'XS' : 3.36,
	},
	'ST_t-channel_top' : {
		'2016' : {
			'nanoAOD' : [ '/ST_t-channel_top_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 67975483.38, 68001000  ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM', 5982064.0, 5982064 ],
			'nanoAODPost' : [ '',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 16603455266.97, 154307600 ],
			'nanoAODPost' : [ '',   ],
		},
        'XS' : 136.02,
	},
	'ST_t-channel_antitop' : {
		'2016' : {
			'nanoAOD' : [ '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 17771478.65, 17780700  ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 64689262.55, 64722800 ],
			'nanoAODPost' : [ '',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 5125996535.38, 79090800 ],
			'nanoAODPost' : [ '',   ],
		},
        'XS' : 80.95,
	},
	'ST_tW_top' : {
		'2016' : {
			'nanoAOD' : [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 173908712.95, 4983500 ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 272081073.53, 7794186 ],
			'nanoAODPost' : [ '',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 334874722.20, 9598000 ],
			'nanoAODPost' : [ '',   ],
		},
        'XS' : 35.85,
	},
	'ST_tW_antitop' : {
		'2016' : {
			'nanoAOD' : [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM', 174109580.67, 4980600  ],
			'nanoAODPost' : [ '',   ],
		},
		'2017' : {
			'nanoAOD' : [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',  279005351.85, 7977430 ],
			'nanoAODPost' : [ '',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM', 266470421.96, 7623000 ],
			'nanoAODPost' : [ '',   ],
		},
        'XS' : 35.85,
	},
	'WJetsToQQ_HT400to600' : {
		'2017' : {
			'nanoAOD' : [ '/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 9412603.0, 9441439 ],
			'nanoAODPost' : [ '/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToQQ_HT400to600_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 10046074.61, 10071273  ],
			'nanoAODPost' : [ '/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToQQ_HT400to600_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 314.6,       #### 3.146e+02 +- 2.797e-01 pb
	},
	'WJetsToQQ_HT600to800' : {
		'2017' : {
			'nanoAOD' : [ '/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 8761386.0, 8798398 ],
			'nanoAODPost' : [ '/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToQQ_HT600to800_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 15246402.33, 15298056  ],
			'nanoAODPost' : [ '/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToQQ_HT600to800_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 68.60,
	},
	'WJetsToQQ_HT-800toInf' : {
		'2017' : {
			'nanoAOD' : [ '/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 8028207.0, 8081153 ],
			'nanoAODPost' : [ '/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToQQ_HT-800toInf_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 14552824.37, 14627242  ],
			'nanoAODPost' : [ '/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-WJetsToQQ_HT-800toInf_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 34.78,
	},
	'ZJetsToQQ_HT400to600' : {
		'2017' : {
			'nanoAOD' : [ '/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 10285185.0, 10316727 ],
			'nanoAODPost' : [ '/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-ZJetsToQQ_HT400to600_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 16669536.82, 16704355  ],
			'nanoAODPost' : [ '/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-ZJetsToQQ_HT400to600_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 146.1,           #### 1.461e+02 +- 1.380e-01 pb
	},
	'ZJetsToQQ_HT600to800' : {
		'2017' : {
			'nanoAOD' : [ '/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM', 8845052.0, 8882592 ],
			'nanoAODPost' : [ '/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-ZJetsToQQ_HT600to800_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 14600689.07, 14642701  ],
			'nanoAODPost' : [ '/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-ZJetsToQQ_HT600to800_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 34.01,           #### 3.401e+01 +- 3.225e-02 pb
	},
	'ZJetsToQQ_HT-800toInf' : {
		'2017' : {
			'nanoAOD' : [ '/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',  7764804.0, 7818660 ],
			'nanoAODPost' : [ '/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-ZJetsToQQ_HT-800toInf_nanoAODPostProcessor_2017_v03-31deb7c86682c648bf5094175e82e051/USER',   ],
		},
		'2018' : {
			'nanoAOD' : [ '/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM', 10513086.25, 10561192 ],
			'nanoAODPost' : [ '/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-ZJetsToQQ_HT-800toInf_nanoAODPostProcessor_2018_v03-b007c9995322e232a5f950905968126e/USER',   ],
		},
        'XS' : 18.54,            ##### 1.854e+01 +- 1.772e-02 pb
	},
}

def checkDict( string, dictio ):
    return next(v for k,v in dictio.items() if string in k)

