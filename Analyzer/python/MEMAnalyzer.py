import ROOT
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import numpy as np

from TTH.Analyzer.MEMUtils import set_integration_vars, add_obj
from TTH.Analyzer.MEMConfig import MEMConfig

import logging

#Pre-define shorthands for permutation and integration variable vectors
CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")
#CmapDistributionTypeTH3D = getattr(ROOT, "std::map<MEM::DistributionType::DistributionType,TH3D>")

LOG_MODULE_NAME = logging.getLogger(__name__)

def normalize_proba(vec):
    proba_vec = np.array(vec)
    proba_vec[proba_vec <= 1E-50] = 1E-50
    ret = np.array(np.log10(proba_vec), dtype="float64")
    return ret

class MEMPermutation:
    MAXOBJECTS=10

    def __init__(self, idx,
        perm,
        p_mean, p_std,
        p_tf_mean, p_tf_std,
        p_me_mean, p_me_std,
        ):
        self.idx = idx
        self.perm = perm
        for i in range(MEMPermutation.MAXOBJECTS):
            r = perm[i] if i<len(perm) else -99
            setattr(self, "perm_{0}".format(i), r)
        self.p_mean = p_mean
        self.p_std = p_std
        self.p_tf_mean = p_tf_mean
        self.p_tf_std = p_tf_std
        self.p_me_mean = p_me_mean
        self.p_me_std = p_me_std

