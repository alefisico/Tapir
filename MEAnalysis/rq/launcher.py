import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

from rq import Queue
from redis import Redis
from rq import push_connection, get_failed_queue, Queue, Worker
from job import count, sparse, plot, makecategory, makelimits, mergeFiles, validateFiles
import socket

import time, os, sys
import shutil
from collections import Counter
import uuid
import cPickle as pickle

import subprocess

import ROOT
from TTH.MEAnalysis.samples_base import getSitePrefix, chunks
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
from TTH.Plotting.Datacards.MakeCategory import make_datacard
from TTH.Plotting.Datacards.sparse import add_hdict

import TTH.Plotting.joosep.plotlib as plotlib #heplot, 

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt

####
# Configuation
####

def basic_job_status(jobs):
    status = [j.status for j in jobs]
    status_counts = dict(Counter(status))
    
    sys.stdout.write("\033[K") # Clear this line
    sys.stdout.write("\033[92mstatus\033[0m {4:.2f}%\tq={0}\ts={1}\tf={2}\tE={3}\n".format(
        status_counts.get("queued", 0),
        status_counts.get("started", 0),
        status_counts.get("finished", 0),
        status_counts.get("failed", 0),
        100.0 * status_counts.get("finished", 0) / sum(status_counts.values()),
    ))
    sys.stdout.write("\033[F") # Cursor up one line

def waitJobs(jobs, redis_conn, qmain, qfail, num_retries=0, callback=basic_job_status):
    """Given a list of redis jobs, wait for them to finish and retrieve the results.
    
    Args:
        jobs (list of redis jobs): The jobs that we want to do
        redis_conn (Connection): The redis connection
        qmain (Queue): The queue on which to do work
        qfail (Queue): The queue on which failed jobs end up on
        num_retries (int, optional): The number of times to retry a failed job
        callback (function, optional):  a function jobs -> output that will be called at every polling iteration 
    
    Returns:
        TYPE: Description
    
    Raises:
        Exception: Description
    """
    done = False
    istep = 0
    perm_failed = []
    workflow_failed = False

    while not done:
        logger.debug("queues: main({0}) failed({1})".format(len(qmain), len(qfail)))
        logger.debug("--- all")
        
        for job in jobs:
            #logger.debug("id={0} status={1} meta={2}".format(job.id, job.status, job.meta))
            if job.status == "failed":

                #resubmit job if failed
                if job.meta["retries"] < num_retries:
                    job.meta["retries"] += 1
                    logger.info("requeueing job {0}".format(job.id))
                    logger.error("job error: {0}".format(job.exc_info))
                    qfail.requeue(job.id)
                else:
                    #job failed permanently, abort workflow
                    job.refresh()
                    perm_failed += [job]
                    raise Exception("job {0} failed with exception {1}".format(
                        job,
                        job.exc_info
                    ))
            
            #This can happen if the worker died
            if job.status is None:
                print "Job id={0} status is None, probably worker died, trying to requeue".format(
                    job.id
                )
                qfail.requeue(job.id)

            #if the job is done, create a unique hash from the job arguments that will be
            #used to "memoize" or store the result in the database
            if job.status == "finished":
                key = (job.func.func_name, job.meta["args"])
                if job.meta["args"] != "": 
                    hkey = hash(str(key))
                    if not redis_conn.exists(hkey):
                        logger.debug("setting key {0} in db".format(hkey))
                        redis_conn.set(hkey, pickle.dumps(job.result))
        
        #count the job statuses 
        status = [j.status for j in jobs]
        status_counts = dict(Counter(status))

        #fail the workflow if any jobs failed permanently
        if len(perm_failed) > 0:
            logger.error("--- fail queue has {0} items".format(len(qfail)))
            for job in qfail.jobs:
                workflow_failed = True
                logger.error("job {0} failed with message:\n{1}".format(job.id, job.exc_info))
                qfail.remove(job.id)
        
        #workflow is done if all jobs are done
        if status_counts.get("started", 0) == 0 and status_counts.get("queued", 0) == 0:
            done = True
            break

        time.sleep(1)
        
        if not callback is None:
            callback(jobs)
        istep += 1

    if workflow_failed:
        raise Exception("workflow failed, see errors above")

    #fetch the results
    results = [j.result for j in jobs]
    return results

