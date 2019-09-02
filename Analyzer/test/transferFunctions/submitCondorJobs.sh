#!/bin/bash

listSamples="2016_TTToSemiLeptonic 2016_ttHTobb_ttToSemiLep 2017_TTToSemiLeptonic 2017_ttHTobb_ttToSemiLep 2018_TTToSemiLeptonic 2018_ttHTobb_ttToSemiLep"

for sample in ${listSamples[@]}; do
    condorFile=${sample}_condorJob
    echo '''universe    =  vanilla
arguments   =  '${sample}'
executable  =  '${PWD}'/condorJob_TF.sh
log         =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId).log
error       =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).err
output      =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).out
initialdir  = '${PWD}'
getenv      =  True
requirements = (OpSysAndVer =?= "SLCern6")
+JobFlavour = "testmatch"
queue
    ''' > condorlogs/${condorFile}.sub

condor_submit condorlogs/${condorFile}.sub
done
