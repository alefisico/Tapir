import json, copy, os, imp, multiprocessing, sys
import sparse, ROOT
import logging
import subprocess

def hadd_files(analysis, indir, outdir):
    #split the big dictionary to category-based dictionaries
    #produce the event counts per category
    logging.getLogger('MergeCatFiles').info("main: hadding files")

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    process = subprocess.Popen(
        "cp -r {1}/* {0}/".format(outdir, indir),
        shell=True,
        stdout=subprocess.PIPE
    )

    process.communicate()


    cat_names = list(set([cat.name for cat in analysis.categories]))

    for cat_name in cat_names:

        process = subprocess.Popen(
            "hadd {0}/{1}.root {0}/{1}/*/*.root".format(outdir, cat_name),
            shell=True,
            stdout=subprocess.PIPE
        )


    analysis.serialize("{0}/analysis.pickle".format(outdir))

def move_shape_files(analysis, indir, outdir):

    logging.getLogger('MergeCatFiles').info("main: move shape files")

    process = subprocess.Popen(
        "mv {0}/*/*/*.txt {0}/".format(outdir),
        shell=True,
        stdout=subprocess.PIPE
    )

    process = subprocess.Popen(
        "mv {0}/*/*/*.root {0}/".format(outdir),
        shell=True,
        stdout=subprocess.PIPE
    )



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    import argparse
    parser = argparse.ArgumentParser(
        description='Merge files from "MakeCategory'
    )
    parser.add_argument(
        '--indir',
        action = "store",
        help = "Input root file",
        type = str,
        required = True
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Analysis configuration",
        type = str,
        required = True
    )

    parser.add_argument(
        '--outdir',
        action = "store",
        help = "per-analsyis output directory (will be created)",
        default = "./categories/"
    )

    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    args = parser.parse_args()
    analysis = analysisFromConfig(args.config)

    hadd_files(analysis, args.indir, args.outdir)
    move_shape_files(analysis, args.indir, args.outdir)
