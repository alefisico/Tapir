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
	met_(consumes<pat::METCollection>(iConfig.getParameter<edm::InputTag>("met")))
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


	if ( mets->size() > 0 ) {
		//const pat::MET &met = mets->front();
		//LogWarning("met") << met.pt();

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
			
			/////// AK4 jets
			pat::JetCollection jetCandidates;
			pat::JetCollection bjetCandidates;
			pat::JetCollection bjetCleanCandidates;
			for (const pat::Jet &ak4jet : *AK4jets) {
				if ( ak4jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") > 0.8838 ) {
					bjetCandidates.push_back( ak4jet );
				} else {
					jetCandidates.push_back( ak4jet );
				}
			}

			/////// AK8 jets	
			pat::JetCollection boostedHiggsCandidates;
			for (const pat::Jet &ak8jet : *AK8jets) {

				if ( ak8jet.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags") > 0.9 ) {
					//LogWarning("btag") << ak8jet.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags");
					boostedHiggsCandidates.push_back( ak8jet );
				}
			}

			histos1D_[ "numDoubleBjets" ]->Fill( boostedHiggsCandidates.size() );
			if ( boostedHiggsCandidates.size() > 0 ) { 
				const pat::Jet &ak8DoubleBCanddidate = boostedHiggsCandidates.front();

				if ( ( bjetCandidates.size() > 2 ) and ( jetCandidates.size() > 1 ) ) {
				       //LogWarning("bjets") << bjetsCandidates.size();
					for (const pat::Jet &ak4bjet : bjetCandidates ) {

						double btagsDeltaR =  ROOT::Math::VectorUtil::DeltaR( ak4bjet.momentum(), boostedHiggsCandidates.front().momentum() );
						//LogWarning("bjetsDeltaR") << btagsDeltaR;
						if ( btagsDeltaR > 0.7 ) bjetCleanCandidates.push_back( ak4bjet );
					}
				}

				if (bjetCleanCandidates.size() > 0 ) {
					//LogWarning("bjetsClean") << bjetCleanCandidates.size();

					//histos1D_[ "doubleBjet1Mass" ]->Fill( ak8DoubleBCanddidate.userFloat("ak8PFJetsPuppiSoftDropMass") );
					histos1D_[ "doubleBjet1Mass" ]->Fill( ak8DoubleBCanddidate.userFloat("ak8PFJetsCHSSoftDropMass") );
					histos1D_[ "doubleBjet1Pt" ]->Fill( ak8DoubleBCanddidate.pt() );
					histos1D_[ "doubleBjet1Eta" ]->Fill( ak8DoubleBCanddidate.eta() );
				}
			}
		}
	}

}


// ------------ method called once each job just before starting event loop  ------------
void quickAnalyzer::beginJob() {

	edm::Service< TFileService > fileService;

	histos1D_[ "doubleBjet1Mass" ] = fileService->make< TH1D >( "doubleBjet1Mass", "doubleBjet1Mass", 500, 0, 500 );
	histos1D_[ "doubleBjet1Pt" ] = fileService->make< TH1D >( "doubleBjet1Pt", "doubleBjet1Pt", 500, 0, 500 );
	histos1D_[ "doubleBjet1Eta" ] = fileService->make< TH1D >( "doubleBjet1Eta", "doubleBjet1Eta", 20, -5, 5 );
	histos1D_[ "numDoubleBjets" ] = fileService->make< TH1D >( "numDoubleBjets", "numDoubleBjets", 10, 0, 10 );

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
