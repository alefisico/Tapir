########################################
# Imports
########################################

import imp, os, sys, time
import subprocess

from CombineHelper import limit, pulls, signal_injection, freeze_limits
from EnvForCombine import PATH, LD_LIBRARY_PATH, PYTHONPATH

import logging

from TTH.Plotting.joosep import plotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=False)

import numpy as np
import json
import ROOT

import multiprocessing

########################################
# Actual work
########################################

LOG_MODULE_NAME = logging.getLogger(__name__)

def get_bins_errs(h):
    labels = []
    bins = []
    errors = []
    for i in range(1, h.GetNbinsX()+1):
        l = h.GetXaxis().GetBinLabel(i)
        y = h.GetBinContent(i)
        e = h.GetBinError(i)
        if "Bin" in l:
            continue
        labels += [l]
        bins += [y]
        errors += [e]
    return labels, np.array(bins), np.array(errors)

def plot_pulls(fn, first=0, maxn=20):
    f = ROOT.TFile(fn)
    hs = f.Get("prefit_fit_s")
    hb = f.Get("prefit_fit_b")

    labels1, bins1, errors1 = get_bins_errs(hs)
    labels2, bins2, errors2 = get_bins_errs(hb)

    plt.figure(figsize=(4,5))
    ys = np.arange(0, len(bins1))[::-1]
    order = sorted(range(len(bins1)), key=lambda x: errors1[x], reverse=False)
    
    plt.errorbar(bins1[order[first:maxn]], ys[first:maxn] - 0.15, xerr=errors1[order[first:maxn]], marker="o", lw=0, elinewidth=2, color="red", label="s+b")
    plt.errorbar(bins2[order[first:maxn]], ys[first:maxn] + 0.15, xerr=errors2[order[first:maxn]], marker="o", lw=0, elinewidth=2, color="blue", label="b")
    
    plt.legend(loc="best")
    plt.grid()
    plt.yticks(ys[first:maxn], [labels1[o] for o in order[first:maxn]]);
    plt.xlim(-1.5, 1.5)
    
    f.Close()

def combine_cards(group_name, group, workdir):
    LOG_MODULE_NAME.info("running limit on group={0}".format(group))
    LOG_MODULE_NAME.info("Doing group={0} consisting of N={1} categories".format(group_name, len(group))) 

    # Get all the per-category datacards and use combineCards to merge into one "group datacard"
    input_dcard_names = ["shapes_{0}.txt".format(c.full_name) for c in group]
    add_dcard_command = ["combineCards.py"] + input_dcard_names 

    LOG_MODULE_NAME.debug("running combineCards.py command: " + " ".join(add_dcard_command))
    

    process = subprocess.Popen(add_dcard_command, 
                               stdout=subprocess.PIPE, 
                               cwd=workdir,
                               #env=dict(os.environ, 
                               #         PATH=PATH,
                               #         LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                               #         PYTHONPATH=PYTHONPATH
                               #     )
        )

    group_dcard, stderr = process.communicate()
    if process.returncode != 0:
        LOG_MODULE_NAME.error("Error running combineCards.py: " + stderr)
        raise Exception("Could not run combineCards command")
    LOG_MODULE_NAME.info("Finished with group_card making")

    # Write the group datacard to a file
    group_dcard_filename = os.path.join(workdir, "shapes_group_{0}.txt".format(group_name))
    group_dcard_file = open(group_dcard_filename, "w")
    group_dcard_file.write(group_dcard)
    group_dcard_file.close()

    LOG_MODULE_NAME.info("Written to file {0}, running limit setting".format(group_dcard_filename))
    return group_dcard_filename

def run_pulls(group_name, dcard_filename, workdir, asimov=True):
    #write constraints
    suf = ""
    if asimov:
        suf += "_asimov"

    for sig in [1, 0]:
        #Run Asimov constraints
        constraints, pulls_file = pulls(dcard_filename, sig, workdir, asimov)
        of = open(workdir + "/constraints_{0}_sig{1}{2}.txt".format(group_name, sig, suf), "w")
        of.write(constraints)
        of.close()

        for ranges in [(0,20), (20, 40), (40, 60)]:
            plot_pulls(os.path.join(workdir, pulls_file), ranges[0], ranges[1])
            plt.title("{0}\nmu={1} Asimov".format(group_name, sig))
            plotlib.svfg(os.path.join(workdir, "pulls_{0}_sig{1}_r{2}_{3}{4}.pdf".format(group_name, sig, ranges[0], ranges[1], suf)))

