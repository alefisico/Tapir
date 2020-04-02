from __future__ import print_function
import sys
import os, glob
import rhalphalib as rl
import numpy as np
import scipy.stats
from array import array
import pickle
import ROOT
import json, argparse
import CMS_lumi as CMS_lumi
import tdrstyle as tdrstyle
from DrawHistogram import jsonToTH1
from datasets import dictSamples

rl.util.install_roofit_helpers()
rl.ParametericSample.PreferRooParametricHist = False

selection = 'test'

########################################
def load_from_json(sample, ptStart, ptStop, msd_start_idx, msd_stop_idx, region, obs):
  '''Danieles load from json '''
  #filepath = '/afs/cern.ch/work/d/druini/public/hepaccelerate/results/'+selection+'/out_'+sample+'.json'
  filepath = '/eos/home-a/algomez/tmpFiles/hepacc/results/v02/out_'+sample+'.json'
  #filepath = 'out_'+sample+'.json'
  with open(filepath) as json_file:
    data = json.load(json_file)
    data = data['hist_leadAK8JetMass_2J2WdeltaRTau21_'+region+'_pt%sto%s' % (ptStart, ptStop)]
  assert( np.all(np.array(obs.binning)==np.array(data['edges'])[msd_start_idx:msd_stop_idx+1]) )
  return(np.array(data['contents'])[msd_start_idx:msd_stop_idx], obs.binning, obs.name)

########################################
def mergeJsons( bkgFiles, signalFiles, folder, minMass, maxMass, histos, rebinX, ptBins ):
    """docstring for mergeJsons"""

    dataHistos = {}
    bkgHistos = {}
    signalHistos = {}

    print('|----> Reading json files and merging')
    for ih in histos:
        tmpDataHistos = {}
        for iSamData in glob.glob(folder+'/*Single*'):
            tmpDataHistos[ iSamData.split('out_')[1].split('.json')[0] ] = jsonToTH1( iSamData, [ih] )
        for ihdata in tmpDataHistos.keys():
            try: dataHistos[ ih ].Add( tmpDataHistos[ ihdata ].Clone() )
            except (KeyError, AttributeError) as e:
                dataHistos[ ih ] = tmpDataHistos[ ihdata ].Clone()

        tmpBkgHistos = {}
        for bkgSamples in bkgFiles:
            try: tmpBkgHistos[ bkgSamples+ih ] = jsonToTH1( folder+'/out_'+bkgSamples+'.json', [ih] )
            except IOError:
                print('Sample missing: ', bkgSamples)
                bkgFiles.remove( bkgSamples )
                continue
        for ihbkg in tmpBkgHistos.keys():
            try: bkgHistos[ ih ].Add( tmpBkgHistos[ ihbkg ].Clone() )
            except (KeyError, AttributeError) as e:
                bkgHistos[ ih ] = tmpBkgHistos[ ihbkg ].Clone()

        tmpSignalHistos = {}
        for sigSamples in signalFiles:
            try: tmpSignalHistos[ sigSamples+ih ] = jsonToTH1( folder+'/out_'+sigSamples+'.json', [ih] )
            except IOError:
                print('Sample missing: ', sigSamples)
                signalFiles.remove( sigSamples )
                continue
        for ihsig in tmpSignalHistos.keys():
            try: signalHistos[ ih ].Add( tmpSignalHistos[ ihsig ].Clone() )
            except (KeyError, AttributeError) as e:
                signalHistos[ ih ] = tmpSignalHistos[ ihsig ].Clone()

    return mergePtBinsAndCreateArrays( dataHistos, ptBins, rebinX, minMass, maxMass ), mergePtBinsAndCreateArrays( bkgHistos, ptBins, rebinX, minMass, maxMass ), mergePtBinsAndCreateArrays( signalHistos, ptBins, rebinX, minMass, maxMass )


