#include "TTH/Plotting/interface/Event.h"
#include "TTH/Plotting/interface/metree.h"

using namespace std;

Configuration::Configuration(
    vector<string>& _filenames,
    double _lumi,
    string _process,
    long _firstEntry,
    long _numEntries,
    int _printEvery
    ) :
    filenames(_filenames),
    lumi(_lumi),
    process(_process),
    firstEntry(_firstEntry),
    numEntries(_numEntries),
    printEvery(_printEvery)
{
}

const Configuration Configuration::makeConfiguration(JsonValue& value) {
    vector<string> filenames;
    double lumi = -1.0;
    string process = "UNDEFINED";
    long firstEntry = -1;
    long numEntries = -1;
    long printEvery = -1;

    for (auto lev1 : value) {
        const string ks = string(lev1->key);
        if (ks == "filenames") {
            for (auto lev2 : lev1->value) {
                if (lev2->value.getTag() == JSON_STRING) {
                    filenames.push_back(lev2->value.toString());
                }
            }
        }
        else if (ks == "lumi") {
            lumi = lev1->value.toNumber();
        }
        else if (ks == "process") {
            process = lev1->value.toString();
        }
        else if (ks == "firstEntry") {
            firstEntry = (long)(lev1->value.toNumber());
        }
        else if (ks == "numEntries") {
            numEntries = (long)(lev1->value.toNumber());
        }
        else if (ks == "printEvery") {
            printEvery = (long)(lev1->value.toNumber());
        }

    }
    return Configuration(filenames, lumi, process, firstEntry, numEntries, printEvery);
}

string Configuration::to_string() const {
    stringstream ss;
    ss << "Configuration(" << endl;;
    for (auto fn : this->filenames) {
        ss << "  file=" << fn << "," << endl;
    }
    ss << "  lumi=" << this->lumi << endl;
    ss << "  process=" << this->process << endl;
    ss << "  firstEntry=" << this->firstEntry << endl;
    ss << "  numEntries=" << this->numEntries << endl;
    ss << ")" << endl;
    return ss.str();
}


namespace SystematicKey {
const string to_string(SystematicKey k) {
    switch (k) {
        case nominal:
            return "nominal";
        case CMS_scale_jUp:
            return "CMS_scale_jUp";
        case CMS_scale_jDown:
            return "CMS_scale_jDown";
        case CMS_ttH_CSVStats1Up:
            return "CMS_ttH_CSVStats1Up";
        case CMS_ttH_CSVStats1Down:
            return "CMS_ttH_CSVStats1Down";
        case CMS_ttH_CSVStats2Up:
            return "CMS_ttH_CSVStats2Up";
        case CMS_ttH_CSVStats2Down:
            return "CMS_ttH_CSVStats2Down";
        case CMS_ttH_CSVLFUp:
            return "CMS_ttH_CSVLFUp";
        case CMS_ttH_CSVLFDown:
            return "CMS_ttH_CSVLFDown";
        case CMS_ttH_CSVHFUp:
            return "CMS_ttH_CSVHFUp";
        case CMS_ttH_CSVHFDown:
            return "CMS_ttH_CSVHFDown";

        default:
            return "UNKNOWN";
    }
}
}

namespace HistogramKey {
const string to_string(HistogramKey k) {
    switch (k) {
        case jet0_pt:
            return "jet0_pt";
        case mem_SL_0w2h2t:
            return "mem_SL_0w2h2t";
        case mem_SL_2w2h2t:
            return "mem_SL_2w2h2t";
        case mem_SL_2w2h2t_sj:
            return "mem_SL_2w2h2t_sj";
        case mem_DL_0w2h2t:
            return "mem_DL_0w2h2t";
        default:
            return "UNKNOWN";
    }
}
}

