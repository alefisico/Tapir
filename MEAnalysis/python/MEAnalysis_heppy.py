#!/usr/bin/env python
import os
import PhysicsTools.HeppyCore.framework.config as cfg
import ROOT
import imp

#pickle and transfer function classes to load transfer functions
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys

from TTH.Plotting.joosep.sparsinator import BufferedTree

sys.modules["TFClasses"] = TFClasses
ROOT.gROOT.SetBatch(True)

class BufferedChain( object ):
    """Wrapper to TChain, with a python iterable interface.

    Example of use:  #TODO make that a doctest / nose?
       from chain import Chain
       the_chain = Chain('../test/test_*.root', 'test_tree')
       event3 = the_chain[2]
       print event3.var1

       for event in the_chain:
           print event.var1
    """

    def __init__(self, input, tree_name=None):
        """
        Create a chain.

        Parameters:
          input     = either a list of files or a wildcard (e.g. 'subdir/*.root').
                      In the latter case all files matching the pattern will be used
                      to build the chain.
          tree_name = key of the tree in each file.
                      if None and if each file contains only one TTree,
                      this TTree is used.
        """
        self.files = input
        self.base_chain = ROOT.TChain(tree_name)
        for file in self.files:
            self.base_chain.Add(file)
        self.chain = BufferedTree(self.base_chain)

    def __getattr__(self, attr):
        """
        All functions of the wrapped TChain are made available
        """
        return getattr(self.chain, attr)

    def __iter__(self):
        return self.chain

    def __len__(self):
        return int(self.chain.GetEntries())

    def __getitem__(self, index):
        """
        Returns the event at position index.
        """
        self.chain.GetEntry(index)
        return self


def main(analysis_cfg, sample_name=None, schema=None, firstEvent=0, numEvents=None, files=[], output_name=None):
    mem_python_config = analysis_cfg.mem_python_config.replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])
    #Create python configuration object based on path
    if len(mem_python_config) > 0:
        print "Loading ME config from", mem_python_config
        meconf = imp.load_source("meconf", mem_python_config)
        from meconf import Conf as python_conf
    else:
        print "Loading ME config from TTH.MEAnalysis.MEAnalysis_cfg_heppy"
        from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf
    from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str

    #Load transfer functions from pickle file
    pi_file = open(python_conf.general["transferFunctionsPickle"] , 'rb')
    python_conf.tf_matrix = pickle.load(pi_file)

    #Pre-compute the TF formulae
    # eval_gen:specifies how the transfer functions are interpreted
    #     If True, TF [0] - reco, x - gen
    #     If False, TF [0] - gen, x - reco
    #FIXME!!!: remove this flag in future versions!
    eval_gen=False
    python_conf.tf_formula = {}
    for fl in ["b", "l"]:
        python_conf.tf_formula[fl] = {}
        for bin in [0, 1]:
                python_conf.tf_formula[fl][bin] = python_conf.tf_matrix[fl][bin].Make_Formula(eval_gen)

    pi_file.close()

    #Load the subjet transfer functions from pickle file
    pi_file = open(python_conf.general["transferFunctions_sj_Pickle"] , 'rb')
    python_conf.tf_sj_matrix = pickle.load(pi_file)
    pi_file.close()

    if sample_name:
        an_sample = analysis_cfg.get_sample(sample_name)
        sample_name = an_sample.name
        vhbb_tree_name = an_sample.vhbb_tree_name
        schema = an_sample.schema
        if len(files) == 0:
            files = an_sample.file_names_step1[:an_sample.debug_max_files]
        if not output_name:
            output_name = "Loop_" + sample_name
    elif schema:
        sample_name = "sample"
        vhbb_tree_name = "tree"
        pass
    else:
        raise Exception("Must specify either sample name or schema")

    #Event contents are defined here
    #This is work in progress
    if schema == "mc":
        from TTH.MEAnalysis.VHbbTree import EventAnalyzer
    else:
        from TTH.MEAnalysis.VHbbTree_data import EventAnalyzer

    #This analyzer reads branches from event.input (the TTree/TChain) to event.XYZ (XYZ is e.g. jets, leptons etc)
    evs = cfg.Analyzer(
        EventAnalyzer,
        'events',
    )

    #Here we define all the main analyzers
    import TTH.MEAnalysis.MECoreAnalyzers as MECoreAnalyzers

    prefilter = cfg.Analyzer(
        MECoreAnalyzers.PrefilterAnalyzer,
        'prefilter',
        _conf = python_conf
    )
    #
    counter = cfg.Analyzer(
        MECoreAnalyzers.CounterAnalyzer,
        'counter',
        _conf = python_conf
    )

    evtid_filter = cfg.Analyzer(
        MECoreAnalyzers.EventIDFilterAnalyzer,
        'eventid',
        _conf = python_conf
    )

    pvana = cfg.Analyzer(
        MECoreAnalyzers.PrimaryVertexAnalyzer,
        'pvana',
        _conf = python_conf
    )

    trigger = cfg.Analyzer(
        MECoreAnalyzers.TriggerAnalyzer,
        'trigger',
        _conf = python_conf
    )

    #This class performs lepton selection and SL/DL disambiguation
    leps = cfg.Analyzer(
        MECoreAnalyzers.LeptonAnalyzer,
        'leptons',
        _conf = python_conf
    )

    #This class performs jet selection and b-tag counting
    jets = cfg.Analyzer(
        MECoreAnalyzers.JetAnalyzer,
        'jets',
        _conf = python_conf
    )

    #calculates the number of matched simulated B, C quarks for tt+XY matching
    genrad = cfg.Analyzer(
        MECoreAnalyzers.GenRadiationModeAnalyzer,
        'genrad',
        _conf = python_conf
    )

    #calculates the b-tag likelihood ratio
    btaglr = cfg.Analyzer(
        MECoreAnalyzers.BTagLRAnalyzer,
        'btaglr',
        _conf = python_conf,
        btagAlgo = "btagCSV"
    )

    ##calculates the b-tag likelihood ratio
    #btaglr_bdt = cfg.Analyzer(
    #    MECoreAnalyzers.BTagLRAnalyzer,
    #    'btaglr_bdt',
    #    _conf = python_conf,
    #    btagAlgo = "btagBDT"
    #)

    #calculates the b-tag likelihood ratio
    qglr = cfg.Analyzer(
        MECoreAnalyzers.QGLRAnalyzer,
        'qglr',
        _conf = python_conf
    )

    #assigns the ME category based on leptons, jets and the bLR
    mecat = cfg.Analyzer(
        MECoreAnalyzers.MECategoryAnalyzer,
        'mecat',
        _conf = python_conf
    )

    #performs W-tag calculation on pairs of untagged jets
    wtag = cfg.Analyzer(
        MECoreAnalyzers.WTagAnalyzer,
        'wtag',
        _conf = python_conf
    )

    subjet_analyzer = cfg.Analyzer(
        MECoreAnalyzers.SubjetAnalyzer,
        'subjet',
        _conf = python_conf
    )

    #multiclass_analyzer = cfg.Analyzer(
    #    MECoreAnalyzers.MulticlassAnalyzer,
    #    'multiclass',
    #    _conf = conf
    #)

    #Calls the C++ MEM integrator with good_jets, good_leptons and
    #the ME category
    mem_analyzer = cfg.Analyzer(
        MECoreAnalyzers.MEAnalyzer,
        'mem',
        _conf = python_conf
    )

    gentth = cfg.Analyzer(
        MECoreAnalyzers.GenTTHAnalyzer,
        'gentth',
        _conf = python_conf
    )

