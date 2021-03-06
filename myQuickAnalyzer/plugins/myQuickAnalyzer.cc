// -*- C++ -*-
//
// Package:    myTTH/myQuickAnalyzer
// Class:      myQuickAnalyzer
// 
/**\class myQuickAnalyzer myQuickAnalyzer.cc myTTH/myQuickAnalyzer/plugins/myQuickAnalyzer.cc

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

#include "DataFormats/PatCandidates/interface/Jet.h"
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

class myQuickAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit myQuickAnalyzer(const edm::ParameterSet&);
      ~myQuickAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
		edm::EDGetTokenT<pat::JetCollection> AK4jets_;
		edm::EDGetTokenT<pat::JetCollection> AK8jets_;
		edm::EDGetTokenT<reco::GenParticleCollection> genParticles_;
		int particle1, particle2, particle3;

		int boostedHiggs = 0;
		int resolvedHiggs = 0;
		int boostedAndResolvedHiggs = 0;
		int noneboostedAndResolvedHiggs = 0;

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
myQuickAnalyzer::myQuickAnalyzer(const edm::ParameterSet& iConfig):
    AK4jets_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("AK4jets"))),
    AK8jets_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("AK8jets"))),
    genParticles_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles")))
{
    particle1 = iConfig.getParameter<int>("particle1");
    particle2 = iConfig.getParameter<int>("particle2");
   //now do what ever initialization is needed
   usesResource("TFileService");

}


myQuickAnalyzer::~myQuickAnalyzer()
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
void myQuickAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

	edm::Handle<pat::JetCollection> AK4jets;
	iEvent.getByToken(AK4jets_, AK4jets);
	
	edm::Handle<pat::JetCollection> AK8jets;
	iEvent.getByToken(AK8jets_, AK8jets);
	
	edm::Handle<reco::GenParticleCollection> genParticles;
	iEvent.getByToken(genParticles_, genParticles);

	/////// GEN INFO
	reco::CandidateCollection p1Collection, p2Collection, finalParticlesCollection;
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

		bool parton = ( ( TMath::Abs( p.pdgId() ) < 6 ) || ( p.pdgId() == 21 )  );
		if( p.status() == 23 && parton ) { 
			finalParticlesCollection.push_back( p );
			//LogWarning("daughter") << p.pdgId();
		}

	}

	////// HIGGS
	vector< fullParentInfo > higgsInfo; 
	for( auto & part : p1Collection ) {

		reco::CandidateCollection higgsDaughterColection = checkDaughters( part, finalParticlesCollection ); 
		
		pat::JetCollection ak8JetsHiggsMatched, ak4JetsHiggsMatched;
		//double tmpAK8JetPt = 999, tmpAK4JetPt = 999;
		//int tmpNumDauAK8 = 0; 
		for( auto & dau : higgsDaughterColection ) {
			//LogWarning( "daughters") << "Parent " << part.pdgId() << " daughter " << dau.pdgId();
			pat::Jet tmpAK8Jet = checkDeltaR( dau, AK8jets, 0.6, histos1D_[ "boostedHiggsDeltaR" ] );
			if( tmpAK8Jet.pt() > 0 ) ak8JetsHiggsMatched.push_back( tmpAK8Jet );
			/*if( tmpAK8Jet.pt() > 0 ) { 
				tmpNumDauAK8+=1;
				if( ( tmpNumDauAK8 > 1 ) && ( tmpAK8JetPt == tmpAK8Jet.pt() ) ) ak8JetsHiggsMatched.push_back( tmpAK8Jet );
				tmpAK8JetPt = tmpAK8Jet.pt();
			}*/

			pat::Jet tmpAK4Jet = checkDeltaR( dau, AK4jets, 0.3, histos1D_[ "resolvedHiggsDeltaR" ] );
			if( tmpAK4Jet.pt() > 0 ) ak4JetsHiggsMatched.push_back( tmpAK4Jet );
			/*if( ( tmpAK4Jet.pt() > 0 ) && ( tmpAK4JetPt != tmpAK4Jet.pt() ) ) {
				//LogWarning("testAK4") << tmpAK4JetPt << " " << tmpAK4Jet.pt();
				ak4JetsHiggsMatched.push_back( tmpAK4Jet );
				tmpAK4JetPt = tmpAK4Jet.pt();
			}*/

		}
		//for( auto & ak8J : ak8JetsHiggsMatched ) LogWarning("matched AK8") << ak8J.pt();
		//for( auto & ak4J : ak4JetsHiggsMatched ) LogWarning("matched AK4") << ak4J.pt();

		TLorentzVector tmpParentP4;
		tmpParentP4.SetPtEtaPhiE( part.pt(), part.eta(), part.phi(), part.energy() );
		
		fullParentInfo tmpParent;
		tmpParent.genPartP4 = tmpParentP4;
		tmpParent.genPartId = part.pdgId();
		tmpParent.AK8matchedJets = ak8JetsHiggsMatched;
		tmpParent.AK4matchedJets = ak4JetsHiggsMatched;
		tmpParent.daughters = higgsDaughterColection;
		higgsInfo.push_back( tmpParent );
	}

	double numBoostedHiggs = 0;
	double numResolvedHiggs = 0;
	for( auto & higgsBoson : higgsInfo ){
		//LogWarning("higgsBoson") << higgsBoson.genPartId << " size ak8jets " << higgsBoson.AK8matchedJets.size() << " size ak4 jets " << higgsBoson.AK4matchedJets.size();
		if ( higgsBoson.AK8matchedJets.size() == 2 ) {
			if ( higgsBoson.AK8matchedJets[0].pt() ==  higgsBoson.AK8matchedJets[1].pt() ) { 
				numBoostedHiggs += 1;
				histos1D_[ "boostedHiggsMass" ]->Fill( higgsBoson.AK8matchedJets[1].userFloat("ak8PFJetsCHSValueMap:ak8PFJetsCHSPrunedMass") );
				histos1D_[ "boostedHiggsPt" ]->Fill( higgsBoson.AK8matchedJets[1].pt() );
				//LogWarning("matched ak8") << higgsBoson.AK8matchedJets[0].pt() << " " << higgsBoson.AK8matchedJets[1].pt();
			}
		}

		if ( higgsBoson.AK4matchedJets.size() == 2 ) {
			if( higgsBoson.AK4matchedJets[0].pt() !=  higgsBoson.AK4matchedJets[1].pt() ) { 
				numResolvedHiggs += higgsBoson.AK4matchedJets.size();
				TLorentzVector tmpAK4jets1, tmpAK4jets2;
				tmpAK4jets1.SetPtEtaPhiE( higgsBoson.AK4matchedJets[0].pt(), higgsBoson.AK4matchedJets[0].eta(), higgsBoson.AK4matchedJets[0].phi(), higgsBoson.AK4matchedJets[0].energy() ); 
				tmpAK4jets2.SetPtEtaPhiE( higgsBoson.AK4matchedJets[1].pt(), higgsBoson.AK4matchedJets[1].eta(), higgsBoson.AK4matchedJets[1].phi(), higgsBoson.AK4matchedJets[1].energy() ); 

				//LogWarning("matched ak4") << higgsBoson.AK4matchedJets[0].pt() << " " << higgsBoson.AK4matchedJets[1].pt();
				histos1D_[ "resolvedHiggs1Pt" ]->Fill( higgsBoson.AK4matchedJets[0].pt() );
				histos1D_[ "resolvedHiggs2Pt" ]->Fill( higgsBoson.AK4matchedJets[1].pt() );
				histos1D_[ "resolvedHiggsDeltaR" ]->Fill( tmpAK4jets1.DeltaR( tmpAK4jets2 ) );
			}
		}

		for( auto & dau : higgsBoson.daughters ) histos1D_[ "HiggsDaughtersPdgId" ]->Fill( dau.pdgId() );
		
		if ( higgsBoson.daughters.size() == 2 ) {
			double dau1Pt = higgsBoson.daughters[0].pt();
			double dau2Pt = higgsBoson.daughters[1].pt();
			if ( dau1Pt > dau2Pt ) {
				histos1D_[ "HiggsDaughters1Pt" ]->Fill( dau1Pt );
				histos1D_[ "HiggsDaughters1Eta" ]->Fill( higgsBoson.daughters[0].eta() );
				histos1D_[ "HiggsDaughters2Pt" ]->Fill( dau2Pt );
				histos1D_[ "HiggsDaughters2Eta" ]->Fill( higgsBoson.daughters[1].eta() );
				histos2D_[ "HiggsDaughters2DPt" ]->Fill( dau1Pt, dau2Pt );
			} else {
				histos1D_[ "HiggsDaughters1Pt" ]->Fill( dau2Pt );
				histos1D_[ "HiggsDaughters1Eta" ]->Fill( higgsBoson.daughters[1].eta() );
				histos1D_[ "HiggsDaughters2Pt" ]->Fill( dau1Pt );
				histos1D_[ "HiggsDaughters2Eta" ]->Fill( higgsBoson.daughters[0].eta() );
				histos2D_[ "HiggsDaughters2DPt" ]->Fill( dau2Pt, dau1Pt );
			}

			TLorentzVector tmpStop, tmpDau1, tmpDau2;
			tmpDau1.SetPtEtaPhiE( higgsBoson.daughters[0].pt(), higgsBoson.daughters[0].eta(), higgsBoson.daughters[0].phi(), higgsBoson.daughters[0].energy() ); 
			tmpDau2.SetPtEtaPhiE( higgsBoson.daughters[1].pt(), higgsBoson.daughters[1].eta(), higgsBoson.daughters[1].phi(), higgsBoson.daughters[1].energy() ); 
			tmpStop = tmpDau1 + tmpDau2;
			histos1D_[ "HiggsDaughters12Pt" ]->Fill( tmpStop.Pt() );
			histos1D_[ "HiggsDaughters12Eta" ]->Fill( tmpStop.Eta() );
			histos1D_[ "HiggsDaughtersDeltaR" ]->Fill( tmpDau1.DeltaR( tmpDau2 ) );

		}

	}
	//LogWarning("count") << numBoostedHiggs << " " << numResolvedHiggs;
	
	if ( ( numBoostedHiggs==1 ) && ( numResolvedHiggs == 0 ) ) boostedHiggs+=1;
	else if ( ( numBoostedHiggs==1 ) && ( numResolvedHiggs == 2 ) ) boostedAndResolvedHiggs+=1;
	else if ( ( numBoostedHiggs==0 ) && ( numResolvedHiggs == 2 ) ) resolvedHiggs+=1;
	else noneboostedAndResolvedHiggs+=1; 

