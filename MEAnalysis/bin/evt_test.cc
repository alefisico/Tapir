#include "TTH/MEAnalysis/interface/EventModel.h"
#include "TFile.h"
#include <iostream>

int main(){
    
    TFile* tf = TFile::Open("root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/Sep4_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Sep4_v1/170904_145634/0000/tree_1.root");

    TTH_MEAnalysis::TreeDescriptionMC<float> tree(tf, TTH_MEAnalysis::SampleDescription(TTH_MEAnalysis::SampleDescription::MC));

    int i = 0;
    while (tree.reader.Next()) {
        i++;
    }
    return 0;
}