namespace CategoryKey {
const string to_string(CategoryKey k) {
    switch (k) {
        
        case sl:
            return "sl";
        case dl:
            return "dl";
        case j3_t2:
            return "j3_t2";
        case jge4_t2:
            return "jge4_t2";
        case jge3_tge3:
            return "jge3_tge3";
        case jge4_tge4:
            return "jge4_tge4";
        case j5_t3:
            return "j5_t3";
        case j5_tge4:
            return "j5_tge4";
        case jge6_t2:
            return "jge6_t2";
        case jge6_t3:
            return "jge6_t3";
        case jge6_tge4:
            return "jge6_tge4";
        case blrL:
            return "blrL";
        case blrH:
            return "blrH";
        default:
            return "UNKNOWN";
    }
}
bool is_sl(vector<CategoryKey> k) {
    return k[0] == sl;
}

bool is_dl(vector<CategoryKey> k) {
    return k[0] == dl;

}
}

void saveResults(ResultMap& res, const string& prefix, const string& filename) {
    cout << "Saving results to " << filename << ":" << prefix << endl;
    TFile of(filename.c_str(), "RECREATE");
    
    vector<ResultMap::key_type> resKeys;
    for (auto& kv : res) {
        resKeys.push_back(kv.first);
    }
    sort(resKeys.begin(), resKeys.end());

    for (auto rk : resKeys) {
        const auto systKey = get<1>(rk);
        const auto histKey = get<2>(rk);
        stringstream ss;
        ss << prefix << "/";

        //Add all categories together with underscores
        int ind = 0;
        for (auto& catKey : get<0>(rk)) {
            ss << CategoryKey::to_string(catKey);
            if (ind < get<0>(rk).size() - 1) {
                ss << "_";
            }
            ind++;
        }
        //make root dir if doesn't exist
        const string dirname = ss.str();
        if (of.Get(dirname.c_str()) == nullptr) {
            of.mkdir(dirname.c_str());
        }
        TDirectory* dir = (TDirectory*)(of.Get(dirname.c_str()));
        assert(dir != nullptr);

        //rename histogram
        stringstream ss2;
        ss2 << HistogramKey::to_string(histKey);

        //For variations, add also systematic name to histogram
        if (systKey != SystematicKey::nominal) {
            ss2 << "_" << SystematicKey::to_string(systKey);
        }
        const string histname = ss2.str();
        cout << dirname << "/ " << histname << endl;

        //We need to make a copy of the histogram here, otherwise ROOT scoping goes crazy
        //and of.Close() segfaults later
        TH1D hist = TH1D(res.at(rk));
        hist.SetName(histname.c_str());
        hist.SetDirectory(dir);
        dir->Write();
        //hist.Write();
    }
    cout << "writing..." << endl;
    of.Write();
    of.Close();
    cout << "done..." << endl;
}


Event::Event(
    bool _is_sl,
    bool _is_dl,
    bool _pass_trig_sl,
    bool _pass_trig_dl,
    bool _passPV,
    int _numJets,
    int _nBCSVM,
    const vector<Jet>& _jets,
    const Event::WeightMap& _weightFuncs,
    double _weight_xs,
    double _mem_SL_0w2h2t,
    double _mem_SL_2w2h2t,
    double _mem_SL_2w2h2t_sj,
    double _mem_DL_0w2h2t,
    double _bTagWeight,
    double _bTagWeight_Stats1Up,
    double _bTagWeight_Stats1Down,
    double _bTagWeight_Stats2Up,
    double _bTagWeight_Stats2Down,
    double _bTagWeight_LFUp,
    double _bTagWeight_LFDown,
    double _bTagWeight_HFUp,
    double _bTagWeight_HFDown
    ) :
    is_sl(_is_sl),
    is_dl(_is_dl),
    pass_trig_sl(_pass_trig_sl),
    pass_trig_dl(_pass_trig_dl),
    passPV(_passPV),
    numJets(_numJets),
    nBCSVM(_nBCSVM),
    jets(_jets),
    weightFuncs(_weightFuncs),
    weight_xs(_weight_xs),
    mem_SL_0w2h2t(_mem_SL_0w2h2t),
    mem_SL_2w2h2t(_mem_SL_2w2h2t),
    mem_SL_2w2h2t_sj(_mem_SL_2w2h2t_sj),
    mem_DL_0w2h2t(_mem_DL_0w2h2t),
    bTagWeight(_bTagWeight),
    bTagWeight_Stats1Up(_bTagWeight_Stats1Up),
    bTagWeight_Stats1Down(_bTagWeight_Stats1Down),
    bTagWeight_Stats2Up(_bTagWeight_Stats2Up),
    bTagWeight_Stats2Down(_bTagWeight_Stats2Down),
    bTagWeight_LFUp(_bTagWeight_LFUp),
    bTagWeight_LFDown(_bTagWeight_LFDown),
    bTagWeight_HFUp(_bTagWeight_HFUp),
    bTagWeight_HFDown(_bTagWeight_HFDown)
{
}


