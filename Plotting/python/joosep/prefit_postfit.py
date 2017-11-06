from matplotlib import rc
rc('text', usetex=False)
from TTH.Plotting.joosep import plotlib
import rootpy
import rootpy.io
import sys

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

channel_titles = dict([
    ("sl_j4_t3", "SL 4j3t"),
    ("sl_j4_tge4", "SL 4j4t"),
    ("sl_j5_t3", "SL 5j3t"),
    ("sl_j5_tge4", "SL 5j $\geq$4t"),
    ("sl_jge6_t3", "SL $\geq$6j 3t"),
    ("sl_jge6_tge4", "SL $\geq$6j $\geq$4t"),
    ("dl_jge4_t3", "DL $\geq$4j 3t"),
    ("dl_jge4_tge4", "DL $\geq$4j $\geq$4t")
])

channel_map = dict([
    ("ch1", "sl_j4_t3"),
    ("ch2", "sl_j4_tge4"),
    ("ch3", "sl_j5_t3"),
    ("ch4", "sl_j5_tge4"),
    ("ch5", "sl_jge6_t3"),
    ("ch6", "sl_jge6_tge4"),
    ("ch7", "dl_jge4_tge4"),
    ("ch8", "dl_jge4_t3"),
])

def postprocess_hist(h, template):
    if h.GetNbinsX() != template.GetNbinsX():
        raise Exception("Expected {0} bins but got {1}".format(h.GetNbinsX(), template.GetNbinsX()))
    h2 = template.Clone(h.GetName())
    for ibin in range(h.GetNbinsX()+2):
        h2.SetBinContent(ibin, h.GetBinContent(ibin))
        h2.SetBinError(ibin, h.GetBinError(ibin))
    return h2

def draw_channel_prefit_postfit(ch, chname, template, xlabel, path):

    available_hists = [k.GetName() for k in tf.Get("shapes_prefit").Get(ch).GetListOfKeys()]
    
    procs = []
    for proc in procs_names:
        if proc[0] in available_hists:
            procs += [proc]
    ret = plotlib.draw_data_mc(tf, "",
        procs,
        ["ttH_hbb", "ttH_nonhbb"],
        dataname = "data",
        rebin = 1,
        colors = plotlib.colors,
        pattern="shapes_prefit/" + ch + "/{sample}",
        legend_loc="best",
        title_extended = channel_titles[chname] + " prefit",
        legend_fontsize=12,
        xlabel = xlabel,
        ylabel = "events / bin",
        xunit = "",
        postprocess_hist = lambda x, template=template: postprocess_hist(x, template),
        do_tex = False
    )
    ymax = 2.0*sum([h.GetMaximum() for h in ret["nominal"].values()])
    ret["axes"][0].set_ylim(0, ymax)
    ret["axes"][1].set_ylim(0.5, 1.5)
    plotlib.svfg(path + "/{0}_prefit.pdf".format(chname))

    ret = plotlib.draw_data_mc(tf, "",
        procs,
        ["ttH_hbb", "ttH_nonhbb"],
        dataname = "data",
        rebin = 1,
        colors = plotlib.colors,
        pattern="shapes_fit_s/" + ch + "/{sample}",
        legend_loc="best",
        title_extended = channel_titles[chname] + " postfit",
        legend_fontsize=12,
        xlabel = xlabel,
        ylabel = "events / bin",
        xunit = "",
        postprocess_hist = lambda x, template=template: postprocess_hist(x, template),
        do_tex = False

    )
    ret["axes"][0].set_ylim(0, ymax)
    ret["axes"][1].set_ylim(0.5, 1.5)
    plotlib.svfg(path + "/{0}_postfit.pdf".format(chname))
    return ret

if __name__ == "__main__":
    path = sys.argv[1]
    tf = rootpy.io.File(path + "/limits/mlfitshapes_group_group_sldl.root")

    for ch, chname, template, xlabel in [
        ("ch1", "sl_j4_t3", rootpy.plotting.Hist(6,-1,4), "btag LR"),
        ("ch2", "sl_j4_tge4", rootpy.plotting.Hist(6,0,1), "MEM"),
        ("ch3", "sl_j5_t3", rootpy.plotting.Hist(6,0,5), "btag LR"),
        ("ch4", "sl_j5_tge4", rootpy.plotting.Hist(6,0,1), "MEM"),
        ("ch5", "sl_jge6_t3", rootpy.plotting.Hist(6,1,6), "btag LR"),
        ("ch6", "sl_jge6_tge4", rootpy.plotting.Hist(6,0,1), "MEM"),
        ("ch8", "dl_jge4_t3", rootpy.plotting.Hist(6,-1,6), "btag LR"),
        ("ch7", "dl_jge4_tge4", rootpy.plotting.Hist(6,0,1), "MEM"),
        ]:
        
        ret = draw_channel_prefit_postfit(ch, chname, template, xlabel, path)
