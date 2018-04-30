import sys, re, shutil
from copy import deepcopy
import subprocess
import json

from splitLumi import getLumiListInFiles, chunks 
from FWCore.PythonUtilities.LumiList import LumiList

#the golden json file for data
json_file = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"

#Each time you call multicrab.py, you choose to submit jobs from one of these workflows
workflows = [
    "data", #real data
    "data_leptonic", #real data, SL and DL only
    "data_hadronic", #real data, FH only
    "leptonic", #ttH with SL/DL decays
    "leptonic_nome", #ttH with SL/DL decays
    "hadronic", #ttH with FH decays
    "hadronic_nome",
    "hadronic_nome_testing", #ttH with FH decays data + MC
    "QCD_nome", #QCD samples without MEM
    "pilot", #ttH sample only, with no MEM
    "signal", #signal sample with common config
    "testing", #single-lumi jobs, a few samples
    "testing_withme", #single-lumi jobs, a few samples
    "allmc_nome", # SL, DL and FH, no matrix element
    "testall",#Test all samples w/ small nJobs and no ME
    "testing_hadronic_withme", #single-lumi jobs, a few samples
    "memcheck", #specific MEM jobs that contain lots of hypotheses for validation, many interpretations
    "memcheck2", #specific MEM jobs that contain lots of hypotheses for validation, JES variations
    #"memcheck3", #Sudakov/Recoil
]

import argparse
parser = argparse.ArgumentParser(description='Submits crab jobs')
parser.add_argument('--workflow', action="store", required=True, help="Type of workflow to run", type=str, choices=workflows)
parser.add_argument('--tag', action="store", required=True, help="the version tag for this run, e.g. VHBBHeppyV22_tthbbV10_test1")
parser.add_argument('--dataset', action="store", required=False, help="submit only matching datasets (shortname)", default="*") 
parser.add_argument('--recovery', action="store", required=False, help="the patand json_filename of the job to recover", default="")#Never tested it. Use with caution
args = parser.parse_args()

#list of configurations that we are using, should be in TTH/MEAnalysis/python/
me_cfgs = {
    "default": "MEAnalysis_cfg_heppy.py",
    "cMVA": "MEAnalysis_cfg_heppy.py",
    "nome": "cfg_noME.py",
    "nometesting": "cfg_noME_testing.py",
    "leptonic": "cfg_leptonic.py",
    "nome_hadSel" : "cfg_noME_FH.py",
    "hadronic": "cfg_FH.py",
    "memcheck": "cfg_memcheck.py",
    "memcheck2": "cfg_memcheck2.py"
}

sets_data = [
    "/MuonEG/Run2017B-31Mar2018-v1/MINIAOD",
    "/MuonEG/Run2017C-31Mar2018-v1/MINIAOD",
    "/MuonEG/Run2017D-31Mar2018-v1/MINIAOD",
    "/MuonEG/Run2017E-31Mar2018-v1/MINIAOD",
    "/MuonEG/Run2017F-31Mar2018-v1/MINIAOD",

    "/DoubleMuon/Run2017B-31Mar2018-v1/MINIAOD",
    "/DoubleMuon/Run2017C-31Mar2018-v1/MINIAOD",
    "/DoubleMuon/Run2017D-31Mar2018-v1/MINIAOD",
    "/DoubleMuon/Run2017E-31Mar2018-v1/MINIAOD",
    "/DoubleMuon/Run2017F-31Mar2018-v1/MINIAOD",
    
    "/DoubleEG/Run2017B-31Mar2018-v1/MINIAOD",
    "/DoubleEG/Run2017C-31Mar2018-v1/MINIAOD",
    "/DoubleEG/Run2017D-31Mar2018-v1/MINIAOD",
    "/DoubleEG/Run2017E-31Mar2018-v1/MINIAOD",
    "/DoubleEG/Run2017F-31Mar2018-v1/MINIAOD",

    "/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD",
    "/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD",
    "/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD",
    "/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD",
    "/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD",

    "/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD",
    "/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD",
    "/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD",
    "/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD",
    "/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD",

    "/JetHT/Run2017B-31Mar2018-v1/MINIAOD",
    "/JetHT/Run2017C-31Mar2018-v1/MINIAOD",
    "/JetHT/Run2017D-31Mar2018-v1/MINIAOD",
    "/JetHT/Run2017E-31Mar2018-v1/MINIAOD",
    "/JetHT/Run2017F-31Mar2018-v1/MINIAOD",

    "/BTagCSV/Run2017B-31Mar2018-v1/MINIAOD",
    "/BTagCSV/Run2017C-31Mar2018-v1/MINIAOD",
    "/BTagCSV/Run2017D-31Mar2018-v1/MINIAOD",
    "/BTagCSV/Run2017E-31Mar2018-v1/MINIAOD",
    "/BTagCSV/Run2017F-31Mar2018-v1/MINIAOD",
]

