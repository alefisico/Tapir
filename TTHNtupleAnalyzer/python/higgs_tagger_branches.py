#sample branches file for headergen.py
#uses branch classes from headergen
from TTH.TTHNtupleAnalyzer.headergen import *

defines.extend(["#define ADD_TRUE_TOP_MATCHING_FOR_FJ 1",
                "#define ADD_TRUE_TOP_MATCHING_FOR_HTT 1",
                "#define ADD_TRUE_TOP_MATCHING_FOR_CMSTT 1",
                "#define ADD_TRUE_HIGGS_MATCHING_FOR_FJ 1",
                "#define ADD_TRUE_HIGGS_MATCHING_FOR_HTT 1",
                "#define ADD_TRUE_HIGGS_MATCHING_FOR_CMSTT 1",
                "#define ADD_TRUE_PARTON_MATCHING_FOR_FJ 1",
                "#define ADD_TRUE_PARTON_MATCHING_FOR_HTT 1",
                "#define ADD_TRUE_PARTON_MATCHING_FOR_CMSTT 1"])


#define branches to add here
process = [
	Scalar("gen_t__dpt_alt", "float"),
	Scalar("gen_tbar__dpt_alt", "float"),
]


process += Scalar("weight__genmc", "float"),

# Simple Truth Branches
# - Just the kinematics
# - above a pT threshold
# - these are the objects the jets/taggers are matched to and know the indices of
for particle in ["hadtop", "higgs", "parton"]:

    counter_name =  "n__gen_{0}".format(particle)
    process += [Scalar(counter_name, "int")]

    for v in ["eta", "mass", "phi", "pt"]:
        full_branch_name = "gen_{0}__{1}".format(particle, v)
        process += [Dynamic1DArray(full_branch_name, "float", counter_name, "N_MAX")]
# End of Simple Truth


# True Top Branches
for t in ["t", "tbar", "t2", "tbar2"]:
    for v in [
        ("eta"), ("mass"), ("phi"), ("pt"), ("status"),
        ("b__eta"), ("b__mass"), ("b__phi"), ("b__pt"), ("b__status"),
        ("w_d1__eta"), ("w_d1__mass"), ("w_d1__phi"), ("w_d1__pt"), ("w_d1__status"), ("w_d1__id"),
        ("w_d2__eta"), ("w_d2__mass"), ("w_d2__phi"), ("w_d2__pt"), ("w_d2__status"), ("w_d2__id")
    ]:
        typ = "float"
        if "status" in v or "id" in v:
            typ = "int"
        process += [Scalar("gen_%s__%s" % (t, v), typ)]

# True Top Branches
for t in ["b", "bbar"]:
    for v in ["eta", "mass", "phi", "pt", "status", "id"]:
        typ = "float"
        if "status" in v or "id" in v:
            typ = "int"
        process += [Scalar("gen_%s__%s" % (t, v), typ)]

for t in ["pt", "eta", "phi", "mass",
    "dxy", "dz",
    "ch_iso", "ec_iso", "hc_iso",
    "mva",
    "p_iso", "ph_iso", "puch_iso", "rel_iso", "rel_iso2"]:
    full_branch_name = "lep__{0}".format(t)
    process += [
        Dynamic1DArray(full_branch_name, "float", "n__lep", "N_MAX")
    ]

for t in ["id", "id_bitmask", "is_loose", "is_medium", "is_tight",
    "is_tight_id", "charge", "type"]:
    full_branch_name = "lep__{0}".format(t)
    process += [
        Dynamic1DArray(full_branch_name, "int", "n__lep", "N_MAX")
    ]

for t in ["pt", "eta", "phi", "pass"]:
    for x in ["lep", "jet"]:
        full_branch_name = "trig_{0}__{1}".format(x, t)
        process += [
            Dynamic1DArray(full_branch_name, "int" if t=="pass" else "float", "n__{0}".format(x), "N_MAX")
        ]

for t in ["pt", "eta", "phi", "mass"]:
    full_branch_name = "sig_lep__{0}".format(t)
    process += [
        Dynamic1DArray(full_branch_name, "float", "n__sig_lep", "N_MAX")
    ]

for t in ["charge", "id", "idx", "type"]:
    full_branch_name = "sig_lep__{0}".format(t)
    process += [
        Dynamic1DArray(full_branch_name, "int", "n__sig_lep", "N_MAX")
    ]

for t in [
    "bd_csv",
    "ce_e",
    "ch_e",
    "el_e",
    "energy",
    "eta",
    "mass",
    "mu_e",
    "ne_e",
    "nh_e",
    "ph_e",
    "phi",
    "pileupJetId",
    "pt",
    "pt_alt",
    "unc",
    "vtx3DSig",
    "vtx3DVal",
    "vtxMass",
    "vtxNtracks"]:
    full_branch_name = "jet__{0}".format(t)
    process += [
        Dynamic1DArray(full_branch_name, "float", "n__jet", "N_MAX")
    ]

for t in [
    "id",
    "jetId",
    "pass_pileupJetId",
    "type"]:
    full_branch_name = "jet__{0}".format(t)
    process += [
        Dynamic1DArray(full_branch_name, "int", "n__jet", "N_MAX")
    ]

for t in [
    "mass",
    "phi",
    "pt",
    "eta"]:
    for x in ["gen_jet", "gen_jet_parton", "gen_lep"]:
        full_branch_name = "{0}__{1}".format(x, t)
        process += [
            Dynamic1DArray(full_branch_name, "float", "n__jet" if "jet" in x
                else "n__lep", "N_MAX")
        ]

for t in [
    "id",
    "status",
    "type"]:
    for x in ["gen_jet", "gen_jet_parton", "gen_lep"]:
        full_branch_name = "{0}__{1}".format(x, t)
        process += [
            Dynamic1DArray(full_branch_name, "int", "n__jet" if "jet" in x
                else "n__lep", "N_MAX")
        ]


# Fatjet Branches
for fj_name in ['ca15', 'ca15trimmedr2f4', 'ca15trimmedr2f6',
                'ca15trimmedr2f8', 'ca15softdropz15b00', 'ca15softdropz20b10',
                'ca15softdropz30b20', 'ca15softdropz30b30', 'ca15softdropz30b100']:

    print "Adding", fj_name

    # How many of these objects do we have?
    full_counter_name = "n__jet_{0}".format(fj_name)
    process += [Scalar(full_counter_name, "int")]

    # And all the individual float branches
    for branch_name in [
            "pt", "eta", "phi", "mass",  # Kinematics
            "tau1", "tau2", "tau3",      # N-subjettiness
            "btag",                      # b-tag discriminator
            "chi",                       # Shower deconstruction chi
                                         # (only fill for ca15 wo grooming at the moment)
            "qvol",                      # Qjet Volatility
                                         # (only fill for ca15 wo grooming at the moment)
            "close_hadtop_pt",  "close_hadtop_dr", "close_hadtop_i", # top truth matching
            "close_parton_pt",  "close_parton_dr", "close_parton_i", # parton truth matching
            "close_higgs_pt",   "close_higgs_dr",  "close_higgs_i"   # higgs truth matching
            ]:

        # Don't do chi unless we have the unfiltered fatjets
        if (branch_name in ["chi","qvol"]) and not (fj_name in ["ca15"]):
            continue

        if branch_name in ["close_higgs_i", "close_hadtop_i", "close_parton_i"]:
            the_type = "int"
        else:
            the_type = "float"

        full_branch_name = "jet_{0}__{1}".format(fj_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, 
                                   the_type,
                                   full_counter_name,
                                   "N_MAX"
                               )]

    # End of loop over branches
# End of loop over fat jets