//	////// TOP 
//	vector< fullParentInfo > higgsInfo; 
//	for( auto & part : p1Collection ) {
//
//		reco::CandidateCollection higgsDaughterColection = checkDaughters( part, finalParticlesCollection ); 
//		
//		pat::JetCollection ak8JetsHiggsMatched, ak4JetsHiggsMatched;
//		//double tmpAK8JetPt = 999, tmpAK4JetPt = 999;
//		//int tmpNumDauAK8 = 0; 
//		for( auto & dau : higgsDaughterColection ) {
//			//LogWarning( "daughters") << "Parent " << part.pdgId() << " daughter " << dau.pdgId();
//			pat::Jet tmpAK8Jet = checkDeltaR( dau, AK8jets, 0.6, histos1D_[ "boostedHiggsDeltaR" ] );
//			if( tmpAK8Jet.pt() > 0 ) ak8JetsHiggsMatched.push_back( tmpAK8Jet );
//			/*if( tmpAK8Jet.pt() > 0 ) { 
//				tmpNumDauAK8+=1;
//				if( ( tmpNumDauAK8 > 1 ) && ( tmpAK8JetPt == tmpAK8Jet.pt() ) ) ak8JetsHiggsMatched.push_back( tmpAK8Jet );
//				tmpAK8JetPt = tmpAK8Jet.pt();
//			}*/
//
//			pat::Jet tmpAK4Jet = checkDeltaR( dau, AK4jets, 0.3, histos1D_[ "resolvedHiggsDeltaR" ] );
//			if( tmpAK4Jet.pt() > 0 ) ak4JetsHiggsMatched.push_back( tmpAK4Jet );
//			/*if( ( tmpAK4Jet.pt() > 0 ) && ( tmpAK4JetPt != tmpAK4Jet.pt() ) ) {
//				//LogWarning("testAK4") << tmpAK4JetPt << " " << tmpAK4Jet.pt();
//				ak4JetsHiggsMatched.push_back( tmpAK4Jet );
//				tmpAK4JetPt = tmpAK4Jet.pt();
//			}*/
//
//		}
//		//for( auto & ak8J : ak8JetsHiggsMatched ) LogWarning("matched AK8") << ak8J.pt();
//		//for( auto & ak4J : ak4JetsHiggsMatched ) LogWarning("matched AK4") << ak4J.pt();
//
//		TLorentzVector tmpParentP4;
//		tmpParentP4.SetPtEtaPhiE( part.pt(), part.eta(), part.phi(), part.energy() );
//		
//		fullParentInfo tmpParent;
//		tmpParent.genPartP4 = tmpParentP4;
//		tmpParent.genPartId = part.pdgId();
//		tmpParent.AK8matchedJets = ak8JetsHiggsMatched;
//		tmpParent.AK4matchedJets = ak4JetsHiggsMatched;
//		tmpParent.daughters = higgsDaughterColection;
//		higgsInfo.push_back( tmpParent );
//	}
//
//	double numBoostedHiggs = 0;
//	double numResolvedHiggs = 0;
//	for( auto & parent : higgsInfo ){
//		//LogWarning("parent") << parent.genPartId << " size ak8jets " << parent.AK8matchedJets.size() << " size ak4 jets " << parent.AK4matchedJets.size();
//		if ( parent.AK8matchedJets.size() == 2 ) {
//			if ( parent.AK8matchedJets[0].pt() ==  parent.AK8matchedJets[1].pt() ) { 
//				numBoostedHiggs += 1;
//				histos1D_[ "boostedHiggsMass" ]->Fill( parent.AK8matchedJets[1].userFloat("ak8PFJetsCHSValueMap:ak8PFJetsCHSPrunedMass") );
//				histos1D_[ "boostedHiggsPt" ]->Fill( parent.AK8matchedJets[1].pt() );
//				//LogWarning("matched ak8") << parent.AK8matchedJets[0].pt() << " " << parent.AK8matchedJets[1].pt();
//			}
//		}
//
//		if ( parent.AK4matchedJets.size() == 2 ) {
//			if( parent.AK4matchedJets[0].pt() !=  parent.AK4matchedJets[1].pt() ) { 
//				numResolvedHiggs += parent.AK4matchedJets.size();
//				TLorentzVector tmpAK4jets1, tmpAK4jets2;
//				tmpAK4jets1.SetPtEtaPhiE( parent.AK4matchedJets[0].pt(), parent.AK4matchedJets[0].eta(), parent.AK4matchedJets[0].phi(), parent.AK4matchedJets[0].energy() ); 
//				tmpAK4jets2.SetPtEtaPhiE( parent.AK4matchedJets[1].pt(), parent.AK4matchedJets[1].eta(), parent.AK4matchedJets[1].phi(), parent.AK4matchedJets[1].energy() ); 
//
//				//LogWarning("matched ak4") << parent.AK4matchedJets[0].pt() << " " << parent.AK4matchedJets[1].pt();
//				histos1D_[ "resolvedHiggs1Pt" ]->Fill( parent.AK4matchedJets[0].pt() );
//				histos1D_[ "resolvedHiggs2Pt" ]->Fill( parent.AK4matchedJets[1].pt() );
//				histos1D_[ "resolvedHiggsDeltaR" ]->Fill( tmpAK4jets1.DeltaR( tmpAK4jets2 ) );
//			}
//		}
//
//		for( auto & dau : parent.daughters ) histos1D_[ "HiggsDaughtersPdgId" ]->Fill( dau.pdgId() );
//		
//		if ( parent.daughters.size() == 2 ) {
//			double dau1Pt = parent.daughters[0].pt();
//			double dau2Pt = parent.daughters[1].pt();
//			if ( dau1Pt > dau2Pt ) {
//				histos1D_[ "HiggsDaughters1Pt" ]->Fill( dau1Pt );
//				histos1D_[ "HiggsDaughters1Eta" ]->Fill( parent.daughters[0].eta() );
//				histos1D_[ "HiggsDaughters2Pt" ]->Fill( dau2Pt );
//				histos1D_[ "HiggsDaughters2Eta" ]->Fill( parent.daughters[1].eta() );
//				histos2D_[ "HiggsDaughters2DPt" ]->Fill( dau1Pt, dau2Pt );
//			} else {
//				histos1D_[ "HiggsDaughters1Pt" ]->Fill( dau2Pt );
//				histos1D_[ "HiggsDaughters1Eta" ]->Fill( parent.daughters[1].eta() );
//				histos1D_[ "HiggsDaughters2Pt" ]->Fill( dau1Pt );
//				histos1D_[ "HiggsDaughters2Eta" ]->Fill( parent.daughters[0].eta() );
//				histos2D_[ "HiggsDaughters2DPt" ]->Fill( dau2Pt, dau1Pt );
//			}
//
//			TLorentzVector tmpStop, tmpDau1, tmpDau2;
//			tmpDau1.SetPtEtaPhiE( parent.daughters[0].pt(), parent.daughters[0].eta(), parent.daughters[0].phi(), parent.daughters[0].energy() ); 
//			tmpDau2.SetPtEtaPhiE( parent.daughters[1].pt(), parent.daughters[1].eta(), parent.daughters[1].phi(), parent.daughters[1].energy() ); 
//			tmpStop = tmpDau1 + tmpDau2;
//			histos1D_[ "HiggsDaughters12Pt" ]->Fill( tmpStop.Pt() );
//			histos1D_[ "HiggsDaughters12Eta" ]->Fill( tmpStop.Eta() );
//			histos1D_[ "HiggsDaughtersDeltaR" ]->Fill( tmpDau1.DeltaR( tmpDau2 ) );
//
//		}
//
//	}
//	//LogWarning("count") << numBoostedHiggs << " " << numResolvedHiggs;
//	
//	if ( ( numBoostedHiggs==1 ) && ( numResolvedHiggs == 0 ) ) boosted+=1;
//	else if ( ( numBoostedHiggs==1 ) && ( numResolvedHiggs == 2 ) ) boostedAndResolved+=1;
//	else if ( ( numBoostedHiggs==0 ) && ( numResolvedHiggs == 2 ) ) resolved+=1;
//	else noneboostedAndResolved+=1; 


}