#all available datasets.
datasets = {}
datanames = []
for sd in sets_data:
    name = "-".join(sd.split("/")[1:3])
    datanames += [name]
    datasets[name] = {
        "ds": sd,
        "maxlumis": -1,
        "perjob": 30,
        "runtime": 20, #hours
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script_data.sh',
        "json" : "",
        "isMC" : False
    }



#Add MC datasets from JSON files
import multicrabHelper
datasets.update(multicrabHelper.getDatasets(mem_cfg = me_cfgs["default"], script = "heppy_crab_script.sh"))


#now we construct the workflows from all the base datasets
workflow_datasets = {}
workflow_datasets["leptonic"] = {}
for k in [
        "ttHTobb",
        #"ttHToNonbb",
        #"TTbar_had",
        "TTbar_sl1",
        "TTbar_dl1",
        #"ttbb",
        #"TTbar_isr_up",
        #"TTbar_isr_down1",
        #"TTbar_isr_down2",
        #"TTbar_fsr_up1",
        #"TTbar_fsr_up2",
        #"TTbar_fsr_down",
        #"TTbar_tune_up1",
        #"TTbar_tune_up2",
        #"TTbar_tune_down1",
        #"TTbar_tune_down2",
        #"TTbar_hdamp_up1",
        #"TTbar_hdamp_up2",
        #"TTbar_hdamp_down1",
        #"TTbar_hdamp_down2",
        #"ww1", "ww2",
        #"wz1", "wz2",
        #"zz1", "zz2",
        #"st_t", "stbar_t",
        #"st_tw", "stbar_tw",
        #"st_s",
        #"ttw_wlnu1",
        #"ttw_wlnu2",
        #"ttz_zllnunu1",
        #"ttz_zllnunu2",
        #"ttw_wqq",
        #"ttz_zqq",
        #"wjets",
        #"dy_50_inf1", "dy_50_inf2", "dy_10_50"
    ]:
    D = deepcopy(datasets[k])
    D["mem_cfg"] = "cfg_leptonic.py"
    workflow_datasets["leptonic"][k] = D

#now we construct the workflows from all the base datasets
workflow_datasets["memcheck"] = {}
for k in [
        "ttHTobb",
        "ttHToNonbb",
        "TTbar_had",
        #"ttbb",
        "TTbar_sl1",
        "TTbar_dl1",
    ]:
    D = deepcopy(datasets[k])
    D["mem_cfg"] = "cfg_memcheck.py"
    workflow_datasets["memcheck"][k] = D

workflow_datasets["memcheck2"] = {}
for k in [
        "ttHTobb",
    ]:
    D = deepcopy(datasets[k])
    D["mem_cfg"] = "cfg_memcheck2.py"
    workflow_datasets["memcheck2"][k] = D

workflow_datasets["signal"] = {}
for k in ["ttHTobb", "ttHToNonbb", "TTbar_had","TTbar_sl1",]:
    D = deepcopy(datasets[k])
    workflow_datasets["signal"][k] = D

