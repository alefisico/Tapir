import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoBTag.SecondaryVertex.pfCombinedInclusiveSecondaryVertexV2BJetTags_cfi import *
from RecoBTag.ImpactParameter.pfImpactParameterTagInfos_cfi import pfImpactParameterTagInfos
from RecoBTag.SecondaryVertex.pfInclusiveSecondaryVertexFinderTagInfos_cfi import *
from RecoBTag.SecondaryVertex.candidateCombinedSecondaryVertexV2Computer_cfi import *
from RecoBTag.SecondaryVertex.pfBoostedDoubleSVAK8TagInfos_cfi import *
from RecoBTag.Configuration.RecoBTag_cff import *
from Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff import *
from Configuration.Geometry.GeometryRecoDB_cff import *
from RecoBTag.Combined.pfDeepCSVJetTags_cfi import pfDeepCSVJetTags
from RecoBTag.SecondaryVertex.combinedSecondaryVertexCommon_cff import combinedSecondaryVertexCommon
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *



def customizedBoostedTools( process, path=None ):
    """docstring for customizedBoostedTools"""

    ##################### User floats producers, selectors ##########################

    #Default parameters for HTTV2 and CA15 Fatjets
    delta_r = 1.5
    jetAlgo = "CambridgeAachen"
    subjet_label = "SubJets"
    initial_jet = "ca15PFJetsCHS"
    maxSVDeltaRToJet = 1.3
    weightFile = 'RecoBTag/SecondaryVertex/data/BoostedDoubleSV_CA15_BDT_v3.weights.xml.gz'

    ######################
    ####    HTTV2     ####
    ######################

    # Get input objects for HTTV2 calculation
    process.selectedMuonsTmp = cms.EDProducer("MuonRemovalForBoostProducer",
        src = cms.InputTag("slimmedMuons"),
        vtx = cms.InputTag("offlineSlimmedPrimaryVertices"))
    process.selectedMuons = cms.EDFilter("CandPtrSelector",
        src = cms.InputTag("selectedMuonsTmp"),
        cut = cms.string("1"))
    process.selectedElectronsTmp = cms.EDProducer("ElectronRemovalForBoostProducer",
        src = cms.InputTag("slimmedElectrons"),
        mvaIDMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight"),
        rho = cms.InputTag("fixedGridRhoFastjetAll"))
    process.selectedElectrons = cms.EDFilter("CandPtrSelector",
        src = cms.InputTag("selectedElectronsTmp"),
        cut = cms.string("1"))
    process.chsTmp1 = cms.EDFilter("CandPtrSelector",
        src = cms.InputTag("packedPFCandidates"),
        cut = cms.string("fromPV"))
    process.chsTmp2 =  cms.EDProducer("CandPtrProjector",
        src = cms.InputTag("chsTmp1"),
        veto = cms.InputTag("selectedMuons"))
    process.chs = cms.EDProducer("CandPtrProjector",
        src = cms.InputTag("chsTmp2"),
        veto = cms.InputTag("selectedElectrons"))

    #Calculate HTT tagger
    process.looseOptRHTT = cms.EDProducer(
                "HTTTopJetProducer",
                PFJetParameters.clone(
                    src               = cms.InputTag("chs"),
                    doAreaFastjet     = cms.bool(True),
                    doRhoFastjet      = cms.bool(False),
                    jetPtMin          = cms.double(200.0)
                    ),
                AnomalousCellParameters,
                useExplicitGhosts = cms.bool(True),
                algorithm           = cms.int32(1),
                jetAlgorithm        = cms.string("CambridgeAachen"),
                rParam              = cms.double(1.5),
                optimalR            = cms.bool(True),
                qJets               = cms.bool(False),
                minFatjetPt         = cms.double(200.),
                minSubjetPt         = cms.double(0.),
                minCandPt           = cms.double(0.),
                maxFatjetAbsEta     = cms.double(99.),
                subjetMass          = cms.double(30.),
                muCut               = cms.double(0.8),
                filtR               = cms.double(0.3),
                filtN               = cms.int32(5),
                mode                = cms.int32(4),
                minCandMass         = cms.double(0.),
                maxCandMass         = cms.double(999999.),
                massRatioWidth      = cms.double(999999.),
                minM23Cut           = cms.double(0.),
                minM13Cut           = cms.double(0.),
                maxM13Cut           = cms.double(999999.),
                writeCompound       = cms.bool(True),
                jetCollInstanceName = cms.string("SubJets")
                )

    #Calculate subjet btags
    process.looseOptRHTTImpactParameterTagInfos = pfImpactParameterTagInfos.clone(
        primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
        candidates = cms.InputTag("chs"),
        computeGhostTrack = cms.bool(True),
        computeProbabilities = cms.bool(True),
        maxDeltaR = cms.double(0.4),
        jets = cms.InputTag("looseOptRHTT", "SubJets")
    )

    process.looseOptRHTTImpactParameterTagInfos.explicitJTA = cms.bool(True)

    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos = pfInclusiveSecondaryVertexFinderTagInfos.clone(
        extSVCollection = cms.InputTag('slimmedSecondaryVertices'),
        trackIPTagInfos = cms.InputTag("looseOptRHTTImpactParameterTagInfos"),
    )

    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.useSVClustering = cms.bool(True)
    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.rParam = cms.double(delta_r)
    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.extSVDeltaRToJet = cms.double(0.3)
    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.trackSelection.jetDeltaRMax = cms.double(0.3)
    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(0.4)
    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.jetAlgorithm = cms.string(jetAlgo)
    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.fatJets  =  cms.InputTag(initial_jet)
    process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos.groomedFatJets = cms.InputTag("looseOptRHTT","")

    process.looseOptRHTTpfDeepCSVInfos = process.pfDeepCSVTagInfos.clone(
        svTagInfos = cms.InputTag("looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos"),
        computer = combinedSecondaryVertexCommon
        )

    process.looseOptRHTTpfCombinedInclusiveSecondaryVertexV2BJetTags = process.pfDeepCSVJetTags.clone(
        src = cms.InputTag('looseOptRHTTpfDeepCSVInfos')
    )


    process.jetCorrFactorsHTT = process.patJetCorrFactors.clone(src=cms.InputTag("looseOptRHTT", "SubJets"),
        levels = cms.vstring('L1FastJet',
            'L2Relative',
            'L3Absolute',
        'L2L3Residual'),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    )

    process.looseOptRHTTpatSubJets = cms.EDProducer("PATJetProducer",
        jetSource = cms.InputTag("looseOptRHTT", "SubJets"),
        embedPFCandidates = cms.bool(False),
        addJetCorrFactors    = cms.bool(True),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("jetCorrFactorsHTT") ),
        # btag information
        addBTagInfo          = cms.bool(True),   ## master switch
        addDiscriminators    = cms.bool(True),   ## addition btag discriminators
        discriminatorSources = cms.VInputTag(cms.InputTag('looseOptRHTTpfCombinedInclusiveSecondaryVertexV2BJetTags', 'probb'),cms.InputTag('looseOptRHTTpfCombinedInclusiveSecondaryVertexV2BJetTags', 'probbb')),
        addTagInfos     = cms.bool(False),
        tagInfoSources  = cms.VInputTag(),
        addAssociatedTracks    = cms.bool(False),
        trackAssociationSource = cms.InputTag("ak4JetTracksAssociatorAtVertexPF"),
        addJetCharge    = cms.bool(False),
        jetChargeSource = cms.InputTag("patJetCharge"),
        addJetID = cms.bool(False),
        jetIDMap = cms.InputTag("ak4JetID"),
        addGenPartonMatch   = cms.bool(False),
        embedGenPartonMatch = cms.bool(False),
        genPartonMatch      = cms.InputTag("NOT_IMPLEMENTED"),
        addGenJetMatch      = cms.bool(False),
        embedGenJetMatch    = cms.bool(False),
        genJetMatch         = cms.InputTag("NOT_IMPLEMENTED"),
        addPartonJetMatch   = cms.bool(False),
        partonJetSource     = cms.InputTag("NOT_IMPLEMENTED"),
        getJetMCFlavour    = cms.bool(False),
        useLegacyJetMCFlavour = cms.bool(False),
        addJetFlavourInfo  = cms.bool(False),
        JetPartonMapSource = cms.InputTag("NOT_IMPLEMENTED"),
        JetFlavourInfoSource = cms.InputTag("NOT_IMPLEMENTED"),
        addEfficiencies = cms.bool(False),
        efficiencies    = cms.PSet(),
        addResolutions = cms.bool(False),
        resolutions     = cms.PSet()
    )

    #This reorders the subjets as in the original subjet list (ordered by pt in the patjet conversion)
    process.looseOptRHTTSubjetsOrdered =  cms.EDProducer("HTTBtagMatchProducer",
        jetSource = cms.InputTag("looseOptRHTT", "SubJets"),
        patsubjets = cms.InputTag("looseOptRHTTpatSubJets")
    )

    #Now, make all the tables
    process.HTTV2Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("looseOptRHTT"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("HTTV2"),
        doc  = cms.string("HTTV2 candidates calculated from CA15 fatjets"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars,
            #area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
            subJetIdx1 = Var("?numberOfSourceCandidatePtrs()>0 && sourceCandidatePtr(0).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(0).key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2 = Var("?numberOfSourceCandidatePtrs()>1 && sourceCandidatePtr(1).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(1).key():-1", int,
                 doc="index of second subjet"),
            subJetIdx3 = Var("?numberOfSourceCandidatePtrs()>2 && sourceCandidatePtr(2).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(2).key():-1", int,
                 doc="index of third subjet"),
        )
    )

    #Get HTTV2 variables:  fRec,Ropt...
    process.HTTV2InfoTable = cms.EDProducer("SimpleHTTInfoFlatTableProducer",
        src = cms.InputTag("looseOptRHTT"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("HTTV2"),
        doc  = cms.string("Information to HTT candidates"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(True),
        variables = cms.PSet(
            fRec = Var("abs(properties().fRec())", float, doc="relative W width",precision=10),
            Ropt = Var("properties().ropt()", float, doc="optimal value of R",precision=10),
            RoptCalc = Var("properties().roptCalc()", float, doc="expected value of optimal R",precision=10),
            ptForRoptCalc = Var("properties().ptForRoptCalc()", float, doc="pT used for calculation of RoptCalc",precision=10)
        )
    )

    #Add HTT subjets
    process.HTTV2SubjetsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("looseOptRHTTSubjetsOrdered"),
        cut = cms.string(""),
        name = cms.string("HTTV2Subjets"),
        doc  = cms.string("Btags of HTT candidate subjets"),
        singleton = cms.bool(False),
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars,
            rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
            IDPassed = Var("?pt() <= 20 || abs(eta()) >= 2.4 || neutralHadronEnergyFraction()>=0.90 || neutralEmEnergyFraction() >= 0.90 ||(chargedMultiplicity()+neutralMultiplicity()) <= 1 || chargedHadronEnergyFraction() <= 0 || chargedMultiplicity() <= 0?0:1",float, doc="Subjet ID passed?",precision=1),
            btagDeepB = Var("bDiscriminator('looseOptRHTTpfCombinedInclusiveSecondaryVertexV2BJetTags:probb')+bDiscriminator('looseOptRHTTpfCombinedInclusiveSecondaryVertexV2BJetTags:probbb')",float,doc="CSV V2 btag discriminator",precision=10),
            #area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        )
    )



    #############################
    ####    CA15 Fatjets     ####
    #############################

    process.ca15PFJetsCHS = cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam = cms.double(1.5))

    process.ca15PFJetsCHS.src = cms.InputTag("chs")
    process.ca15PFJetsCHS.jetPtMin = cms.double(200.)


    #Hbb tag
    process.ca15PFJetsCHSImpactParameterTagInfos = process.pfImpactParameterTagInfos.clone(
        primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
        candidates = cms.InputTag("packedPFCandidates"),
        computeProbabilities = cms.bool(False),
        computeGhostTrack = cms.bool(False),
        maxDeltaR = cms.double(delta_r),
        jets = cms.InputTag("ca15PFJetsCHS"),
    )

    process.ca15PFJetsCHSImpactParameterTagInfos.explicitJTA = cms.bool(False)

    process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos = process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
        extSVCollection = cms.InputTag('slimmedSecondaryVertices'),
        trackIPTagInfos = cms.InputTag("ca15PFJetsCHSImpactParameterTagInfos"),
    )

    process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.useSVClustering = cms.bool(False)
    process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.rParam = cms.double(delta_r)
    process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.extSVDeltaRToJet = cms.double(delta_r)
    process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.trackSelection.jetDeltaRMax = cms.double(delta_r)
    process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(delta_r)
    process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.jetAlgorithm = cms.string(jetAlgo)

    process.ca15PFJetsCHSpfBoostedDoubleSVTagInfos = process.pfBoostedDoubleSVAK8TagInfos.clone(
        svTagInfos = cms.InputTag("ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos"),
    )

    process.ca15PFJetsCHSpfBoostedDoubleSVTagInfos.trackSelection.jetDeltaRMax = cms.double(delta_r)

    process.ca15PFJetsCHScandidateBoostedDoubleSecondaryVertexComputer = cms.ESProducer("CandidateBoostedDoubleSecondaryVertexESProducer",
       trackSelectionBlock,
       beta = cms.double(1.0),
       R0 = cms.double(delta_r),
       maxSVDeltaRToJet = cms.double(maxSVDeltaRToJet),
       useCondDB = cms.bool(False),
       weightFile = cms.FileInPath(weightFile),
       useGBRForest = cms.bool(True),
       useAdaBoost = cms.bool(False),
       trackPairV0Filter = cms.PSet(k0sMassWindow = cms.double(0.03))
    )

    process.ca15PFJetsCHScandidateBoostedDoubleSecondaryVertexComputer.trackSelection.jetDeltaRMax = cms.double(delta_r)

    process.ca15PFJetsCHSpfBoostedDoubleSecondaryVertexBJetTags = cms.EDProducer("JetTagProducer",
        jetTagComputer = cms.string("ca15PFJetsCHScandidateBoostedDoubleSecondaryVertexComputer"),
        tagInfos = cms.VInputTag(cms.InputTag("ca15PFJetsCHSpfBoostedDoubleSVTagInfos"))
    )

    process.ca15PFJetsCHSpatFatjet = cms.EDProducer("PATJetProducer",
        jetSource = cms.InputTag("ca15PFJetsCHS"),
        embedPFCandidates = cms.bool(False),
        addJetCorrFactors    = cms.bool(False),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactors") ),
        # btag information
        addBTagInfo          = cms.bool(True),   ## master switch
        addDiscriminators    = cms.bool(True),   ## addition btag discriminators
        discriminatorSources = cms.VInputTag(
            cms.InputTag("ca15PFJetsCHSpfBoostedDoubleSecondaryVertexBJetTags"),
        ),
        addTagInfos     = cms.bool(False),
        tagInfoSources  = cms.VInputTag(),
        addAssociatedTracks    = cms.bool(False),
        trackAssociationSource = cms.InputTag("ak4JetTracksAssociatorAtVertexPF"),
        addJetCharge    = cms.bool(False),
        jetChargeSource = cms.InputTag("patJetCharge"),
        addJetID = cms.bool(False),
        jetIDMap = cms.InputTag("ak4JetID"),
        addGenPartonMatch   = cms.bool(False),                           ## switch on/off matching to quarks from hard scatterin
        embedGenPartonMatch = cms.bool(False),                           ## switch on/off embedding of the GenParticle parton for this jet
        genPartonMatch      = cms.InputTag("NOT_IMPLEMENTED"),        ## particles source to be used for the matching
        addGenJetMatch      = cms.bool(False),                           ## switch on/off matching to GenJet's
        embedGenJetMatch    = cms.bool(False),                           ## switch on/off embedding of matched genJet's
        genJetMatch         = cms.InputTag("NOT_IMPLEMENTED"),        ## GenJet source to be used for the matching
        addPartonJetMatch   = cms.bool(False),                          ## switch on/off matching to PartonJet's (not implemented yet)
        partonJetSource     = cms.InputTag("NOT_IMPLEMENTED"),          ## ParticleJet source to be used for the matching
        getJetMCFlavour    = cms.bool(False),
        useLegacyJetMCFlavour = cms.bool(False),
        addJetFlavourInfo  = cms.bool(False),
        JetPartonMapSource = cms.InputTag("NOT_IMPLEMENTED"),
        JetFlavourInfoSource = cms.InputTag("NOT_IMPLEMENTED"),
        addEfficiencies = cms.bool(False),
        efficiencies    = cms.PSet(),
        addResolutions = cms.bool(False),
        resolutions     = cms.PSet()
    )

    process.ca15PFJetsCHSFatjetOrdered =  cms.EDProducer("HTTBtagMatchProducer",
        jetSource = cms.InputTag("ca15PFJetsCHS"),
        patsubjets = cms.InputTag("ca15PFJetsCHSpatFatjet")
    )

    process.ca15PFJetsCHSNSubjettiness  = cms.EDProducer("NjettinessAdder",
        src=cms.InputTag("ca15PFJetsCHSFatjetOrdered"),
        cone=cms.double(1.5),
        Njets = cms.vuint32(1,2,3),
        # variables for measure definition :
        measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
        beta = cms.double(1.0),              # CMS default is 1
        R0 = cms.double(1.5),                # CMS default is jet cone size
        Rcutoff = cms.double( 999.0),       # not used by default
        # variables for axes definition :
        axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
        nPass = cms.int32(999),             # not used by default
        akAxesR0 = cms.double(-999.0)        # not used by default
    )

    process.FatjetsWithUserData = cms.EDProducer("PATJetUserDataEmbedder",
         src = cms.InputTag("ca15PFJetsCHSFatjetOrdered"),
         userFloats = cms.PSet(
            tau1= cms.InputTag("ca15PFJetsCHSNSubjettiness:tau1"),
            tau2= cms.InputTag("ca15PFJetsCHSNSubjettiness:tau2"),
            tau3= cms.InputTag("ca15PFJetsCHSNSubjettiness:tau3"),
         ),
    )

    process.finalFatjets = cms.EDFilter("PATJetRefSelector",
        src = cms.InputTag("FatjetsWithUserData"),
        cut = cms.string("pt > 5 ")
    )

    #Make all tables
    process.ca15Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("ca15PFJetsCHS"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("FatjetCA15"),
        doc  = cms.string("CA15 fatjets (ungroomed)"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars,
            #jetId = Var("userInt('tightId')*2+userInt('looseId')",int,doc="Jet ID flags bit1 is loose, bit2 is tight"),
            area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        )
    )

    #Add Nsubjettiness and BBtag
    process.FatjetBBTagTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("finalFatjets"),
        cut = cms.string(""),
        name = cms.string("FatjetCA15"),
        doc  = cms.string("CA15 fatjets (ungroomed)"),
        singleton = cms.bool(False),
        extension = cms.bool(True),
        variables = cms.PSet(
            bbtag  = Var("bDiscriminator('ca15PFJetsCHSpfBoostedDoubleSecondaryVertexBJetTags')",float,doc="Double btag discriminator",precision=10),
            tau1  = Var("userFloat('tau1')",float,doc="N-subjettiness",precision=10),
            tau2  = Var("userFloat('tau2')",float,doc="N-subjettiness",precision=10),
            tau3  = Var("userFloat('tau3')",float,doc="N-subjettiness",precision=10),
        )
    )


    ######################################
    ####    CA15 Softdrop Fatjets     ####
    ######################################

    # Apply softdrop to CA R=1.5 jets
    process.ca15PFSoftdropJetsCHS = process.ca15PFJetsCHS.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.1),
        beta = cms.double(0.0),
        R0 = cms.double(1.5),
        useExplicitGhosts = cms.bool(True),
        writeCompound = cms.bool(True), # Also write subjets
        jetCollInstanceName=cms.string("SubJets"),
    )

    #Get Softdrop subjet btags
    process.ca15PFSoftdropJetsCHSImpactParameterTagInfos = pfImpactParameterTagInfos.clone(
        primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
        candidates = cms.InputTag("chs"),
        computeGhostTrack = cms.bool(True),
        computeProbabilities = cms.bool(True),
        maxDeltaR = cms.double(0.4),
        jets = cms.InputTag("ca15PFSoftdropJetsCHS", "SubJets")
    )

    process.ca15PFSoftdropJetsCHSImpactParameterTagInfos.explicitJTA = cms.bool(True)

    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos = pfInclusiveSecondaryVertexFinderTagInfos.clone(
        extSVCollection = cms.InputTag('slimmedSecondaryVertices'),
        trackIPTagInfos = cms.InputTag("ca15PFSoftdropJetsCHSImpactParameterTagInfos"),
    )

    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.useSVClustering = cms.bool(True)
    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.rParam = cms.double(delta_r)
    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.extSVDeltaRToJet = cms.double(0.3)
    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.trackSelection.jetDeltaRMax = cms.double(0.3)
    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(0.4)
    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.jetAlgorithm = cms.string(jetAlgo)
    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.fatJets  =  cms.InputTag(initial_jet)
    process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.groomedFatJets = cms.InputTag("ca15PFSoftdropJetsCHS","")


    process.ca15PFSoftdropJetsCHSpfDeepCSVInfos = pfDeepCSVTagInfos.clone(
        svTagInfos = cms.InputTag("ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos"),
        computer = combinedSecondaryVertexCommon
        )

    process.ca15PFSoftdropJetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags = pfDeepCSVJetTags.clone(
        src = cms.InputTag('ca15PFSoftdropJetsCHSpfDeepCSVInfos')
    )


    process.jetCorrFactorsSD = patJetCorrFactors.clone(src=cms.InputTag("ca15PFSoftdropJetsCHS", "SubJets"),
        levels = cms.vstring('L1FastJet',
            'L2Relative',
            'L3Absolute',
        'L2L3Residual'),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    )

    process.ca15PFSoftdropJetsCHSpatSubJets = cms.EDProducer("PATJetProducer",
        jetSource = cms.InputTag("ca15PFSoftdropJetsCHS", "SubJets"),
        embedPFCandidates = cms.bool(False),
        addJetCorrFactors    = cms.bool(True),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("jetCorrFactorsSD") ),
        # btag information
        addBTagInfo          = cms.bool(True),   ## master switch
        addDiscriminators    = cms.bool(True),   ## addition btag discriminators
        discriminatorSources = cms.VInputTag(cms.InputTag('ca15PFSoftdropJetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags', 'probb'),cms.InputTag('ca15PFSoftdropJetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags', 'probbb')),
        addTagInfos     = cms.bool(False),
        tagInfoSources  = cms.VInputTag(),
        addAssociatedTracks    = cms.bool(False),
        trackAssociationSource = cms.InputTag("ak4JetTracksAssociatorAtVertexPF"),
        addJetCharge    = cms.bool(False),
        jetChargeSource = cms.InputTag("patJetCharge"),
        addJetID = cms.bool(False),
        jetIDMap = cms.InputTag("ak4JetID"),
        addGenPartonMatch   = cms.bool(False),                           ## switch on/off matching to quarks from hard scatterin
        embedGenPartonMatch = cms.bool(False),                           ## switch on/off embedding of the GenParticle parton for this jet
        genPartonMatch      = cms.InputTag("patJetPartonMatch"),        ## particles source to be used for the matching
        addGenJetMatch      = cms.bool(False),                           ## switch on/off matching to GenJet's
        embedGenJetMatch    = cms.bool(False),                           ## switch on/off embedding of matched genJet's
        genJetMatch         = cms.InputTag("patJetGenJetMatch"),        ## GenJet source to be used for the matching
        addPartonJetMatch   = cms.bool(False),                          ## switch on/off matching to PartonJet's (not implemented yet)
        partonJetSource     = cms.InputTag("NOT_IMPLEMENTED"),          ## ParticleJet source to be used for the matching
        getJetMCFlavour    = cms.bool(False),
        useLegacyJetMCFlavour = cms.bool(False),
        addJetFlavourInfo  = cms.bool(False),
        JetPartonMapSource = cms.InputTag("patJetFlavourAssociationLegacy"),
        JetFlavourInfoSource = cms.InputTag("patJetFlavourAssociation"),
        addEfficiencies = cms.bool(False),
        efficiencies    = cms.PSet(),
        addResolutions = cms.bool(False),
        resolutions     = cms.PSet()
    )

    process.ca15PFSoftdropJetsCHSSubjetsOrdered =  cms.EDProducer("HTTBtagMatchProducer",
        jetSource = cms.InputTag("ca15PFSoftdropJetsCHS", "SubJets"),
        patsubjets = cms.InputTag("ca15PFSoftdropJetsCHSpatSubJets")
    )

    #Now get softdrop Hbb and Nsubjettiness

    #Need to recreate softdrop jets without subjets to get jet constituents.
    process.ca15PFSoftdropJetsCHSNoSub = process.ca15PFJetsCHS.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.1),
        beta = cms.double(0.0),
        R0 = cms.double(1.5),
        useExplicitGhosts = cms.bool(True),
    )


    process.ca15PFSDJetsCHSImpactParameterTagInfos = process.pfImpactParameterTagInfos.clone(
        primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
        candidates = cms.InputTag("packedPFCandidates"),
        computeProbabilities = cms.bool(False),
        computeGhostTrack = cms.bool(False),
        maxDeltaR = cms.double(delta_r),
        jets = cms.InputTag("ca15PFSoftdropJetsCHSNoSub"),
    )

    process.ca15PFSDJetsCHSImpactParameterTagInfos.explicitJTA = cms.bool(False)

    process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos = process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
        extSVCollection = cms.InputTag('slimmedSecondaryVertices'),
        trackIPTagInfos = cms.InputTag("ca15PFSDJetsCHSImpactParameterTagInfos"),
    )

    process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.useSVClustering = cms.bool(False)
    process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.rParam = cms.double(delta_r)
    process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.extSVDeltaRToJet = cms.double(delta_r)
    process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.trackSelection.jetDeltaRMax = cms.double(delta_r)
    process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(delta_r)
    process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos.jetAlgorithm = cms.string(jetAlgo)

    process.ca15PFSDJetsCHSpfBoostedDoubleSVTagInfos = process.pfBoostedDoubleSVAK8TagInfos.clone(
        svTagInfos = cms.InputTag("ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos"),
    )

    process.ca15PFSDJetsCHSpfBoostedDoubleSVTagInfos.trackSelection.jetDeltaRMax = cms.double(delta_r)

    process.ca15PFSDJetsCHScandidateBoostedDoubleSecondaryVertexComputer = cms.ESProducer("CandidateBoostedDoubleSecondaryVertexESProducer",
       trackSelectionBlock,
       beta = cms.double(1.0),
       R0 = cms.double(delta_r),
       maxSVDeltaRToJet = cms.double(maxSVDeltaRToJet),
       useCondDB = cms.bool(False),
       weightFile = cms.FileInPath(weightFile),
       useGBRForest = cms.bool(True),
       useAdaBoost = cms.bool(False),
       trackPairV0Filter = cms.PSet(k0sMassWindow = cms.double(0.03))
    )

    process.ca15PFSDJetsCHScandidateBoostedDoubleSecondaryVertexComputer.trackSelection.jetDeltaRMax = cms.double(delta_r)

    process.ca15PFSDJetsCHSpfBoostedDoubleSecondaryVertexBJetTags = cms.EDProducer("JetTagProducer",
        jetTagComputer = cms.string("ca15PFSDJetsCHScandidateBoostedDoubleSecondaryVertexComputer"),
        tagInfos = cms.VInputTag(cms.InputTag("ca15PFSDJetsCHSpfBoostedDoubleSVTagInfos"))
    )

    process.ca15PFSDJetsCHSpatFatjet = cms.EDProducer("PATJetProducer",
        jetSource = cms.InputTag("ca15PFSoftdropJetsCHSNoSub"),
        embedPFCandidates = cms.bool(False),
        addJetCorrFactors    = cms.bool(False),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactors") ),
        # btag information
        addBTagInfo          = cms.bool(True),   ## master switch
        addDiscriminators    = cms.bool(True),   ## addition btag discriminators
        discriminatorSources = cms.VInputTag(
            cms.InputTag("ca15PFSDJetsCHSpfBoostedDoubleSecondaryVertexBJetTags"),
        ),
        addTagInfos     = cms.bool(False),
        tagInfoSources  = cms.VInputTag(),
        addAssociatedTracks    = cms.bool(False),
        trackAssociationSource = cms.InputTag("ak4JetTracksAssociatorAtVertexPF"),
        addJetCharge    = cms.bool(False),
        jetChargeSource = cms.InputTag("patJetCharge"),
        addJetID = cms.bool(False),
        jetIDMap = cms.InputTag("ak4JetID"),
        addGenPartonMatch   = cms.bool(False),                           ## switch on/off matching to quarks from hard scatterin
        embedGenPartonMatch = cms.bool(False),                           ## switch on/off embedding of the GenParticle parton for this jet
        genPartonMatch      = cms.InputTag("NOT_IMPLEMENTED"),        ## particles source to be used for the matching
        addGenJetMatch      = cms.bool(False),                           ## switch on/off matching to GenJet's
        embedGenJetMatch    = cms.bool(False),                           ## switch on/off embedding of matched genJet's
        genJetMatch         = cms.InputTag("NOT_IMPLEMENTED"),        ## GenJet source to be used for the matching
        addPartonJetMatch   = cms.bool(False),                          ## switch on/off matching to PartonJet's (not implemented yet)
        partonJetSource     = cms.InputTag("NOT_IMPLEMENTED"),          ## ParticleJet source to be used for the matching
        getJetMCFlavour    = cms.bool(False),
        useLegacyJetMCFlavour = cms.bool(False),
        addJetFlavourInfo  = cms.bool(False),
        JetPartonMapSource = cms.InputTag("NOT_IMPLEMENTED"),
        JetFlavourInfoSource = cms.InputTag("NOT_IMPLEMENTED"),
        addEfficiencies = cms.bool(False),
        efficiencies    = cms.PSet(),
        addResolutions = cms.bool(False),
        resolutions     = cms.PSet()
    )

    process.ca15PFSDJetsCHSFatjetOrdered =  cms.EDProducer("HTTBtagMatchProducer",
        jetSource = cms.InputTag("ca15PFSoftdropJetsCHSNoSub"),
        patsubjets = cms.InputTag("ca15PFSDJetsCHSpatFatjet")
    )

    process.ca15PFSDJetsCHSNSubjettiness  = cms.EDProducer("NjettinessAdder",
        src=cms.InputTag("ca15PFSDJetsCHSFatjetOrdered"),
        cone=cms.double(1.5),
        Njets = cms.vuint32(1,2,3),
        # variables for measure definition :
        measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
        beta = cms.double(1.0),              # CMS default is 1
        R0 = cms.double(1.5),                # CMS default is jet cone size
        Rcutoff = cms.double( 999.0),       # not used by default
        # variables for axes definition :
        axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
        nPass = cms.int32(999),             # not used by default
        akAxesR0 = cms.double(-999.0)        # not used by default
    )

    process.SDFatjetsWithUserData = cms.EDProducer("PATJetUserDataEmbedder",
         src = cms.InputTag("ca15PFSDJetsCHSFatjetOrdered"),
         userFloats = cms.PSet(
            tau1= cms.InputTag("ca15PFSDJetsCHSNSubjettiness:tau1"),
            tau2= cms.InputTag("ca15PFSDJetsCHSNSubjettiness:tau2"),
            tau3= cms.InputTag("ca15PFSDJetsCHSNSubjettiness:tau3"),
         ),
    )

    process.finalSDFatjets = cms.EDFilter("PATJetRefSelector",
        src = cms.InputTag("SDFatjetsWithUserData"),
        cut = cms.string("pt > 5 ")
    )

    #Make all tables
    process.ca15SoftDropTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("ca15PFSoftdropJetsCHS"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("FatjetCA15SoftDrop"),
        doc  = cms.string("Softdrop CA15 fatjets (zcut = 0.1, beta = 0)"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars,
            #jetId = Var("userInt('tightId')*2+userInt('looseId')",int,doc="Jet ID flags bit1 is loose, bit2 is tight"),
            area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
            subJetIdx1 = Var("?numberOfSourceCandidatePtrs()>0 && sourceCandidatePtr(0).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(0).key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2 = Var("?numberOfSourceCandidatePtrs()>1 && sourceCandidatePtr(1).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(1).key():-1", int,
                 doc="index of second subjet"),
        )
    )

    #Add Nsubjettiness and BBtag
    process.SDFatjetBBTagTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("finalSDFatjets"),
        cut = cms.string(""),
        name = cms.string("FatjetCA15SoftDrop"),
        doc  = cms.string("Softdrop CA15 fatjets (zcut = 0.1, beta = 0)"),
        singleton = cms.bool(False),
        extension = cms.bool(True),
        variables = cms.PSet(
            bbtag  = Var("bDiscriminator('ca15PFSDJetsCHSpfBoostedDoubleSecondaryVertexBJetTags')",float,doc="Double btag discriminator",precision=10),
            tau1  = Var("userFloat('tau1')",float,doc="N-subjettiness",precision=10),
            tau2  = Var("userFloat('tau2')",float,doc="N-subjettiness",precision=10),
            tau3  = Var("userFloat('tau3')",float,doc="N-subjettiness",precision=10),
        )
    )

    process.ca15SoftDropSubjetsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("ca15PFSoftdropJetsCHSSubjetsOrdered"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("FatjetCA15SoftDropSubjets"),
        doc  = cms.string("Softdrop CA15 subjets (zcut = 0.1, beta = 0)"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars,
            rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
            #jetId = Var("userInt('tightId')*2+userInt('looseId')",int,doc="Jet ID flags bit1 is loose, bit2 is tight"),
            area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
            btag  = Var("bDiscriminator('ca15PFSoftdropJetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags:probb')+bDiscriminator('ca15PFSoftdropJetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags:probbb')",float,doc="CMVA V2 btag discriminator",precision=10),
            IDPassed = Var("?pt() <= 20 || abs(eta()) >= 2.4 || neutralHadronEnergyFraction()>=0.90 || neutralEmEnergyFraction() >= 0.90 ||(chargedMultiplicity()+neutralMultiplicity()) <= 1 || chargedHadronEnergyFraction() <= 0 || chargedMultiplicity() <= 0?0:1",float, doc="Subjet ID passed?",precision=1),
        )
    )

    ######################################################
    ####    CA15 Softdrop Fatjets (beta=1, z=0.2)     ####
    ######################################################

    # Apply softdrop to CA R=1.5 jets
    process.ca15PFSoftdrop2JetsCHS = process.ca15PFJetsCHS.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.2),
        beta = cms.double(1.0),
        R0 = cms.double(1.5),
        useExplicitGhosts = cms.bool(True),
        writeCompound = cms.bool(True), # Also write subjets
        jetCollInstanceName=cms.string("SubJets"),
    )

    #Get Softdrop subjet btags
    process.ca15PFSoftdrop2JetsCHSImpactParameterTagInfos = process.pfImpactParameterTagInfos.clone(
        primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
        candidates = cms.InputTag("chs"),
        computeGhostTrack = cms.bool(True),
        computeProbabilities = cms.bool(True),
        maxDeltaR = cms.double(0.4),
        jets = cms.InputTag("ca15PFSoftdrop2JetsCHS", "SubJets")
    )

    process.ca15PFSoftdrop2JetsCHSImpactParameterTagInfos.explicitJTA = cms.bool(True)

    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos = process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
        extSVCollection = cms.InputTag('slimmedSecondaryVertices'),
        trackIPTagInfos = cms.InputTag("ca15PFSoftdrop2JetsCHSImpactParameterTagInfos"),
    )

    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.useSVClustering = cms.bool(True)
    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.rParam = cms.double(delta_r)
    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.extSVDeltaRToJet = cms.double(0.3)
    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.trackSelection.jetDeltaRMax = cms.double(0.3)
    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(0.4)
    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.jetAlgorithm = cms.string(jetAlgo)
    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.fatJets  =  cms.InputTag(initial_jet)
    process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.groomedFatJets = cms.InputTag("ca15PFSoftdrop2JetsCHS","")


    process.ca15PFSoftdrop2JetsCHSpfDeepCSVInfos = process.pfDeepCSVTagInfos.clone(
        svTagInfos = cms.InputTag("ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos"),
        computer = combinedSecondaryVertexCommon
        )

    process.ca15PFSoftdrop2JetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags = process.pfDeepCSVJetTags.clone(
        src = cms.InputTag('ca15PFSoftdrop2JetsCHSpfDeepCSVInfos')
    )


    process.jetCorrFactorsSD2 = process.patJetCorrFactors.clone(src=cms.InputTag("ca15PFSoftdrop2JetsCHS", "SubJets"),
        levels = cms.vstring('L1FastJet',
            'L2Relative',
            'L3Absolute',
        'L2L3Residual'),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    )


    process.ca15PFSoftdrop2JetsCHSpatSubJets = cms.EDProducer("PATJetProducer",
        jetSource = cms.InputTag("ca15PFSoftdrop2JetsCHS", "SubJets"),
        embedPFCandidates = cms.bool(False),
        addJetCorrFactors    = cms.bool(True),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("jetCorrFactorsSD2") ),
        # btag information
        addBTagInfo          = cms.bool(True),   ## master switch
        addDiscriminators    = cms.bool(True),   ## addition btag discriminators
        discriminatorSources = cms.VInputTag(cms.InputTag('ca15PFSoftdrop2JetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags', 'probb'),cms.InputTag('ca15PFSoftdrop2JetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags', 'probbb')),
        addTagInfos     = cms.bool(False),
        tagInfoSources  = cms.VInputTag(),
        addAssociatedTracks    = cms.bool(False),
        trackAssociationSource = cms.InputTag("ak4JetTracksAssociatorAtVertexPF"),
        addJetCharge    = cms.bool(False),
        jetChargeSource = cms.InputTag("patJetCharge"),
        addJetID = cms.bool(False),
        jetIDMap = cms.InputTag("ak4JetID"),
        addGenPartonMatch   = cms.bool(False),                           ## switch on/off matching to quarks from hard scatterin
        embedGenPartonMatch = cms.bool(False),                           ## switch on/off embedding of the GenParticle parton for this jet
        genPartonMatch      = cms.InputTag("patJetPartonMatch"),        ## particles source to be used for the matching
        addGenJetMatch      = cms.bool(False),                           ## switch on/off matching to GenJet's
        embedGenJetMatch    = cms.bool(False),                           ## switch on/off embedding of matched genJet's
        genJetMatch         = cms.InputTag("patJetGenJetMatch"),        ## GenJet source to be used for the matching
        addPartonJetMatch   = cms.bool(False),                          ## switch on/off matching to PartonJet's (not implemented yet)
        partonJetSource     = cms.InputTag("NOT_IMPLEMENTED"),          ## ParticleJet source to be used for the matching
        getJetMCFlavour    = cms.bool(False),
        useLegacyJetMCFlavour = cms.bool(False),
        addJetFlavourInfo  = cms.bool(False),
        JetPartonMapSource = cms.InputTag("patJetFlavourAssociationLegacy"),
        JetFlavourInfoSource = cms.InputTag("patJetFlavourAssociation"),
        addEfficiencies = cms.bool(False),
        efficiencies    = cms.PSet(),
        addResolutions = cms.bool(False),
        resolutions     = cms.PSet()
    )

    process.ca15PFSoftdrop2JetsCHSSubjetsOrdered =  cms.EDProducer("HTTBtagMatchProducer",
        jetSource = cms.InputTag("ca15PFSoftdrop2JetsCHS", "SubJets"),
        patsubjets = cms.InputTag("ca15PFSoftdrop2JetsCHSpatSubJets")
    )

    #Now get softdrop Hbb and Nsubjettiness

    #Need to recreate softdrop jets without subjets to get jet constituents.
    process.ca15PFSoftdrop2JetsCHSNoSub = process.ca15PFJetsCHS.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.2),
        beta = cms.double(1.0),
        R0 = cms.double(1.5),
        useExplicitGhosts = cms.bool(True),
    )

    process.ca15PFSD2JetsCHSImpactParameterTagInfos = process.pfImpactParameterTagInfos.clone(
        primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
        candidates = cms.InputTag("packedPFCandidates"),
        computeProbabilities = cms.bool(False),
        computeGhostTrack = cms.bool(False),
        maxDeltaR = cms.double(delta_r),
        jets = cms.InputTag("ca15PFSoftdrop2JetsCHSNoSub"),
    )

    process.ca15PFSD2JetsCHSImpactParameterTagInfos.explicitJTA = cms.bool(False)

    process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos = process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
        extSVCollection = cms.InputTag('slimmedSecondaryVertices'),
        trackIPTagInfos = cms.InputTag("ca15PFSD2JetsCHSImpactParameterTagInfos"),
    )

    process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.useSVClustering = cms.bool(False)
    process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.rParam = cms.double(delta_r)
    process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.extSVDeltaRToJet = cms.double(delta_r)
    process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.trackSelection.jetDeltaRMax = cms.double(delta_r)
    process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(delta_r)
    process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos.jetAlgorithm = cms.string(jetAlgo)

    process.ca15PFSD2JetsCHSpfBoostedDoubleSVTagInfos = process.pfBoostedDoubleSVAK8TagInfos.clone(
        svTagInfos = cms.InputTag("ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos"),
    )

    process.ca15PFSD2JetsCHSpfBoostedDoubleSVTagInfos.trackSelection.jetDeltaRMax = cms.double(delta_r)

    process.ca15PFSD2JetsCHScandidateBoostedDoubleSecondaryVertexComputer = cms.ESProducer("CandidateBoostedDoubleSecondaryVertexESProducer",
       trackSelectionBlock,
       beta = cms.double(1.0),
       R0 = cms.double(delta_r),
       maxSVDeltaRToJet = cms.double(maxSVDeltaRToJet),
       useCondDB = cms.bool(False),
       weightFile = cms.FileInPath(weightFile),
       useGBRForest = cms.bool(True),
       useAdaBoost = cms.bool(False),
       trackPairV0Filter = cms.PSet(k0sMassWindow = cms.double(0.03))
    )

    process.ca15PFSD2JetsCHScandidateBoostedDoubleSecondaryVertexComputer.trackSelection.jetDeltaRMax = cms.double(delta_r)

    process.ca15PFSD2JetsCHSpfBoostedDoubleSecondaryVertexBJetTags = cms.EDProducer("JetTagProducer",
        jetTagComputer = cms.string("ca15PFSD2JetsCHScandidateBoostedDoubleSecondaryVertexComputer"),
        tagInfos = cms.VInputTag(cms.InputTag("ca15PFSD2JetsCHSpfBoostedDoubleSVTagInfos"))
    )

    process.ca15PFSD2JetsCHSpatFatjet = cms.EDProducer("PATJetProducer",
        jetSource = cms.InputTag("ca15PFSoftdrop2JetsCHSNoSub"),
        embedPFCandidates = cms.bool(False),
        addJetCorrFactors    = cms.bool(False),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactors") ),
        # btag information
        addBTagInfo          = cms.bool(True),   ## master switch
        addDiscriminators    = cms.bool(True),   ## addition btag discriminators
        discriminatorSources = cms.VInputTag(
            cms.InputTag("ca15PFSD2JetsCHSpfBoostedDoubleSecondaryVertexBJetTags"),
        ),
        addTagInfos     = cms.bool(False),
        tagInfoSources  = cms.VInputTag(),
        addAssociatedTracks    = cms.bool(False),
        trackAssociationSource = cms.InputTag("ak4JetTracksAssociatorAtVertexPF"),
        addJetCharge    = cms.bool(False),
        jetChargeSource = cms.InputTag("patJetCharge"),
        addJetID = cms.bool(False),
        jetIDMap = cms.InputTag("ak4JetID"),
        addGenPartonMatch   = cms.bool(False),                           ## switch on/off matching to quarks from hard scatterin
        embedGenPartonMatch = cms.bool(False),                           ## switch on/off embedding of the GenParticle parton for this jet
        genPartonMatch      = cms.InputTag("NOT_IMPLEMENTED"),        ## particles source to be used for the matching
        addGenJetMatch      = cms.bool(False),                           ## switch on/off matching to GenJet's
        embedGenJetMatch    = cms.bool(False),                           ## switch on/off embedding of matched genJet's
        genJetMatch         = cms.InputTag("NOT_IMPLEMENTED"),        ## GenJet source to be used for the matching
        addPartonJetMatch   = cms.bool(False),                          ## switch on/off matching to PartonJet's (not implemented yet)
        partonJetSource     = cms.InputTag("NOT_IMPLEMENTED"),          ## ParticleJet source to be used for the matching
        getJetMCFlavour    = cms.bool(False),
        useLegacyJetMCFlavour = cms.bool(False),
        addJetFlavourInfo  = cms.bool(False),
        JetPartonMapSource = cms.InputTag("NOT_IMPLEMENTED"),
        JetFlavourInfoSource = cms.InputTag("NOT_IMPLEMENTED"),
        addEfficiencies = cms.bool(False),
        efficiencies    = cms.PSet(),
        addResolutions = cms.bool(False),
        resolutions     = cms.PSet()
    )

    process.ca15PFSD2JetsCHSFatjetOrdered =  cms.EDProducer("HTTBtagMatchProducer",
        jetSource = cms.InputTag("ca15PFSoftdrop2JetsCHSNoSub"),
        patsubjets = cms.InputTag("ca15PFSD2JetsCHSpatFatjet")
    )

    process.ca15PFSD2JetsCHSNSubjettiness  = cms.EDProducer("NjettinessAdder",
        src=cms.InputTag("ca15PFSD2JetsCHSFatjetOrdered"),
        cone=cms.double(1.5),
        Njets = cms.vuint32(1,2,3),
        # variables for measure definition :
        measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
        beta = cms.double(1.0),              # CMS default is 1
        R0 = cms.double(1.5),                # CMS default is jet cone size
        Rcutoff = cms.double( 999.0),       # not used by default
        # variables for axes definition :
        axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
        nPass = cms.int32(999),             # not used by default
        akAxesR0 = cms.double(-999.0)        # not used by default
    )

    process.SD2FatjetsWithUserData = cms.EDProducer("PATJetUserDataEmbedder",
         src = cms.InputTag("ca15PFSD2JetsCHSFatjetOrdered"),
         userFloats = cms.PSet(
            tau1= cms.InputTag("ca15PFSD2JetsCHSNSubjettiness:tau1"),
            tau2= cms.InputTag("ca15PFSD2JetsCHSNSubjettiness:tau2"),
            tau3= cms.InputTag("ca15PFSD2JetsCHSNSubjettiness:tau3"),
         ),
    )

    process.finalSD2Fatjets = cms.EDFilter("PATJetRefSelector",
        src = cms.InputTag("SD2FatjetsWithUserData"),
        cut = cms.string("pt > 5 ")
    )

    #Make all tables
    process.ca15SoftDrop2Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("ca15PFSoftdrop2JetsCHS"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("FatjetCA15SoftDrop_b1z02"),
        doc  = cms.string("Softdrop CA15 fatjets (zcut = 0.2, beta = 1)"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars,
            #jetId = Var("userInt('tightId')*2+userInt('looseId')",int,doc="Jet ID flags bit1 is loose, bit2 is tight"),
            area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
            subJetIdx1 = Var("?numberOfSourceCandidatePtrs()>0 && sourceCandidatePtr(0).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(0).key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2 = Var("?numberOfSourceCandidatePtrs()>1 && sourceCandidatePtr(1).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(1).key():-1", int,
                 doc="index of second subjet"),
        )
    )

    #Add Nsubjettiness and BBtag
    process.SD2FatjetBBTagTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("finalSD2Fatjets"),
        cut = cms.string(""),
        name = cms.string("FatjetCA15SoftDrop_b1z02"),
        doc  = cms.string("Softdrop CA15 fatjets (zcut = 0.2, beta = 1)"),
        singleton = cms.bool(False),
        extension = cms.bool(True),
        variables = cms.PSet(
            bbtag  = Var("bDiscriminator('ca15PFSD2JetsCHSpfBoostedDoubleSecondaryVertexBJetTags')",float,doc="Double btag discriminator",precision=10),
            tau1  = Var("userFloat('tau1')",float,doc="N-subjettiness",precision=10),
            tau2  = Var("userFloat('tau2')",float,doc="N-subjettiness",precision=10),
            tau3  = Var("userFloat('tau3')",float,doc="N-subjettiness",precision=10),
        )
    )

    process.ca15SoftDrop2SubjetsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("ca15PFSoftdrop2JetsCHSSubjetsOrdered"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("FatjetCA15SoftDropSubjets_b1z02"),
        doc  = cms.string("Softdrop CA15 subjets (zcut = 0.2, beta = 1)"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars,
            rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
            #jetId = Var("userInt('tightId')*2+userInt('looseId')",int,doc="Jet ID flags bit1 is loose, bit2 is tight"),
            area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
            btag  = Var("bDiscriminator('ca15PFSoftdrop2JetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags:probb')+bDiscriminator('ca15PFSoftdrop2JetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags:probbb')",float,doc="CMVA V2 btag discriminator",precision=10),
            IDPassed = Var("?pt() <= 20 || abs(eta()) >= 2.4 || neutralHadronEnergyFraction()>=0.90 || neutralEmEnergyFraction() >= 0.90 ||(chargedMultiplicity()+neutralMultiplicity()) <= 1 || chargedHadronEnergyFraction() <= 0 || chargedMultiplicity() <= 0?0:1",float, doc="Subjet ID passed?",precision=1),
        )
    )

    #---- Gen HTT - Needed for JEC calculation

    from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
    process.selectedHadronsAndPartons = process.selectedHadronsAndPartons.clone(
        particles = "prunedGenParticles"
    )

    process.jetFlavourInfosHTTV2PFJets = cms.EDProducer("JetFlavourClustering",
        jets                     = cms.InputTag("looseOptRHTT"),
        groomedJets              = cms.InputTag("looseOptRHTT"),
        subjets                  = cms.InputTag("looseOptRHTT", "SubJets"),
        bHadrons                 = cms.InputTag("selectedHadronsAndPartons","bHadrons"),
        cHadrons                 = cms.InputTag("selectedHadronsAndPartons","cHadrons"),
        partons                  = cms.InputTag("selectedHadronsAndPartons","algorithmicPartons"),
        leptons                  = cms.InputTag("selectedHadronsAndPartons","leptons"),
        jetAlgorithm             = cms.string("CambridgeAachen"),
        rParam                   = cms.double(1.5),
        ghostRescaling           = cms.double(1e-18),
        hadronFlavourHasPriority = cms.bool(False)
    )

    process.HTTSubjetFlavourTable = cms.EDProducer("HTTSubjetFlavourTableProducer",
        name = HTTV2SubjetsTable.name,
        src = HTTV2SubjetsTable.src,
        cut = HTTV2SubjetsTable.cut,
        deltaR = cms.double(0.05),
        subjetFlavourInfos = cms.InputTag("jetFlavourInfosHTTV2PFJets","SubJets"),
    )


    #HTTMCTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    #    src = cms.InputTag("looseOptRHTTSubjetsOrdered"),
    #    cut = cms.string(""), #probably already applied in miniaod
    #    name = cms.string("HTTV2Subjets"),
    #    singleton = cms.bool(False), # the number of entries is variable
    #    extension = cms.bool(True), # this is the main table for the jets
    #    variables = cms.PSet(
    #        partonFlavour = Var("partonFlavour()", int, doc="flavour from parton matching"),
    #        hadronFlavour = Var("hadronFlavour()", int, doc="flavour from hadron ghost clustering"),
    #        genJetIdx = Var("?genJetFwdRef().backRef().isNonnull()?genJetFwdRef().backRef().key():-1", int, doc="index of matched gen jet"),
    #    )
    #)

    genJetParticleCollection = "packedGenParticles"

    # determine particles for clustering custom genJets
    from RecoJets.Configuration.GenJetParticles_cff import genParticlesForJetsNoNu
    process.genParticlesforHTT = process.genParticlesForJetsNoNu.clone(
        src = cms.InputTag(genJetParticleCollection)
    )

    process.genHTT = cms.EDProducer(
                "HTTTopJetProducer",
                process.GenJetParameters.clone(
                    src = cms.InputTag("genParticlesforHTT"),
                    doAreaFastjet = cms.bool(False),
                    doRhoFastjet = cms.bool(False)
                    ),
                #GenJetParameters.clone(
                #    src               = cms.InputTag("genParticlesForJets"),
                #    doAreaFastjet     = cms.bool(False),
                #    doRhoFastjet      = cms.bool(False),
                #    jetPtMin          = cms.double(200.0)
                #    ),
                AnomalousCellParameters,
                useExplicitGhosts = cms.bool(True),
                algorithm           = cms.int32(1),
                jetAlgorithm        = cms.string("CambridgeAachen"),
                rParam              = cms.double(1.5),
                optimalR            = cms.bool(True),
                qJets               = cms.bool(False),
                minFatjetPt         = cms.double(200.),
                minSubjetPt         = cms.double(0.),
                minCandPt           = cms.double(0.),
                maxFatjetAbsEta     = cms.double(99.),
                subjetMass          = cms.double(30.),
                muCut               = cms.double(0.8),
                filtR               = cms.double(0.3),
                filtN               = cms.int32(5),
                mode                = cms.int32(4),
                minCandMass         = cms.double(0.),
                maxCandMass         = cms.double(999999.),
                massRatioWidth      = cms.double(999999.),
                minM23Cut           = cms.double(0.),
                minM13Cut           = cms.double(0.),
                maxM13Cut           = cms.double(999999.),
                writeCompound       = cms.bool(True),
                jetCollInstanceName = cms.string("SubJets")
                )

    process.genHTTV2Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("genHTT"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("genHTTV2"),
        doc  = cms.string("gen HTTV2 candidates"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars
        )
    )

    process.genHTTV2SubjetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("genHTT", "SubJets"),
        cut = cms.string(""), #we should not filter on cross linked collections
        name = cms.string("genHTTV2Subjets"),
        doc  = cms.string("gen HTTV2 candidates"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False),
        variables = cms.PSet(P4Vars
        )
    )

    process.boostedSequence = cms.Task(
    ####process.boostedSequence = cms.Sequence(
        #Prepare input objects
            process.selectedMuonsTmp,
            process.selectedMuons,
            process.selectedElectronsTmp,
            process.selectedElectrons,
            process.chsTmp1,
            process.chsTmp2,
            process.chs,
            process.ca15PFJetsCHS,
            process.#HTTV2 , subjet btags
            process.looseOptRHTT,
            process.looseOptRHTTImpactParameterTagInfos,
            process.looseOptRHTTpfInclusiveSecondaryVertexFinderTagInfos,
            process.looseOptRHTTpfDeepCSVInfos,
            process.looseOptRHTTpfCombinedInclusiveSecondaryVertexV2BJetTags,
            process.jetCorrFactorsHTT,
            process.looseOptRHTTpatSubJets,
            process.looseOptRHTTSubjetsOrdered,
            process.#CA15 double btag
            process.ca15PFJetsCHSImpactParameterTagInfos,
            process.ca15PFJetsCHSpfInclusiveSecondaryVertexFinderTagInfos,
            process.ca15PFJetsCHSpfBoostedDoubleSVTagInfos,
            process.ca15PFJetsCHSpfBoostedDoubleSecondaryVertexBJetTags,
            process.ca15PFJetsCHSpatFatjet,
            process.ca15PFJetsCHSFatjetOrdered,
            process.ca15PFJetsCHSNSubjettiness,
            process.FatjetsWithUserData,
            process.finalFatjets,
            process.#Softdrop CA15 jets , subjet btags
            process.ca15PFSoftdropJetsCHS,
            process.ca15PFSoftdropJetsCHSImpactParameterTagInfos,
            process.ca15PFSoftdropJetsCHSpfInclusiveSecondaryVertexFinderTagInfos,
            process.ca15PFSoftdropJetsCHSpfDeepCSVInfos,
            process.ca15PFSoftdropJetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags,
            process.jetCorrFactorsSD,
            process.ca15PFSoftdropJetsCHSpatSubJets,
            process.ca15PFSoftdropJetsCHSSubjetsOrdered,
            process.#Softdrop bbtag , nsubjettiness
            process.ca15PFSoftdropJetsCHSNoSub,
            process.ca15PFSDJetsCHSImpactParameterTagInfos,
            process.ca15PFSDJetsCHSpfInclusiveSecondaryVertexFinderTagInfos,
            process.ca15PFSDJetsCHSpfBoostedDoubleSVTagInfos,
            process.ca15PFSDJetsCHSpfBoostedDoubleSecondaryVertexBJetTags,
            process.ca15PFSDJetsCHSpatFatjet,
            process.ca15PFSDJetsCHSFatjetOrdered,
            process.ca15PFSDJetsCHSNSubjettiness,
            process.SDFatjetsWithUserData,
            process.finalSDFatjets,
            process.#Softdrop beta = 1, zcut = 0.2
            process.ca15PFSoftdrop2JetsCHS,
            process.ca15PFSoftdrop2JetsCHSImpactParameterTagInfos,
            process.ca15PFSoftdrop2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos,
            process.ca15PFSoftdrop2JetsCHSpfDeepCSVInfos,
            process.ca15PFSoftdrop2JetsCHSpfCombinedInclusiveSecondaryVertexV2BJetTags,
            process.jetCorrFactorsSD2,
            process.ca15PFSoftdrop2JetsCHSpatSubJets,
            process.ca15PFSoftdrop2JetsCHSSubjetsOrdered,
            process.#Softdrop bbtag , nsubjettiness
            process.ca15PFSoftdrop2JetsCHSNoSub,
            process.ca15PFSD2JetsCHSImpactParameterTagInfos,
            process.ca15PFSD2JetsCHSpfInclusiveSecondaryVertexFinderTagInfos,
            process.ca15PFSD2JetsCHSpfBoostedDoubleSVTagInfos,
            process.ca15PFSD2JetsCHSpfBoostedDoubleSecondaryVertexBJetTags,
            process.ca15PFSD2JetsCHSpatFatjet,
            process.ca15PFSD2JetsCHSFatjetOrdered,
            process.ca15PFSD2JetsCHSNSubjettiness,
            process.SD2FatjetsWithUserData,
            process.finalSD2Fatjets
            )


    process.boostedTables = cms.Task(
            process.HTTV2Table,
            process.HTTV2InfoTable,
            process.HTTV2SubjetsTable,
            process.ca15Table,
            process.FatjetBBTagTable,
            process.ca15SoftDropTable,
            process.SDFatjetBBTagTable,
            process.ca15SoftDropSubjetsTable,
            process.ca15SoftDrop2Table,
            process.SD2FatjetBBTagTable,
            process.ca15SoftDrop2SubjetsTable
    )

    process.boostedMC = cms.Task(
            process.selectedHadronsAndPartons,
            process.jetFlavourInfosHTTV2PFJets,
            process.HTTSubjetFlavourTable,
            process.genParticlesforHTT,
            process.genHTT,
            process.genHTTV2Table,
            process.genHTTV2SubjetTable
            )

    if path is None: process.schedule.associate(process.customizedAK8Task)
    else: getattr(process, path).associate(process.customizedAK8Task)
