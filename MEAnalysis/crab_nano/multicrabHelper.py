import json, yaml
import os

#def getDatasets(mem_cfg, script, files = ["ttH.json","ttbar.json","otherbkg.json", "QCD.json"]):
#def getDatasets(mem_cfg, script, files = ["ttH_CMSSW_9X.json","ttbar_CMSSW_9X.json","otherbkg_CMSSW_9X.json", "QCD_CMSSW_9X.json"]):
def getDatasets(mem_cfg, script, files = ["ttH_CMSSW_102X.json","ttbar_CMSSW_102X.json"]):
    pwd = os.getcwd()


    #Some Error handling for completeness
    iFiles = 0
    for filename in files:
        try:
            open(pwd+"/"+filename, 'r')
        except IOError:
            print "Dataset file not in "+pwd
            print "Removing file from file list"
            files.remove(filename)
        else:
            iFiles += 1

    if iFiles == 0:
        print "No file for MC datasets"
        answer = raw_input("Is this correct? Type y to go on: ")
        if answer != "y":
            print "Exiting!"
            exit()

    retDataSets = {}

    for filename in files:
        data = None
        with open(filename, 'r') as f:
            data = yaml.safe_load(f) #json loads all entries as unicode (u'..')
        for ds in data:
            data[ds]["mem_cfg"] = mem_cfg
            data[ds]["script"] = script
            data[ds]["json"] = ""
            data[ds]["isMC"] = True
            retDataSets[ds] = data[ds]

    return retDataSets





if __name__ == "__main__":
    print "Getting Datasets"
    datasets = getDatasets("MEAnalysis_cfg_heppy.py", "heppy_crab_script.sh")
    print "Printing datsets"
    print datasets