workflow_datasets["leptonic_nome"] = {}
for k in [
        "ttHTobb",
        "ttHToNonbb",
        "TTbar_had",
        "TTbar_sl1",
        "TTbar_dl1",
        #"ww1", "ww2",
        #"wz1", "wz2",
        #"zz1", "zz2",
        #"st_t", "stbar_t",
        #"st_tw", "stbar_tw",
        #"st_s",
        #"ttw_wlnu1",
        #"ttw_wlnu2",
        #"ttw_wqq",
        #"ttz_zqq",
        # "wjets_ht_100_200",
        # "wjets_ht_200_400",
        # "wjets_ht_400_600",
        # "wjets_ht_600_800",
        # "wjets_ht_800_1200",
        # "wjets_ht_1200_2500",
        # "wjets_ht_2500_inf",
        #"dy_10_50",
        #"dy_50_inf"
    ]:
    D = deepcopy(datasets[k])

    D["mem_cfg"] = "cfg_noME.py"
    workflow_datasets["leptonic_nome"][k] = D

workflow_datasets["data"] = {}
for k in datasets.keys():
    if "data" in datasets[k]["script"]:
        D = deepcopy(datasets[k])
#        D["maxlumis"] = 1
        workflow_datasets["data"][k] = D

workflow_datasets["data_leptonic"] = {}
for k in datasets.keys():
    # Ignore hadronic
    if k.startswith("JetHT") or k.startswith("BTagCSV"):
        continue
    
    if "data" in datasets[k]["script"]:
        D = deepcopy(datasets[k])
        workflow_datasets["data_leptonic"][k] = D

workflow_datasets["data_hadronic"] = {}
for k in datasets.keys():
    if "JetHT" in k or "BTagCSV" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["hadronic"]
        D["perjob"] = 20
        D["runtime"] = 24
        workflow_datasets["data_hadronic"][k] = D

workflow_datasets["hadronic"] = {}
for k in datasets.keys():
    if "QCD300_ext1" in k: #"TTbar_inc" in k: #"QCD" in k or or "ttH" in k 
        D = deepcopy(datasets[k])
    if k == "ttHTobb":
        D["perjob"] = 4 #for ttH target 500 ev/job => 4 LSs => 8hrs/job
    elif k == "TTbar_inc":
        D["perjob"] = 70 #for ttbar target 8000 ev/job => 52 LSs => 6hrs/job
        D["mem_cfg"] = me_cfgs["hadronic"]
        D["runtime"] = max(20,D["runtime"])
#        D["maxlumis"] = 1
        workflow_datasets["hadronic"][k] = D

        
workflow_datasets["QCD_nome"] = {}
for k in datasets.keys():
    if "QCD" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["nome"]
        workflow_datasets["QCD_nome"][k] = D


workflow_datasets["allmc_nome"] = {}
for k in datasets.keys():
    if "QCD" in k or k in ["ttHTobb", "ttHToNonbb", "TTbar_had", "TTbar_sl1", "TTbar_dl1",] :
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["nome"]
        workflow_datasets["allmc_nome"][k] = D


workflow_datasets["hadronic_nome"] = {}
for k in datasets.keys():
    if k == "TTbar_had" or k == "ttHTobb" or "QCD" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["nome_hadSel"]
        workflow_datasets["hadronic_nome"][k] = D
    if ("BTagCSV" in k or "JetHT" in k) and "Run2017C" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["nome_hadSel"]
        D["perjob"] = 75
        D["runtime"] = 24
        D["json"] = json_file 
        workflow_datasets["hadronic_nome"][k] = D

workflow_datasets["hadronic_nome_testing"] = {}
for k in  workflow_datasets["hadronic_nome"].keys():
    D = deepcopy(workflow_datasets["hadronic_nome"][k])
    D["maxlumis"] = 2
    D["runtime"] = 1
    workflow_datasets["hadronic_nome_testing"][k] = D


