import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import resource
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MemoryAnalyzer(Module):
    def __init__(self):
        self.logger = logging.getLogger("MemoryAnalyzer")
        self.hpy = None
        self.do_heapy = False
        if self.do_heapy:
            try:
                from guppy import hpy
                self.hpy = hpy()
                self.hpy.setrelheap()
            except Exception as e:
                logging.error("Could not import guppy, skipping memory logging")

        self.heap_prev = None
    def beginJob(self):
        self.iEv = 0

    def analyze(self, event):
        self.iEv+=1
        memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if self.iEv % 1 == 0:
            logging.debug("memory usage at event {0}: {1:.2f} MB".format(self.iEv, memory/1024.0))

        if not self.hpy is None:
            heap = self.hpy.heap()
            if not self.heap_prev is None:
                diff = heap - self.heap_prev
                print diff
            self.heap_prev = heap
        return True
