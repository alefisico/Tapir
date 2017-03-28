import os
import ConfigParser
from itertools import izip
import cPickle as pickle

import ROOT

from TTH.MEAnalysis import samples_base
from TTH.MEAnalysis.samples_base import get_files, getSitePrefix

# From:
# http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

def triplewise(iterable):
    "s -> (s0, s1, s2), (s3, s4, s5), (s5, s6, s7), ..."
    a = iter(iterable)
    return izip(a, a, a)

FUNCTION_TABLE = {
    "btag_LR_4b_2b_btagCSV_logit": lambda ev: ev["btag_LR_4b_2b_btagCSV_logit"],
    "common_bdt": lambda ev: ev["common_bdt"],
    "jetsByPt_0_eta": lambda ev: ev["jets_p4"][0].Eta(),
    "jetsByPt_0_pt": lambda ev: ev["jets_p4"][0].Pt(),
    "leps_0_pt": lambda ev: ev["leps_pt"][0],
    "mem_DL_0w2h2t_p": lambda ev: ev["mem_DL_0w2h2t_p"],
    "mem_SL_0w2h2t_p": lambda ev: ev["mem_SL_0w2h2t_p"],
    "mem_SL_1w2h2t_p": lambda ev: ev["mem_SL_1w2h2t_p"],
    "mem_SL_2w2h2t_p": lambda ev: ev["mem_SL_2w2h2t_p"],
    "Wmass": lambda ev: ev["Wmass"]
}

class Cut(object):

    @staticmethod
    def string_to_cuts(s):
        cuts = []
        for cut_name, lower, upper in triplewise(s):
            cuts.append((cut_name, float(lower), float(upper)))
        return cuts

    @staticmethod
    def cuts_to_string(cuts):
        s = ""
        for cut_name, lower, upper in cuts:
            s += "{0} {1} {2}\n".format(cut_name, lower, upper)
        return s

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.sparsinator = kwargs.get("sparsinator", [])
        self.skim = kwargs.get("skim", None)

    @staticmethod
    def fromConfigParser(config, name):
        return Cut(
            name = name,
            sparsinator = Cut.string_to_cuts(config.get(name, "sparsinator").split()),
            skim = config.get(name, "skim")
        )

    def __str__(self):
        s = []
        for c in self.sparsinator:
            s += ["({1} <= {0} < {2})".format(*c)]
        return "AND".join(s)

class Sample(object):
    def __init__(self, *args, **kwargs):
        self.debug = kwargs.get("debug")
        self.name = kwargs.get("name")
        self.schema = kwargs.get("schema")
        self.files_load = kwargs.get("files_load")
        self.files_load_step1 = kwargs.get("files_load_step1", None)
        self.step_size_sparsinator = int(kwargs.get("step_size_sparsinator"))
        self.debug_max_files = int(kwargs.get("debug_max_files"))

        try:
            self.file_names = [getSitePrefix(fn) for fn in get_files(self.files_load)]
        except Exception as e:
            print "ERROR: could not load sample file {0}: {1}".format(self.files_load, e)
            self.file_names = []

        if self.files_load_step1 is None:
            self.file_names_step1 = self.file_names
        else:
            try:
                self.file_names_step1 = [getSitePrefix(fn) for fn in get_files(self.files_load_step1)]
            except Exception as e:
                print "ERROR: could not load sample file {0}: {1}".format(self.files_load_step1, e)
                self.file_names_step1 = []

        if self.debug:
            self.file_names = self.file_names[:self.debug_max_files]
        self.ngen = int(kwargs.get("ngen"))
        self.xsec = kwargs.get("xsec")
        self.classifier_db_path = kwargs.get("classifier_db_path")
        self.skim_file = kwargs.get("skim_file")
        self.vhbb_tree_name = kwargs.get("vhbb_tree_name", "vhbb/tree")
        
    @staticmethod
    def fromConfigParser(config, sample_name):
        sample = Sample(
            debug = config.getboolean("general", "debug"),
            name = sample_name,
            files_load = config.get(sample_name, "files_load"),
            files_load_step1 = config.get(sample_name, "files_load_step1"),
            schema = config.get(sample_name, "schema"),
            step_size_sparsinator = config.get(sample_name, "step_size_sparsinator"),
            debug_max_files = config.get(sample_name, "debug_max_files"),
            ngen = config.getfloat(sample_name, "ngen"),
            classifier_db_path = config.get(sample_name, "classifier_db_path", None),
            skim_file = config.get(sample_name, "skim_file", None),
            vhbb_tree_name = config.get(sample_name, "vhbb_tree_name", "vhbb/tree"),
            xsec = config.getfloat(sample_name, "xsec"),
        )
        return sample

class HistogramOutput:
    def __init__(self, hist, func, cut_name):
        self.hist = hist
        self.func = func
        self.cut_name = cut_name

    def cut(self, event):
        return event.get(self.cut_name, False)

    def fill(self, event, weight = 1.0):
        self.hist.Fill(self.func(event), weight)

