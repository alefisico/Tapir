// -*- C++ -*-
//
// Package:    Tapir/myQuickAnalyzer
// Class:      quickAnalyzer
// 
/**\class quickAnalyzer quickAnalyzer.cc Tapir/myQuickAnalyzer/plugins/quickAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Alejandro Gomez Espinosa (ETHZ) [algomez]
//         Created:  Thu, 19 Apr 2018 13:27:51 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "Tapir/myQuickAnalyzer/interface/METzCalculator.h"

#include "TH1D.h"
#include <TH2D.h>
#include <TLorentzVector.h>
//
// class declaration
//
using namespace edm;
using namespace reco;
using namespace std;

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class quickAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
	public:
		explicit quickAnalyzer(const edm::ParameterSet&);
		~quickAnalyzer();

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

	private:
		virtual void beginJob() override;
		virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
		virtual void endJob() override;

		// ----------member data ---------------------------
		edm::EDGetTokenT<pat::JetCollection> AK4jets_;
		edm::EDGetTokenT<pat::JetCollection> AK8jets_;
		edm::EDGetTokenT<pat::ElectronCollection> electrons_;
		edm::EDGetTokenT<pat::MuonCollection> muons_;
		edm::EDGetTokenT<pat::METCollection> met_;
		edm::EDGetTokenT<std::vector<std::vector<int>>> listOfJetCandidates_;

		std::map< std::string, TH1D* > histos1D_;
		std::map< std::string, TH2D* > histos2D_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
quickAnalyzer::quickAnalyzer(const edm::ParameterSet& iConfig):
	AK4jets_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("AK4jets"))),
	AK8jets_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("AK8jets"))),
	electrons_(consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("electrons"))),
	muons_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
	met_(consumes<pat::METCollection>(iConfig.getParameter<edm::InputTag>("met"))),
	listOfJetCandidates_(consumes<std::vector<std::vector<int>>>(iConfig.getParameter<edm::InputTag>("listOfJetCandidates")))
{
	//now do what ever initialization is needed
	usesResource("TFileService");

}


quickAnalyzer::~quickAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//
vector<int> kinFit( pat::JetCollection bjets, pat::JetCollection ljets, TLorentzVector lepton, TLorentzVector neutrino ){

  vector<int> index;
  index.push_back( 1 );

   for (size_t iljet = 0; iljet < ljets.size()-1; iljet++) {
    TLorentzVector tmpIJet; 
    tmpIJet.SetPtEtaPhiE( ljets[iljet].pt(), ljets[iljet].eta(), ljets[iljet].phi(), ljets[iljet].energy() );
    for (size_t jljet = iljet+1; jljet < ljets.size(); jljet++) {
      if ( iljet == jljet ) continue;
      //cout << iljet << " " << jljet << endl;
      TLorentzVector tmpJJet; 
      tmpJJet.SetPtEtaPhiE( ljets[jljet].pt(), ljets[jljet].eta(), ljets[jljet].phi(), ljets[jljet].energy() );
      TLorentzVector candWhad;
      candWhad = tmpIJet + tmpJJet;



    }
   }

  return index;
}

// ------------ method called for each event  ------------
void quickAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

	using namespace edm;

	edm::Handle<pat::JetCollection> AK4jets;
	iEvent.getByToken(AK4jets_, AK4jets);
	
	edm::Handle<pat::JetCollection> AK8jets;
	iEvent.getByToken(AK8jets_, AK8jets);

	edm::Handle<pat::ElectronCollection> electrons;
	iEvent.getByToken(electrons_, electrons);

	edm::Handle<pat::MuonCollection> muons;
	iEvent.getByToken(muons_, muons);

	edm::Handle<pat::METCollection> mets;
	iEvent.getByToken(met_, mets);

	edm::Handle<std::vector<std::vector<int>>> listOfJetCandidates;
	iEvent.getByToken(listOfJetCandidates_, listOfJetCandidates);


  // METzCalculator* metz = new METzCalculator();
  METzCalculator zcalculator;

	if ( mets->size() > 0 ) {
		TLorentzVector metP4;
		const pat::MET &met = mets->front();
		metP4.SetPtEtaPhiE( met.pt(), 0, met.phi(), met.pt() );
		//LogWarning("met") << met.pt() << " " << metP4.Pt();

		////// Semileptonic selection
		if ( (( electrons->size()==1 ) and ( muons->size() < 1) ) or ( (electrons->size()<1) and ( muons->size()==1 ) ) ) {

			//LogWarning("test") << electrons->size() << " " << muons->size() << " Semileptonic event";
			/////// Leptons
			TLorentzVector leptonP4;	
			if (electrons->size()==1) { 
				const pat::Electron &ele = electrons->front();
				leptonP4.SetPtEtaPhiE( ele.pt(), ele.eta(), ele.phi(), ele.energy());
			} else {
				const pat::Muon &muon = muons->front();
				leptonP4.SetPtEtaPhiE( muon.pt(), muon.eta(), muon.phi(), muon.energy());
			}
			//LogWarning("lepton") << leptonP4.Pt();

      //////// Neutrino
      zcalculator.SetMET( metP4 );
      zcalculator.SetLepton( leptonP4 );
      double neutrinoPz = zcalculator.Calculate(1);// closest to the lepton Pz
      //LogWarning("neutrino") << neutrinoPz;
      TLorentzVector neutrino;
      neutrino.SetPxPyPzE( met.px(), met.py(), neutrinoPz, sqrt(met.px()*met.px() + met.py()*met.py() + neutrinoPz*neutrinoPz) );

      //////// Leptonic W
      TLorentzVector lepW;
      lepW = leptonP4 + neutrino;
      //LogWarning("lepW") << lepW.M();
      histos1D_[ "recoLepWMass" ]->Fill( lepW.M() );

      /// Resolved top reconstruction
      bool ableToRecoTops = 0;
      Int_t bestWindex[2] = { -1, -1 };
      Int_t HadBindex = -1;
      Int_t LepBindex = -1;
      for (const auto &i : *listOfJetCandidates) {
        int dummy=0;
        for (const auto &j : i ) {
          //LogWarning("test") << i[j] << " " << j ;
          if ( j!= -1 ) {
            ableToRecoTops = 1;
            if (dummy==0) bestWindex[0] = j;
            if (dummy==1) bestWindex[1] = j;
            if (dummy==2) HadBindex = j;
            if (dummy==3) LepBindex = j;
            ++dummy;
          }
        }
      }
      //if ( LepBindex>0 ) LogWarning("test") << bestWindex[0] << " " << bestWindex[1] << " " << HadBindex << " " << LepBindex;
			/////// AK4 jets
			pat::JetCollection allJetCandidates;
			pat::JetCollection allBJetCandidates;
			pat::JetCollection isoBjetCandidates;
			pat::JetCollection isoJetCandidates;
      TLorentzVector lepTopBjet, hadTopBjet, hadWjet1, hadWjet2;
      int idummy = 0;
			for (const pat::Jet &ak4jet : *AK4jets) {

        if (ableToRecoTops){
          TLorentzVector tmp;
          tmp.SetPtEtaPhiE( ak4jet.pt(), ak4jet.eta(), ak4jet.phi(), ak4jet.energy() );
          if ( idummy==LepBindex ) lepTopBjet = tmp;
          if ( idummy==HadBindex ) hadTopBjet = tmp;
          if ( idummy==bestWindex[0] ) hadWjet1 = tmp;
          if ( idummy==bestWindex[1] ) hadWjet2 = tmp;
          ++idummy;
        }

				if ( ak4jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") > 0.8838 ) {
					allBJetCandidates.push_back( ak4jet );
				} else {
					allJetCandidates.push_back( ak4jet );
				}
			}

      if (ableToRecoTops){
        TLorentzVector hadTop, lepTop;
        lepTop = lepW + lepTopBjet;
        hadTop = hadTopBjet + hadWjet1 + hadWjet2;
        //LogWarning("tops") << lepTop.M() << " " << hadTop.M();
        histos1D_[ "recoLepTopMass" ]->Fill( lepTop.M() );
        histos1D_[ "recoHadTopMass" ]->Fill( hadTop.M() );
        histos1D_[ "recoHadWMass" ]->Fill( ( hadWjet1 + hadWjet2 ).M() );
      }
      /////////////////////////////

			/////// AK8 jets	
			pat::JetCollection boostedHiggsCandidates;
      /// COllection of AK8 doubleB jets
			for (const pat::Jet &ak8jet : *AK8jets) {
				if ( ak8jet.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags") > 0.9 ) {
					//LogWarning("btag") << ak8jet.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags");
					boostedHiggsCandidates.push_back( ak8jet );
				}
			}
      /// Sort collection based on btag discriminant
			sort(boostedHiggsCandidates.begin(), boostedHiggsCandidates.end(), [](const pat::Jet &j1, const pat::Jet &j2) { return j1.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags") > j2.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags"); }); 

			histos1D_[ "numDoubleBjets" ]->Fill( boostedHiggsCandidates.size() );
      /// Remove AK4bjets that overlap leading AK8 doubleB candidate
			if ( boostedHiggsCandidates.size() > 0 ) { 
				const pat::Jet &ak8DoubleBCanddidate = boostedHiggsCandidates.front();

        //LogWarning("bjets") << bjetsCandidates.size();
        for (const pat::Jet &ak4bjet : allBJetCandidates ) {
          double btagsDeltaR =  ROOT::Math::VectorUtil::DeltaR( ak4bjet.momentum(), boostedHiggsCandidates.front().momentum() );
          //LogWarning("bjetsDeltaR") << btagsDeltaR;
          if ( btagsDeltaR > 0.8 ) isoBjetCandidates.push_back( ak4bjet );
        }

        for (const pat::Jet &ak4jet : allJetCandidates ) {
          double jetsDeltaR =  ROOT::Math::VectorUtil::DeltaR( ak4jet.momentum(), boostedHiggsCandidates.front().momentum() );
          //LogWarning("bjetsDeltaR") << btagsDeltaR;
          if ( jetsDeltaR > 0.8 ) isoJetCandidates.push_back( ak4jet );
        }

				if ( (isoBjetCandidates.size() > 0 ) and ( isoBjetCandidates.size() > 1 ) and ( isoJetCandidates.size() > 1 ) ){

					//histos1D_[ "doubleBjet1Mass_fullSel" ]->Fill( ak8DoubleBCanddidate.userFloat("ak8PFJetsPuppiSoftDropMass") );
					histos1D_[ "doubleBjet1Mass_fullSel" ]->Fill( ak8DoubleBCanddidate.userFloat("ak8PFJetsCHSSoftDropMass") );
					histos1D_[ "doubleBjet1Pt_fullSel" ]->Fill( ak8DoubleBCanddidate.pt() );
					histos1D_[ "doubleBjet1Eta_fullSel" ]->Fill( ak8DoubleBCanddidate.eta() );
					histos1D_[ "numDoubleBjets_fullSel" ]->Fill( boostedHiggsCandidates.size() );

					histos1D_[ "leptonPt_fullSel" ]->Fill( leptonP4.Pt() );
					histos1D_[ "leptonEta_fullSel" ]->Fill( leptonP4.Eta() );
					histos1D_[ "MET_fullSel" ]->Fill( met.pt() );

					histos1D_[ "numBjets_fullSel" ]->Fill( isoBjetCandidates.size() );
					histos1D_[ "numJets_fullSel" ]->Fill( allJetCandidates.size() );

					int ibjet = 0;
					for (const pat::Jet & b : isoBjetCandidates) {
						++ibjet;
						if (ibjet == 1) { 
							histos1D_[ "bjet1Pt_fullSel" ]->Fill( b.pt() );
							histos1D_[ "bjet1Eta_fullSel" ]->Fill( b.eta() );
						}
						if (ibjet == 2) { 
							histos1D_[ "bjet2Pt_fullSel" ]->Fill( b.pt() );
							histos1D_[ "bjet2Eta_fullSel" ]->Fill( b.eta() );
						}
					}

					int ijet = 0;
					for (const pat::Jet & j : isoJetCandidates ) {
						++ijet;
						if (ijet == 1) { 
							histos1D_[ "jet1Pt_fullSel" ]->Fill( j.pt() );
							histos1D_[ "jet1Eta_fullSel" ]->Fill( j.eta() );
						}
						if (ijet == 2) { 
							histos1D_[ "jet2Pt_fullSel" ]->Fill( j.pt() );
							histos1D_[ "jet2Eta_fullSel" ]->Fill( j.eta() );
						}
					}

          vector<int> test; 
          test = kinFit( isoJetCandidates, isoBjetCandidates, leptonP4, neutrino );
          for ( auto i : test ){
            LogWarning("test") << i;
          }
        }
			}
		}
	}

}


// ------------ method called once each job just before starting event loop  ------------
void quickAnalyzer::beginJob() {

	edm::Service< TFileService > fileService;

	histos1D_[ "numDoubleBjets" ] = fileService->make< TH1D >( "numDoubleBjets", "numDoubleBjets", 10, 0, 10 );

	histos1D_[ "leptonPt_fullSel" ] = fileService->make< TH1D >( "leptonPt_fullSel", "leptonPt_fullSel", 1000, 0, 1000 );
	histos1D_[ "leptonEta_fullSel" ] = fileService->make< TH1D >( "leptonEta_fullSel", "leptonEta_fullSel", 20, -5, 5 );
	histos1D_[ "MET_fullSel" ] = fileService->make< TH1D >( "MET_fullSel", "MET_fullSel", 500, 0, 500 );

	histos1D_[ "doubleBjet1Mass_fullSel" ] = fileService->make< TH1D >( "doubleBjet1Mass_fullSel", "doubleBjet1Mass_fullSel", 500, 0, 500 );
	histos1D_[ "doubleBjet1Pt_fullSel" ] = fileService->make< TH1D >( "doubleBjet1Pt_fullSel", "doubleBjet1Pt_fullSel", 1000, 0, 1000 );
	histos1D_[ "doubleBjet1Eta_fullSel" ] = fileService->make< TH1D >( "doubleBjet1Eta_fullSel", "doubleBjet1Eta_fullSel", 20, -5, 5 );
	histos1D_[ "numDoubleBjets_fullSel" ] = fileService->make< TH1D >( "numDoubleBjets_fullSel", "numDoubleBjets_fullSel", 10, 0, 10 );

	histos1D_[ "numBjets_fullSel" ] = fileService->make< TH1D >( "numBjets_fullSel", "numBjets_fullSel", 10, 0, 10 );
	histos1D_[ "bjet1Pt_fullSel" ] = fileService->make< TH1D >( "bjet1Pt_fullSel", "bjet1Pt_fullSel", 1000, 0, 1000 );
	histos1D_[ "bjet1Eta_fullSel" ] = fileService->make< TH1D >( "bjet1Eta_fullSel", "bjet1Eta_fullSel", 20, -5, 5 );
	histos1D_[ "bjet2Pt_fullSel" ] = fileService->make< TH1D >( "bjet2Pt_fullSel", "bjet2Pt_fullSel", 1000, 0, 1000 );
	histos1D_[ "bjet2Eta_fullSel" ] = fileService->make< TH1D >( "bjet2Eta_fullSel", "bjet2Eta_fullSel", 20, -5, 5 );
	histos1D_[ "numJets_fullSel" ] = fileService->make< TH1D >( "numJets_fullSel", "numJets_fullSel", 10, 0, 10 );
	histos1D_[ "jet1Pt_fullSel" ] = fileService->make< TH1D >( "jet1Pt_fullSel", "jet1Pt_fullSel", 1000, 0, 1000 );
	histos1D_[ "jet1Eta_fullSel" ] = fileService->make< TH1D >( "jet1Eta_fullSel", "jet1Eta_fullSel", 20, -5, 5 );
	histos1D_[ "jet2Pt_fullSel" ] = fileService->make< TH1D >( "jet2Pt_fullSel", "jet2Pt_fullSel", 1000, 0, 1000 );
	histos1D_[ "jet2Eta_fullSel" ] = fileService->make< TH1D >( "jet2Eta_fullSel", "jet2Eta_fullSel", 20, -5, 5 );

	histos1D_[ "recoLepTopMass" ] = fileService->make< TH1D >( "recoLepTopMass", "recoLepTopMass", 500, 0, 500 );
	histos1D_[ "recoHadTopMass" ] = fileService->make< TH1D >( "recoHadTopMass", "recoHadTopMass", 500, 0, 500 );
	histos1D_[ "recoLepWMass" ] = fileService->make< TH1D >( "recoLepWMass", "recoLepWMass", 500, 0, 500 );
	histos1D_[ "recoHadWMass" ] = fileService->make< TH1D >( "recoHadWMass", "recoHadWMass", 500, 0, 500 );

	///// Sumw2 all the histos
	for( auto const& histo : histos1D_ ) histos1D_[ histo.first ]->Sumw2();
	for( auto const& histo : histos2D_ ) histos2D_[ histo.first ]->Sumw2();
}

// ------------ method called once each job just after ending the event loop  ------------
void 
quickAnalyzer::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
quickAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(quickAnalyzer);