def mergePtBinsAndCreateArrays( dictHistos, ptBins, reBin, minMass, maxMass ):
    """helper to merge pt bins and create arrays"""

    print('|----> Merging ptbins, rebinning, making new histos with different ranges')
    for pts in ptBins:
        for ih in dictHistos.keys():
            if ih.endswith(tuple(pts[1:])):
                dictHistos[ ih.split('_pt')[0]+'_pt'+pts[0] ].Add( dictHistos[ih].Clone() )
                dictHistos.pop( ih, None )

    finalDictHistos = {}
    for ih in dictHistos.keys():
        dictHistos[ih] = dictHistos[ih].Rebin( reBin )

        newTotalBin = (maxMass-minMass)/dictHistos[ih].GetBinWidth(1)
        dictHistos[ 'New_'+ih ] = ROOT.TH1F( 'msd', ih, int(newTotalBin), minMass, maxMass )
        for ibin in range(1, dictHistos[ih].GetNbinsX()+1):
            for jbin in range(1, dictHistos['New_'+ih].GetNbinsX()+1):
                if (dictHistos[ih].GetXaxis().GetBinLowEdge(ibin)== dictHistos['New_'+ih].GetXaxis().GetBinLowEdge(jbin)):
                    dictHistos['New_'+ih].SetBinContent( jbin, dictHistos[ih].GetBinContent(ibin) )
                    dictHistos['New_'+ih].SetBinError( jbin, dictHistos[ih].GetBinError(ibin) )

        binCont = []
        binErr = []
        for ibin in range(1,dictHistos['New_'+ih].GetNbinsX()):
            binCont.append( dictHistos['New_'+ih].GetBinContent(ibin) )
            binErr.append( dictHistos['New_'+ih].GetBinError(ibin) )
        finalDictHistos[ ih.split('21_')[1].split('to')[0] ] = [ dictHistos['New_'+ih], binCont, binErr ]

    return finalDictHistos



