import FWCore.ParameterSet.Config as cms
from TTH.NanoAODTools.boosted_cff import customizedBoostedTools

def nanoHTT_customizeCommon(process):
    customizedBoostedTools(process)
    return process


def nanoHRT_customizeData(process):
    process = nanoHRT_customizeCommon(process, False)
    process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)  # needed for crab publication
    return process



def nanoHRT_customizeMC(process):
    process = nanoHRT_customizeCommon(process, True)
    process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)  # needed for crab publication
    return process
