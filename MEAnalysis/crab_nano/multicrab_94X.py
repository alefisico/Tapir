import sys, re, shutil
from copy import deepcopy
import subprocess
import json

from splitLumi import getLumiListInFiles, chunks 
from FWCore.PythonUtilities.LumiList import LumiList
das_client = "/afs/cern.ch/user/v/valya/public/das_client.py"

#Each time you call multicrab.py, you choose to submit jobs from one of these workflows
workflows = [
    "data", #real data
    "data_leptonic", #real data, SL and DL only
    "data_hadronic", #real data, FH only
    "leptonic", #ttH with SL/DL decays
    "leptonic_nome", #ttH with SL/DL decays
    "hadronic", #ttH with FH decays
    "QCD_nome", #QCD samples without MEM
    "pilot", #ttH sample only, with no MEM
    "signal", #signal sample with common config
    "testing", #single-lumi jobs, a few samples
    "localtesting", #run combined jobs locally
    "localtesting_withme", #run combined jobs locally
    "testing_withme", #single-lumi jobs, a few samples
    "allmc_nome", # SL, DL and FH, no matrix element
    "testing_hadronic_withme", #single-lumi jobs, a few samples
    "memcheck", #specific MEM jobs that contain lots of hypotheses for validation, many interpretations
    "memcheck2", #specific MEM jobs that contain lots of hypotheses for validation, JES variations
    #"memcheck3", #Sudakov/Recoil
]

import argparse
parser = argparse.ArgumentParser(description='Submits crab jobs')
parser.add_argument('--workflow', action="store", required=True, help="Type of workflow to run", type=str, choices=workflows)
parser.add_argument('--tag', action="store", required=True, help="the version tag for this run, e.g. VHBBHeppyV22_tthbbV10_test1")
parser.add_argument('--dataset', action="store", required=False, help="submit only matching datasets (shortname)", default="*") #FROM FH branch -> Not added yet
parser.add_argument('--recovery', action="store", required=False, help="the patand json_filename of the job to recover", default="")#FROM FH branch -> Not added yet
args = parser.parse_args()

localtesting = "localtesting" in args.workflow

#list of configurations that we are using, should be in TTH/MEAnalysis/python/
me_cfgs = {
    "default": "MEAnalysis_cfg_heppy.py",
    "cMVA": "MEAnalysis_cfg_heppy.py",
    "nome": "cfg_noME.py",
    "leptonic": "cfg_leptonic.py",
    "hadronic": "cfg_FH.py",
    "memcheck": "cfg_memcheck.py",
    "memcheck2": "cfg_memcheck2.py"
}