const string Event::to_string() const {
    stringstream ss;
    ss << "Event(" << this->numJets << "J, " << this->nBCSVM << "T";
    ss << endl;
    for (auto& jet : this->jets) {
        ss << " j " << jet.to_string() << endl;
    }
    ss << " bw=" << this->bTagWeight << endl;
    ss << ");" << endl;
    return ss.str();
}
//jetMaker - a function from JetFactory to make the jets
const vector<Jet> makeAllJets(const TreeData& data,
    const Jet (*jetMaker)(const TreeData&, int)) {
    vector<Jet> jets;

    for (int nj=0; nj<data.njets; nj++) {
        const Jet& jet = jetMaker(data, nj); 
        jets.push_back(jet);
    }
    return jets;
}

double nominal_weight(const Event& ev) {
    return ev.weight_xs * ev.bTagWeight;
}
//Vector of nominal weight functions
static const Event::WeightMap nominalWeights = {
    {SystematicKey::nominal, nominal_weight}
};

static const Event::WeightMap systWeights = {
    {SystematicKey::nominal, nominal_weight},
    {
        SystematicKey::CMS_ttH_CSVStats1Up,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats1Up;}
    },
    {
        SystematicKey::CMS_ttH_CSVStats1Down,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats1Down;}
    },
    {
        SystematicKey::CMS_ttH_CSVStats2Up,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats2Up;}
    },
    {
        SystematicKey::CMS_ttH_CSVStats2Down,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats2Down;}
    },
    {
        SystematicKey::CMS_ttH_CSVLFUp,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_LFUp;}
    },
    {
        SystematicKey::CMS_ttH_CSVLFDown,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_LFDown;}
    },
    {
        SystematicKey::CMS_ttH_CSVHFUp,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_HFUp;}
    },
    {
        SystematicKey::CMS_ttH_CSVHFDown,
        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_HFDown;}
    },
};

bool pass_trig_dl(const TreeData& data) {
    return (
        data.HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v ||
        data.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v ||
        data.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v ||
        data.HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v
    );
}

bool pass_trig_sl(const TreeData& data) {
    return (
        data.HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v ||
        data.HLT_BIT_HLT_IsoMu24_eta2p1_v
    );
}

double mem_p(double p_tth, double p_ttbb) {
    return p_tth / (p_tth + 0.02 * p_ttbb);
}

const Event EventFactory::makeNominal(const TreeData& data) {
    
    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeNominal));
    const Event ev(
        data.is_sl,
        data.is_dl,
        pass_trig_sl(data),
        pass_trig_dl(data),
        data.passPV,
        data.numJets,
        data.nBCSVM,
        jets,
        systWeights,
        data.weight_xs,
        mem_p(data.mem_tth_p[0], data.mem_ttbb_p[0]), //SL 022
        mem_p(data.mem_tth_p[5], data.mem_ttbb_p[5]), //SL 222
        mem_p(data.mem_tth_p[9], data.mem_ttbb_p[9]), //SL 222 sj
        mem_p(data.mem_tth_p[1], data.mem_ttbb_p[1]), //DL 022,
        data.bTagWeight,
        data.bTagWeight_Stats1Up,
        data.bTagWeight_Stats1Down,
        data.bTagWeight_Stats2Up,
        data.bTagWeight_Stats2Down,
        data.bTagWeight_LFUp,
        data.bTagWeight_LFDown,
        data.bTagWeight_HFUp,
        data.bTagWeight_HFDown
    );
    return ev;
}

