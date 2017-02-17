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

    def updateConfig(self, config):
        config.set(self.name, "sparsinator", Cut.cuts_to_string(self.sparsinator))
        config.set(self.name, "skim", Cut.cuts_to_string(self.skim))

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
        self.process = kwargs.get("process")
        self.files_load = kwargs.get("files_load")
        self.step_size_sparsinator = int(kwargs.get("step_size_sparsinator"))
        self.debug_max_files = int(kwargs.get("debug_max_files"))
        try:
            self.file_names = [getSitePrefix(fn) for fn in get_files(self.files_load)]
        except Exception as e:
            print "ERROR: could not load sample file {0}".format(files_load)
            self.file_names = []
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
            process = config.get(sample_name, "process"),
            files_load = config.get(sample_name, "files_load"),
            schema = config.get(sample_name, "schema"),
            is_data = config.get(sample_name, "is_data"),
            step_size_sparsinator = config.get(sample_name, "step_size_sparsinator"),
            debug_max_files = config.get(sample_name, "debug_max_files"),
            ngen = config.getfloat(sample_name, "ngen"),
            classifier_db_path = config.get(sample_name, "classifier_db_path", None),
            skim_file = config.get(sample_name, "skim_file", None),
            xsec = config.getfloat(sample_name, "xsec"),
        )
        return sample

    def updateConfig(self, config):
        for field in dir(self):
            if field.startswith("__"):
                continue
            config.set(self.name, field, str(getattr(self, field)))

class Process(object):
    """
    Defines how an input process should be mapped to an output histogram.
    """
    def __init__(self, *args, **kwargs):
        self.input_name = kwargs.get("input_name")
        self.output_name = kwargs.get("output_name")
        self.cuts = kwargs.get("cuts", [])
        self.xs_weight = kwargs.get("xs_weight", 1.0)
    
    def __repr__(self):
        s = "Process: maps {0}->{1} with cuts=[{2}], xsw={3}".format(
            self.input_name,
            self.output_name,
            ",".join(map(str, self.cuts)),
            self.xs_weight
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
        self.full_name = "{0}_{1}".format(self.name, self.discriminator.name)
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
        s = "Category: {0} ({1}) discr={2} cuts={3} do_limit={4}".format(
            self.name,
            self.full_name,
            self.discriminator,
            self.cuts,
            self.do_limit
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

    def to_JSON(self):
        return json.dumps(self.__dict__, indent=2)
    
    def __repr__(self):
        s = "Analysis:\n"
        s += "  processes:\n"
        for proc in self.processes:
            s += "    {0}\n".format(proc)
        s += "  categories:\n"
        for cat in self.categories:
            s += "    {0}\n".format(cat)
        
        s += "  groups for combine:\n"
        for groupname, cats in self.groups.items():
            s += "    {0}: {1}\n".format(groupname, [c.name for c in self.groups[groupname]])
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
