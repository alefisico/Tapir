########################################
# Imports
########################################

from multiprocessing import Pool

import ROOT

import Categorize
from Forest import trees
from CombineHelper import LimitGetter, DummyLimitGetter
from Axis import axis
from Cut import Cut

import pickle

########################################
# Configuration
########################################

#ControlPlotsSparse_2015_10_15_withBLR.root
#input_file = "/home/joosep/tth/datacards/prev16/Nov27.root"
#input_file = "/home/joosep/tth/datacards/prev16/Dec3.root"
input_file = "/dev/shm/joosep/ControlPlotsSparse_corr.root"
output_path = "/dev/shm/joosep/categorization2/"

n_proc = 50
n_iter = 8

signals = [
    "ttH_hbb", 
#    "ttH_nohbb"
]

backgrounds = [
    "ttbarPlus2B",
    "ttbarPlusB",
    "ttbarPlusBBbar",
    "ttbarPlusCCbar",
    "ttbarOther",
#    "ttw_wlnu",       
#    "ttw_wqq",        
#    "ttz_zllnunu",    
#    "ttz_zqq",
]        


########################################
# Analysis helper functions
########################################

def split_leaves_by_BLR():
    """ Attempt to optimize BLR splitting of classic analysis categories """

    r = Categorize.CategorizationFromString(trees["old"])
    initial_leaves = r.get_leaves()
    cut_axes = [8] #btag LR axis
    discriminator_axes = [0, 1, 2] #MEM SL 022 axis
    for l in initial_leaves:
        l.find_categories_async(1, 
                                cut_axes, 
                                discriminator_axes)
    return r
# End of split_leaves_by_BLR


def optimize(r):
    """ Further optimize a given tree r """    

    # TODO: something clever for boosted prereq - it can be
    # conditional on mass or other variables... For now we just
    # evaluate it for more events than we should - costs a bit in
    # computing but should be safe physics wise
    #axes[0].discPrereq = [Cut(3,3,3)]
    #axes[1].discPrereq = [Cut(3,3,3)]

    cut_axes = ["numJets", "nBCSVM", "btag_LR_4b_2b_logit", "Wmass"]
    discriminator_axes = ["mem_SL_2w2h2t", "mem_SL_0w2h2t"]
    
    r.find_categories_async(n_iter, 
                            cut_axes, 
                            discriminator_axes)    
# End of optimize


def make_latex(name):
    """ Get name of tree (in trees), produce the latex version and
    safe it to a tex file """

    r = Categorize.CategorizationFromString(trees[name])
    r.axes = Categorize.Categorization.axes

    #r.print_yield_table()
    of = open( name + ".tex","w")
    of.write(r.print_tree_latex())
    of.close()
    of = open(name + ".pickle", "w")
    of.write(pickle.dumps(r))
    of.close()
# End of make_latex


if __name__ == "__main__":

    ########################################
    # Setup Categorization
    ########################################

    h_sig, h_bkg, h_sig_sys, h_bkg_sys = Categorize.GetSparseHistograms(
        input_file,
        signals,
        backgrounds,
        "sl"
    )
    axes = Categorize.GetAxes(h_sig["ttH_hbb"])

    Cut.axes = axes
    Categorize.Categorization.axes = axes
    Categorize.Categorization.h_sig = h_sig
    Categorize.Categorization.h_bkg = h_bkg
    Categorize.Categorization.h_sig_sys = h_sig_sys
    Categorize.Categorization.h_bkg_sys = h_bkg_sys

    Categorize.Categorization.output_path = output_path
    Categorize.Categorization.pool = Pool(n_proc)
    Categorize.do_stat_variations = False

    Categorize.Categorization.lg = LimitGetter(output_path)
   
    #print "Old categorization"
    #make_latex("old_dl")
    #make_latex("old_2t")

    #r = split_leaves_by_BLR()
    #of = open("old_blr.tex", "w")
    #of.write(r.print_tree_latex())
    #of.close()

    print "Optimization"
    r = Categorize.CategorizationFromString(trees["3cat"])
    name = "opt"

    import cProfile, time
    def f(): optimize(r)
    p = cProfile.Profile(time.clock)
    p.runcall(f)
    p.print_stats()
    
    of = open( name + ".tex","w")
    of.write(r.print_tree_latex())
    of.close()
    of = open(name + ".pickle", "w")
    of.write(pickle.dumps(r))
    of.close()


    #for i in range(5,7):
    #    make_latex("{0}cat".format(i))
    #    r = Categorize.CategorizationFromString(trees["{0}cat".format(i)])
    #    print r.eval_limit("{0}cat".format(i))
        
