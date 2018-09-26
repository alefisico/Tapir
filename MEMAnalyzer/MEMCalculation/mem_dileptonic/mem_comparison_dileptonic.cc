/*
 *  MoMEMta: a modular implementation of the Matrix Element Method
 *  Copyright (C) 2016  Universite catholique de Louvain (UCL), Belgium
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


#include <momemta/ConfigurationReader.h>
#include <momemta/Logging.h>
#include <momemta/MoMEMta.h>
#include <momemta/Unused.h>

#include <TTree.h>
#include <TChain.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <Math/PtEtaPhiM4D.h>
#include <Math/LorentzVector.h>
#include <TMath.h>

#include <chrono>
#include <memory>
#include <iostream>

/*///////////// oldMEM
#include "../../../TTH/MEIntegratorStandalone/interface/Integrand.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "Math/GSLMCIntegrator.h"
#include "Math/IOptions.h"
#include "Math/IntegratorOptions.h"
#include "Math/AllIntegrationTypes.h"
#include "TFile.h"
#include <iostream>
*/

using namespace std::chrono;
using namespace std;
//using namespace MEM;

using LorentzVectorM = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>;

/*
 * Example executable file loading an input sample of events,
 * computing weights using MoMEMta in the fully-leptonic ttbar hypothesis,
 * and saving these weights along with a copy of the event content in an output file.
 */

void normalizeInput(LorentzVector& p4) {
    if (p4.M() > 0)
        return;

    // Increase the energy until M is positive
    p4.SetE(p4.P());
    while (p4.M2() < 0) {
        double delta = p4.E() * 1e-5;
        p4.SetE(p4.E() + delta);
    };
}