const Event EventFactory::makeJESUp(const TreeData& data) {
    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJESUp));

    return Event(
        data.is_sl,
        data.is_dl,
        pass_trig_sl(data),
        pass_trig_dl(data),
        data.passPV,
        data.numJets_JESUp,
        data.nBCSVM_JESUp,
        jets,
        nominalWeights,
        data.weight_xs,
        mem_p(data.mem_tth_JESUp_p[0], data.mem_ttbb_JESUp_p[0]), //SL 022
        mem_p(data.mem_tth_JESUp_p[5], data.mem_ttbb_JESUp_p[5]), //SL 222
        mem_p(data.mem_tth_JESUp_p[9], data.mem_ttbb_JESUp_p[9]), //SL 222 sj
        mem_p(data.mem_tth_JESUp_p[1], data.mem_ttbb_JESUp_p[1]), //DL 022,
        data.bTagWeight,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    );
}

const Event EventFactory::makeJESDown(const TreeData& data) {
    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJESDown));

    return Event(
        data.is_sl,
        data.is_dl,
        pass_trig_sl(data),
        pass_trig_dl(data),
        data.passPV,
        data.numJets_JESDown,
        data.nBCSVM_JESDown,
        jets,
        nominalWeights,
        data.weight_xs,
        mem_p(data.mem_tth_JESDown_p[0], data.mem_ttbb_JESDown_p[0]), //SL 022
        mem_p(data.mem_tth_JESDown_p[5], data.mem_ttbb_JESDown_p[5]), //SL 222
        mem_p(data.mem_tth_JESDown_p[9], data.mem_ttbb_JESDown_p[9]), //SL 222 sj
        mem_p(data.mem_tth_JESDown_p[1], data.mem_ttbb_JESDown_p[1]), //DL 022,
        data.bTagWeight,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    );
}


Jet::Jet(const TLorentzVector& _p4, int _btagCSV) : 
    p4(_p4),
    btagCSV(_btagCSV)
{
}

const Jet JetFactory::makeNominal(const TreeData& data, int njet) {
    assert(njet <= data.njets);
    TLorentzVector p4;
    p4.SetPtEtaPhiM(
        data.jets_pt[njet],
        data.jets_eta[njet],
        data.jets_phi[njet],
        data.jets_mass[njet]
    );
    return Jet(p4, data.jets_btagCSV[njet]);
}

const Jet JetFactory::makeJESUp(const TreeData& data, int njet) {
    assert(njet <= data.njets);
    TLorentzVector p4;
    p4.SetPtEtaPhiM(
        data.jets_pt[njet],
        data.jets_eta[njet],
        data.jets_phi[njet],
        data.jets_mass[njet]
    );
    //Undo nominal correction, re-do JESUp correction
    const double corr = data.jets_corr_JESUp[njet] / data.jets_corr[njet];
    p4 *= (1.0 / corr);
    return Jet(p4, data.jets_btagCSV[njet]);
}


const Jet JetFactory::makeJESDown(const TreeData& data, int njet) {
    assert(njet <= data.njets);
    TLorentzVector p4;
    p4.SetPtEtaPhiM(
        data.jets_pt[njet],
        data.jets_eta[njet],
        data.jets_phi[njet],
        data.jets_mass[njet]
    );
    //Undo nominal correction, re-do JESDown correction
    const double corr = data.jets_corr_JESDown[njet] / data.jets_corr[njet];
    p4 *= (1.0 / corr);
    return Jet(p4, data.jets_btagCSV[njet]);
}


const string Jet::to_string() const {
    stringstream ss;
    ss << "pt=" << this->p4.Pt()
        << " eta=" << this->p4.Eta()
        << " phi=" << this->p4.Phi()
        << " m=" << this->p4.M()
        << " btagCSV=" << this->btagCSV;
    return ss.str();
}

void CategoryProcessor::fillHistograms(
    const Event& event,
    ResultMap& results,
    const tuple<
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey
    > key,
    double weight
    ) const {


    const auto jet0_pt_key = make_tuple(
        get<0>(key),
        get<1>(key),
        HistogramKey::jet0_pt
    );
    if (!results.count(jet0_pt_key)) {
        results[jet0_pt_key] = TH1D("jet0_pt", "Leading jet pt", 100, 0, 500);
    }
    results[jet0_pt_key].Fill(event.jets[0].p4.Pt(), weight);
    // cout << "CategoryProcessor::fillHistograms " <<
    //     to_string(jet0_pt_key) << " " <<
    //     event.jets[0].p4.Pt() << " " << weight << endl;
}

