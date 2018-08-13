# Trigger SF for ttH FH
For the ttH(bb) FH analysis a comination of the HLT paths
- HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5
- HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2
- HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0
- HLT_PFHT1050
- HLT_PFJet500
is used.

## Datasets and selection
The SF are calulated w.r.t. to `IsoMu_27`. The following dataset are used:

| dataset                                                                                                                               | nanoAOD files                                                                            | tthbb13 files                                                                              | ngen      | xsec    |
|---------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|-----------|---------|
| /SingleMuon/Run2017*-31Mar2018-v1/MINIAOD                                                                                             | datasets/ttH_AH_TriggerSF_v1_re/SingleMuon_All.txt                                       | datasets/ttH_AH_TriggerSF_v1p2/SingleMuon.txt                                              | -         | -       |
| /TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM                  | datasets/ttH_AH_TriggerSF_v1/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.txt                  | datasets/ttH_AH_TriggerSF_v1p2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.txt                  | 8608726   |  90.578 |
| /TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM               | datasets/ttH_AH_TriggerSF_v1/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.txt | datasets/ttH_AH_TriggerSF_v1p2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.txt | 104846497 | 367.804 |
|  /TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSI | datasets/ttH_AH_TriggerSF_v1/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.txt               | datasets/ttH_AH_TriggerSF_v1p2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.txt               | 40548871  | 373.3   |

Use the MEAnalysis config `MEAnalysis/python/cfg_FH_trigSF.py`. It will set up, that all events will be saved in the output and the `is_fh` will be set to true in every event.

The Baseline selection for the scale factors is then `(HLT_BIT_HLT_IsoMu27) && is_sl && abs(leps_pdgId[0]) == 13`. This selection as well as some other cuts are directly applied in `MEAnalysis/python/projectSkimTriggerSF.py`.

### Run dependencies
For the Sf calulation not the whole dataset can be used, because `HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5` was prescaled for the first part of RunC (299337 - 300999). Including them would reduce the efficiency.

The `SixPFJet` and `QuadPFJet` trigger changed names between run B and C (s. `MEAnalysis/python/TriggerTable.py`). This is handeled in the tthbb13 code and the output nTuple containd the variable `HLT_ttH_FH` which is `HLT_ttH_FH_RunB or HLT_ttH_FH_RunCF`.

## Calculating the SF
### Running ntuples
The run on crab use the `hadronic_trigger` workflow in the multicrab script.

You can also run from previously processed nanoAOD files using grid control and `MEAnalysis/gc/confs/MEAnalysis_TriggerSF.conf`. Here you might have to change the me_config in `config_FH.cfg` to reference `mem_python_config: $CMSSW_BASE/src/TTH/MEAnalysis/python/cfg_FH_trigSF.py`.

### Getting the Lumi:
Since the beginning of RunB is not usable for the measruement the cirrect lumi has to be calculated:
```bash
#On lxlpus
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb  -i final_TriggerSF_JSON.txt
```
The json is saved here: `/scratch/koschwei/DONOTREMOVE/ttH/2017/TriggerSF/final_TriggerSF_JSON.txt`

This results in:
```
#Summary:
+-------+------+--------+--------+-------------------+------------------+
| nfill | nrun | nls    | ncms   | totdelivered(/fb) | totrecorded(/fb) |
+-------+------+--------+--------+-------------------+------------------+
| 146   | 369  | 177285 | 176520 | 37.220            | 35.336           |
+-------+------+--------+--------+-------------------+------------------+
```
### Getting the SF
To calculate the SF the script `Plotting/Daniel/Trigger_SFs.py`. It will produce 1D efficiency plots for relevant variables (HT, NBCSVM, pt[5] and pt[3]) as well as Denominator and numerator histograms. Furthermore it will produce a root file containing the SF in a 3D histogram.       
Thing to consider:
- Input files (`mcFiles` and `fdata` in `TriggerSF()`)
- ngen and xsec values are set for each MC sample (`mcInfo` and `fdata` in `TriggerSF()`)
- Trigger confguration (`trigger` var in `TriggerSF()`)
- Binning (`binning` var in `make3DSFs()`)