def run_pulls_tup(tup):
    return run_pulls(*tup)

def main(
        workdir,
        analysis,
        group = None,
        runSignalInjection = False,
        runPulls = False
):
    
    limits = {}

    # Decide what to run on
    if group:
        groups = [group]
    #Run on all groups
    else:
        groups = analysis.groups.keys()

    # Prepare the limit getter

    limits = {}
    for group_name in groups:

        group = [x for x in analysis.groups[group_name] if x.do_limit]

        group_dcard_filename = combine_cards(group_name, group, workdir)

        # Asymptotic limits from observed
        lims = limit(group_dcard_filename, workdir, asimov=False)
        limits[group_name] = lims[0][2]
        # Expected limits from Asimov
        lims = limit(group_dcard_filename, workdir, asimov=True)
        limits[group_name + "_asimov"] = lims[0]
        
        if runSignalInjection:
            limits[group_name + "_siginject"] = signal_injection(group_dcard_filename, workdir)
        
        if runPulls:
            run_pulls(group_name, group_dcard_filename, workdir) 

    # End loop over groups

    # End of loop over analyses
    return limits

def run_limit(group_name, dcard_path, workdir):
    limits = {}
    
    lims = limit(dcard_path, workdir, asimov=True)
    limits[group_name + "_asimov"] = lims[0][2]
    limits[group_name + "_lims_asimov"] = lims[0]
    
    lims = limit(dcard_path, workdir, asimov=False)
    limits[group_name] = lims[0][2]
    limits[group_name + "_lims"] = lims[0]
    
    of = open(os.path.join(workdir, "limits_{0}.json".format(group_name)), "w")
    json.dump(limits, of, indent=2)
    of.close()
    return limits

def run_limit_tup(tup):
    return run_limit(*tup)

def run_parallel(func, tups):
    pool = multiprocessing.Pool(10)
    ret = pool.map(func, tups)
    pool.close()
    return ret

def run_serial(func, tups):
    ret = map(func, tups)
    return ret

def run_freeze(group_name, dcard_path, workdir):
    frozen = freeze_limits(dcard_path)
    of = open(os.path.join(workdir, "frozen_{0}.json".format(group_name)), "w")
    json.dump(frozen, of, indent=2)
    of.close()

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
    
    import argparse
    parser = argparse.ArgumentParser(
        description='Runs the workflow'
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Path to analysis pickle file",
        type = str,
        required = True
    )
    parser.add_argument(
        '--category',
        action = "store",
        help = "Fit category",
        type = str,
    )
    parser.add_argument(
        '--jobtype',
        action = "store",
        help = "Type of job",
        type = str,
        choices = ["main", "pulls", "syst", "limit"]
    )
    parser.add_argument(
        '--runSignalInjection',
        action = "store_true",
        help = "Run signal injection",
    )
    parser.add_argument(
        '--runPulls',
        action = "store_true",
        help = "Run constraints",
    )
    parser.add_argument(
        '--noAsimov',
        action = "store_true",
        help = "Ron only on asimov dataset",
    )
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG
    )
    analysis = Analysis.deserialize(args.config)
    workdir = os.path.dirname(args.config) + "/limits"

    if not args.category:
        print "choose a category:", sorted(analysis.groups.keys())
    else:
        if args.category == "all":
            categories = analysis.groups.keys()
        categories = args.category.split(",")
        if args.jobtype == "main":
            main(workdir, analysis, args.category, args.runSignalInjection, args.runPulls)
        elif args.jobtype == "limit":
            if len(categories)>1:
                run_parallel(run_limit_tup, [(g, os.path.join(workdir, "shapes_group_{0}.txt".format(g)), workdir) for g in categories])
            else:
                run_limit(args.category, os.path.join(workdir, "shapes_group_{0}.txt".format(args.category)), workdir)
        elif args.jobtype == "pulls":
            if len(categories)>1:
                run_parallel(run_pulls_tup, [(g, os.path.join(workdir, "shapes_group_{0}.txt".format(g)), workdir, not args.noAsimov) for g in categories])
            else:
                run_pulls(args.category, os.path.join(workdir, "shapes_group_{0}.txt".format(args.category)), workdir, not args.noAsimov)
        elif args.jobtype == "syst":
            run_freeze(args.category, os.path.join(workdir, "shapes_group_{0}.txt".format(args.category)), workdir)