class CategoryCut:
    def __init__(self, cuts):
        self.cuts = cuts
            
    def cut(self, event):
        ret = True
        for cut in self.cuts:
            for cname, clow, chigh in cut.sparsinator:
                v = event[cname]
                ret = ret and (v >= clow and v < chigh)
                if not ret:
                    return False
        return ret

class Process(object):
    """
    Defines how an input sample should be mapped to an output histogram.
    Possibly applies cuts on the event to separate a sample into processes
    based on some event-level quantity such as ttCls
    """
    def __init__(self, *args, **kwargs):
        self.input_name = kwargs.get("input_name")
        self.output_name = kwargs.get("output_name")
        self.cuts = kwargs.get("cuts", [])
        self.xs_weight = kwargs.get("xs_weight", 1.0)
        #self.index = kwargs.get("index", -1)
        self.full_name = " ".join([self.input_name, self.output_name, ",".join([c.name for c in self.cuts])])

    def __repr__(self):
        s = "Process(input_name={0}, output_name={1})".format(self.input_name, self.output_name)
        return s

    def output_path(self, category_name, discriminator_name, systematic_string=None):
        to_join = [self.output_name, category_name, discriminator_name]
        if systematic_string:
            to_join += [systematic_string]
        name = "__".join(to_join)
        return name
    
    def createOutputs(self, outdir, analysis, systematics):
        """Creates an output dictionary with fillable objects in TDirectories based on categories and systematics. 
        
        Args:
            outdir (TYPE): Description
            analysis (TYPE): Description
            sample (TYPE): Description
            systematics (list of string): list of systematics for which to create outputs
        
        Returns:
            dict of string->output: Dictionary of fillable outputs
        """
    
        outdict_syst = {}
        outdict_cuts = {}
    
        ROOT.TH1.AddDirectory(False)
    
        for syst in systematics:
            outdict_syst[syst] = {}
            syst_str = syst
            if syst == "nominal":
                syst_str = None
            #for every category in every group
            for group_name in analysis.groups.keys():
                for category in analysis.groups[group_name]:
                    #create a new cut object that applies both the Category and Process cuts
                    category_cut = CategoryCut(
                        category.cuts
                    )
                    cut_name = (category.full_name, self.full_name)
                    if not outdict_cuts.has_key(cut_name):
                        outdict_cuts[cut_name] = category_cut
                    name = self.output_path(category.name, category.discriminator.name, syst_str)
                    if not outdict_syst[syst].has_key(name):
                        h = category.discriminator.get_TH1(name)
                        outdict_syst[syst][name] = HistogramOutput(
                            h,
                            FUNCTION_TABLE[category.discriminator.func],
                            cut_name,
                        )
        return outdict_syst, outdict_cuts

class SystematicProcess(Process):
    def __init__(self, *args, **kwargs):
        super(SystematicProcess, self).__init__(self, *args, **kwargs)
        self.systematic_name = kwargs.get("systematic_name")

    def output_path(self, category_name, discriminator_name, systematic_string=None):
        return super(SystematicProcess, self).output_path(
            category_name,
            discriminator_name,
            self.systematic_name
        )
    
    def createOutputs(self, outdir, analysis, systematics):
        outdict_syst = {"nominal": {}}
        outdict_cuts = {}
    
        ROOT.TH1.AddDirectory(False)
        for group_name in analysis.groups.keys():
            for category in analysis.groups[group_name]:
                #create a new cut object that applies both the Category and Process cuts
                category_cut = CategoryCut(
                    category.cuts
                )
                cut_name = (category.full_name, self.full_name)
                if not outdict_cuts.has_key(cut_name):
                    outdict_cuts[cut_name] = category_cut
                name = self.output_path(category.name, category.discriminator.name)
                if not outdict_syst["nominal"].has_key(name):
                    h = category.discriminator.get_TH1(name)
                    outdict_syst["nominal"][name] = HistogramOutput(
                        h,
                        FUNCTION_TABLE[category.discriminator.func],
                        cut_name,
                    )
        return outdict_syst, outdict_cuts
    
    def __repr__(self):
        s = "SystematicProcess(input_name={0}, output_name={1}, systematic_name={2})".format(
            self.input_name,
            self.output_name,
            self.systematic_name
        )
        return s
            
class DataProcess(Process):
    def __init__(self, *args, **kwargs):
        super(DataProcess, self).__init__(self, *args, **kwargs)
        self.lumi = kwargs.get("lumi", 1.0)

class Histogram:
    def __init__(self, name, func, bins):
        self.name = name
        self.func = func
        self.bins = bins

    @staticmethod
    def from_string(s):
        name, func, bins = s.split()
        return Histogram(name, func, bins)

    def to_string(self):
        return "{0} {1} {2}".format(self.name, self.func, self.bins)

    def get_binning(self):
        bs = self.bins.split(",")
        if len(bs) == 3:
            return int(bs[0]), float(bs[1]), float(bs[2])
        else:
            raise Exception("Unknown binning spec")

    def get_TH1(self, name):
        th = ROOT.TH1D(name, name, *self.get_binning())
        return th