#    mva = cfg.Analyzer(
#        MECoreAnalyzers.MVAVarAnalyzer,
#        'mva',
#        _conf = python_conf
#    )

    treevar = cfg.Analyzer(
        MECoreAnalyzers.TreeVarAnalyzer,
        'treevar',
        _conf = python_conf
    )
    memory_ana = cfg.Analyzer(
        MECoreAnalyzers.MemoryAnalyzer,
        'memory',
        _conf = python_conf,
    )
    from TTH.MEAnalysis.metree import getTreeProducer
    treeProducer = getTreeProducer(python_conf)

    # definition of a sequence of analyzers,
    # the analyzers will process each event in this order
    sequence = cfg.Sequence([
        memory_ana,
        counter,
        evtid_filter,
        prefilter,
        evs,
        pvana,
        trigger,
        leps,
        jets,
        btaglr,
        #btaglr_bdt,
        qglr,
        wtag,
        mecat,
        subjet_analyzer,
        genrad,
        gentth,
        #multiclass_analyzer,
        mem_analyzer,
        #mva,
        treevar,
        treeProducer
    ])

    #Book the output file
    from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
    output_service = cfg.Service(
        TFileService,
        'outputfile',
        name="outputfile",
        fname='tree.root',
        option='recreate'
    )

    comp_cls = cfg.MCComponent
    if schema == "data":
        comp_cls = cfg.DataComponent

    comp = comp_cls(
        sample_name,
        files = files,
        tree_name = vhbb_tree_name,
    )

    #from PhysicsTools.HeppyCore.framework.chain import Chain
    heppy_config = cfg.Config(
        #Run across these inputs
        components = [comp],

        #Using this sequence
        sequence = sequence,

        #save output to these services
        services = [output_service],

        #This defines how events are loaded
        #BufferedChain should be faster, but is kind of hacky
        events_class = BufferedChain
        #events_class = Chain
    )

    #Configure the number of events to run
    from PhysicsTools.HeppyCore.framework.looper import Looper

    kwargs = {}
    if python_conf.general.get("eventWhitelist", None) is None and not (numEvents is None):
        kwargs["nEvents"] = numEvents
    kwargs["firstEvent"] = firstEvent
    looper = Looper(
        output_name,
        heppy_config,
        nPrint = 0,
        **kwargs
    )

    print "Running looper"
    #execute the code
    looper.loop()
    print "Looper done"

    tf = looper.setup.services["PhysicsTools.HeppyCore.framework.services.tfile.TFileService_outputfile"].file
    #tf.cd()
    #ts = ROOT.TNamed("config", conf_to_str(python_conf))
    #ts.Write("", ROOT.TObject.kOverwrite)

    #write the output
    looper.write()
    return python_conf

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    an = analysisFromConfig(sys.argv[1])

    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis')
    parser.add_argument(
        '--sample',
        action="store",
        help="Sample to process",
        choices=[samp.name for samp in an.samples],
        required=True
    )
    parser.add_argument(
        '--numEvents',
        action="store",
        help="Number of events to process",
        default=1000,
    )
    args = parser.parse_args(sys.argv[2:])

    main(an, sample_name=args.sample, numEvents=args.numEvents)