workflow_datasets["testall"] = {}
for k in [ "SingleElectron-Run2017F-31Mar2018-v1",
           "MuonEG-Run2017F-31Mar2018-v1",
           "JetHT-Run2017B-31Mar2018-v1",
           "BTagCSV-Run2017B-31Mar2018-v1",
           "TTbar_had",
           "TTbar_sl1",
           "ttHTobb",
           "QCD1500to2000"
]:
    D = deepcopy(datasets[k])
    D["mem_cfg"] = me_cfgs["nometesting"]
    D["perjob"] = 1
    D["maxlumis"] = 1
    D["runtime"] = 4
    if not D["isMC"]:
        D["json"] = json_file
    workflow_datasets["testall"][k] = D
    
#Pilot job for updating transfer functions, retraining BLR
workflow_datasets["pilot"] = {}
pilot_name = 'ttHTobb'
D = deepcopy(datasets[pilot_name])
D["perjob"] = 20
D["mem_cfg"] = me_cfgs["nome"]
workflow_datasets["pilot"][pilot_name] = D

#1-lumi per job, 10 job testing of a few samples
workflow_datasets["testing"] = {}

for k in [
    "SingleElectron-Run2017F-31Mar2018-v1",
    "ttHTobb",
    ]:
    D = deepcopy(datasets[k])
    D["maxlumis"] = 4
    D["perjob"] = 2
    if not D["isMC"]:
        D["maxlumis"] = 10
        D["perjob"] = 5
        D["json"] = json_file
    D["runtime"] = 2
    D["mem_cfg"] = "cfg_noME.py"
    workflow_datasets["testing"][k] = D

datasets_local = {
    "mc": {
        "mem_cfg": me_cfgs["nome"],

        "script": 'heppy_crab_script.sh'
    },
    "data": {
        "maxlumis": -1,
        "mem_cfg": me_cfgs["nome"],
        "script": 'heppy_crab_script_data.sh'
    }
}

workflow_datasets["testing_withme"] = {}
for k in ["TTbar_had","TTbar_sl1","TTbar_dl1"]:
    D = deepcopy(datasets[k])
    D["perjob"] = int(D["perjob"]/10)
    D["maxlumis"] = 10 * D["perjob"]
    D["runtime"] = int(D["runtime"]/5)
    D["mem_cfg"] = me_cfgs["default"]
    workflow_datasets["testing_withme"][k] = D

workflow_datasets["testing_hadronic_withme"] = {}
for k in ["ttHTobb"]: #"JetHT-Run2016D-23Sep2016-v1"]: #, "QCD1000", "JetHT-Run2016B-PromptReco-v1"]:
    D = deepcopy(datasets[k])
    if k == "ttHTobb":
        D["perjob"] = 1 #for ttH target 500 ev/job => 4 LSs => 8hrs/job
    else:
        D["perjob"] = 20 #for ttbar target 8000 ev/job => 52 LSs => 6hrs/job
    D["maxlumis"] = 4 * D["perjob"]
    D["runtime"] = 20
    D["mem_cfg"] = me_cfgs["hadronic"]
    workflow_datasets["testing_hadronic_withme"][k] = D



