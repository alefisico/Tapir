#!/bin/bash
export DATASETPATH="Feb6_leptonic_nome__TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"
export FILE_NAMES="/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_155.root"
export MAX_EVENTS=900
export SKIP_EVENTS=1000
python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/default.cfg
