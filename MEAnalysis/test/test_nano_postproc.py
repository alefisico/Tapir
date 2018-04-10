import sys, logging, os
from TTH.MEAnalysis.nano_postproc import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis tests')
    parser.add_argument(
        '--sample',
        action="store",
        help="Sample to process",
        required=True,
    )
    parser.add_argument(
        '--analysis_cfg',
        action="store",
        help="Analysis cfg (eg. MEAnalysis/data/default.cfg)",
        required=False,
        default=os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/default.cfg"
    )
    args = parser.parse_args(sys.argv[1:])
    
    analysis = analysisFromConfig(args.analysis_cfg)
    
    samples = {
        sample.name: sample for sample in analysis.samples
    }
    sample = samples[args.sample] 

    files = sample.file_names_step1[:1]

    #replace local SE access with remote SE access
    files = [fi.replace("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/", "root://t3se.psi.ch//") for fi in files]
    main(outdir="./", _input=files)