sets_data = [
    "/DoubleEG/Run2017B-17Nov2017-v1/MINIAOD",
    "/DoubleEG/Run2017C-17Nov2017-v1/MINIAOD",
    "/DoubleEG/Run2017D-17Nov2017-v1/MINIAOD",
    "/DoubleEG/Run2017E-17Nov2017-v1/MINIAOD",
    "/DoubleEG/Run2017F-17Nov2017-v1/MINIAOD",
    
    "/DoubleMuon/Run2017B-17Nov2017-v1/MINIAOD",
    "/DoubleMuon/Run2017C-17Nov2017-v1/MINIAOD",
    "/DoubleMuon/Run2017D-17Nov2017-v1/MINIAOD",
    "/DoubleMuon/Run2017E-17Nov2017-v1/MINIAOD",
    "/DoubleMuon/Run2017F-17Nov2017-v1/MINIAOD",

    "/MuonEG/Run2017B-17Nov2017-v1/MINIAOD",
    "/MuonEG/Run2017C-17Nov2017-v1/MINIAOD",
    "/MuonEG/Run2017D-17Nov2017-v1/MINIAOD",
    "/MuonEG/Run2017E-17Nov2017-v1/MINIAOD",
    "/MuonEG/Run2017F-17Nov2017-v1/MINIAOD",
   
    "/SingleMuon/Run2017B-17Nov2017-v1/MINIAOD",
    "/SingleMuon/Run2017C-17Nov2017-v1/MINIAOD",
    "/SingleMuon/Run2017D-17Nov2017-v1/MINIAOD",
    "/SingleMuon/Run2017E-17Nov2017-v1/MINIAOD",
    "/SingleMuon/Run2017F-17Nov2017-v1/MINIAOD",
   
    "/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD",
    "/SingleElectron/Run2017C-17Nov2017-v1/MINIAOD",
    "/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD",
    "/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD",
    "/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD",
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
        "script": 'heppy_crab_script_data.sh'
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
        "TTbar_had",
        "TTbar_sl1",#"TTbar_sl2",
        "TTbar_dl1",# "TTbar_dl2",
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
        "TTbar_sl1","TTbar_sl2",
        "TTbar_dl1", "TTbar_dl2",
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
for k in ["ttHTobb", "ttHToNonbb", "TTbar_had","TTbar_sl1","TTbar_sl2"]:
    D = deepcopy(datasets[k])
    workflow_datasets["signal"][k] = D

workflow_datasets["leptonic_nome"] = {}
for k in [
        "ttHTobb",
        "ttHToNonbb",
        "TTbar_had",
        "TTbar_sl1","TTbar_sl2",
        "TTbar_dl1", "TTbar_dl2",
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
    if k.startswith("JetHT"):
        continue
    
    if "data" in datasets[k]["script"]:
        D = deepcopy(datasets[k])
        workflow_datasets["data_leptonic"][k] = D

workflow_datasets["data_hadronic"] = {}
for k in datasets.keys():
    if "JetHT" in k:
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
    if "QCD" in k or k in ["ttHTobb", "ttHToNonbb", "TTbar_had", "TTbar_sl1", "TTbar_sl2", "TTbar_dl1","TTbar_dl2"] :
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["nome"]
        workflow_datasets["allmc_nome"][k] = D


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
    "ttHTobb",
    #"TTbar_inc",
    #"SingleMuon-Run2016H-03Feb2017_ver3-v1"
    ]:
    D = deepcopy(datasets[k])
    D["maxlumis"] = 4
    D["perjob"] = 2
    if "data" in D["script"]:
        D["maxlumis"] = 4
        D["perjob"] = 2
    D["runtime"] = 0.2
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

workflow_datasets["localtesting"] = {}
for k in ["mc", "data"]:
    D = deepcopy(datasets_local[k])
    D["mem_cfg"] = "cfg_noME.py"
    workflow_datasets["localtesting"][k] = D

workflow_datasets["localtesting_withme"] = {}
for k in ["mc", "data"]:
    D = deepcopy(datasets_local[k])
    D["mem_cfg"] = me_cfgs["leptonic"]
    workflow_datasets["localtesting_withme"][k] = D

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
"""
TODO: Chekc if DS is nanoAOD to change workflow
#Check if Dataset are nanoAOD
nanoFlag = None
for datasetKey in sel_datasets:
    isNANOAOD = workflow_datasets[args.workflow][datasetKey]["isNANOAOD"]
    if nanoFlag is None:
        nanoFlag = isNANOAOD
    if not(nanoFlag and isNANOAOD):
        exit() 
"""
if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.UserUtilities import getUsernameFromSiteDB
    
    def submit(config):
        res = crabCommand('submit', config = config)
        with open(config.General.workArea + "/crab_" + config.General.requestName + "/crab_config.py", "w") as fi:
            fi.write(config.pythonise_())

    def localsubmit(config, dname, opts):
        TMPDIR = "/scratch/{0}/crab_work/{1}/crab_{2}".format(os.environ["USER"], args.tag, dname)
        CMSSW_VERSION = "CMSSW_9_4_1"
        workdir = os.path.join(TMPDIR, CMSSW_VERSION, "work")
        try: 
            shutil.rmtree(TMPDIR)
        except Exception as e:
            pass
        os.makedirs(TMPDIR)
        os.system("cd {0}".format(TMPDIR))
        pwd = os.getcwd() 
        os.chdir(TMPDIR)
        os.system("scramv1 project CMSSW {0}".format(CMSSW_VERSION))
        os.makedirs(workdir)
        os.chdir(pwd)
        for inf in config.JobType.inputFiles + [config.JobType.scriptExe, 'PSet_local.py']:
            shutil.copy(inf, os.path.join(workdir, os.path.basename(inf)))
        os.system("cp -r $CMSSW_BASE/lib {0}/".format(workdir)) 
        os.system("mv {0}/PSet_local.py {0}/PSet.py".format(workdir)) 
        os.system("cp {0} {1}/x509_proxy".format(os.environ["X509_USER_PROXY"], workdir)) 
        os.system("cp -r $CMSSW_BASE/lib/slc*/proclib {0}/lib/slc*/".format(workdir)) 
        os.system('find $CMSSW_BASE/src/ -path "*/data/*" -type f | sed -s "s|$CMSSW_BASE/||" > files')
        os.system('cp files $CMSSW_BASE/; cd $CMSSW_BASE; for f in `cat files`; do cp --parents $f {0}/; done'.format(workdir))
        runfile = open(workdir+"/run.sh", "w")
        runfile.write(
            """
            #!/bin/bash
            source /cvmfs/cms.cern.ch/cmsset_default.sh
            scram b ProjectRename
            eval `scramv1 runtime -sh`
            scram b
            env
            ./{0} 1 {1}
            """.format(config.JobType.scriptExe, " ".join(config.JobType.scriptArgs)).strip() + '\n'
        )
        runfile.close()
        os.system('chmod +x {0}/run.sh'.format(workdir))
        os.system('cd {0}/{1};eval `scram runtime -sh`;scram b;'.format(TMPDIR, CMSSW_VERSION))
        archive_name = "_".join([dname, args.workflow, args.tag])
        os.system('cd {0};tar zcfv job_{1}.tar.gz {2} > {1}.log'.format(TMPDIR, archive_name, CMSSW_VERSION))
        os.system("cp {0}/job_{1}.tar.gz ./".format(TMPDIR, archive_name))
        #os.system("cp -r $CMSSW_BASE/src {0}/".format(workdir)) 

    from CRABClient.UserUtilities import config
    config = config()
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
        tth_data_dir + '/BDT.pickle',
        #nanoTools_dir + '/scripts/nano_postproc.py',
        #nanoTools_dir + '/python/postprocessing/modules/jme/jecUncertainties.py'
    ]

    config.Data.inputDBS = 'global'
    config.Data.splitting = 'LumiBased'
    config.Data.publication = False
    config.Data.ignoreLocality = False
    config.Data.allowNonValidInputDataset = True

    #config.Site.whitelist = ["T2_CH_CSCS", "T1_US_FNAL", "T2_DE_DESY", "T1_DE_KIT"]
    config.Site.blacklist = ["T2_US_UCSD", "T3_UK_London_RHUL", "T3_UK_London_QMUL"]

    config.Site.storageSite = "T3_CH_PSI"

    #loop over samples
    for sample in sel_datasets.keys():
        print 'submitting ' + sample, sel_datasets[sample]
        
        mem_cfg = sel_datasets[sample]["mem_cfg"]
        config.JobType.scriptExe = sel_datasets[sample]["script"]
        
        if not localtesting:
            dataset = sel_datasets[sample]["ds"]
            nlumis = sel_datasets[sample]["maxlumis"]
            perjob = sel_datasets[sample]["perjob"]
            runtime_min = int(sel_datasets[sample].get("runtime_min", sel_datasets[sample]["runtime"]*60))

            config.JobType.maxJobRuntimeMin = runtime_min
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
        
        if localtesting:
            localsubmit(config, sample, sel_datasets[sample])
        else:
            try:
                submit(config)
            except Exception as e:
                print e
                print "skipping"