// ------------ method called once each job just before starting event loop  ------------
void myQuickAnalyzer::beginJob() {

	edm::Service< TFileService > fileService;

	histos1D_[ "higgsPdgId" ] = fileService->make< TH1D >( "higgsPdgId", "higgsPdgId", 50, 0, 50 );
	histos1D_[ "higgsPdgId" ]->SetXTitle( "higgs pdgId" );
	histos1D_[ "topPdgId" ] = fileService->make< TH1D >( "topPdgId", "topPdgId", 100, -50, 50 );
	histos1D_[ "topPdgId" ]->SetXTitle( "top abs(pdfId)" );

	histos1D_[ "HiggsDaughtersPdgId" ] = fileService->make< TH1D >( "HiggsDaughtersPdgId", "HiggsDaughtersPdgId", 61, -30.5, 30.5 );
	histos1D_[ "HiggsDaughtersPdgId" ]->SetXTitle( "Higgs daughters pdgId" );

	histos1D_[ "boostedHiggsDeltaR" ] = fileService->make< TH1D >( "boostedHiggsDeltaR", "boostedHiggsDeltaR", 150, 0., 1.5 );
	histos1D_[ "boostedHiggsDeltaR" ]->SetXTitle( "boosted Higgs #Delta R(jet, partons)" );

	histos1D_[ "resolvedHiggsDeltaR" ] = fileService->make< TH1D >( "resolvedHiggsDeltaR", "resolvedHiggsDeltaR", 150, 0., 1.5 );
	histos1D_[ "resolvedHiggsDeltaR" ]->SetXTitle( "resolved Higgs #Delta R( jet, parton)" );

	histos1D_[ "HiggsDaughters1Pt" ] = fileService->make< TH1D >( "HiggsDaughters1Pt", "HiggsDaughters1Pt", 1000, 0, 1000 );
	histos1D_[ "HiggsDaughters1Pt" ]->SetXTitle( "HiggsCollection daughters 1 Pt" );
	histos1D_[ "HiggsDaughters2Pt" ] = fileService->make< TH1D >( "HiggsDaughters2Pt", "HiggsDaughters2Pt", 1000, 0, 1000 );
	histos1D_[ "HiggsDaughters2Pt" ]->SetXTitle( "HiggsCollection daughters 2 Pt" );
	histos1D_[ "HiggsDaughters12Pt" ] = fileService->make< TH1D >( "HiggsDaughters12Pt", "HiggsDaughters12Pt", 1000, 0, 1000 );
	histos1D_[ "HiggsDaughters12Pt" ]->SetXTitle( "HiggsCollection daughters 12 Pt" );
	histos1D_[ "HiggsDaughters1Eta" ] = fileService->make< TH1D >( "HiggsDaughters1Eta", "HiggsDaughters1Eta", 40, -5, 5 );
	histos1D_[ "HiggsDaughters1Eta" ]->SetXTitle( "HiggsCollection daughters 1 Eta" );
	histos1D_[ "HiggsDaughters2Eta" ] = fileService->make< TH1D >( "HiggsDaughters2Eta", "HiggsDaughters2Eta", 40, -5, 5 );
	histos1D_[ "HiggsDaughters2Eta" ]->SetXTitle( "HiggsCollection daughters 2 Eta" );
	histos1D_[ "HiggsDaughters12Eta" ] = fileService->make< TH1D >( "HiggsDaughters12Eta", "HiggsDaughters12Eta", 40, -5, 5 );
	histos1D_[ "HiggsDaughters12Eta" ]->SetXTitle( "HiggsCollection daughters 12 Eta" );
	histos2D_[ "HiggsDaughters2DPt" ] = fileService->make< TH2D >( "HiggsDaughters2DPt", "HiggsDaughters2DPt", 1000, 0, 1000, 1000, 0, 1000 );
	histos1D_[ "HiggsDaughtersDeltaR" ] = fileService->make< TH1D >( "HiggsDaughtersDeltaR", "HiggsDaughtersDeltaR", 50, 0, 5 );
	histos1D_[ "HiggsDaughtersDeltaR" ]->SetXTitle( "Delta R (b,b) from Higgs" );

	histos1D_[ "boostedHiggsMass" ] = fileService->make< TH1D >( "boostedHiggsMass", "boostedHiggsMass", 300, 0, 300 );
	histos1D_[ "boostedHiggsMass" ]->SetXTitle( "boosted higgs pruned mass" );
	histos1D_[ "boostedHiggsPt" ] = fileService->make< TH1D >( "boostedHiggsPt", "boostedHiggsPt", 1000, 0, 1000 );
	histos1D_[ "boostedHiggsPt" ]->SetXTitle( "boosted higgs pt" );

	histos1D_[ "resolvedHiggs1Pt" ] = fileService->make< TH1D >( "resolvedHiggs1Pt", "resolvedHiggs1Pt", 1000, 0, 1000 );
	histos1D_[ "resolvedHiggs1Pt" ]->SetXTitle( "resolved higgs 1Pt" );
	histos1D_[ "resolvedHiggs2Pt" ] = fileService->make< TH1D >( "resolvedHiggs2Pt", "resolvedHiggs2Pt", 1000, 0, 1000 );
	histos1D_[ "resolvedHiggs2Pt" ]->SetXTitle( "resolved higgs 2Pt" );
	histos1D_[ "resolvedHiggsDeltaR" ] = fileService->make< TH1D >( "resolvedHiggsDeltaR", "resolvedHiggsDeltaR", 50, 0, 5 );
	histos1D_[ "resolvedHiggsDeltaR" ]->SetXTitle( "Delta R (bj,bj) from Higgs" );

	histos1D_[ "jetHiggsCategories" ] = fileService->make< TH1D >( "jetHiggsCategories", "jetHiggsCategories", 10, 0, 10 );

	///// Sumw2 all the histos
	for( auto const& histo : histos1D_ ) histos1D_[ histo.first ]->Sumw2();
	for( auto const& histo : histos2D_ ) histos2D_[ histo.first ]->Sumw2();

}