class JobMemoize:
    """
    Fake job instance with manually configured properties
    """
    def __init__(self, result, func, args, meta):
        self.result = result
        self.status = "finished"
        self.func = func
        self.args = args
        self.meta = meta

def enqueue_nomemoize(queue, **kwargs):
    return queue.enqueue_call(**kwargs)

def enqueue_memoize(queue, **kwargs):
    """
    Check if result already exists in redis DB, then return it, otherwise compute it.
    """
    key = (kwargs.get("func").func_name, kwargs.get("meta")["args"])
    hkey = hash(str(key))
    logger.debug("checking for key {0} -> {1}".format(hkey, str(key)))
    if redis_conn.exists(hkey):
        res = pickle.loads(redis_conn.get(hkey))
        logger.debug("found key {0}, res={1}".format(hkey, res))
        return JobMemoize(res, kwargs.get("func"), kwargs.get("args"), kwargs.get("meta"))
    else:
        logger.debug("didn't find key, enqueueing")
        return queue.enqueue_call(**kwargs)

class Task(object):
    def __init__(self, workdir, name, analysis):
        self.workdir = workdir
        self.name = name
        self.analysis = analysis

    def run(self, inputs, redis_conn, qmain, qfail):
        jobs = {}
        return jobs

    def get_analysis_config(self, workdir = None):
        if not workdir:
            workdir = self.workdir
        return os.path.join(workdir, "analysis.pickle")

    def save_state(self):
        self.analysis.serialize(self.get_analysis_config())

    def load_state(self, workdir):
        self.analysis = self.analysis.deserialize(
            self.get_analysis_config(workdir)
        )

