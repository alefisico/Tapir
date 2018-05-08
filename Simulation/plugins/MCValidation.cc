// -*- C++ -*-
//
// Package:    Tapir/Simulation
// Class:      MCValidation
// 
/**\class MCValidation MCValidation.cc Tapir/Simulation/plugins/MCValidation.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Alejandro Gomez Espinosa (ETHZ) [algomez]
//         Created:  Mon, 16 Apr 2018 12:51:16 GMT
//
//


// system include files
#include <memory>
#include <map>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"
#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"

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

class MCValidation : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit MCValidation(const edm::ParameterSet&);
      ~MCValidation();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
		edm::EDGetTokenT<reco::VertexCollection> Vertices_;
		edm::EDGetTokenT<pat::JetCollection> AK4jets_;
		edm::EDGetTokenT<pat::JetCollection> AK8jets_;
		edm::EDGetTokenT<pat::MuonCollection> Muons_;
		edm::EDGetTokenT<pat::ElectronCollection> Electrons_;
		edm::EDGetTokenT<pat::METCollection> MET_;
		edm::EDGetTokenT<double> rho_;

		edm::EDGetTokenT<reco::GenParticleCollection> genParticles_;
		int particle1, particle2, particle3;

		double muonIso;
		double eleIso;
		double btagWP;
		EffectiveAreas   effectiveAreas_;

		std::map< std::string, TH1D* > histos1D_;
		std::map< std::string, TH2D* > histos2D_;
};

//
// constants, enums and typedefs
//
typedef struct {
	pat::JetCollection AK8matchedJets;
	pat::JetCollection AK4matchedJets;
	reco::CandidateCollection daughters;
	TLorentzVector genPartP4;
	int genPartId;
} fullParentInfo;


//
// static data member definitions
//

//
// constructors and destructor
//
MCValidation::MCValidation(const edm::ParameterSet& iConfig):
	Vertices_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("Vertices"))),
	AK4jets_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("AK4jets"))),
	AK8jets_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("AK8jets"))),
	Muons_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("Muons"))),
	Electrons_(consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("Electrons"))),
	MET_(consumes<pat::METCollection>(iConfig.getParameter<edm::InputTag>("MET"))),
	rho_(consumes<double>(iConfig.getParameter<edm::InputTag>("rho"))),
	genParticles_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles"))),
	effectiveAreas_( (iConfig.getParameter<edm::FileInPath>("effAreasConfigFile")).fullPath() )
{
	particle1 = iConfig.getParameter<int>("particle1");
	particle2 = iConfig.getParameter<int>("particle2");
	particle3 = iConfig.getParameter<int>("particle3");
	muonIso = iConfig.getParameter<double>("muonIso");
	eleIso = iConfig.getParameter<double>("eleIso");
	btagWP = iConfig.getParameter<double>("btagWP");
	//now do what ever initialization is needed
	usesResource("TFileService");
}


MCValidation::~MCValidation()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

//Check recursively if any ancestor of particle is the given one
bool isAncestor(reco::Candidate & ancestor, const reco::Candidate * particle) {

	//particle is already the ancestor
	//edm::LogWarning("testing") << ancestor->pdgId() << " " << ancestor->pt() << " " << particle->pdgId() << " " << particle->pt();
        if( ( ancestor.pdgId() == particle->pdgId() ) && ( ancestor.mass() == particle->mass() ) ) {  
		//edm::LogWarning("is ancestor") << ancestor->pdgId() << " " << ancestor->status() << " " << particle->mother()->pdgId() << " " << particle->pdgId();
		if ( ( ancestor.pt() == particle->pt() ) && ( particle->status() == 22 ) ) return true;
	}

	//otherwise loop on mothers, if any and return true if the ancestor is found
	if( particle->mother() != nullptr ) {
		if( isAncestor( ancestor, particle->mother()) ) return true;
	}
	//if we did not return yet, then particle and ancestor are not relatives
	return false;
}

pat::Jet checkDeltaR(reco::Candidate & p1, Handle<pat::JetCollection> jets, double minDeltaR, TH1D * allDeltaR){

	pat::Jet matchedJet;
	double deltaR = 99999;

	for( unsigned int j=0; j<jets->size(); j++ ) {
		const pat::Jet & p2 = (*jets)[j];
		//double tmpdeltaR2 = reco::deltaR2( p1.rapidity(), p1.phi(), p2.rapidity(), p2.phi() );
		double tmpdeltaR = reco::deltaR2( p1.eta(), p1.phi(), p2.eta(), p2.phi() );
		//TLorentzVector tmp1, tmp2;
		//tmp1.SetPtEtaPhiE( p1.pt(), p1.eta(), p1.phi(), p1.energy() );
		//tmp2.SetPtEtaPhiE( p2.pt(), p2.eta(), p2.phi(), p2.energy() );
		//double tmpdeltaR = tmp1.DeltaR( tmp2 );
		//double tmpdeltaR3 = TMath::Sqrt( TMath::Power( (p1.eta()-p2.eta()), 2) + TMath::Power( (p1.phi()-p2.phi()), 2) );
		allDeltaR->Fill( tmpdeltaR );
		//edm::LogWarning("calc deltaR") << j << " "  << tmpdeltaR << " " << p2.pt();
		if( tmpdeltaR < deltaR ) {
			deltaR = tmpdeltaR;
			if( deltaR < minDeltaR ) { 
				matchedJet = p2;
				//edm::LogWarning("final deltaR") << j << " "  << tmpdeltaR << " " << matchedJet.pt();
			}
		}
	}
	//edm::LogWarning("deltaR") << deltaR; // << " " << ind ;
	return matchedJet; 
}

reco::CandidateCollection checkDaughters( reco::Candidate & p1, reco::CandidateCollection finalParticlesCollection ){

	reco::CandidateCollection daughters;
	for( auto & fp : finalParticlesCollection ) {
		const reco::Candidate * finalMother = fp.mother();
		if( isAncestor( p1, finalMother ) ) daughters.push_back( fp ); // LogWarning("Particle found 1") << jp1->pdgId() << " " << fp.pdgId(); }
	}

	return daughters;
}


// ------------ method called for each event  ------------
void MCValidation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

	edm::Handle<reco::GenParticleCollection> genParticles;
	iEvent.getByToken(genParticles_, genParticles);

	edm::Handle<reco::VertexCollection> vertices;
	iEvent.getByToken(Vertices_, vertices);
	
	edm::Handle<pat::JetCollection> AK4jets;
	iEvent.getByToken(AK4jets_, AK4jets);
	
	edm::Handle<pat::JetCollection> AK8jets;
	iEvent.getByToken(AK8jets_, AK8jets);
	
	edm::Handle<pat::MuonCollection> muons;
	iEvent.getByToken(Muons_, muons);
	
	edm::Handle<pat::ElectronCollection> electrons;
	iEvent.getByToken(Electrons_, electrons);
	
	edm::Handle<pat::METCollection> mets;
	iEvent.getByToken(MET_, mets);

	edm::Handle<double> rho;
	iEvent.getByToken(rho_, rho);

	
	/////// GEN INFO
	reco::CandidateCollection p1Collection, p2Collection, p3Collection, finalParticlesJetCollection, finalParticlesLeptonCollection;
	for( size_t i = 0; i < genParticles->size(); i++ ) {

		const reco::Candidate &p = ( *genParticles )[i];

		if( ( TMath::Abs( p.pdgId() ) == particle1 ) && p.status() == 22 ) { 
			p1Collection.push_back( p );
			histos1D_[ "higgsPdgId" ]->Fill( TMath::Abs( p.pdgId() ) );
			//LogWarning("mother") << p.pdgId();
		}
		if( ( TMath::Abs( p.pdgId() ) == particle2 ) && p.status() == 22 ) { 
			p2Collection.push_back( p );
			histos1D_[ "topPdgId" ]->Fill( TMath::Abs( p.pdgId() ) );
			//LogWarning("mother") << p.pdgId();
		}
		if( ( TMath::Abs( p.pdgId() ) == particle3 ) && p.status() == 22 ) { 
			p3Collection.push_back( p );
			histos1D_[ "WPdgId" ]->Fill( TMath::Abs( p.pdgId() ) );
			//LogWarning("mother") << p.pdgId();
		}

		bool parton = ( ( TMath::Abs( p.pdgId() ) < 6 ) || ( p.pdgId() == 21 )  );
		if( p.status() == 23 && parton ) { 
			finalParticlesJetCollection.push_back( p );
			//LogWarning("daughter") << p.pdgId();
		}

		bool leptons = ( ( TMath::Abs( p.pdgId() ) > 10 ) && ( TMath::Abs( p.pdgId() ) < 17 ) );
		//vector< double > tmpLeptons;
		if( ( ( p.status() == 23 ) || ( p.status() == 1 ) ) && leptons ) { 
			//tmpLeptons.push_back( p.pt() );
			//if(std::find(tmpLeptons.begin(), tmpLeptons.end(), p.pt() ) != tmpLeptons.end()) LogWarning("test") << p.pt();
			//else LogWarning("test") << "nothing";
			finalParticlesLeptonCollection.push_back( p );
			//LogWarning("lepton") << p.pdgId() << " " << p.status() << " " << p.pt();
		}
	}


	////// RECO INFO
	/// Vertices
	if (vertices->empty()) return; // skip the event if no PV found
	//const reco::Vertex &PV = vertices->front();
	histos1D_[ "numPV" ]->Fill( vertices->size() );
	//LogWarning("vertex") << vertices->size();


	/// MUONS
	int numMuons = 0;
	pat::MuonCollection selectedMuons;
	for ( const pat::Muon &mu : *muons ) {
		if ((mu.pfIsolationR04().sumChargedHadronPt + max(0., mu.pfIsolationR04().sumNeutralHadronEt + mu.pfIsolationR04().sumPhotonEt - 0.5*mu.pfIsolationR04().sumPUPt))/mu.pt() > muonIso ) continue; 
		//LogWarning("muon") << mu.pt() << " " << mu.eta();
		//} else  LogWarning("muon") << " no selected"; 
		selectedMuons.push_back( mu );

		if ((++numMuons)==1) {
			histos1D_[ "muon1Pt" ]->Fill( mu.pt() );
			histos1D_[ "muon1Eta" ]->Fill( mu.eta() );
		}
		if (numMuons==2) {
			histos1D_[ "muon2Pt" ]->Fill( mu.pt() );
			histos1D_[ "muon2Eta" ]->Fill( mu.eta() );
		}
	}
	histos1D_[ "numSelMuons" ]->Fill( selectedMuons.size() );
	/////////////////////////////////////

	/// ELECTRONS
	int numEle = 0;
	pat::ElectronCollection selectedElectrons;
	for ( const pat::Electron &ele : *electrons ) {

		float eA = effectiveAreas_.getEffectiveArea( TMath::Abs( ele.eta() ) );   /// in recipe ele.superCluster().eta(), but it does not work
		if ((ele.pfIsolationVariables().sumChargedHadronPt + max(0., ele.pfIsolationVariables().sumNeutralHadronEt + ele.pfIsolationVariables().sumPhotonEt - eA*(*rho)))/ele.pt() > eleIso ) continue; 
		//LogWarning("electron") << ele.pt() << " " << ele.eta();
		selectedElectrons.push_back( ele );

		if ((++numEle)==1) {
			histos1D_[ "electron1Pt" ]->Fill( ele.pt() );
			histos1D_[ "electron1Eta" ]->Fill( ele.eta() );
		}
		if (numEle==2) {
			histos1D_[ "electron2Pt" ]->Fill( ele.pt() );
			histos1D_[ "electron2Eta" ]->Fill( ele.eta() );
		}
	}
	histos1D_[ "numSelElectrons" ]->Fill( selectedElectrons.size() );
	/////////////////////////////////////

	/// MET
	if (mets->empty()) return; // skip the event if no MET found
	const pat::MET &met = mets->front();
	//LogWarning("met") << met.pt() << " " << met.phi();
	histos1D_[ "MET" ]->Fill( met.pt() );

	/// JETS
	int numJets = 0;
	int numLightJets = 0;
	int numBJets = 0;
	pat::JetCollection selectedJets;
	pat::JetCollection selectedLightJets;
	pat::JetCollection selectedBJets;
	for ( const pat::Jet &jet : *AK4jets ) {
		if ( (jet.neutralHadronEnergyFraction()<0.99 && jet.neutralEmEnergyFraction()<0.99 && (jet.chargedMultiplicity()+jet.neutralMultiplicity())>1) && ((abs(jet.eta())<=2.4 && jet.chargedHadronEnergyFraction()>0 && jet.chargedMultiplicity()>0 && jet.chargedEmEnergyFraction()<0.99) || abs(jet.eta())>2.4) && abs(jet.eta())<=2.7) {
			//LogWarning("jets") << jet.pt() << " " << jet.eta();
			selectedJets.push_back( jet );
			if ((++numJets)==1) {
				histos1D_[ "jet1Pt" ]->Fill( jet.pt() );
				histos1D_[ "jet1Eta" ]->Fill( jet.eta() );
			}
			if (numJets==2) {
				histos1D_[ "jet2Pt" ]->Fill( jet.pt() );
				histos1D_[ "jet2Eta" ]->Fill( jet.eta() );
			}
			if (numJets==3) {
				histos1D_[ "jet3Pt" ]->Fill( jet.pt() );
				histos1D_[ "jet3Eta" ]->Fill( jet.eta() );
			}
			if (numJets==4) {
				histos1D_[ "jet4Pt" ]->Fill( jet.pt() );
				histos1D_[ "jet4Eta" ]->Fill( jet.eta() );
			}
			if (numJets==5) {
				histos1D_[ "jet5Pt" ]->Fill( jet.pt() );
				histos1D_[ "jet5Eta" ]->Fill( jet.eta() );
			}
			if (numJets==6) {
				histos1D_[ "jet6Pt" ]->Fill( jet.pt() );
				histos1D_[ "jet6Eta" ]->Fill( jet.eta() );
			}
			
			if ( jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") > btagWP ) {
				selectedBJets.push_back( jet );
				if ((++numBJets)==1) {
					histos1D_[ "bjet1Pt" ]->Fill( jet.pt() );
					histos1D_[ "bjet1Eta" ]->Fill( jet.eta() );
				}
				if (numBJets==2) {
					histos1D_[ "bjet2Pt" ]->Fill( jet.pt() );
					histos1D_[ "bjet2Eta" ]->Fill( jet.eta() );
				}
				if (numBJets==3) {
					histos1D_[ "bjet3Pt" ]->Fill( jet.pt() );
					histos1D_[ "bjet3Eta" ]->Fill( jet.eta() );
				}
				if (numBJets==4) {
					histos1D_[ "bjet4Pt" ]->Fill( jet.pt() );
					histos1D_[ "bjet4Eta" ]->Fill( jet.eta() );
				}
			} else {
				selectedLightJets.push_back( jet );
				if ((++numLightJets)==1) {
					histos1D_[ "ljet1Pt" ]->Fill( jet.pt() );
					histos1D_[ "ljet1Eta" ]->Fill( jet.eta() );
				}
				if (numLightJets==2) {
					histos1D_[ "ljet2Pt" ]->Fill( jet.pt() );
					histos1D_[ "ljet2Eta" ]->Fill( jet.eta() );
				}
				if (numLightJets==3) {
					histos1D_[ "ljet3Pt" ]->Fill( jet.pt() );
					histos1D_[ "ljet3Eta" ]->Fill( jet.eta() );
				}
			}

		}
	}
	histos1D_[ "numSelJets" ]->Fill( selectedJets.size() );
	histos1D_[ "numSelLightJets" ]->Fill( selectedLightJets.size() );
	histos1D_[ "numSelBJets" ]->Fill( selectedBJets.size() );

	////// Dilepton Analysis
	bool dilepton;
	if ( ( selectedMuons.size() == 2 ) and ( selectedElectrons.size() == 0 ) ) {
		if ((selectedMuons.at(0).pt()> 25) and ( selectedMuons.at(0).charge() != selectedMuons.at(1).charge() ) ) dilepton = true;
		//LogWarning("test") << "dimuon " << selectedMuons.at(0).pt() << " " << selectedMuons.at(0).charge() << " " << selectedMuons.at(1).charge();
	} else if ( ( selectedMuons.size() == 0 ) and ( selectedElectrons.size() == 2 ) ) {
		//LogWarning("test") << "dimuon";
		if ((selectedElectrons.at(0).pt()> 25) and ( selectedElectrons.at(0).charge() != selectedElectrons.at(1).charge() ) ) dilepton = true;
	} else if ( ( selectedMuons.size() == 1 ) and ( selectedElectrons.size() == 1 ) ) {
		//LogWarning("test") << "dimuon";
		if ( (max( selectedElectrons.at(0).pt(), selectedMuons.at(0).pt() ) > 25) and ( selectedElectrons.at(0).charge() != selectedMuons.at(0).charge() ) ) dilepton = true;
	} else dilepton = false;//LogWarning("test") << selectedMuons.size() << " " << selectedElectrons.size();
	//LogWarning("dilepton") << dilepton;
	
	if (dilepton) {
	}
	

}


// ------------ method called once each job just before starting event loop  ------------
void MCValidation::beginJob() {

	edm::Service< TFileService > fileService;

	histos1D_[ "higgsPdgId" ] = fileService->make< TH1D >( "higgsPdgId", "higgsPdgId", 50, 0, 50 );
	histos1D_[ "higgsPdgId" ]->SetXTitle( "higgs pdgId" );
	histos1D_[ "topPdgId" ] = fileService->make< TH1D >( "topPdgId", "topPdgId", 100, -50, 50 );
	histos1D_[ "topPdgId" ]->SetXTitle( "top abs(pdfId)" );
	histos1D_[ "WPdgId" ] = fileService->make< TH1D >( "WPdgId", "WPdgId", 100, -50, 50 );
	histos1D_[ "WPdgId" ]->SetXTitle( "W abs(pdfId)" );

	histos1D_[ "numPV" ] = fileService->make< TH1D >( "numPV", "numPV", 100, 0, 100 );
	histos1D_[ "numPV" ]->SetXTitle( "Number of primary vertex" );

	histos1D_[ "numSelMuons" ] = fileService->make< TH1D >( "numSelMuons", "numSelMuons", 10, 0, 10 );
	histos1D_[ "numSelMuons" ]->SetXTitle( "Number of selected muons" );
	histos1D_[ "muon1Pt" ] = fileService->make< TH1D >( "muon1Pt", "muon1Pt", 500, 0, 500);
	histos1D_[ "muon1Pt" ]->SetXTitle( "Leading muon pt" );
	histos1D_[ "muon1Eta" ] = fileService->make< TH1D >( "muon1Eta", "muon1Eta", 40, -5, 5);
	histos1D_[ "muon1Eta" ]->SetXTitle( "Leading muon eta" );
	histos1D_[ "muon2Pt" ] = fileService->make< TH1D >( "muon2Pt", "muon2Pt", 500, 0, 500);
	histos1D_[ "muon2Pt" ]->SetXTitle( "2nd Leading muon pt" );
	histos1D_[ "muon2Eta" ] = fileService->make< TH1D >( "muon2Eta", "muon2Eta", 40, -5, 5);
	histos1D_[ "muon2Eta" ]->SetXTitle( "2nd Leading muon eta" );

	histos1D_[ "numSelElectrons" ] = fileService->make< TH1D >( "numSelElectrons", "numSelElectrons", 10, 0, 10 );
	histos1D_[ "numSelElectrons" ]->SetXTitle( "Number of selected electrons" );
	histos1D_[ "electron1Pt" ] = fileService->make< TH1D >( "electron1Pt", "electron1Pt", 500, 0, 500);
	histos1D_[ "electron1Pt" ]->SetXTitle( "Leading electron pt" );
	histos1D_[ "electron1Eta" ] = fileService->make< TH1D >( "electron1Eta", "electron1Eta", 40, -5, 5);
	histos1D_[ "electron1Eta" ]->SetXTitle( "Leading electron eta" );
	histos1D_[ "electron2Pt" ] = fileService->make< TH1D >( "electron2Pt", "electron2Pt", 500, 0, 500);
	histos1D_[ "electron2Pt" ]->SetXTitle( "2nd Leading electron pt" );
	histos1D_[ "electron2Eta" ] = fileService->make< TH1D >( "electron2Eta", "electron2Eta", 40, -5, 5);
	histos1D_[ "electron2Eta" ]->SetXTitle( "2nd Leading electron eta" );

	histos1D_[ "MET" ] = fileService->make< TH1D >( "MET", "MET", 500, 0, 500);
	histos1D_[ "MET" ]->SetXTitle( "MET" );

	histos1D_[ "numSelJets" ] = fileService->make< TH1D >( "numSelJets", "numSelJets", 10, 0, 10 );
	histos1D_[ "numSelJets" ]->SetXTitle( "Number of selected jets" );
	histos1D_[ "jet1Pt" ] = fileService->make< TH1D >( "jet1Pt", "jet1Pt", 500, 0, 500);
	histos1D_[ "jet1Pt" ]->SetXTitle( "Leading jet pt" );
	histos1D_[ "jet1Eta" ] = fileService->make< TH1D >( "jet1Eta", "jet1Eta", 40, -5, 5);
	histos1D_[ "jet1Eta" ]->SetXTitle( "Leading jet eta" );
	histos1D_[ "jet2Pt" ] = fileService->make< TH1D >( "jet2Pt", "jet2Pt", 500, 0, 500);
	histos1D_[ "jet2Pt" ]->SetXTitle( "2nd Leading jet pt" );
	histos1D_[ "jet2Eta" ] = fileService->make< TH1D >( "jet2Eta", "jet2Eta", 40, -5, 5);
	histos1D_[ "jet2Eta" ]->SetXTitle( "2nd Leading jet eta" );
	histos1D_[ "jet3Pt" ] = fileService->make< TH1D >( "jet3Pt", "jet3Pt", 500, 0, 500);
	histos1D_[ "jet3Pt" ]->SetXTitle( "3nd Leading jet pt" );
	histos1D_[ "jet3Eta" ] = fileService->make< TH1D >( "jet3Eta", "jet3Eta", 40, -5, 5);
	histos1D_[ "jet3Eta" ]->SetXTitle( "3nd Leading jet eta" );
	histos1D_[ "jet4Pt" ] = fileService->make< TH1D >( "jet4Pt", "jet4Pt", 500, 0, 500);
	histos1D_[ "jet4Pt" ]->SetXTitle( "4nd Leading jet pt" );
	histos1D_[ "jet4Eta" ] = fileService->make< TH1D >( "jet4Eta", "jet4Eta", 40, -5, 5);
	histos1D_[ "jet4Eta" ]->SetXTitle( "4nd Leading jet eta" );
	histos1D_[ "jet5Pt" ] = fileService->make< TH1D >( "jet5Pt", "jet5Pt", 500, 0, 500);
	histos1D_[ "jet5Pt" ]->SetXTitle( "5nd Leading jet pt" );
	histos1D_[ "jet5Eta" ] = fileService->make< TH1D >( "jet5Eta", "jet5Eta", 40, -5, 5);
	histos1D_[ "jet5Eta" ]->SetXTitle( "5nd Leading jet eta" );
	histos1D_[ "jet6Pt" ] = fileService->make< TH1D >( "jet6Pt", "jet6Pt", 500, 0, 500);
	histos1D_[ "jet6Pt" ]->SetXTitle( "6nd Leading jet pt" );
	histos1D_[ "jet6Eta" ] = fileService->make< TH1D >( "jet6Eta", "jet6Eta", 40, -5, 5);
	histos1D_[ "jet6Eta" ]->SetXTitle( "6nd Leading jet eta" );


	histos1D_[ "numSelBJets" ] = fileService->make< TH1D >( "numSelBJets", "numSelBJets", 10, 0, 10 );
	histos1D_[ "numSelBJets" ]->SetXTitle( "Number of selected bjets" );
	histos1D_[ "bjet1Pt" ] = fileService->make< TH1D >( "bjet1Pt", "bjet1Pt", 500, 0, 500);
	histos1D_[ "bjet1Pt" ]->SetXTitle( "Leading bjet pt" );
	histos1D_[ "bjet1Eta" ] = fileService->make< TH1D >( "bjet1Eta", "bjet1Eta", 40, -5, 5);
	histos1D_[ "bjet1Eta" ]->SetXTitle( "Leading bjet eta" );
	histos1D_[ "bjet2Pt" ] = fileService->make< TH1D >( "bjet2Pt", "bjet2Pt", 500, 0, 500);
	histos1D_[ "bjet2Pt" ]->SetXTitle( "2nd Leading bjet pt" );
	histos1D_[ "bjet2Eta" ] = fileService->make< TH1D >( "bjet2Eta", "bjet2Eta", 40, -5, 5);
	histos1D_[ "bjet2Eta" ]->SetXTitle( "2nd Leading bjet eta" );
	histos1D_[ "bjet3Pt" ] = fileService->make< TH1D >( "bjet3Pt", "bjet3Pt", 500, 0, 500);
	histos1D_[ "bjet3Pt" ]->SetXTitle( "3nd Leading bjet pt" );
	histos1D_[ "bjet3Eta" ] = fileService->make< TH1D >( "bjet3Eta", "bjet3Eta", 40, -5, 5);
	histos1D_[ "bjet3Eta" ]->SetXTitle( "3nd Leading bjet eta" );
	histos1D_[ "bjet4Pt" ] = fileService->make< TH1D >( "bjet4Pt", "bjet4Pt", 500, 0, 500);
	histos1D_[ "bjet4Pt" ]->SetXTitle( "4nd Leading bjet pt" );
	histos1D_[ "bjet4Eta" ] = fileService->make< TH1D >( "bjet4Eta", "bjet4Eta", 40, -5, 5);
	histos1D_[ "bjet4Eta" ]->SetXTitle( "4nd Leading bjet eta" );


	histos1D_[ "numSelLightJets" ] = fileService->make< TH1D >( "numSelLightJets", "numSelLightJets", 10, 0, 10 );
	histos1D_[ "numSelLightJets" ]->SetXTitle( "Number of selected light jets" );
	histos1D_[ "ljet1Pt" ] = fileService->make< TH1D >( "ljet1Pt", "ljet1Pt", 500, 0, 500);
	histos1D_[ "ljet1Pt" ]->SetXTitle( "Leading ljet pt" );
	histos1D_[ "ljet1Eta" ] = fileService->make< TH1D >( "ljet1Eta", "ljet1Eta", 40, -5, 5);
	histos1D_[ "ljet1Eta" ]->SetXTitle( "Leading ljet eta" );
	histos1D_[ "ljet2Pt" ] = fileService->make< TH1D >( "ljet2Pt", "ljet2Pt", 500, 0, 500);
	histos1D_[ "ljet2Pt" ]->SetXTitle( "2nd Leading ljet pt" );
	histos1D_[ "ljet2Eta" ] = fileService->make< TH1D >( "ljet2Eta", "ljet2Eta", 40, -5, 5);
	histos1D_[ "ljet2Eta" ]->SetXTitle( "2nd Leading ljet eta" );
	histos1D_[ "ljet3Pt" ] = fileService->make< TH1D >( "ljet3Pt", "ljet3Pt", 500, 0, 500);
	histos1D_[ "ljet3Pt" ]->SetXTitle( "3nd Leading ljet pt" );
	histos1D_[ "ljet3Eta" ] = fileService->make< TH1D >( "ljet3Eta", "ljet3Eta", 40, -5, 5);
	histos1D_[ "ljet3Eta" ]->SetXTitle( "3nd Leading ljet eta" );

	///// Sumw2 all the histos
	for( auto const& histo : histos1D_ ) histos1D_[ histo.first ]->Sumw2();
	for( auto const& histo : histos2D_ ) histos2D_[ histo.first ]->Sumw2();

}

// ------------ method called once each job just after ending the event loop  ------------
void MCValidation::endJob() {

}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void MCValidation::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no Validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	//desc.setUnknown();
	desc.add<InputTag>("Vertices", 		InputTag("offlineSlimeedPrimaryVertices"));
	desc.add<InputTag>("AK4jets", 		InputTag("slimmedJets"));
	desc.add<InputTag>("AK8jets", 		InputTag("slimmedAK8Jets"));
	desc.add<InputTag>("Muons", 		InputTag("slimmedMuons"));
	desc.add<InputTag>("Electrons", 	InputTag("slimmedElectrons"));
	desc.add<InputTag>("MET", 		InputTag("slimmedMETs"));
	desc.add<InputTag>("genParticles", 	InputTag("prunedGenParticles"));
	desc.add<InputTag>("rho", 		InputTag("fixedGridRhoFastjetAll"));
	desc.add<FileInPath>("effAreasConfigFile", 	FileInPath("Tapir/Simulation/data/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt"));
	desc.add<int>("particle1", 	25);
	desc.add<int>("particle2", 	25);
	desc.add<int>("particle3", 	25);
	desc.add<double>("muonIso", 	0.25);
	desc.add<double>("eleIso", 	0.06);
	desc.add<double>("btagWP", 	0.8484);
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MCValidation);
