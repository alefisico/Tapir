#!/bin/bash
export DATASETPATH="Feb6_leptonic_nome__TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"
export FILE_NAMES="/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_428.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_429.root
/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_43.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_430.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_431.root
/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_432.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_433.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_434.root
/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_435.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_436.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_437.root
/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_438.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_439.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_44.root
/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_440.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_441.root /store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_442.root
/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_443.root"
export MAX_EVENTS=50000
export SKIP_EVENTS=1595
python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/default.cfg