int main(int argc, char* argv[]) {

    UNUSED(argc);
    //UNUSED(argv);
    string outputName("mem_diLeptonic_weights");
    outputName.append(argv[1]);
    outputName.append(".root");

    string ttH("ttH");
    string ttbar("ttbar");
    LOG(info) << "Running sample " << outputName;

    using std::swap;

    /*
     * Load events from input file, retrieve reconstructed particles and MET
     */
    TChain chain("tree");
    //chain.Add("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Jul18_withME/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/Jul18_withME/180718_120512/0000/tree_82.root");
    if (outputName.find(ttH) != string::npos) {
      chain.Add("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Jul18_withME/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/Jul18_withME/180718_120512/0000/tree_139.root");
    } else {
      chain.Add("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Jul18_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Jul18_withME/180718_120426/0000/tree_182.root");
    }
    TTreeReader myReader(&chain);

    /*TTreeReaderValue<LorentzVectorM> lep_plus_p4M(myReader, "lep1_p4");
    TTreeReaderValue<LorentzVectorM> lep_minus_p4M(myReader, "lep2_p4");
    TTreeReaderValue<LorentzVectorM> bjet1_p4M(myReader, "bjet1_p4");
    TTreeReaderValue<LorentzVectorM> bjet2_p4M(myReader, "bjet2_p4");
    TTreeReaderValue<LorentzVectorM> bjet3_p4M(myReader, "jet3_p4");
    TTreeReaderValue<LorentzVectorM> bjet4_p4M(myReader, "jet4_p4");
    */
    TTreeReaderValue<int> numLep(myReader, "nleps");
    TTreeReaderArray<Float_t> lepspt(myReader, "leps_pt");
    TTreeReaderArray<Float_t> lepseta(myReader, "leps_eta");
    TTreeReaderArray<Float_t> lepsphi(myReader, "leps_phi");
    TTreeReaderArray<Float_t> lepsmass(myReader, "leps_mass");
    TTreeReaderValue<int> numJets(myReader, "njets");
    TTreeReaderArray<Float_t> jetspt(myReader, "jets_pt");
    TTreeReaderArray<Float_t> jetseta(myReader, "jets_eta");
    TTreeReaderArray<Float_t> jetsphi(myReader, "jets_phi");
    TTreeReaderArray<Float_t> jetsmass(myReader, "jets_mass");
    TTreeReaderArray<Float_t> jetsBtagFlag(myReader, "jets_btagFlag");
    TTreeReaderValue<float> METmet(myReader, "met_pt");
    TTreeReaderValue<float> METphi(myReader, "met_phi");
    TTreeReaderArray<Float_t> lepspdfId(myReader, "leps_pdgId");

    /*
     * Define output TTree, which will contain the weights we're computing (including uncertainty and computation time)
     */
    std::unique_ptr<TTree> out_tree = std::make_unique<TTree>("memTree", "memTree");
    double weight_TTH, weight_TTH_err, weight_TTH_time, weight_TTbb, weight_TTbb_err, weight_TTbb_time, mem;
    out_tree->Branch("weight_TTH", &weight_TTH);
    out_tree->Branch("weight_TTH_err", &weight_TTH_err);
    out_tree->Branch("weight_TTH_time", &weight_TTH_time);
    out_tree->Branch("weight_TTbb", &weight_TTbb);
    out_tree->Branch("weight_TTbb_err", &weight_TTbb_err);
    out_tree->Branch("weight_TTbb_time", &weight_TTbb_time);
    out_tree->Branch("mem", &mem);

    /*
     * Prepare MoMEMta to compute the weights
     */
    // Set MoMEMta's logging level to `debug`, options: trace, debug, info, warning, error, fatal, off
    logging::set_level(logging::level::info);

    //////////////////////// ttH
    ConfigurationReader configTTH("/mnt/t3nfs01/data01/shome/algomez/work/ttH/CMSSW_9_4_9/src/MoMEMta/Tutorials/mem_dileptonic/ttH_TTToFullyLeptonic_HToBBbar.lua"); // Construct the ConfigurationReader from the Lua file
    MoMEMta weightTTH(configTTH.freeze());   // Instantiate MoMEMta using a **frozen** configuration
    //////////////////////// ttbb
    ConfigurationReader configTTbb("/mnt/t3nfs01/data01/shome/algomez/work/ttH/CMSSW_9_4_9/src/MoMEMta/Tutorials/mem_dileptonic/ttbb_TTToFullyLeptonic.lua"); // Construct the ConfigurationReader from the Lua file
    MoMEMta weightTTbb(configTTbb.freeze());   // Instantiate MoMEMta using a **frozen** configuration

    /*
     * Loop over all input events
     */
    // int dummy = 0;
    while (myReader.Next()) {
        /*
         * Prepare the LorentzVectors passed to MoMEMta:
         * In the input file they are written in the PtEtaPhiM<float> basis,
         * while MoMEMta expects PxPyPzE<double>, so we have to perform this change of basis:
         *
         * We define here Particles, allowing MoMEMta to correctly map the inputs to the configuration file.
         * The string identifier used here must be the same as used to declare the inputs in the config file
         */

        vector<LorentzVectorM> bjets;
        if (*numJets>4){
          for (size_t ijet = 0; ijet < jetspt.GetSize(); ijet++) {
            //cout << "Alll " << jetsBtagFlag[ijet]  << endl;
            if ( ( jetsBtagFlag[ijet] != 0 )  and (jetspt[ijet] > 30) ){
              //cout << "Pass " << jetsBtagFlag[ijet]  << endl;
              LorentzVectorM tmp { jetspt[ijet], jetseta[ijet], jetsphi[ijet], jetsmass[ijet] };
              bjets.push_back( tmp );
            }
          }
        }
        //cout << bjets.size() << endl;

        if ( ( (*numLep) > 1 ) and ( bjets.size() > 3 ) ){
          //if((dummy++)==10) break;
          if ((( lepspt[0] > 25 ) and ( lepseta[0] < 2.4 )) and 
            (( lepspt[1] > 15 ) and ( lepseta[1] < 2.4 )) and 
            ((*METmet) > 40 ))  {

            LorentzVectorM lep1 { lepspt[0], lepseta[0], lepsphi[0], lepsmass[0] };
            momemta::Particle lep_plus("lepton1", LorentzVector { lep1.Px(), lep1.Py(), lep1.Pz(), lep1.E() });
            LorentzVectorM lep2 { lepspt[1], lepseta[1], lepsphi[1], lepsmass[1] };
            momemta::Particle lep_minus("lepton2", LorentzVector { lep2.Px(), lep2.Py(), lep2.Pz(), lep2.E() });

            momemta::Particle bjet1("top_bjet1", LorentzVector { bjets[0].Px(), bjets[0].Py(), bjets[0].Pz(), bjets[0].E() });
            momemta::Particle bjet2("top_bjet2", LorentzVector { bjets[1].Px(), bjets[1].Py(), bjets[1].Pz(), bjets[1].E() });
            momemta::Particle bjet3("higgs_bjet1", LorentzVector { bjets[2].Px(), bjets[2].Py(), bjets[2].Pz(), bjets[2].E() });
            momemta::Particle bjet4("higgs_bjet2", LorentzVector { bjets[3].Px(), bjets[3].Py(), bjets[3].Pz(), bjets[3].E() });

            // Due to numerical instability, the mass can sometimes be negative. If it's the case, change the energy in order to be mass-positive
            normalizeInput(lep_plus.p4);
            normalizeInput(lep_minus.p4);
            normalizeInput(bjet1.p4);
            normalizeInput(bjet2.p4);
            normalizeInput(bjet3.p4);
            normalizeInput(bjet4.p4);

            LorentzVectorM met_p4M { *METmet, 0, *METphi, 0 };
            LorentzVector met_p4 { met_p4M.Px(), met_p4M.Py(), met_p4M.Pz(), met_p4M.E() };

            // Ensure the leptons are given in the correct order w.r.t their charge
            if ( lepspdfId[0] < lepspdfId[1] )  swap(lep_plus, lep_minus);

            auto start_time = system_clock::now();
            // Compute the weights for ttH
            std::vector<std::pair<double, double>> weightsTTH = weightTTH.computeWeights({lep_minus, bjet1, lep_plus, bjet2, bjet3, bjet4}, met_p4);
            auto end_time = system_clock::now();
            // Retrieve the weight and uncertainty
            weight_TTH = - TMath::Log( weightsTTH.back().first );
            weight_TTH_err = weightsTTH.back().second;
            weight_TTH_time = std::chrono::duration_cast<milliseconds>(end_time - start_time).count();

            // Comput the weights for ttbb
            auto start_time_ttbb = system_clock::now();
            std::vector<std::pair<double, double>> weightsTTbb = weightTTbb.computeWeights({lep_minus, bjet1, lep_plus, bjet2, bjet3, bjet4}, met_p4);  /// order here has to match order in particles ids.
            auto end_time_ttbb = system_clock::now();
            weight_TTbb = - TMath::Log( weightsTTbb.back().first );
            weight_TTbb_err = weightsTTbb.back().second;
            weight_TTbb_time = std::chrono::duration_cast<milliseconds>(end_time_ttbb - start_time_ttbb).count();

            //LOG(debug) << "Event " << myReader.GetCurrentEntry() << " result: " << weight_TT << " +- " << weight_TT_err;
            mem = weight_TTH / ( weight_TTH + weight_TTbb );
            //double mem = weight_TTH / ( weight_TTH + (0.1 * weight_TTbb) );
            LOG(info) << "Event " << myReader.GetCurrentEntry() << " result ttH: " << weight_TTH << " +- " << weight_TTH_err << "; result ttbb: " << weight_TTbb << " +- " << weight_TTbb_err << " mem: " << mem;
            LOG(info) << "Weight computed in " << weight_TTH_time << "ms and " << weight_TTbb_time << "ms";

            out_tree->Fill();
            }
        }
    }

    // Save our output TTree
    out_tree->SaveAs(outputName.c_str());

    return 0;
}
