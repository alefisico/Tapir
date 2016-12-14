import socket
from redis import Redis
from rq import Queue, get_failed_queue
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
import os

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3

import TTH.Plotting.joosep.plotlib as plotlib #heplot, 
from launcher import make_workdir, waitJobs
from job import plot

#FIXME: configure all these via conf file!
procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
    ("diboson", "diboson"),
    ("stop", "single top"),
    ("ttv", "tt+V"),
    ("wjets", "w+jets"),
    ("dy", "dy")
]
procs = [x[0] for x in procs_names]

syst_pairs = [
    ("__puUp", "__puDown"),
    ("__CMS_scale_jUp", "__CMS_scale_jDown"),
    ("__CMS_res_jUp", "__CMS_res_jDown"),
    ("__CMS_ttH_CSVcferr1Up", "__CMS_ttH_CSVcferr1Down"),
    ("__CMS_ttH_CSVcferr2Up", "__CMS_ttH_CSVcferr2Down"),
    ("__CMS_ttH_CSVhfUp", "__CMS_ttH_CSVhfDown"),
    ("__CMS_ttH_CSVhfstats1Up", "__CMS_ttH_CSVhfstats1Down"),
    ("__CMS_ttH_CSVhfstats2Up", "__CMS_ttH_CSVhfstats2Down"),
    ("__CMS_ttH_CSVjesUp", "__CMS_ttH_CSVjesDown"),
    ("__CMS_ttH_CSVlfUp", "__CMS_ttH_CSVlfDown"),
    ("__CMS_ttH_CSVlfstats1Up", "__CMS_ttH_CSVlfstats1Down"),
    ("__CMS_ttH_CSVlfstats2Up", "__CMS_ttH_CSVlfstats2Down")
]

def get_base_plot(basepath, outpath, analysis, category, variable):
    s = "{0}/{1}/{2}".format(basepath, analysis, category)
    return {
        "infile": s + ".root",
        "histname": "__".join([category, variable]),
        "outname": os.path.abspath("/".join([outpath, category, variable])),
        "procs": procs_names,
        "signal_procs": ["ttH_hbb"],
        "dataname": "data",
        "rebin": 1,
        "xlabel": plotlib.varnames[variable] if variable in plotlib.varnames.keys() else "PLZ add me to Varnames in plotlib.py",
        "xunit": plotlib.varunits[variable] if variable in plotlib.varunits.keys() else "",
        "legend_fontsize": 12,
        "legend_loc": "best",
        "colors": [plotlib.colors.get(p) for p in procs],
        "do_legend": True,
        "show_overflow": True,
        "title_extended": r"$,\ \mathcal{L}=17\ \mathrm{fb}^{-1}$, ",
        "systematics": syst_pairs,
        "do_syst": True, #currently crashes with True due to some dvipng/DISPLAY issue
        "blindFunc": "blind_mem" if "common" in variable else "no_blind",
    }


def run_plots(workdir, analysis, path_to_files, redis_conn, qmain, qfail):
    all_jobs = []
    for cat in analysis.categories:
        outpath = os.path.abspath("/".join([workdir, "plots", cat.name, cat.discriminator.name]))
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        all_jobs += [
            qmain.enqueue_call(
                func=plot,
                args=[
                    get_base_plot(
                        path_to_files, 
                        os.path.join(workdir, "plots"),
                        "",
                        cat.name,
                        cat.discriminator.name
                    )
                ],
                timeout = 20*60,
                result_ttl = 60*60,
                meta = {"retries": 0, "args": ""},
            )
        ]

    waitJobs(all_jobs, redis_conn, qmain, qfail)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description='Runs the workflow'
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Analysis configuration",
        type = str,
        required = True
    )
    parser.add_argument(
        '--hostname',
        action = "store",
        help = "Redis hostname",
        type = str,
        default = socket.gethostname()
    )
    parser.add_argument(
        '--port',
        action = "store",
        help = "Redis port",
        type = int,
        default = 6379
    )
    args = parser.parse_args()

    redis_conn = Redis(host=args.hostname, port=args.port)
    qmain = Queue("default", connection=redis_conn, async=True)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)

    analysis_name, analysis = analysisFromConfig(args.config)

    workdir = make_workdir()

    run_plots(workdir, analysis, os.path.join(os.path.dirname(args.config), "categories"), redis_conn, qmain, qfail)