#Now select a set of datasets
sel_datasets = workflow_datasets[args.workflow]
print sel_datasets
raw_input("Press ret to start")
if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.UserUtilities import getUsernameFromSiteDB
    
    def submit(config):
        res = crabCommand('submit', config = config)
        with open(config.General.workArea + "/crab_" + config.General.requestName + "/crab_config.py", "w") as fi:
            fi.write(config.pythonise_())

    from CRABClient.UserUtilities import config
    config = config()
    if args.recovery:
	submitname = args.recovery.split("/")[1].split(".json")[0]
    else:
	submitname = args.tag
    
    config.General.workArea = 'crab_projects/' + submitname
    config.General.transferLogs = True
   
    #Disable overflow to prevent buggy site T2_US_UCSD
    config.section_("Debug")
    config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'heppy_crab_fake_pset.py'
    config.JobType.maxMemoryMB = 2500
    #with 3000MB, almost no jobs will run at T2_CH_CSCS, our default site.
    #therefore, 3000MB should only be used for resubmissions

    import os
    os.system("tar czf python.tar.gz --directory $CMSSW_BASE python `find $CMSSW_BASE/src -name python | perl -pe s#$CMSSW_BASE/## `")
    os.system("tar czf data.tar.gz --dereference --directory $CMSSW_BASE/src/TTH/MEAnalysis root")
    if not "testing" in args.workflow:
        os.system("make -sf $CMSSW_BASE/src/TTH/Makefile get_hashes")
        os.system("echo '\n\n{0}\n-------------' >> $CMSSW_BASE/src/TTH/logfile.md".format(submitname))
        os.system("cat $CMSSW_BASE/src/TTH/hash >> $CMSSW_BASE/src/TTH/logfile.md")
       
    nanoTools_dir = os.environ.get("CMSSW_BASE") + "/src/PhysicsTools/NanoAODTools"
    nano_dir = os.environ.get("CMSSW_BASE") + "/src/PhysicsTools/NanoAOD"
    tth_data_dir = os.environ.get("CMSSW_BASE") + "/src/TTH/MEAnalysis/data"
    
    config.JobType.inputFiles = [
        'hash',
        'analyze_log.py',
        'FrameworkJobReport.xml',
        'env.sh',
        'post.sh',
        'heppy_crab_script.py',
        'mem_crab_script.py',
        'heppy_crab_functions.py',
        'python.tar.gz',
        'data.tar.gz',
        'MEAnalysis_heppy.py',
        #nanoTools_dir + '/scripts/nano_postproc.py',
        #nanoTools_dir + '/python/postprocessing/modules/jme/jecUncertainties.py'
    ]

    config.Data.inputDBS = 'global'
    config.Data.splitting = 'LumiBased'
    config.Data.publication = False
    config.Data.ignoreLocality = False
    config.Data.allowNonValidInputDataset = True
    
    #config.Site.whitelist = ["T2_US_Vanderbilt"]
    config.Site.blacklist = [
        "T3_UK_London_QMUL",
    ] 

    config.Site.storageSite = "T3_CH_PSI"

    #loop over samples
    for sample in sel_datasets.keys():
        if not args.dataset=="*" and not args.dataset in sample:
	    continue
	if args.recovery and not sample in args.recovery:
	    continue
        if not args.recovery and sel_datasets[sample]["json"] != "":
            print "Setting json for Dataset:",sample
            config.Data.lumiMask = sel_datasets[sample]["json"]
        else:
            config.Data.lumiMask = args.recovery


        print 'submitting ' + sample, sel_datasets[sample]

        mem_cfg = sel_datasets[sample]["mem_cfg"]
        config.JobType.scriptExe = sel_datasets[sample]["script"]
        
        dataset = sel_datasets[sample]["ds"]
        nlumis = sel_datasets[sample]["maxlumis"]
        perjob = sel_datasets[sample]["perjob"]
        runtime_min = int(sel_datasets[sample].get("runtime_min", sel_datasets[sample]["runtime"]*60))

        config.JobType.maxJobRuntimeMin = runtime_min
        if args.recovery:
	    config.General.requestName = submitname
	else:
	    config.General.requestName = sample + "_" + submitname
        config.Data.inputDataset = dataset
        config.Data.unitsPerJob = perjob
        config.Data.totalUnits = nlumis
        config.Data.outputDatasetTag = submitname
        try:
            config.Data.outLFNDirBase = '/store/user/{0}/tth/'.format(getUsernameFromSiteDB()) + submitname
        except Exception as e:
            config.Data.outLFNDirBase = '/store/user/{0}/tth/'.format(os.environ["USER"]) + submitname

        config.JobType.scriptArgs = ['ME_CONF={0}'.format(mem_cfg)]
        print  config.JobType.scriptArgs
        
        try:
            submit(config)
        except Exception as e:
            print e
            print "skipping"
