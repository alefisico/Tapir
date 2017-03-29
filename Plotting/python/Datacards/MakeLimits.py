########################################
# Imports
########################################

import imp, os, sys
import subprocess

from CombineHelper import LimitGetter, ConstraintGetter

from EnvForCombine import PATH, LD_LIBRARY_PATH, PYTHONPATH

print "MakeLimits.py called from cwd={0}".format(os.getcwd())


########################################
# Actual work
########################################

def main(
        workdir,
        analysis,
        group
):
    
    limits = {}

    # Decide what to run on
    if group:
        groups = [group]
    else:
        groups = analysis.groups.keys()

    # Prepare the limit getter
    lg = LimitGetter(workdir)

    constraint_getter = ConstraintGetter(workdir)

    limits = {}
    for group_name in groups:

        group = [x for x in analysis.groups[group_name] if x.do_limit]

        print "running limit on", group
        
        print "Doing {0} consisting of {1} categories".format(group_name, len(group))    

        # Get all the per-category datacards and use combineCards to merge into one "group datacard"
        input_dcard_names = ["shapes_{0}.txt".format(c.full_name) for c in group]
        add_dcard_command = ["combineCards.py"] + input_dcard_names 

        print "running combineCards.py"
        print " ".join(add_dcard_command)

        process = subprocess.Popen(add_dcard_command, 
                                   stdout=subprocess.PIPE, 
                                   cwd=workdir,
                                   env=dict(os.environ, 
                                            PATH=PATH,
                                            LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                            PYTHONPATH=PYTHONPATH
                                        ))

        group_dcard, stderr = process.communicate()
        if process.returncode != 0:
            print "Error running combineCards.py"
            print stderr
            raise Exception("Could not run combineCards command")
        print "Finished with group_card making"

        # Write the group datacard to a file
        group_dcard_filename = os.path.join(workdir, "shapes_group_{0}.txt".format(group_name))
        group_dcard_file = open(group_dcard_filename, "w")
        group_dcard_file.write(group_dcard)
        group_dcard_file.close()

        print "Written to file, running limit setting"

        # And run limit setting on it
        limits[group_name] = lg(group_dcard_filename)[0][2]

        #write constraints
        for sig in [1, 0]:
            constraints = constraint_getter(group_dcard_filename, sig)
            of = open(workdir + "/contraints_{0}_sig{1}.txt".format(group_name, sig), "w")
            of.write(constraints)
            of.close()

    # End loop over groups

    # End of loop over analyses
    return limits


#if __name__ == "__main__":
#
#    if not len(sys.argv) in [3,4,5]:
#        print "Wrong number of arguments"
#        print "Usage: "
#        print "{0} datacard_file.py workdir [analysis_to_process [group to_process]]".format(sys.argv[0])
#        sys.exit()
#
#    dcard_path = sys.argv[1]
#
#    # Get the input/output directory
#    workdir = sys.argv[2]
#
#    if len(sys.argv) >= 4:
#        analysis_arg = sys.argv[3]
#    else:
#        analysis_arg = ""
#
#    if len(sys.argv) == 5:
#        group_arg = sys.argv[4]
#    else:
#        group_arg = ""
#
#    main(dcard_path, workdir, analysis_arg, group_arg)
