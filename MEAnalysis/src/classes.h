#include "TTH/MEAnalysis/interface/EventShapeVariables.h"
#include "TTH/MEAnalysis/interface/EventModel.h"

namespace {
    namespace {
        std::vector<TLorentzVector> _TTHMEAnalysis_i1;
        std::vector<TTH_MEAnalysis::Jet> _TTHMEAnalysis_i2;
        std::pair<TTH_MEAnalysis::Systematic::Event, TTH_MEAnalysis::Systematic::Direction> _TTHMEAnalysis_i3;
        std::map<TTH_MEAnalysis::Systematic::SystId, double> _TTHMEAnalysis_i4;
        
        TTH_MEAnalysis::TreeDescription<float> _TTHMEAnalysis_i5(nullptr, TTH_MEAnalysis::SampleDescription(TTH_MEAnalysis::SampleDescription::MC));
        TTH_MEAnalysis::TreeDescription<double> _TTHMEAnalysis_i6(nullptr, TTH_MEAnalysis::SampleDescription(TTH_MEAnalysis::SampleDescription::MC));
        
        TTH_MEAnalysis::TreeDescriptionMC<float> _TTHMEAnalysis_i7(nullptr, TTH_MEAnalysis::SampleDescription(TTH_MEAnalysis::SampleDescription::MC));
        TTH_MEAnalysis::TreeDescriptionMC<double> _TTHMEAnalysis_i8(nullptr, TTH_MEAnalysis::SampleDescription(TTH_MEAnalysis::SampleDescription::MC));
        
        TTH_MEAnalysis::TreeDescriptionMCSystematic<float> _TTHMEAnalysis_i9(nullptr, TTH_MEAnalysis::SampleDescription(TTH_MEAnalysis::SampleDescription::MC));
        TTH_MEAnalysis::TreeDescriptionMCSystematic<double> _TTHMEAnalysis_i10(nullptr, TTH_MEAnalysis::SampleDescription(TTH_MEAnalysis::SampleDescription::MC));
    }
}
