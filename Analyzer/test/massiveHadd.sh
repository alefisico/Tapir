version=v10
boosted='_boosted'

if [[ $# -eq 0 ]] ; then
    echo 'First argument, name of sample, is needed. Have a good day :)'
else
    sample=$1

    if [[ "$sample" == "simple" ]]; then

        hadd -f Rootfiles/${version}/histograms_ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8${boosted}.root ~/cernbox/tmpFiles/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8${boosted}.root ~/cernbox/tmpFiles/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/histograms*${version}${boosted}.root

    elif [[ "$sample" == "MC" ]]; then

        hadd -f Rootfiles/${version}/histograms_ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8${boosted}.root ~/cernbox/tmpFiles/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8${boosted}.root ~/cernbox/tmpFiles/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8${boosted}.root ~/cernbox/tmpFiles/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8${boosted}.root ~/cernbox/tmpFiles/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8${boosted}.root ~/cernbox/tmpFiles/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTToHadronic_TuneCP5_13TeV-powheg-pythia8${boosted}.root ~/cernbox/tmpFiles/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8${boosted}.root ~/cernbox/tmpFiles/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8${boosted}.root ~/cernbox/tmpFiles/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8${boosted}.root ~/cernbox/tmpFiles/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8${boosted}.root ~/cernbox/tmpFiles/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8${boosted}.root ~/cernbox/tmpFiles/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WW_TuneCP5_13TeV-pythia8${boosted}.root ~/cernbox/tmpFiles/WW_TuneCP5_13TeV-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WZ_TuneCP5_13TeV-pythia8${boosted}.root ~/cernbox/tmpFiles/WZ_TuneCP5_13TeV-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ZZ_TuneCP5_13TeV-pythia8${boosted}.root ~/cernbox/tmpFiles/ZZ_TuneCP5_13TeV-pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8${boosted}.root ~/cernbox/tmpFiles/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8${boosted}.root ~/cernbox/tmpFiles/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/histograms_*${version}${boosted}.root

    elif [[ "$sample" == "Muon" ]]; then

        hadd -f Rootfiles/${version}/histograms_SingleMuon_Run2017B${boosted}.root ~/cernbox/tmpFiles/SingleMuon_Run2017B/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleMuon_Run2017C${boosted}.root ~/cernbox/tmpFiles/SingleMuon_Run2017C/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleMuon_Run2017D${boosted}.root ~/cernbox/tmpFiles/SingleMuon_Run2017D/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleMuon_Run2017E${boosted}.root ~/cernbox/tmpFiles/SingleMuon_Run2017E/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleMuon_Run2017F${boosted}.root ~/cernbox/tmpFiles/SingleMuon_Run2017F/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleMuon_Run2017ALL${boosted}.root Rootfiles/${version}/histograms_SingleMuon_Run2017*${boosted}.root

    elif [[ "$sample" == "Electron" ]]; then

        hadd -f Rootfiles/${version}/histograms_SingleElectron_Run2017B${boosted}.root ~/cernbox/tmpFiles/SingleElectron_Run2017B/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleElectron_Run2017C${boosted}.root ~/cernbox/tmpFiles/SingleElectron_Run2017C/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleElectron_Run2017D${boosted}.root ~/cernbox/tmpFiles/SingleElectron_Run2017D/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleElectron_Run2017E${boosted}.root ~/cernbox/tmpFiles/SingleElectron_Run2017E/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleElectron_Run2017F${boosted}.root ~/cernbox/tmpFiles/SingleElectron_Run2017F/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_SingleElectron_Run2017ALL${boosted}.root Rootfiles/${version}/histograms_SingleElectron_Run2017*${boosted}.root
    fi

fi
#hadd -f Rootfiles/${version}/histograms_${boosted}.root ~/cernbox/tmpFiles//histograms_*${version}${boosted}.root
