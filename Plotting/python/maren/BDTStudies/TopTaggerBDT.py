########################################
# Imports
########################################

from BDTTrainingBaseTop import *


#################################################
#Define parameters
#################################################

#Branches to be loaded from file
#brs = ["mass", "nsub", "bbtag", "btagf", "btags", "fromhiggs","ptdr","nsj","nsub2"]
brs = ["mass", "massuncor", "nsub2", "frec" , "btagf", "btags", "fromtop"]

#Variables to be used in the BDT
#input_vars = ["mass", "nsub", "bbtag", "btagf", "btags","ptdr","nsj","nsub2"]
input_vars = ["mass", "nsub2", "frec"]

#Cut based discriminator: Mass, Nsub, bbtag, btagF, btagS
#To be generalized for more points
cutpointsmin = {}
cutpointsmax = {}
cutpointsmin["mass"] = [-1,50]
cutpointsmin["nsub2"] = [0]
cutpointsmin["frec"] = [0]
cutpointsmin["btagf"] = [0.6,0.97]
cutpointsmin["btags"] = [-2,0.6]

cutpointsmax["mass"] = [600]
cutpointsmax["nsub2"] = [0.7,0.9]
cutpointsmax["frec"] = [0.05,0.1]
cutpointsmax["btagf"] = [1]
cutpointsmax["btags"] = [1]


output_dir = "results/TopStudiesBDT_20180522/"

default_params = {        
	# Common parameters
	"n_chunks"          : 1,
	"n_estimators"   : 3000,
    "max_depth"      : 2, 
    "learning_rate"  : 0.05, 
    "max_leaf_nodes" : 3,   
    "subsample"      : 0.8,     
    "verbose"        : 0,    
    "samples_per_epoch" : None, # later filled from input files
}


param_grid = {"n_estimators": [1100,1200,1300],
          "max_depth": [2, 3],
          'learning_rate': [0.05,0.1]}


#Training/Test file + get np arrays
infname_train = "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_6/CMSSW_9_4_6_patch1/src/TTH/Plotting/python/maren/BDTStudies/Top_BDT_Train.root"
infname_test = "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_6/CMSSW_9_4_6_patch1/src/TTH/Plotting/python/maren/BDTStudies/Top_BDT_Test.root"

########################################
# Read in parameters
########################################

params = {}
for param in default_params.keys():

    if param in os.environ.keys():
        cls = default_params[param].__class__
        value = cls(os.environ[param])
        params[param] = value
    else:
        params[param] = default_params[param]

########################################
# Count effective training samples
########################################

# We want to know the "real" number of training samples
# This is a bit tricky as we read the file in "chunks" and then divide each chunk into "batches"
# both operations might loose a few events at the end
# So we actually do this procedure on a "cheap" branch

n_train_samples = 0 
# Loop over signal and background sample

# get the number of events in the root file so we can determine the chunk size
rf = ROOT.TFile.Open(infname_train)
entries = rf.Get("t2").GetEntries()
rf.Close()

step = entries/params["n_chunks"]    
i_start = 0

# Loop over chunks from file
for i_chunk in range(params["n_chunks"]):

    # get the samples in this chunk that survive the fiducial selection + training sample selection
    n_samples = len(root_numpy.root2array(infname_train, treename="t2", branches=["fromtop"], start=i_start, stop=i_start+step).view(np.recarray))

    # round to batch_size
    n_train_samples += n_samples
    i_start += step

print "Total number of training samples = ", n_train_samples
params["samples_per_epoch"] = n_train_samples


########################################
# Prepare data and scalers
########################################

datagen_train = datagen("(1)", brs, infname_train, n_chunks=params["n_chunks"])
datagen_test  = datagen("(1)", brs, infname_test, n_chunks=params["n_chunks"])

#esig,ebkg = calc_cutbased(infname_test,input_vars,cutpointsmin,cutpointsmax)
esig,ebkg = 0,0 

# This function produces the necessary shape for MVA training/evaluation
# (batch_size,1,40,40)
# However it uses the raw values in the image
# If we want a rescaled one, use to_image_scaled 
def to_image(df):
    return df[input_vars].values


def modelGradientBoosting(params):

    classif = GradientBoostingClassifier(
        n_estimators  = params["n_estimators"],   
        max_leaf_nodes = params["max_leaf_nodes"],      
        learning_rate = params["learning_rate"],  
        subsample     = params["subsample"],      
        verbose       = params["verbose"],        
    )

    return classif


def modelAdaBoost(params):

    classif = AdaBoostClassifier(
    	DecisionTreeClassifier(max_depth=1),
        n_estimators  = params["n_estimators"], 
        algorithm     = "SAMME",
    )

    return classif



classifiers = [
    Classifier("BDT_Top_Testing_Scaling_All", 
               "scikit",
               params,
               False,
               datagen_train,
               datagen_test,               
               modelGradientBoosting(params),
               image_fun = to_image,               
               class_names = {
                   0: "Other", 
                   1: "Top",
               },
               input_vars = input_vars
               ),  
#    Classifier("BDT_Adaboost", 
#               "scikit",
#               params,
#               False,
#               datagen_train,
#               datagen_test,               
#               modelAdaBoost(params),
#               image_fun = to_image,               
#               class_names = {
#                   0: "Other", 
#                   1: "Higgs",
#               },
#               input_vars = input_vars
#               )  
#
]




########################################
# Train/Load classifiers and analyse results
########################################

print "Training the classifiers"
[clf.prepare() for clf in classifiers]

print "Analyzing the classifiers"
[analyze(clf,param_grid,esig,ebkg) for clf in classifiers]