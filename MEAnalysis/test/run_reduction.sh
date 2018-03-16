#!/bin/bash

time python python/reduction.py --files_path /pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/meanalysis/GCba55eb45993c/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8  --prefix TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/ --parallelize multiprocessing --outfile out_1.root
time python python/reduction.py --files_path /pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/meanalysis/GCb6551ff4fd6b/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8 --prefix ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/ --parallelize multiprocessing --outfile out_2.root
