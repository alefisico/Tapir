import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os
import rootpy
import uuid
import glob, time
import multiprocessing

from rq import Queue
from redis import Redis
from multijob import draw_hist, get_count, draw_hist_wrap 

def waitJobs(jobs):
    done = False 
    while not done:
        num_finished = 0
        for job in jobs:
            if job.status == "finished":
                num_finished += 1
            if job.status == "failed":
                job.refresh()
                print job.exc_info
                raise Exception("failed")
        if num_finished == len(jobs):
            done = True
        time.sleep(1)

if __name__ == "__main__":
    redis_conn = Redis(host="t3ui02", port=6379)
    qmain = Queue("default", connection=redis_conn)  # no args implies the default queue
    
    os.environ["CMSSW_BASE"] = "/mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW"
    sys.path.append("/mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW/python/")
    from TTH.MEAnalysis.samples_base import getSitePrefix, chunks
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

    print "opening analysis"
    analysis = analysisFromConfig("/mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW/src/TTH/MEAnalysis/data/lowtag_csv.cfg")

    print "getting weights"
    #ngen = {}
    #ngen["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"] = 3754591.0
    #ngen["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"] = 73672901.0
    weights = {}
    for samp in analysis.samples:
        if samp.schema == "mc":
            jobs = []
            for fi in samp.file_names:
                jobs += [
                    qmain.enqueue_call(get_count, args=([fi], ), timeout=300)
                ]
            waitJobs(jobs) 
            ngen = sum([j.result for j in jobs])
            print samp.name, ngen
            weight = samp.xsec * 3970.0/float(ngen[samp.name])
            weights[samp.name] = weight
   

    def plot_cut(analysis, variable, bins, cut, weights):
        print variable, cut
        args = {}
        for samp in analysis.samples:
            weight = "1.0"
            if samp.schema == "mc":
                weight = "{0}*btagWeightCSV*puWeight".format(weights[samp.name])
            _cut = cut 
            if samp.schema == "data":
                _cut = cut + " && json==1"
            cutstring = "({0}) * ({1})".format(weight, _cut)
            args[samp.name] = (samp.file_names, variable, bins, cutstring)
        
        t0 = time.time()
        jobs = []
        
        jobs_sample = {}
        for samp in analysis.samples:
            jobs_sample[samp.name] = []

        for samp_name, arg in args.items():
            for fn in arg[0]:
                newarg = ([fn], arg[1], arg[2], arg[3])
                job = qmain.enqueue_call(draw_hist_wrap, args=(newarg,), timeout=300)
                jobs += [job]
                jobs_sample[samp_name] += [job]

        waitJobs(jobs)

        res_multi = {}
        for samp in analysis.samples:
            results = [rootpy.asrootpy(job.result) for job in jobs_sample[samp.name]]
            if len(results) > 0: 
                res_multi[samp.name] = sum(results)
        return res_multi

    cutstring_mu = "(HLT_BIT_HLT_IsoMu24_v==1 || HLT_BIT_HLT_IsoTkMu24_v==1) && is_sl==1 && abs(leps_pdgId[0])==13 && numJets>=4 && nBCSVM>=2"
    cutstring_el = "(HLT_BIT_HLT_Ele27_WPTight_Gsf_v==1) && is_sl==1 && abs(leps_pdgId[0])==11 && numJets>=4 && nBCSVM>=2"

    results = {}
    for cutname, cutstring in [("mu", cutstring_mu), ("el", cutstring_el)]:
        results[cutname] = {}
        results[cutname]["numJets"] = plot_cut(analysis, "numJets", (6, 4, 10), cutstring, weights)
        results[cutname]["nPVs"] = plot_cut(analysis, "nPVs", (40, 0, 40), cutstring, weights)
        results[cutname]["nBCSVM"] = plot_cut(analysis, "nBCSVM", (4, 2, 6), cutstring, weights)
        results[cutname]["jet0_pt"] = plot_cut(analysis, "jets_pt[0]", (100, 0, 300), cutstring, weights)
        results[cutname]["jet3_pt"] = plot_cut(analysis, "jets_pt[3]", (100, 0, 300), cutstring, weights)
        results[cutname]["jet4_pt"] = plot_cut(analysis, "jets_pt[4]", (100, 0, 300), cutstring, weights)
        results[cutname]["jet0_eta"] = plot_cut(analysis, "jets_eta[0]", (100, -2.5, 2.5), cutstring, weights)
        results[cutname]["lep0_pt"] = plot_cut(analysis, "leps_pt[0]", (100, 0, 300), cutstring, weights)
        results[cutname]["lep0_eta"] = plot_cut(analysis, "leps_eta[0]", (100, -2.5, 2.5), cutstring, weights)
        results[cutname]["lep0_phi"] = plot_cut(analysis, "leps_phi[0]", (100, -3.14, 3.14), cutstring, weights)
        results[cutname]["lep1_pt"] = plot_cut(analysis, "leps_pt[1]", (100, 0, 300), cutstring, weights)

    of = ROOT.TFile("out.root", "RECREATE")
    
    def save_hists(hists, dirname):
        d = of.mkdir(dirname)
        d.cd()
        for k, v in hists.items():
            h = v.Clone(k)
            h.SetDirectory(d)
            h.Write()
    for cutname in results.keys():
        for histname in results[cutname].keys():
            save_hists(results[cutname][histname], "{0}_{1}".format(histname, cutname))
    
    of.Close()
