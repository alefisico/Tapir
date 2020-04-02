
if [[ $# -eq 0 ]] ; then
    echo 'First argument, name of sample, is needed. Have a good day :)'
else
    sample=$1
    version=$2
    year=$3
    boosted='_boosted_'${year}

    if [[ ${year} == "2016" ]]; then
        ERAlist="Bv1 Bv2 C D E F G H"
    elif [[ ${year} == "2017" ]]; then
        ERAlist="B C D E F"
    elif [[ ${year} == "2018" ]]; then
        ERAlist="A B C D"
    fi


    if [[ "$sample" == "simple" ]]; then

        hadd -f Rootfiles/${version}/histograms_ttHTobb${boosted}.root ~/cernbox/tmpFiles/ttHTobb/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTToSemiLeptonic${boosted}.root ~/cernbox/tmpFiles/TTToSemiLeptonic/histograms*${version}${boosted}.root

    elif [[ "$sample" == "MC" ]]; then

        hadd -f Rootfiles/${version}/histograms_ST_s-channel_4f_leptonDecays${boosted}.root ~/cernbox/tmpFiles/ST_s-channel_4f_leptonDecays/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ST_t-channel_top${boosted}.root ~/cernbox/tmpFiles/ST_t-channel_top/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ST_t-channel_antitop${boosted}.root ~/cernbox/tmpFiles/ST_t-channel_antitop/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ST_tW_antitop${boosted}.root ~/cernbox/tmpFiles/ST_tW_antitop/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ST_tW_top${boosted}.root ~/cernbox/tmpFiles/ST_tW_top/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTTo2L2Nu${boosted}.root ~/cernbox/tmpFiles/TTTo2L2Nu/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTToHadronic${boosted}.root ~/cernbox/tmpFiles/TTToHadronic/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8${boosted}.root ~/cernbox/tmpFiles/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTWJetsToQQ${boosted}.root ~/cernbox/tmpFiles/TTWJetsToQQ/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTGJets${boosted}.root ~/cernbox/tmpFiles/TTGJets/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_TTZToQQ${boosted}.root ~/cernbox/tmpFiles/TTZToQQ/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WW${boosted}.root ~/cernbox/tmpFiles/WW/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WZ${boosted}.root ~/cernbox/tmpFiles/WZ/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ZZ${boosted}.root ~/cernbox/tmpFiles/ZZ/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_ttHToNonbb_M125${boosted}.root ~/cernbox/tmpFiles/ttHToNonbb_M125/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_DYJetsToLL${boosted}.root ~/cernbox/tmpFiles/DYJetsToLL/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_QCD_HT1000to1500${boosted}.root ~/cernbox/tmpFiles/QCD_HT1000to1500/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_QCD_HT1500to2000${boosted}.root ~/cernbox/tmpFiles/QCD_HT1500to2000/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_QCD_HT2000toInf${boosted}.root ~/cernbox/tmpFiles/QCD_HT2000toInf/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_QCD_HT300to500${boosted}.root ~/cernbox/tmpFiles/QCD_HT300to500/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_QCD_HT500to700${boosted}.root ~/cernbox/tmpFiles/QCD_HT500to700/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_QCD_HT700to1000${boosted}.root ~/cernbox/tmpFiles/QCD_HT700to1000/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToLNu_HT-1200To2500${boosted}.root ~/cernbox/tmpFiles/WJetsToLNu_HT-1200To2500/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToLNu_HT-200To400${boosted}.root ~/cernbox/tmpFiles/WJetsToLNu_HT-200To400/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToLNu_HT-2500ToInf${boosted}.root ~/cernbox/tmpFiles/WJetsToLNu_HT-2500ToInf/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToLNu_HT-400To600${boosted}.root ~/cernbox/tmpFiles/WJetsToLNu_HT-400To600/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToLNu_HT-600To800${boosted}.root ~/cernbox/tmpFiles/WJetsToLNu_HT-600To800/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToLNu_HT-800To1200${boosted}.root ~/cernbox/tmpFiles/WJetsToLNu_HT-800To1200/histograms_*${version}${boosted}.root
        hadd -f Rootfiles/${version}/histograms_WJetsToQQ_HT400to600${boosted}.root ~/cernbox/tmpFiles/WJetsToQQ_HT400to600/histograms_*${version}${boosted}.root

    elif [[ "$sample" == "Muon" ]]; then

        for era in $ERAlist; do
            hadd -f Rootfiles/${version}/histograms_SingleMuon_Run${year}${era}${boosted}.root ~/cernbox/tmpFiles/SingleMuon_Run${year}${era}/histograms_*${version}${boosted}.root
        done
        hadd -f Rootfiles/${version}/histograms_SingleMuon_Run${year}ALL${boosted}.root Rootfiles/${version}/histograms_SingleMuon_Run${year}*${boosted}.root

    elif [[ "$sample" == "Electron" ]]; then

        for era in $ERAlist; do
            hadd -f Rootfiles/${version}/histograms_SingleElectron_Run${year}${era}${boosted}.root ~/cernbox/tmpFiles/SingleElectron_Run${year}${era}/histograms_*${version}${boosted}.root
        done
        hadd -f Rootfiles/${version}/histograms_SingleElectron_Run${year}ALL${boosted}.root Rootfiles/${version}/histograms_SingleElectron_Run${year}*${boosted}.root
    else
        hadd -f Rootfiles/${version}/histograms_${sample}${boosted}.root ~/cernbox/tmpFiles/${sample}/histograms_*${version}${boosted}.root
    fi

fi
#hadd -f Rootfiles/${version}/histograms_${boosted}.root ~/cernbox/tmpFiles//histograms_*${version}${boosted}.root