class Category:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.discriminator = kwargs.get("discriminator")
        self.full_name = "{0}__{1}".format(self.name, self.discriminator.name)
        self.src_histogram = kwargs.get("src_histogram")
        self.rebin = kwargs.get("rebin", 1)
        self.do_limit = kwargs.get("do_limit", True)

        self.scale_uncertainties = kwargs.get("scale_uncertainties", {})

        self.cuts = kwargs.get("cuts", [])

        self.processes = kwargs.get("processes", [])
        self.data_processes = kwargs.get("data_processes", [])
        #self.lumi = sum([d.lumi for d in self.data_samples])

        self.signal_processes = kwargs.get("signal_processes", [])
        self.out_processes = list(set([s.output_name for s in self.processes + self.data_processes]))

        #[process][syst]
        self.shape_uncertainties = {}
        self.scale_uncertainties = {}

        #[syst] -> scale factor, common for all processes
        self.common_shape_uncertainties = kwargs.get("common_shape_uncertainties", {})
        self.common_scale_uncertainties = kwargs.get("common_scale_uncertainties", {})
        for proc in self.out_processes:
            self.shape_uncertainties[proc] = {}
            self.scale_uncertainties[proc] = {}
            for systname, systval in self.common_shape_uncertainties.items():
                self.shape_uncertainties[proc][systname] = systval
            for systname, systval in self.common_scale_uncertainties.items():
                self.scale_uncertainties[proc][systname] = systval

        self.proc_shape_uncertainties = kwargs.get("shape_uncertainties", {})
        self.proc_scale_uncertainties = kwargs.get("scale_uncertainties", {})
        
        for k, v in self.proc_shape_uncertainties.items():
            self.shape_uncertainties[k].update(v)

        for k, v in self.proc_scale_uncertainties.items():
            self.scale_uncertainties[k].update(v)

    
    def __str__(self):
        s = "Category(full_name={0})".format(
            self.full_name,
        )
        return s

    # # Define equality via the representation string
    # def __eq__(self,other):
    #     return self.__repr__() == other.__repr__()

    # # hash(object) = hash(representation(object))
    # def __hash__(self):
    #     return self.__repr__().__hash__()


class Analysis:
    def __init__(self, **kwargs):
        self.mem_python_config = kwargs.get("mem_python_config")
        self.config = kwargs.get("config")
        self.debug = kwargs.get("debug", False)
        self.samples = kwargs.get("samples", [])
        self.cuts = kwargs.get("cuts", {})
        self.process_lists = kwargs.get("process_lists")
        self.processes = kwargs.get("processes")
        self.processes_unsplit = kwargs.get("processes_unsplit")
        self.categories = kwargs.get("categories")

        # groups represent calls to combine, i.e. 
        # {"myCombination1": ["cat1", "cat2"] }
        # will calculate the combined limit myCombination1 of cat1 and cat2 
        self.groups = kwargs.get("groups", {})
        self.do_fake_data = kwargs.get("do_fake_data", False)
        self.do_stat_variations = kwargs.get("do_stat_variations", False)
        self.sample_d = dict([(s.name, s) for s in self.samples])

    def get_sample(self, sample_name):
        return self.sample_d[sample_name]

    def __repr__(self):
        s = "Analysis(processes={0}, categories={1}, groups={2})".format(
            len(self.processes),
            len(self.categories),
            len(self.groups),
        )
        return s

    @staticmethod
    def deserialize(filename):
        fi = open(filename, "rb")
        an = pickle.load(fi)
        fi.close()
        return an

    def serialize(self, filename):
        fi = open(filename, "wb")
        pickle.dump(self, fi)
        fi.close()

    @staticmethod
    def getConfigParser(config_file_name):
        config = ConfigParser.SafeConfigParser()
        config.optionxform = str # Turn on case-sensitivity
        config.read(config_file_name)
        if config.has_option("importconfig","parent"):
            parent_file_name = config.get("importconfig","parent").replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])
            parent = ConfigParser.SafeConfigParser()
            parent.optionxform = str # Turn on case-sensitivity
            parent.read(parent_file_name) 
            for s in config.sections():
                if s=="importconfig":
                    continue
                for (i,v) in config.items(s):
                    if parent.get(s,i):
                        parent.set(s, i, v)
            return parent
        return config

def make_csv_categories_abstract(di):

    import csv
    with open('analysis_specs.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'category'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        for analysis_name, analysis in di.iteritems():        

            unique_cat_names = list(set(c.name for c in analysis.categories))
            for cat_name in unique_cat_names:
                csvwriter.writerow([analysis_spec_file, analysis_name, cat_name])

    return [1]

def make_csv_groups_abstract(di):

    import csv
    with open('analysis_groups.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'group'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack    
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        for analysis_name, analysis in di.iteritems():        
            for group_name in analysis.groups.keys():
                csvwriter.writerow([analysis_spec_file, analysis_name, group_name])

    return [1]
