########################################
# Imports
########################################

import imp, os, sys, time
import subprocess

from CombineHelper import LimitGetter, ConstraintGetter

from EnvForCombine import PATH, LD_LIBRARY_PATH, PYTHONPATH

import logging

########################################
# Actual work
########################################

LOG_MODULE_NAME = logging.getLogger(__name__)

def main(
        workdir,
        analysis,
        group = None,
        runToys = False,
        runSignalInjection = False,
        runPulls = False
):
    
    limits = {}

    # Decide what to run on
    if group:
        groups = [group]
    #Run on all groups
    else:
        groups = analysis.groups.keys()

    # Prepare the limit getter
    lg = LimitGetter(workdir)

    constraint_getter = ConstraintGetter(workdir)

    limits = {}
    for group_name in groups:

        group = [x for x in analysis.groups[group_name] if x.do_limit]

        LOG_MODULE_NAME.info("running limit on group={0}".format(group))
        
        LOG_MODULE_NAME.info("Doing group={0} consisting of N={1} categories".format(group_name, len(group))) 

        # Get all the per-category datacards and use combineCards to merge into one "group datacard"
        input_dcard_names = ["shapes_{0}.txt".format(c.full_name) for c in group]
        add_dcard_command = ["combineCards.py"] + input_dcard_names 

        LOG_MODULE_NAME.debug("running combineCards.py command: " + " ".join(add_dcard_command))
        

        process = subprocess.Popen(add_dcard_command, 
                                   stdout=subprocess.PIPE, 
                                   cwd=workdir,
                                   #env=dict(os.environ, 
                                   #         PATH=PATH,
                                   #         LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                   #         PYTHONPATH=PYTHONPATH
                                   #     )
            )

        group_dcard, stderr = process.communicate()
        if process.returncode != 0:
            LOG_MODULE_NAME.error("Error running combineCards.py: " + stderr)
            raise Exception("Could not run combineCards command")
        LOG_MODULE_NAME.info("Finished with group_card making")

        # Write the group datacard to a file
        group_dcard_filename = os.path.join(workdir, "shapes_group_{0}.txt".format(group_name))
        group_dcard_file = open(group_dcard_filename, "w")
        group_dcard_file.write(group_dcard)
        group_dcard_file.close()

        LOG_MODULE_NAME.info("Written to file {0}, running limit setting".format(group_dcard_filename))

        # And run limit setting on it
        limits[group_name] = lg(group_dcard_filename)[0][2]
        
        if runSignalInjection:
            limits[group_name + "_lims"] = lg(group_dcard_filename)[0]
            limits[group_name + "_siginject"] = lg.runSignalInjection(group_dcard_filename)
        
        if runPulls:
            #write constraints
            for sig in [1, 0]:
                #Run Asimov constraints
                constraints = constraint_getter(group_dcard_filename, sig)
                of = open(workdir + "/constraints_{0}_sig{1}_asimov.txt".format(group_name, sig), "w")
                of.write(constraints)
                of.close()
              
                if runToys:
                    #Run constraints with toys
                    constraints = constraint_getter(group_dcard_filename, sig, False)
                    of = open(workdir + "/constraints_{0}_sig{1}.txt".format(group_name, sig), "w")
                    of.write(constraints)
                    of.close()

    # End loop over groups

    # End of loop over analyses
    return limits
    
if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
    
    import argparse
    parser = argparse.ArgumentParser(
        description='Runs the workflow'
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Path to analysis pickle file",
        type = str,
        required = True
    )
    parser.add_argument(
        '--category',
        action = "store",
        help = "Fit category",
        type = str,
    )
    parser.add_argument(
        '--runToys',
        action = "store_true",
        help = "Run toy experiments for pull distributions",
    )
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG
    )
    analysis = Analysis.deserialize(args.config)
    workdir = os.path.dirname(args.analysis) + "/limits"

    if not args.category:
        print "choose a category:", sorted(analysis.groups.keys())
    else:
        print analysis.groups.keys()
        main(workdir, analysis, args.category, args.runToys)