// ------------ method called once each job just after ending the event loop  ------------
void myQuickAnalyzer::endJob() {

	double totalHiggs = 0;
	totalHiggs = ( boostedHiggs + resolvedHiggs + boostedAndResolvedHiggs + noneboostedAndResolvedHiggs );
	LogWarning( "Higgs" ) << "boosted AND resolved " << boostedAndResolvedHiggs/totalHiggs << " " << boostedAndResolvedHiggs 
		<< "\nboosted " << boostedHiggs/totalHiggs << " " << boostedHiggs
		<< "\nresolved " << resolvedHiggs/totalHiggs << " " << resolvedHiggs
		<< "\nno Boosted No Resolved " << noneboostedAndResolvedHiggs/totalHiggs << " " << noneboostedAndResolvedHiggs
		<< "\ntotal " << totalHiggs;

	histos1D_[ "jetHiggsCategories" ]->SetBinContent( 1, boostedHiggs );
	histos1D_[ "jetHiggsCategories" ]->SetBinContent( 2, resolvedHiggs );
	histos1D_[ "jetHiggsCategories" ]->SetBinContent( 3, boostedAndResolvedHiggs );
	histos1D_[ "jetHiggsCategories" ]->SetBinContent( 4, noneboostedAndResolvedHiggs );
	histos1D_[ "jetHiggsCategories" ]->SetBinContent( 5, totalHiggs );

}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
myQuickAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
//The following says we do not know what parameters are allowed so do no validation
// Please change this to state exactly what you do use, even if it is no parameters
edm::ParameterSetDescription desc;
desc.setUnknown();
descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(myQuickAnalyzer);