########################################
def buildRhalphabet( dataHistos, bkgHistos, signalHistos, tmpdir, polyDeg, msd_start, msd_stop, ptBins):
    ''' Build rhalphabet '''

    print('|----> Plotting inputs as cross checks')
    for ihbkg in bkgHistos:
        can = ROOT.TCanvas('can'+ihbkg, 'can'+ihbkg, 750, 500)
        bkgHistos[ihbkg][0].Draw()
        can.SaveAs('Plots/Rhalphabet_checks_'+ihbkg+'.png')


    throwPoisson = False
    jec = rl.NuisanceParameter('CMS_jec', 'lnN')
    massScale = rl.NuisanceParameter('CMS_msdScale', 'shape')
    lumi = rl.NuisanceParameter('CMS_lumi', 'lnN')
    tqqeffSF = rl.IndependentParameter('tqqeffSF', 1., 0, 10)
    tqqnormSF = rl.IndependentParameter('tqqnormSF', 1., 0, 10)

    #ptbins = np.array([450, 500, 550, 600, 675, 800, 1200])
    #ptbins = np.append( np.arange(250,600,50), [600, 675, 800, 1200] )
    #ptbins = np.array([250,300,450,1200])
    ptbins = np.array(ptBins+[1500])
    npt = len(ptbins) - 1
    #msdbins = np.linspace(0,300,21)
    msdbins = np.linspace( dataHistos[ next(iter(dataHistos)) ][0].GetBinLowEdge(1), dataHistos[ next(iter(dataHistos)) ][0].GetXaxis().GetXmax(), dataHistos[ next(iter(dataHistos)) ][0].GetNbinsX()+1 )
    msd_start_idx = np.where(msdbins==msd_start)[0][0]
    msd_stop_idx  = np.where(msdbins==msd_stop)[0][0]
    msdbins = msdbins[msd_start_idx:msd_stop_idx+1]
    msd = rl.Observable('msd', msdbins)

    # here we derive these all at once with 2D array
    ptpts, msdpts = np.meshgrid(ptbins[:-1] + 0.3 * np.diff(ptbins), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    rhopts = 2*np.log(msdpts/ptpts)
    ptscaled = (ptpts - ptbins[0]) / (ptbins[-1] - ptbins[0])
    #import pdb
    #pdb.set_trace()
    rho_start = -6
    rho_stop  = -.55#-1.6
    rhoscaled = (rhopts - rho_start) / (rho_stop - rho_start)
    validbins = (rhoscaled >= 0) & (rhoscaled <= 1)
    rhoscaled[~validbins] = 1  # we will mask these out later

    # Build qcd MC pass+fail model and fit to polynomial
    qcdmodel = rl.Model("qcdmodel")
    qcdpass, qcdfail = 0., 0.
    for ptbin in range(npt):

        failCh = rl.Channel("ptbin%d%s" % (ptbin, 'fail'))
        passCh = rl.Channel("ptbin%d%s" % (ptbin, 'pass'))
        qcdmodel.addChannel(failCh)
        qcdmodel.addChannel(passCh)
        #failTempl = load_from_json('background', ptbins[ptbin], ptbins[ptbin+1], msd_start_idx, msd_stop_idx, 'Fail', msd)
        #passTempl = load_from_json('background', ptbins[ptbin], ptbins[ptbin+1], msd_start_idx, msd_stop_idx, 'Pass', msd)
        failTempl = bkgHistos['Fail_pt'+str(ptbins[ptbin])][0] #[1][msd_start_idx:msd_stop_idx]
        passTempl = bkgHistos['Pass_pt'+str(ptbins[ptbin])][0] #[1][msd_start_idx:msd_stop_idx]
        failCh.setObservation(failTempl)
        passCh.setObservation(passTempl)
        qcdfail += failCh.getObservation().sum()
        qcdpass += passCh.getObservation().sum()

    qcdeff = qcdpass / qcdfail
    tf_MCtempl = rl.BernsteinPoly("tf_MCtempl", (polyDeg, polyDeg), ['pt', 'rho'], limits=(-50, 50))
    tf_MCtempl_params = qcdeff * tf_MCtempl(ptscaled, rhoscaled)
    for ptbin in range(npt):
        failCh = qcdmodel['ptbin%dfail' % ptbin]
        passCh = qcdmodel['ptbin%dpass' % ptbin]
        failObs = failCh.getObservation()
        qcdparams = np.array([rl.IndependentParameter('qcdparam_ptbin%d_msdbin%d' % (ptbin, i), 0) for i in range(msd.nbins)])
        sigmascale = 10.
        scaledparams = failObs * (1 + sigmascale/np.maximum(1., np.sqrt(failObs)))**qcdparams
        fail_qcd = rl.ParametericSample('ptbin%dfail_qcd' % ptbin, rl.Sample.BACKGROUND, msd, scaledparams)
        failCh.addSample(fail_qcd)
        pass_qcd = rl.TransferFactorSample('ptbin%dpass_qcd' % ptbin, rl.Sample.BACKGROUND, tf_MCtempl_params[ptbin, :], fail_qcd)
        passCh.addSample(pass_qcd)

        failCh.mask = validbins[ptbin]
        passCh.mask = validbins[ptbin]

    qcdfit_ws = ROOT.RooWorkspace('qcdfit_ws')
    simpdf, obs = qcdmodel.renderRoofit(qcdfit_ws)
    qcdfit = simpdf.fitTo(obs,
                          ROOT.RooFit.Extended(True),       ### Extended: because the TF is an extended pdf (always True)
                          ROOT.RooFit.SumW2Error(True),     ### SumW2Error: improved error calculation for weighted unbinned likelihood fits.
                          ROOT.RooFit.Strategy(2),
                          ROOT.RooFit.Save(),
                          ROOT.RooFit.Minimizer('Minuit2', 'migrad'),
                          #ROOT.RooFit.PrintLevel(-1),
                          )
    qcdfit_ws.add(qcdfit)
    if "pytest" not in sys.modules:
         qcdfit_ws.writeToFile(os.path.join(str(tmpdir), 'ttHbb_qcdfit.root'))
    if qcdfit.status() != 0:
        raise RuntimeError('Could not fit qcd')

    param_names = [p.name for p in tf_MCtempl.parameters.reshape(-1)]
    decoVector = rl.DecorrelatedNuisanceVector.fromRooFitResult(tf_MCtempl.name + '_deco', qcdfit, param_names)
    tf_MCtempl.parameters = decoVector.correlated_params.reshape(tf_MCtempl.parameters.shape)
    tf_MCtempl_params_final = tf_MCtempl(ptscaled, rhoscaled)
    tf_dataResidual = rl.BernsteinPoly("tf_dataResidual", (2, 2), ['pt', 'rho'], limits=(-20, 20))
    tf_dataResidual_params = tf_dataResidual(ptscaled, rhoscaled)
    tf_params = qcdeff * tf_MCtempl_params_final * tf_dataResidual_params

    # build actual fit model now
    model = rl.Model("ttHbb")

    for ptbin in range(npt):
        for region in ['Pass', 'Fail']:
            ch = rl.Channel("ptbin%d%s" % (ptbin, region))
            model.addChannel(ch)

            templates = {
                #'signal'     : load_from_json('signal', ptbins[ptbin], ptbins[ptbin+1], msd_start_idx, msd_stop_idx, region, msd),
                #'background' : load_from_json('background', ptbins[ptbin], ptbins[ptbin+1], msd_start_idx, msd_stop_idx, region, msd),
                'signal'      : signalHistos[region+'_pt'+str(ptbins[ptbin])][0],
            }
            # some mock expectations
            templ = templates['signal']
            stype = rl.Sample.SIGNAL
            sample = rl.TemplateSample(ch.name + '_signal', stype, templ)

#            # mock systematics
#            jecup_ratio = np.random.normal(loc=1, scale=0.05, size=msd.nbins)
#            msdUp = np.linspace(0.9, 1.1, msd.nbins)
#            msdDn = np.linspace(1.2, 0.8, msd.nbins)
#
#            # for jec we set lnN prior, shape will automatically be converted to norm systematic
#            sample.setParamEffect(jec, jecup_ratio)
#            sample.setParamEffect(massScale, msdUp, msdDn)
#            sample.setParamEffect(lumi, 1.027)

            ch.addSample(sample)

            #yields = sum(tpl[0] for tpl in templates.values())
            #data_obs = (yields, msd.binning, msd.name)
            data_obs = bkgHistos[region+'_pt'+str(ptbins[ptbin])][0]
            ch.setObservation(data_obs)

            # drop bins outside rho validity
            mask = validbins[ptbin]
            # blind bins 11, 12, 13
            # mask[11:14] = False
            ch.mask = mask

    for ptbin in range(npt):
        failCh = model['ptbin%dFail' % ptbin]
        passCh = model['ptbin%dPass' % ptbin]

        qcdparams = np.array([rl.IndependentParameter('qcdparam_ptbin%d_msdbin%d' % (ptbin, i), 0) for i in range(msd.nbins)])
        initial_qcd = failCh.getObservation().astype(float)  # was integer, and numpy complained about subtracting float from it
        for sample in failCh:
            initial_qcd -= sample.getExpectation(nominal=True)
        if np.any(initial_qcd < 0.):
            raise ValueError("initial_qcd negative for some bins..", initial_qcd)
        sigmascale = 10  # to scale the deviation from initial
        scaledparams = initial_qcd * (1 + sigmascale/np.maximum(1., np.sqrt(initial_qcd)))**qcdparams
        fail_qcd = rl.ParametericSample('ptbin%dFail_qcd' % ptbin, rl.Sample.BACKGROUND, msd, scaledparams)
        failCh.addSample(fail_qcd)
        pass_qcd = rl.TransferFactorSample('ptbin%dPass_qcd' % ptbin, rl.Sample.BACKGROUND, tf_params[ptbin, :], fail_qcd)
        passCh.addSample(pass_qcd)

        #tqqpass = passCh['tqq']
        #tqqfail = failCh['tqq']
        #tqqPF = tqqpass.getExpectation(nominal=True).sum() / tqqfail.getExpectation(nominal=True).sum()
        #tqqpass.setParamEffect(tqqeffSF, 1*tqqeffSF)
        #tqqfail.setParamEffect(tqqeffSF, (1 - tqqeffSF) * tqqPF + 1)
        #tqqpass.setParamEffect(tqqnormSF, 1*tqqnormSF)
        #tqqfail.setParamEffect(tqqnormSF, 1*tqqnormSF)

    with open(os.path.join(str(tmpdir), 'RhalphabetResults/ttHbb.pkl'), "wb") as fout:
        pickle.dump(model, fout)

    model.renderCombine(os.path.join(str(tmpdir), 'RhalphabetResults/'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proc', action='store', default='1D', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
    parser.add_argument('-v', '--version', action='store', default='v0', help='Version: v01, v02.' )
    parser.add_argument('-y', '--year', action='store', default='2017', help='Year: 2016, 2017, 2018.' )
    parser.add_argument('-c', '--cut', action='store', nargs='+', default='2J2WdeltaR', help='cut, example: "2J 2J2W"' )
    parser.add_argument('-l', '--lumi', action='store', type=float, default=41530., help='Luminosity, example: 1.' )
    parser.add_argument('-e', '--ext', action='store', default='png', help='Extension of plots.' )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if not os.path.exists('Plots/'): os.makedirs('Plots/')
    if args.year.endswith('2016'): args.lumi = 35920.
    elif args.year.endswith('2017'): args.lumi = 41530.
    elif args.year.endswith('2018'): args.lumi = 59740.
    CMS_lumi.extraText = "Preliminary"
    CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 2 ) )+" fb^{-1}, 13 TeV, "+args.year

    VER = args.version.split('_')[1] if '_' in args.version else args.version
    bkgSamples = list(dictSamples.keys())
    bkgSamples.remove( 'ttHTobb' )
    bkgSamples.remove( 'THW' )
    sigSamples = [ 'ttHTobb', 'THW' ]
    folder = '/eos/home-a/algomez/tmpFiles/hepacc/results/'+args.version+'/'+args.year+'/'
    histos = [ 'hist_leadAK8JetMass_2J2WdeltaRTau21_'+region+'_pt'+pt for region in ['Pass', 'Fail'] for pt in [ '250to300', '300to350', '350to400', '400to450', '450to500', '550to600', '600to675', '675to800', '800to1200' ] ]
    ptBins = [ ['250to300'], [ '300to350', '350to400', '400to450' ], [ '450to500', '550to600',  '600to675', '675to800', '800to1200' ]  ]
    #ptBins = [ ['250to300'], [ '300to350', '350to400', '400to450', '450to500', '550to600',  '600to675', '675to800', '800to1200' ]  ]
    #ptBins = [ [  '250to300', '300to350', '350to400', '400to450', '450to500', '550to600',  '600to675', '675to800', '800to1200' ]  ]

    msd_start = 100
    msd_stop  = 160
    polyDeg   = 2
    dataHistos, bkgHistos, signalHistos = mergeJsons( bkgSamples, sigSamples, folder, msd_start, msd_stop, histos, 1, ptBins )
    buildRhalphabet( dataHistos, bkgHistos, signalHistos, os.getcwd(), polyDeg, msd_start, msd_stop, [ int(x[0].split('to')[0]) for x in ptBins  ])

    ''' from Daniele
    folder = 'ttH_'+selection
    if not os.path.exists(folder):
        os.mkdir(folder)
    for polyDeg in range(2,16):
      try:
        print('trying deg '+str(polyDeg))
        test_rhalphabet(folder, polyDeg)
      except:
        with open('scan_polyDeg_fitRange%d_%d_STXSbins.txt' %(msd_start, msd_stop),'a') as f:
          f.write('Degree '+str(polyDeg)+' failed\n')
    '''