void CategoryProcessor::process(const Event& event, const Configuration& conf, const vector<CategoryKey::CategoryKey>& catKey, SystematicKey::SystematicKey systKey) {
    const bool passes = (*kvCat.second)(event);
    if (passes) {
        for (auto& kvWeight : event.weightFuncs) {
            const double weight = conf.lumi * kvWeight.second(event);
            if (do_print) {
                cout << "w " << SystematicKey::to_string(kvWeight.first) << " " << weight << endl;;
            }
            SystematicKey::SystematicKey _systKey = systKey;
            if (systKey == SystematicKey::nominal) {
                _systKey = kvWeight.first;
            }
            this->fillHistograms(
                event, results,
                make_tuple(catKey, _systKey),
                weight
            );
            for (auto& subcat : this->subCategories) {
                subcat.process(event, conf, catKey, systKey)
            }
        } // weightFuncs
    } // passes
}

void MEMCategoryProcessor::fillHistograms(
    const Event& event,
    ResultMap& results,
    const tuple<
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey
    > key,
    double weight
    ) const {

    //fill base histograms
    CategoryProcessor::fillHistograms(event, results, key, weight);

    if (CategoryKey::is_sl(get<0>(key))) {
        const auto mem_SL_0w2h2t_key = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::mem_SL_0w2h2t
        );

        if (!results.count(mem_SL_0w2h2t_key)) {
            results[mem_SL_0w2h2t_key] = TH1D("mem_SL_0w2h2t", "mem SL 0w2h2t", 12, 0, 1);
        }
        results[mem_SL_0w2h2t_key].Fill(event.mem_SL_0w2h2t, weight);
    } else if (CategoryKey::is_dl(get<0>(key))) {
        const auto mem_DL_0w2h2t_key = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::mem_DL_0w2h2t
        );

        if (!results.count(mem_DL_0w2h2t_key)) {
            results[mem_DL_0w2h2t_key] = TH1D("mem_DL_0w2h2t", "mem DL 0w2h2t", 12, 0, 1);
        }
        results[mem_DL_0w2h2t_key].Fill(event.mem_DL_0w2h2t, weight);
    }
}

string to_string(const ResultKey& k) {
    stringstream ss;
    ss << "ResultKey(";
    for (auto& v : get<0>(k)) {
        ss << CategoryKey::to_string(v) << ", ";
    }
    ss << SystematicKey::to_string(get<1>(k)) << ", ";
    ss << HistogramKey::to_string(get<2>(k)) << ")";
    return ss.str();
}

string to_string(const ResultMap& res) {
    stringstream ss;
    ss << "ResultMap[" << endl;
    for (auto& kv : res) {
        ss << " " << to_string(kv.first)
            << " " << kv.second.GetName()
            << " N=" << kv.second.GetEntries()
            << " I=" << kv.second.Integral()
            << " mu=" << kv.second.GetMean() << endl;
    }
    ss << "]" << endl;
    return ss.str();
}

Configuration parseJsonConf(const string& infile) {
    cout << "Loading json configuration from " << infile << endl;

    std::ifstream t(infile);
    if (!t.good()) {
        cerr << "Could not open file " << infile << endl;
        exit(EXIT_FAILURE);
    }
    std::stringstream buffer;
    buffer << t.rdbuf();

    char *endptr = nullptr;
    string indata = buffer.str();
    char *pindata = new char[indata.length() + 1];
    strcpy(pindata, indata.c_str());

    JsonValue value;
    JsonAllocator jsonAllocator;

    int status = jsonParse(pindata, &endptr, &value, jsonAllocator);
    if (status != JSON_OK) {
        cerr << jsonStrError(status) << endptr - pindata << endl;
        exit(EXIT_FAILURE);
    }
    
    return Configuration::makeConfiguration(value);
}