class MEMAnalyzer(Module):
    """
    Performs ME calculation using the external integrator.
    It supports multiple MEM algorithms at the same time, configured via the
    self.configs dictionary. The outputs are stored in a vector in the event.

    The ME algorithms are run only in case the njet/nlep/Wtag category (event.cat)
    is in the accepted categories specified in the config.
    Additionally, we require the b-tagging category (event.cat_btag) to be "H" (high).

    For each ME configuration on each event, the jets which are counted to be b-tagged
    in event.selected_btagged_jets_high are added as the candidates for t->b (W) or h->bb.
    These jets must be exactly 4, otherwise no permutation is accepted (in case
    using BTagged/QUntagged assumptions).

    Any additional jets are assumed to come from the hadronic W decay. These are
    specified in event.wquark_candidate_jets.

    Based on the event njet/nlep/Wtag category, if a jet fmor the W is counted as missing,
    it is integrated over using additional variables set by self.vars_to_integrate.

    self.vars_to_integrate_any contains the list of particles which are integrated over assuming
    perfect reconstruction efficiency.

    The MEM top pair hypothesis (di-leptonic or single leptonic top pair) is chosen based
    on the reconstructed lepton multiplicity (event.good_leptons).

    The algorithm is shortly as follows:
    1. check if event passes event.cat and event.cat_btag
    2. loop over all MEM configurations i=[0...Nmem)
        2a. add all 4 b-tagged jets to integrator
        2b. add all 0-3 untagged jets to integrator
        2c. add all leptons to integrator
        2d. decide SL/DL top pair hypo based on leptons
        2e. based on event.cat, add additional integration vars
        2f. run ME integrator for both tth and ttbb hypos
        2g. save output in event.mem_output_tth[i] (or ttbb)
        2i. clean up event in integrator

    Relies on:
    event.good_jets, event.good_leptons, event.cat, event.met_pt

    Produces:
    mem_results_tth (MEMOutput): probability for the tt+H(bb) hypothesis
    mem_results_ttbb (MEMOutput): probability for the tt+bb hypothesis

    """
    def __init__(self, cfg_ana, isMC):
        self.conf = cfg_ana
        self.isMC = isMC

        self.mem_configs = self.conf.mem_configs
        for k, v in self.mem_configs.items():
            #v.configure_btag_pdf(self.conf)
            v.configure_transfer_function(self.conf)

        self.memkeysToRun = self.conf.mem["methodsToRun"]

        #Create an empty vector for the integration variables
        self.vars_to_integrate   = CvectorPSVar()
        self.vars_to_marginalize = CvectorPSVar()

        cfg = MEMConfig(self.conf)
        #cfg.configure_btag_pdf(self.conf)
        cfg.configure_transfer_function(self.conf)
        cfg.cfg.num_jet_variations = len(self.conf.mem["jet_corrections"])
        self.integrator = MEM.Integrand(
            1,#verbosity (debug code) 1=output,2=input,4=init,8=init_more,16=event,32=integration
            cfg.cfg
        )

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for key in self.memkeysToRun:
            for (hypo_name, hypo) in [ ("tth", MEM.Hypothesis.TTH), ("ttbb", MEM.Hypothesis.TTBB) ]:
                self.out.branch("mem_{0}_{1}".format(hypo_name, key),  "F");
        pass


    def getRightCorrection(self, jet, corr):
        corrfactor = 1
        if corr == "JERUp" or corr == "JERDown":
            corrfactor = jet.corr_JER
        else:
            corrfactor = jet.corr
        return getattr(jet, "corr_" + corr)/corrfactor

    def configure_mem(self, event, mem_cfg,confname):
        mem_cfg.cfg.num_jet_variations = len(self.conf.mem["jet_corrections"])
        self.vars_to_integrate.clear()
        self.vars_to_marginalize.clear()
        self.integrator.next_event()
        self.integrator.set_cfg(mem_cfg.cfg)

        set_integration_vars(self.vars_to_integrate, self.vars_to_marginalize, mem_cfg.mem_assumptions)

        bquarks = sorted(list(mem_cfg.b_quark_candidates(event)), key=lambda x: x.pt, reverse=True)
        for b in bquarks:
            b.btagFlag = 1.0

        if len(bquarks) > mem_cfg.maxBJets:
            LOG_MODULE_NAME.info("More than {0} b-quarks supplied, dropping last {1} from MEM".format(
                mem_cfg.maxBJets, len(bquarks) - mem_cfg.maxBJets
            ))
            for q in bquarks[mem_cfg.maxBJets:]:
                LOG_MODULE_NAME.info("Dropping jet pt={0} eta={1}".format(q.pt, q.eta))
            bquarks = bquarks[:mem_cfg.maxBJets]

        lquarks = sorted(list(mem_cfg.l_quark_candidates(event)), key=lambda x: x.pt, reverse=True)
        for l in lquarks:
            l.btagFlag = 0.0

        if len(lquarks) > mem_cfg.maxLJets:
            LOG_MODULE_NAME.info("More than {0} l-quarks supplied, dropping last {1} from MEM".format(
                mem_cfg.maxLJets, len(lquarks) - mem_cfg.maxLJets
            ))
            for q in lquarks[mem_cfg.maxLJets:]:
                LOG_MODULE_NAME.info("Dropping jet pt={0} eta={1}".format(q.pt, q.eta))
            lquarks = lquarks[:mem_cfg.maxLJets]

        event.mem_jets = bquarks + lquarks

        ##Only take up to 4 candidates, otherwise runtimes become too great
        for jet in bquarks + lquarks:
            #calculate jet corrections with an exception for JER
            #the Jetcorrs are expected to be relative correction. E.g. jetcorrs[JESUp] = JESUp / JES
            #TODO: CHECK THIS AGAIN ONCE JET CORRECTIONS ARE IMPLEMENTED FROM NANOAODPOSTPROCESSING!
            jetcorrs = []
            if (event.systematic=="nominal" or event.systematic=="CatChange") and self.isMC:
                for jc in self.conf.mem["jet_corrections"]:
                    new_pt = getattr(jet, "pt_corr_"+jc)
                    jetcorrs.append( new_pt/jet.pt )

            if "perm" in confname:
                add_obj(
                    self.integrator,
                    MEM.ObjectType.Jet,
                    p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                    obs_dict={
                        MEM.Observable.BTAG: jet.btagFlag,
                        #MEM.Observable.CSV: getattr(jet, mem_cfg.btagMethod, -1),
                        MEM.Observable.PDGID: getattr(jet, "PDGID", 0)
                        },
                    tf_dict={
                        MEM.TFType.bReco: jet.tf_b, MEM.TFType.qReco: jet.tf_l,
                    },
                    corrections = jetcorrs,
                )
            else:
                add_obj(
                    self.integrator,
                    MEM.ObjectType.Jet,
                    p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                    obs_dict={
                        MEM.Observable.BTAG: jet.btagFlag,
                        #MEM.Observable.CSV: getattr(jet, mem_cfg.btagMethod, -1),
                        #MEM.Observable.PDGID: getattr(jet, "PDGID", 0)
                        },
                    tf_dict={
                        MEM.TFType.bReco: jet.tf_b, MEM.TFType.qReco: jet.tf_l,
                    },
                    corrections = jetcorrs,
                    )
            LOG_MODULE_NAME.info("adding jet: pt={0} eta={1} phi={2} mass={3} btagFlag={4} pdgId={5}".format(
                jet.pt, jet.eta, jet.phi, jet.mass, jet.btagFlag, getattr(jet, "PDGID", 0)
            ))

        for lep in mem_cfg.lepton_candidates(event):
            add_obj(
                self.integrator,
                MEM.ObjectType.Lepton,
                p4s=(lep.pt, lep.eta, lep.phi, lep.mass),
                obs_dict={MEM.Observable.CHARGE: lep.charge},
            )
            LOG_MODULE_NAME.info("adding lep: pt={0} eta={1} phi={2} mass={3} charge={4}".format(
                lep.pt, lep.eta, lep.phi, lep.mass, lep.charge
            ))

        met_cand = mem_cfg.met_candidates(event)
        add_obj(
            self.integrator,
            MEM.ObjectType.MET,
            #MET is caused by massless object
            p4s=(met_cand.pt, 0, met_cand.phi, 0),
        )
        LOG_MODULE_NAME.info("adding met: pt={0} phi={1}".format(
            met_cand.pt, met_cand.phi
        ))

    def analyze(self, event):
        if event.catChange: #DS
            LOG_MODULE_NAME.info("MEMAna: processing catChange")
            res = self._process(event.catChange)
            event.catChange = res

        for (syst, event_syst) in event.systResults.items():
            if event_syst.systematic == "CatChange": #DS
                print "\n*************************"
                print "*** strange occurance ***"
                print "*************************\n"
                print "syst =", syst                 #DS

            if event_syst.passes_btag:
                if syst != "nominal":  #DS carry nominal mem results on each systematic (instead of whole nominal event)
                    if hasattr(event.systResults["nominal"], 'res'):
                        event_syst.nominal_memres = event.systResults["nominal"].res
                    if event.catChange:
                        event_syst.catChange_memres = event.catChange.res #DS

                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mem = False
                #fill outputs that need to be there, in case event was skipped
                for key in self.conf.mem["methodsToRun"]:
                    for hypo in ["tth", "ttbb"]:
                        k = "mem_{0}_{1}".format(hypo, key)
                        if not event.systResults.has_key(k):
                            setattr(event.systResults[syst], k, MEM.MEMOutput())
                            setattr(event.systResults[syst], k+"_perm", [])

        return self.conf.general["passall"] or np.any([v.passes_mem for v in event.systResults.values()])


    def _process(self, event):
        eventstr = "{0}:{1}:{2}".format(event.run, event.luminosityBlock, event.event)
        LOG_MODULE_NAME.debug("MEMAnalyzer started {0}".format(eventstr))

        #Clean up any old MEM state
        self.vars_to_integrate.clear()
        self.vars_to_marginalize.clear()
        self.integrator.next_event()
        event.res = {}

        LOG_MODULE_NAME.debug(
            str("MEM id={run},{lumi},{evt} cat={cat} cat_b={cat_btag} nj={nj} nt={nb} nel={n_el} nmu={n_mu} syst={syst} blr={blr} mW={mW}".format(
            run=event.run,
            lumi=event.luminosityBlock,
            evt=event.event,
            cat=event.cat,
            cat_btag=event.cat_btag,
            #is_sl=event.is_sl,
            #is_dl=event.is_dl,
            nj=event.numJets,
            nb=event.nBCSVM,
            n_el=event.n_el_SL,
            n_mu=event.n_mu_SL,
            syst=getattr(event, "systematic", None),
            blr=event.btag_LR_4b_2b,
            mW=event.Wmass,
        )))
        event.was_run = {}

        for hypo in [MEM.Hypothesis.TTH, MEM.Hypothesis.TTBB]:
            skipped = []
            for confname in self.memkeysToRun:
                mem_cfg = self.conf.mem_configs[confname]
                fstate = MEM.FinalState.Undefined
                if "dl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LL
                elif "sl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LH
                elif "fh" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.HH
                else:
                    if confname in self.memkeysToRun:
                        raise ValueError("Need to specify sl, dl of fh in assumptions but got {0}".format(str(mem_cfg.mem_assumptions)))
                    else:
                        event.res[(hypo, confname)] = MEM.MEMOutput()
                        continue

                #Choose resolved or boosted event selection criteria
                sel = "selection"
                if "sj" in confname:
                    sel = "selection_boosted"

                #Run MEM if we did not explicitly disable it
                if (
                        mem_cfg.do_calculate(event, mem_cfg) and
                        self.conf.mem[sel](event) and
                        confname in self.memkeysToRun and
                        (event.systematic in self.conf.mem["enabled_systematics"] or
                         event.systematic == "CatChange" or event.systematic == "nominal") #DS

                    ):

                    self.configure_mem(event, mem_cfg,confname)
                    if self.conf.mem["calcME"]:
                        LOG_MODULE_NAME.info("Integrator::run started hypo={0} conf={1} run:lumi:evt={2}:{3}:{4} {5}".format(
                            hypo, confname,
                            event.run, event.lumi, event.evt,
                            event.category_string
                        ))
                        LOG_MODULE_NAME.info("Integrator conf: candidates for bq={0} lq={1} syst={2}".format(
                            len(mem_cfg.b_quark_candidates(event)),
                            len(mem_cfg.l_quark_candidates(event)),
                            event.systematic
                        ))

                        r = self.integrator.run(
                            fstate,
                            hypo,
                            self.vars_to_integrate,
                            self.vars_to_marginalize,
                            mem_cfg.ncalls #if ncalls > 0, override builtin ncalls in MEIntegratorStandalone/src/Parameters.cpp
                        )
                        event.was_run[confname] = True
                        LOG_MODULE_NAME.info("Integrator::run done hypo={0} conf={1} cat={2}".format(hypo, confname, event.cat))
                    else:
                        #Create a dummy output
                        r = MEM.MEMOutput()

                    #Compute the gradient-based jet corrections
                    dw = {}
                    for fc in self.conf.mem["jet_corrections"]:
                        dw[fc] = 0.0
                    if getattr(event, "systematic", "nominal") and self.isMC:
                        for ijet, jet in enumerate(event.mem_jets):
                            if not (ijet < r.grad.size()):
                                continue
                            old_pt = jet.pt
                            old_corr = jet.corr
                            for fc in self.conf.mem["jet_corrections"]:
                                new_pt =  getattr(jet, "pt_corr_" + fc)
                                delta_pt = (new_pt - old_pt)
                                dw[fc] += r.grad.at(ijet) * delta_pt
                    r.dw = dw
                    event.res[(hypo, confname)] = r
                elif( #DS
                    event.changes_jet_category and
                    mem_cfg.do_calculate(event, mem_cfg) and
                    self.conf.mem["selection"](event) and
                    confname in self.memkeysToRun
                    ):
                    if "meminput" in self.conf.general["verbosity"]:
                        print event.systematic+" changes category - skipping mem "+confname
                    skipped += [confname]
                    r = MEM.MEMOutput()
                    event.res[(hypo, confname)] = r #DS

                else:
                    skipped += [confname]
                    r = MEM.MEMOutput()
                    event.res[(hypo, confname)] = r
            LOG_MODULE_NAME.debug("skipped confs {0}".format(skipped))

        #Add MEM results to event
        for key in self.memkeysToRun:
            p0 = 0.0
            p1 = 0.0

            #if it was a systematic event
            #AND the variation did not change the jet category
            #AND the nominal MEM was computed, get the variation off of that
            ############## check if CatChange is needed
            if event.systematic != "nominal" and event.systematic != "CatChange" and not event.changes_jet_category and hasattr(event, 'nominal_memres') and (MEM.Hypothesis.TTH,key) in event.nominal_memres.keys() and not event.systematic in self.conf.mem["enabled_systematics"]:
                if "meminput" in self.conf.general["verbosity"]:
                    print "getting mem for "+event.systematic+" from event.nominal_memres"

                icorr = self.conf.mem["jet_corrections"].index(event.systematic)
                #r1 = event.nominal_event.res[(MEM.Hypothesis.TTH, key)].variated
                #r2 = event.nominal_event.res[(MEM.Hypothesis.TTBB, key)].variated
                r1 = event.nominal_memres[(MEM.Hypothesis.TTH, key)].variated #DS
                r2 = event.nominal_memres[(MEM.Hypothesis.TTBB, key)].variated #DS

                p0 = r1.at(icorr) if icorr < r1.size() else 0.0
                p1 = r2.at(icorr) if icorr < r2.size() else 0.0
            elif event.systematic != "CatChange" and event.changes_jet_category and hasattr(event, 'catChange_memres') and (MEM.Hypothesis.TTH,key) in event.catChange_memres.keys() and not event.systematic in self.conf.mem["enabled_systematics"]: #DS
                if "meminput" in self.conf.general["verbosity"]:
                    print "getting mem for "+event.systematic+" from event.catChange_memres"
                icorr = self.conf.mem["jet_corrections"].index(event.systematic)
                #r1 = event.catChange_event.res[(MEM.Hypothesis.TTH, key)].variated
                #r2 = event.catChange_event.res[(MEM.Hypothesis.TTBB, key)].variated
                r1 = event.catChange_memres[(MEM.Hypothesis.TTH, key)].variated #DS
                r2 = event.catChange_memres[(MEM.Hypothesis.TTBB, key)].variated #DS
                p0 = r1.at(icorr) if icorr < r1.size() else 0.0
                p1 = r2.at(icorr) if icorr < r2.size() else 0.0 #DS

            #MEM was recomputed
            else:
                if "meminput" in self.conf.general["verbosity"]:
                    print "cannot get mem for "+event.systematic+" from nominal or catChange"

                p0 = event.res[(MEM.Hypothesis.TTH, key)].p
                p1 = event.res[(MEM.Hypothesis.TTBB, key)].p
            mem_p = p0 / (p0 + self.conf.mem["weight"]*p1) if p0 > 0 else -999
            ###print(p0, p1, mem_p)
            setattr(event, "mem_{0}_p".format(key), mem_p)

            for (hypo_name, hypo) in [
                ("tth", MEM.Hypothesis.TTH),
                ("ttbb", MEM.Hypothesis.TTBB)
            ]:
                mem_res = event.res[(hypo, key)]
                if  event.systematic != "nominal": #DS
                    mem_res.p = p0 if hypo_name=="tth" else p1 #DS

                setattr(event, "mem_{0}_{1}".format(hypo_name, key), mem_res)
                #self.out.fillBranch("mem_{0}_{1}".format(hypo_name, key), mem_res)

        #print out the JSON format for the standalone integrator
        for confname in self.memkeysToRun:
            mem_cfg = self.mem_configs[confname]

        event.passes_mem = True
        return event