class TaskValidateFiles(Task):
    def __init__(self, workdir, name, analysis):
        """Given an analysis, creates a counter task that can be executed
        
        Args:
            workdir (string): A directory where the code will execute
            name (string): Name of the task, can be anything
            analysis (Analysis): The Analysis object as constructed from the config
        """
        super(TaskValidateFiles, self).__init__(workdir, name, analysis)
    
    def run(self, inputs, redis_conn, qmain, qfail):
        all_jobs = []
        jobs = {}
        
        for sample in self.analysis.samples:
            #create the jobs that will count the events in this sample
            _jobs = TaskValidateFiles.getGoodFiles(sample, qmain)
            jobs[sample.name] = _jobs
            all_jobs += _jobs

        #wait for the jobs to complete
        waitJobs(all_jobs, redis_conn, qmain, qfail, 0)

        #Count the total number of generated events per sample and save it
        for sample in self.analysis.samples:
            good_files = []
            for job in jobs[sample.name]:
                good_files += job.result
            logger.info("TaskValidateFiles: sample {0} had {1} files, {2} are good".format(
                sample.name,
                len(sample.file_names),
                len(good_files),
            ))
            sample.file_names = good_files
        self.save_state()
    
    @staticmethod
    def getGoodFiles(sample, queue):

        jobs = []
        if len(sample.file_names) == 0:
            raise Exception("No files specified for sample {0}".format(sample.name))

        #split the sample input files into a number of chunks based on the prescribed size
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            jobs += [
                enqueue_nomemoize(
                    queue,
                    func = validateFiles,
                    args = (inputs, ),
                    timeout = 2*60*60,
                    ttl = 2*60*60,
                    result_ttl = 2*60*60,
                    meta = {"retries": 5, "args": str((inputs, ))}
                )
            ]
        logger.info("getGoodFiles: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskNumGen(Task):
    """Counts the number of generated events for a sample
    """
    def __init__(self, workdir, name, analysis):
        """Given an analysis, creates a counter task that can be executed
        
        Args:
            workdir (string): A directory where the code will execute
            name (string): Name of the task, can be anything
            analysis (Analysis): The Analysis object as constructed from the config
        """
        super(TaskNumGen, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)
        all_jobs = []
        jobs = {}
        #Loop over all the samples defined in the analysis
        for sample in self.analysis.samples:
            jobs[sample.name] = []
            if not sample.schema == "mc":
                continue
            #create the jobs that will count the events in this sample
            _jobs = TaskNumGen.getGeneratedEvents(sample, qmain)
            jobs[sample.name] = _jobs
            all_jobs += _jobs

        #wait for the jobs to complete
        waitJobs(all_jobs, redis_conn, qmain, qfail, 0)

        #Count the total number of generated events per sample and save it
        for sample in self.analysis.samples:
            ngen = sum(
                [j.result.get("Count", 0) for j in jobs[sample.name]]
            )
            sample.ngen = int(ngen)
            logger.info("sample.ngen {0} = {1}".format(sample.name, sample.ngen))
        self.save_state()
        return jobs

    @staticmethod
    def getGeneratedEvents(sample, queue):
        """Given a sample with a list of files, count the number of generated events in this sample
        This method is asynchronous, meaning it won't wait until the jobs are done.

        Args:
            sample (Sample): The input sample
            queue (Queue): Redis queue
        
        Returns:
            list of rq jobs: The jobs that will return the result
        """
        jobs = []
        if len(sample.file_names) == 0:
            raise Exception("No files specified for sample {0}".format(sample.name))

        #split the sample input files into a number of chunks based on the prescribed size
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            jobs += [
                enqueue_memoize(
                    queue,
                    func = count,
                    args = (inputs, ),
                    timeout = 2*60*60,
                    ttl = 2*60*60,
                    result_ttl = 2*60*60,
                    meta = {"retries": 5, "args": str((inputs, ))}
                )
            ]
        logger.info("getGeneratedEvents: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskSparsinator(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskSparsinator, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        all_jobs = []
        jobs = {}
        for sample in self.analysis.samples:
            if not sample.name in [p.input_name for p in self.analysis.processes]:
                logger.info("Skipping sample {0} because matched to any process".format(
                    sample.name
                ))
                continue
            logger.info("Submitting sample {0} ngen={1}".format(sample.name, sample.ngen))
            jobs[sample.name] = TaskSparsinator.runSparsinator_async(
                self.get_analysis_config(workdir),
                sample,
                self.workdir
            )
            all_jobs += jobs[sample.name]
        logger.info("waiting on sparsinator jobs")
        waitJobs(all_jobs, redis_conn, qmain, qfail, callback=self.status_callback)
        self.save_state()
        return jobs

    @staticmethod
    def status_callback(jobs):

        basic_job_status(jobs)

        res = []
        samples = set()
        for job in jobs:
            sample_name = job.args[2]
            k = (sample_name, job.status)
            samples.add(sample_name)
            res += [k]

        res = dict(Counter(res))
        res_by_sample = {sample: {"queued": 0, "started": 0, "finished": 0} for sample in samples}
        for k in res.keys():
            res_by_sample[k[0]][k[1]] = res[k]
        
        stat = open("status.md", "w")
        for sample in sorted(samples):
            s = "| " + sample + " | "
            s += " | ".join([str(res_by_sample[sample][k]) for k in ["queued", "started", "finished"]])
            stat.write(s + "\n")
        stat.close()

    @staticmethod
    def runSparsinator_async(config_path, sample, workdir):
        jobs = []
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            ofname = "{0}/sparse/{1}/sparse_{2}.root".format(
                workdir, sample.name, ijob
            )
            jobs += [
                enqueue_memoize(
                    qmain,
                    func = sparse,
                    args = (config_path, inputs, sample.name, ofname),
                    timeout = 2*60*60,
                    ttl = 2*60*60,
                    result_ttl = 2*60*60,
                    meta = {"retries": 2, "args": str((inputs, sample.name))}
                )
            ]
        logger.info("runSparsinator: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskSparseMerge(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskSparseMerge, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        all_jobs = []
        jobs_by_sample = {}

        for sample in self.analysis.samples:
            
            if not sample.name in inputs.keys():
                print "Skipping sample", sample.name
                continue

            jobs_by_sample[sample.name] = []
            sample_results = [os.path.abspath(job.result) for job in inputs[sample.name]]
            logger.info("sparsemerge: submitting merge of {0} files for sample {1}".format(len(sample_results), sample.name))
            outfile = os.path.abspath("{0}/sparse/sparse_{1}.root".format(workdir, sample.name))

            for ijob, sample_inputs in enumerate(chunks(sample_results, 100)):
                job = enqueue_memoize(
                    qmain,
                    func = mergeFiles,
                    args = (outfile + "." + str(ijob), sample_inputs),
                    timeout = 20*60,
                    result_ttl = 60*60,
                    meta = {"retries": 0, "args": sample_inputs}
                )
                jobs_by_sample[sample.name] += [job]
            all_jobs += jobs_by_sample[sample.name]
        waitJobs(all_jobs, redis_conn, qmain, qfail, callback=TaskSparseMerge.status_callback)
        results = [j.result for j in all_jobs]
        logger.info("sparsemerge: {0}".format(results))
        logger.info("sparsemerge: merging final sparse out of {0} files".format(len(results)))
        final_merge = os.path.abspath("{0}/merged.root".format(workdir))
        job = enqueue_memoize(
            qmain,
            func = mergeFiles,
            args = (final_merge, results),
            timeout = 20*60,
            result_ttl = 60*60,
            meta = {"retries": 2, "args": ("final", final_merge, results)}
        )
        waitJobs([job], redis_conn, qmain, qfail, callback=TaskSparseMerge.status_callback)
        self.save_state()
        return final_merge

    @staticmethod
    def status_callback(jobs):

        basic_job_status(jobs)

        res = []
        samples = set()
        for job in jobs:
            sample_name = job.args[0]
            k = (sample_name, job.status)
            samples.add(sample_name)
            res += [k]

        res = dict(Counter(res))
        res_by_sample = {sample: {"queued": 0, "started": 0, "finished": 0} for sample in samples}
        for k in res.keys():
            res_by_sample[k[0]][k[1]] = res[k]
        
        stat = open("status.md", "w")
        for sample in sorted(samples):
            s = "| " + sample + " | "
            s += " | ".join([str(res_by_sample[sample][k]) for k in ["queued", "started", "finished"]])
            stat.write(s + "\n")
        stat.close()

class TaskCategories(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskCategories, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        hdict = {}

        logger.info("Opening {0}".format(inputs))
        tf = ROOT.TFile(inputs)
        ROOT.gROOT.cd()
        for k in tf.GetListOfKeys():

            #check if this is a valid histogram according to its name
            if len(k.GetName().split("__")) >= 3:
                hdict[k.GetName()] = k.ReadObj().Clone()
        
        #make all the datacards for all the categories
        for cat in self.analysis.categories:
            for proc in cat.out_processes:
                print proc
                if proc == "data":
                    continue
                for syst in cat.common_shape_uncertainties.keys():
                    for sdir in ["Up", "Down"]:
                        pat = "__".join([proc, cat.full_name, syst+sdir])
                        if not hdict.has_key(pat):
                            logger.info("Could not find {0}, cloning nominal".format(pat))
                            hdict[pat] = hdict["__".join([proc, cat.full_name])].Clone()
            category_dir = "{0}/categories/{1}/{2}".format(
                workdir, cat.name, cat.discriminator.name
            )
            logger.info("creating category to {0}".format(category_dir))
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
            make_datacard(self.analysis, [cat], category_dir, hdict)

        # hadd Results        
        cat_names = list(set([cat.name for cat in self.analysis.categories]))        

        for cat_name in cat_names:                                                        
            logger.info("hadd-ing: {0}".format(cat_name))
            
            process = subprocess.Popen(
                "hadd {0}/categories/{1}.root {0}/categories/{1}/*/*.root".format(workdir, cat_name),
                shell=True,
                stdout=subprocess.PIPE
            )
            process.communicate()

        # move the shape text files into the right place
        process = subprocess.Popen(
            "mv {0}/categories/*/*/*.txt {0}/categories/".format(workdir),
            shell=True,
            stdout=subprocess.PIPE
        )

        time.sleep(1) #NFS

        result = "{0}/categories".format(workdir)
        self.save_state()
        return result

class TaskPlotting(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskPlotting, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        from plots import run_plots
        self.load_state(self.workdir)
       
        run_plots(
            workdir,
            self.analysis,
            inputs,
            redis_conn,
            qmain,
            qfail
        )

class TaskLimits(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskLimits, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        # Prepare jobs
        all_jobs = []
        try:
            os.makedirs("{0}/limits".format(self.workdir))
        except OSError as e:
            logger.error(e)
        #copy datacard files and root input files to limit directory 
        os.system("cp {0}/categories/shapes*.txt {0}/limits/".format(self.workdir))
        os.system("cp {0}/categories/*/*/*.root {0}/limits/".format(self.workdir))

        for group in self.analysis.groups.keys():
            logger.info("submitting limit jobs for {0}".format(group))
            all_jobs += [
                qmain.enqueue_call(
                    func = makelimits,
                    args = [
                        "{0}/limits".format(self.workdir),
                        self.analysis,
                        group
                    ],
                    timeout = 40*60,
                    result_ttl = 60*60,
                    meta = {"retries": 0, "args": ""})]
            
        limits = waitJobs(all_jobs, redis_conn, qmain, qfail)
        lims_tot = {}
        for lim in limits:
            lims_tot.update(lim)

        of = open(self.workdir + "/limits.csv", "w")
        for k in sorted(lims_tot.keys()):
            of.write("{0},{1}\n".format(k, lims_tot[k]))
        of.close()

        self.save_state()

class TaskTables(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskTables, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        of = open(self.workdir + "/yields.csv", "w")
        for groupname, group in self.analysis.groups.items():
            limit_categories = [c for c in group if c.do_limit]
            for cat in limit_categories:
                tf = ROOT.TFile(self.workdir + "/limits/{0}.root".format(cat.full_name))
                for proc in cat.out_processes:
                    h = tf.Get("{0}__{1}".format(proc, cat.full_name))
                    ih = -1
                    if h:
                        ih = "{0:.2f}".format(h.Integral())
                    of.write(",".join([groupname, cat.full_name, proc, ih]) + "\n")
        of.close()

def make_workdir():
    workflow_id = uuid.uuid4()
    workdir = "results/{0}".format(workflow_id)
    os.makedirs(workdir)
    return workdir

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
    parser.add_argument(
        '--queue',
        action = "store",
        help = "Job queue",
        type = str,
        default = "EXISTING"
    )
    parser.add_argument(
        '--workdir',
        action = "store",
        help = "working directory",
        type = str,
        default = None, 
    )
    
    args = parser.parse_args()
   
    new_workflow = True
    if not args.workdir:
        workdir = make_workdir()
    else:
        new_workflow = False
        workdir = args.workdir
    logger.info("starting workflow {0}".format(workdir))

    queue_kwargs = {}
    if args.queue == "SYNC":
        queue_kwargs["async"] = False
    # Tell RQ what Redis connection to use
    redis_conn = Redis(host=args.hostname, port=args.port)
    qmain = Queue("default", connection=redis_conn, **queue_kwargs)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)
    
    #clean queues in case they are full
    if len(qmain) > 0:
        logger.warning("main queue has jobs, emptying")
        qmain.empty()

    if len(qfail) > 0:
        logger.warning("fail queue has jobs, emptying")
        qfail.empty()
    
    if args.config.endswith("cfg"):
        analysis = analysisFromConfig(args.config)
    elif args.config.endswith("pickle"):
        analysis = Analysis.deserialize(args.config)
    else:
        Exception("Unknown analysis input file")

    tasks = []
    tasks += [
        #TaskValidateFiles(workdir, "VALIDATE", analysis),
        #TaskNumGen(workdir, "NGEN", analysis),
        #TaskSparsinator(workdir, "SPARSE", analysis),
        #TaskSparseMerge(workdir, "MERGE", analysis),
        #TaskCategories(workdir, "CAT", analysis),
        #TaskPlotting(workdir, "PLOT", analysis),
        TaskLimits(workdir, "LIMIT", analysis),
        TaskTables(workdir, "TABLES", analysis)
    ]

    inputs = []

    #create first analysis pickle file
    if new_workflow:
        tasks[0].save_state()

    for task in tasks:
        res = task.run(inputs, redis_conn, qmain, qfail)
        inputs = res
