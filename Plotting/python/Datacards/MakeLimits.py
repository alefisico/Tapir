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
        group = None
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
        
        limits[group_name + "_siginject"] = lg.runSignalInjection(group_dcard_filename)

        #write constraints
        for sig in [1, 0]:
            constraints = constraint_getter(group_dcard_filename, sig)
            of = open(workdir + "/constraints_{0}_sig{1}.txt".format(group_name, sig), "w")
            of.write(constraints)
            of.flush()
            time.sleep(10)
            os.fsync(of)
            time.sleep(10)
            of.close()

    # End loop over groups

    # End of loop over analyses
    return limits


if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
    
    logging.basicConfig(
        level=logging.DEBUG
    )
    workdir = "results/2017-10-03T11-03-54-028815_2cb4de87-30f6-4098-a634-850696533ad0/limits"
    analysis = Analysis.deserialize("results/2017-10-03T11-03-54-028815_2cb4de87-30f6-4098-a634-850696533ad0/analysis.pickle")
    group = "group_sldl"

    print analysis.groups.keys()
    main(workdir, analysis, group)
