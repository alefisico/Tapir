#include "PhysicsTools/NanoAOD/plugins/SimpleFlatTableProducerPlugins.cc"
#include "DataFormats/BTauReco/interface/HTTTopJetTagInfo.h"
typedef SimpleFlatTableProducer<reco::HTTTopJetTagInfo> SimpleHTTInfoFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimpleHTTInfoFlatTableProducer);
