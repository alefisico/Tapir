import os
import pickle
import math
import ROOT
import random

print "Imported basics"

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from TTH.Plotting.joosep.plotlib import *

print "Imported plotlib"

import pandas
import pandas.core.common as com
from pandas.core.index import Index
from pandas.tools import plotting
from pandas.tools.plotting import scatter_matrix
import root_numpy
import numpy as np

print "Imported numpy"

import sklearn
from sklearn import preprocessing
from sklearn.tree  import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler  
from sklearn.svm import SVC
from sklearn.metrics import log_loss, classification_report, roc_auc_score,roc_curve, auc
from sklearn import cross_validation
from sklearn import grid_search
from sklearn.learning_curve import learning_curve


print "Imported sklearn"

#################################################
#Define helper functions
#################################################


########################################
# Helper: datagen
########################################

def new_class(c):

    if c == 0:
        return 0
    elif c == 1:
        return 1

def datagen(sel, brs, infname, n_chunks=10):

    f = ROOT.TFile.Open(infname, "READ")
    entries = f.Get("t2").GetEntries()
    f.Close()

    # Initialize
    step = entries/n_chunks
    i_start = 0

    # Generate data forever
    while True:
        
        d = root_numpy.root2array(infname, treename="t2", branches=brs, selection = sel, start=i_start, stop = i_start + step)

        i_start += step

        # roll over
        if i_start + step >= entries:
            i_start = 0
            
        df = pandas.DataFrame(d)
         

        df["fromtop_new"] = df.apply(lambda x:new_class(x["fromtop"]),axis=1)


        # Shuffle
        df = df.iloc[np.random.permutation(len(df))]
                
        yield df


class Classifier:
    def __init__(self,
                 name,
                 backend,
                 params,
                 load_from_file,
                 datagen_train,
                 datagen_test,
                 model,
                 image_fun,
                 class_names,
                 inpath = ".",
                 plot_name = "",                 
                 input_vars = [],
             ):
        self.name = name
        self.backend = backend
        self.params = params
        self.load_from_file = load_from_file
        self.datagen_train = datagen_train
        self.datagen_test  = datagen_test
        self.model = model
        self.image_fun = image_fun
        self.inpath = inpath
        
        self.class_names = class_names
        self.classes = sorted(class_names.keys())
        
        if plot_name:
            self.plot_name = plot_name
        else:
            self.plot_name = name

        self.input_vars = input_vars

    def prepare(self):

        if not self.load_from_file:
            if self.backend == "scikit":
                train_scikit(self)
            elif self.backend == "keras":
                train_keras(self)
        else:
            if self.backend == "scikit":
                f = open(os.path.join(self.inpath,self.name + ".pickle"), "r")
                self.model = pickle.load(f)
                f.close()
                                
            elif self.backend == "keras":
                f = open(os.path.join(self.inpath,self.name + ".yaml"), "r")
                yaml_string = f.read()
                f.close()
                self.model = model_from_yaml(yaml_string)                
                self.model.load_weights(os.path.join(self.inpath,self.name + "_weights.h5"))
            print "Loading", self.name, "from file: Done..."

########################################
# Helper: train_scitkit
########################################

def train_scikit(clf):

    print "Starting train_scikit on {} with the parameters: ".format(clf.name)
    for k,v in clf.params.iteritems():
        print "\t", k,"=",v
      
    df = clf.datagen_train.next()
    X = clf.image_fun(df)
    y = df["fromtop_new"].values
            
    tmp_weight_dic = df["fromtop_new"].value_counts().to_dict()    
    weight_dic = {}
    for k,v in tmp_weight_dic.iteritems():
        weight_dic[k] = float(len(X))/v 
    weights = np.vectorize(weight_dic.get)(y)
    
    clf.model.fit(X, y, sample_weight=weights)

    f = open(clf.name + ".pickle","wb")
    pickle.dump(clf.model, f)
    f.close()

########################################
# Helper: rocplot
########################################

def rocplot(clf, 
            df):
    
    sig_class = 2
    #prob = "proba_{0}".format(1)
    prob = "mass".format(1)


    plt.clf()
    plt.yscale('log')

    orig_names = {0: "Other", 
                  1: "Top",}


    bkg_class = 0
        
    nbins = 100
    min_prob = min(df[prob])
    max_prob = max(df[prob])

    print min_prob, max_prob
    print "data",df.loc[df["fromtop"] == sig_class,prob]

    if min_prob >= max_prob:
        max_prob = 1.1 * abs(min_prob)




    # Signal 
    h1 = make_df_hist((nbins*200,min_prob,max_prob), df.loc[df["fromtop"] == sig_class,prob])

    # Background
    h2 = make_df_hist((nbins*200,min_prob,max_prob), df.loc[df["fromtop"] == bkg_class,prob])    

    # And turn into ROC
    r, e = calc_roc(h1, h2)

    plt.plot(r[:, 0], 1/r[:, 1], 
             lw=1, 
             ls="--",                 
             label = "BLR vs {0}".format(orig_names[bkg_class])
         )
        
    plt.plot( [0.1088], [1/0.0309], ls = 'None', marker = "o",color='black',  label =  "4tag vs ttb")
    plt.plot( [0.1088], [1/0.0374], ls = 'None', marker = "^", color='black', label = "4tag vs tt2b") 
    plt.plot( [0.1088], [1/0.0140], ls = 'None', marker = "v", color='black', label = "4tag vs ttcc")
    plt.plot( [0.1088], [1/0.0025], ls = 'None', marker = "s", color='black', label = "4tag vs ttll") 

    plt.plot( [0.0577], [1/0.0115], ls = 'None', marker = "o",color='black',  fillstyle = 'full', label = "4tag, highBLR vs ttb")
    plt.plot( [0.0577], [1/0.0157], ls = 'None', marker = "^", color='black', fillstyle = 'full', label = "4tag, highBLR vs tt2b") 
    plt.plot( [0.0577], [1/0.0025], ls = 'None', marker = "v", color='black', fillstyle = 'full', label = "4tag, highBLR vs ttcc")
    plt.plot( [0.0577], [1/0.0003], ls = 'None', marker = "s", color='black', fillstyle = 'full', label = "4tag, highBLR vs ttll") 

         
    # Setup nicely
    plt.legend(loc=2)
    plt.xlabel( "signal match efficiency", fontsize=16)
    plt.ylabel("1/fake match efficiency", fontsize=16)
    plt.legend(loc=2)
    plt.xlim(0,1)
    plt.ylim(1,1000000)

    plt.legend(loc=1)

    plt.show()
    plt.savefig(clf.name + "-ROC.png")

def plot_distributions(data1, data2, column=None, grid=True,
                      xlabelsize=None, xrot=None, ylabelsize=None,
                      yrot=None, ax=None, sharex=False,
                      sharey=False, figsize=None,
                      layout=None, bins=10, **kwds):

    """Draw histogram of the DataFrame's series comparing the distribution
    in `data1` to `data2`.
    
    data1: DataFrame
    data2: DataFrame
    column: string or sequence
        If passed, will be used to limit data to a subset of columns
    grid : boolean, default True
        Whether to show axis grid lines
    xlabelsize : int, default None
        If specified changes the x-axis label size
    xrot : float, default None
        rotation of x axis labels
    ylabelsize : int, default None
        If specified changes the y-axis label size
    yrot : float, default None
        rotation of y axis labels
    ax : matplotlib axes object, default None
    sharex : bool, if True, the X axis will be shared amongst all subplots.
    sharey : bool, if True, the Y axis will be shared amongst all subplots.
    figsize : tuple
        The size of the figure to create in inches by default
    layout: (optional) a tuple (rows, columns) for the layout of the histograms
    bins: integer, default 10
        Number of histogram bins to be used
    kwds : other plotting keyword arguments
        To be passed to hist function
    """
        
    if 'alpha' not in kwds:
        kwds['alpha'] = 0.5

    if column is not None:
        if not isinstance(column, (list, np.ndarray, Index)):
            column = [column]
        data1 = data1[column]
        data2 = data2[column]
        
    data1 = data1._get_numeric_data()
    data2 = data2._get_numeric_data()
    naxes = len(data1.columns)

    fig, axes = plotting._subplots(naxes=naxes, ax=ax, squeeze=False,
                                   sharex=sharex,
                                   sharey=sharey,
                                   figsize=figsize,
                                   layout=layout)
    _axes = plotting._flatten(axes)

    for i, col in enumerate(com._try_sort(data1.columns)):
        ax = _axes[i]
        low = min(data1[col].min(), data2[col].min())
        high = max(data1[col].max(), data2[col].max())
        ax.hist(data1[col].dropna().values,
                bins=bins, range=(low,high), label = "Top", **kwds)
        ax.hist(data2[col].dropna().values,
                bins=bins, range=(low,high), label = "Other", **kwds)
        ax.set_title(col)
        ax.grid(grid)

    plotting._set_ticks_props(axes, xlabelsize=xlabelsize, xrot=xrot,
                              ylabelsize=ylabelsize, yrot=yrot)
    fig.subplots_adjust(wspace=0.3, hspace=0.7)

    fig.savefig("BDTVariables.png")
    fig.clf()


def correlations(data, name,**kwds):
    """Calculate pairwise correlation between features.
    
    Extra arguments are passed on to DataFrame.corr()
    """
    # simply call df.corr() to get a table of
    # correlation values if you do not need
    # the fancy plotting
    corrmat = data.corr(**kwds)

    fig, ax1 = plt.subplots(ncols=1, figsize=(6,5))
    
    opts = {'cmap': plt.get_cmap("RdBu"),
            'vmin': -1, 'vmax': +1}
    heatmap1 = ax1.pcolor(corrmat, **opts)
    plt.colorbar(heatmap1, ax=ax1)

    ax1.set_title("Correlations")

    labels = corrmat.columns.values
    for ax in (ax1,):
        # shift location of ticks to center of the bins
        ax.set_xticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_yticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_xticklabels(labels, minor=False, ha='right', rotation=70)
        ax.set_yticklabels(labels, minor=False)
        
    #plt.tight_layout()
    fig.savefig("Correlations_{}.png".format(name))
    fig.clf()
    plt.clf()

def calc_cutbased(fil,var,cutpointsmin,cutpointsmax):
	esig = []
	ebkg = []

	ntotS = 0
	ntotB = 0
	npassS = [0] * 1000
	npassB = [0] * 1000

	f = ROOT.TFile.Open(fil, "READ")
	ttree = f.Get("t2")
	for ev in ttree:
		passes = {}
		for v in var:
			passes[v] = []


		for v in var:
			ind = var.index(v)
			for imin in cutpointsmin[v]:
				for imax in cutpointsmax[v]:
					if getattr(ev,v)<imin or getattr(ev,v)>imax:
						passes[v].append(0)
					else:
						passes[v].append(1)

		maxlength = 0
		for v in var:
			if len(passes[v])>maxlength:
				maxlength = len(passes[v])

		for v in var:
			while len(passes[v])<maxlength:
				passes[v].append(-1)

		position = 0
		for i in range(maxlength):
			for j in range(maxlength):
				for k in range(maxlength):
					if passes[var[0]][i] == 1 and passes[var[1]][j] == 1 and passes[var[2]][k] == 1:
						if ev.fromtop == 1:
							npassS[position]+= 1
						if ev.fromtop == 0:
							npassB[position]+= 1
					if passes[var[0]][i] == -1 or passes[var[1]][j] == -1 or passes[var[2]][k] == -1:
						pass
					else:
						position += 1

		if ev.fromtop==1:
			ntotS += 1
		if ev.fromtop==0:
			ntotB += 1

	f.Close()

	#		position = 0
	#	for i in range(maxlength):
	#		for j in range(maxlength):
	#			for k in range(maxlength):
	#				for l in range(maxlength):
	#					for m in range(maxlength):
	#						for n in range(maxlength):
	#							for o in range(maxlength):
	#								for p in range(maxlength):
	#									if passes[var[0]][i] == 1 and passes[var[1]][j] == 1 and passes[var[2]][k] == 1 and passes[var[3]][l] == 1 and passes[var[4]][m] == 1 and passes[var[5]][n] == 1 and passes[var[6]][o] == 1 and passes[var[7]][p] == 1:
	#										if ev.fromhiggs == 1:
	#											npassS[position]+= 1
	#										if ev.fromhiggs == 0:
	#											npassB[position]+= 1
	#									if passes[var[0]][i] == -1 or passes[var[1]][j] == -1 or passes[var[2]][k] == -1 or passes[var[3]][l] == -1 or passes[var[4]][m] == -1 or passes[var[5]][n] == -1 or passes[var[6]][o] == -1 or passes[var[7]][p] == -1:
	#										pass
	#									else:
	#										position += 1



	for i in range(len(npassS)):
		if npassS[i] > 0 and npassB[i]>0:
			esig.append(float(npassS[i])/ntotS)
			ebkg.append(float(npassB[i])/ntotB)

	return esig,ebkg


def roccurve(clf,X_test,y_test,esig,ebkg):
    decisions = clf.model.decision_function(X_test)
    
    # Compute ROC curve and area under the curve    
    fpr, tpr, thresholds = roc_curve(y_test, decisions)
    print fpr
    print tpr
    print thresholds
    
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)'%(roc_auc))
    plt.plot(ebkg,esig,linestyle='None',marker='8', color='g', label='Cut based')
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6))
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.grid()
    plt.savefig("ROC_{}.png".format(clf.name))
    plt.clf()


def compare_train_test(clf, X_train, y_train, X_test, y_test, bins=30):
    decisions = []
    for X,y in ((X_train, y_train), (X_test, y_test)):
        d1 = clf.model.decision_function(X[y>0.5]).ravel()
        d2 = clf.model.decision_function(X[y<0.5]).ravel()
        decisions += [d1, d2]
        
    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)
    
    plt.hist(decisions[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='S (train)')
    plt.hist(decisions[1],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='B (train)')

    hist, bins = np.histogram(decisions[2],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')
    
    hist, bins = np.histogram(decisions[3],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

    plt.xlabel("BDT output")
    plt.ylabel("Arbitrary units")
    plt.legend(loc='best')
    plt.savefig("DecisionFunction_{}.png".format(clf.name))
    plt.clf()

def optimize_hyperparameters(param_grid,clf,X_dev,y_dev,X_eval,y_eval):


    gs = grid_search.GridSearchCV(clf.model,
                               param_grid,
                               cv=3,
                               scoring='roc_auc',
                               n_jobs=8)

    _ = gs.fit(X_dev, y_dev) 


    print "Best parameter set found on development set:"
    print
    print gs.best_estimator_
    print
    print "Grid scores on a subset of the development set:"
    print
    for params, mean_score, scores in gs.grid_scores_:
        print "%0.4f (+/-%0.04f) for %r"%(mean_score, scores.std(), params)
    print
    print "With the model trained on the full development set:"

    y_true, y_pred = y_dev, gs.decision_function(X_dev)
    print "  It scores %0.4f on the full development set"%roc_auc_score(y_true, y_pred)
    y_true, y_pred = y_eval, gs.decision_function(X_eval)
    print "  It scores %0.4f on the full evaluation set"%roc_auc_score(y_true, y_pred)

def validation_curve(clf, X_train, y_train, X_test, y_test):
    
    test_score = np.empty(len(clf.model.estimators_))
    train_score = np.empty(len(clf.model.estimators_))

    for i, pred in enumerate(clf.model.staged_decision_function(X_test)):
        test_score[i] = 1-roc_auc_score(y_test, pred)

    for i, pred in enumerate(clf.model.staged_decision_function(X_train)):
        train_score[i] = 1-roc_auc_score(y_train, pred)

    best_iter = np.argmin(test_score)
    #learn = clf.model.get_params()['learning_rate']
    #depth = clf.model.get_params()['max_depth']
    test_line = plt.plot(test_score, label = "test")

    colour = test_line[-1].get_color()
    plt.plot(train_score, '--', color=colour, label= "train")
    
    plt.xlabel("Number of boosting iterations")
    plt.ylabel("1 - area under ROC")
    plt.axvline(x=best_iter, color=colour)
    
    plt.legend(loc='best')
    plt.savefig("ValidationCurve_{}.png".format(clf.name))
    plt.clf()

def loss_function(clf, X_train, y_train, X_test, y_test):

    test_score = np.zeros((clf.model.n_estimators, ), dtype=np.float64)
    train_score = np.zeros((clf.model.n_estimators, ), dtype=np.float64)

    for i, pred in enumerate(clf.model.staged_decision_function(X_test)):
        test_score[i] = clf.model.loss_(y_test, pred)

    for j, y_pred in enumerate(clf.model.staged_decision_function(X_train)):
        train_score[j] = clf.model.loss_(y_train, y_pred)

    best_iter = np.argmin(test_score)
    #learn = clf.model.get_params()['learning_rate']
    #depth = clf.model.get_params()['max_depth']
    test_line = plt.plot(test_score, label = "test")

    colour = test_line[-1].get_color()
    plt.plot(train_score, '--', color=colour, label= "train")
    
    plt.xlabel("Number of boosting iterations")
    plt.ylabel("Loss")
    plt.axvline(x=best_iter, color=colour)
    
    plt.legend(loc='best')
    plt.savefig("LossFunction_{}.png".format(clf.name))
    plt.clf()

def plot_learning_curve(estimator, title, X, y, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5),
                        scoring=None, ax=None, xlabel=True):
    if ax is None:
        plt.figure()
        ax.title(title)
    
    if xlabel:
        ax.set_xlabel("Training examples")
        
    ax.set_ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(estimator,
                                                            X, y,
                                                            cv=cv,
                                                            n_jobs=n_jobs,
                                                            train_sizes=train_sizes,
                                                            scoring=scoring)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    ax.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    ax.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    ax.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    ax.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    ax.set_ylim([0.65, 1.0])
    return plt

def analyze(clf,param_grid,esig,ebkg):

    # Get the data
    # We need test and train as we want to plat to evolution as well
    print "Get train sample"
    df_train = clf.datagen_train.next()            
    print "Get test sample"
    df_test  = clf.datagen_test.next()    

    bg = df_test.fromtop < 0.5
    sig = df_test.fromtop > 0.5
    correlations(df_test[bg].drop(['fromtop',"fromtop_new"], 1),"bkg")
    correlations(df_test[sig].drop(['fromtop',"fromtop_new"], 1),"sig")        

    # Evaluate models
    print "Eval test"
    X_test = clf.image_fun(df_test)
    df_test["output"] = clf.model.predict(X_test)
    
    for ic in clf.classes:
        df_test["proba_{0}".format(ic)] = 0
    df_test[["proba_{0}".format(ic) for ic in clf.classes]] = clf.model.predict_proba(X_test)

    print "Eval train"
    X_train = clf.image_fun(df_train)
    df_train["output"] = clf.model.predict(X_train)

    for ic in clf.classes:
        df_train["proba_{0}".format(ic)] = 0
    df_train[["proba_{0}".format(ic) for ic in clf.classes]] = clf.model.predict_proba(X_train)

    # Plot signal and background distributions for some
    # variables
    # The first two arguments select what is "signal"
    # and what is "background". This means you can
    # use it for more general comparisons of two
    # subsets as well.

    """plot_distributions(df_test[df_test.fromtop<0.5], df_test[df_test.fromtop>0.5],
                      column=["mass",
                              "nsub2",
                              #"nsub2",
                              #"ptdr",
                              #"nsj"],
                              "frec",
                              "btags",
                              "btagf"],
                      bins=40)"""


    y_test = df_test["fromtop_new"].values
    y_train = df_train["fromtop_new"].values
    roccurve(clf,X_test,y_test,esig,ebkg)

    compare_train_test(clf, X_train, y_train, X_test, y_test)

    #optimize_hyperparameters(param_grid,clf,X_train,y_train,X_test,y_test)

    validation_curve(clf,X_train,y_train,X_test,y_test)

    loss_function(clf,X_train,y_train,X_test,y_test)

    classifiers = [clf.model,clf.model]  

    fig, axes = plt.subplots(nrows=len(classifiers), sharex=True)    
    
    for c, ax in zip(classifiers, axes):  
        plot_learning_curve(c,
               "Learning curves",
               X_train, y_train,
               scoring='roc_auc',
               n_jobs=7, cv=4,
               ax=ax, xlabel=False)
       
    axes[0].legend(loc="best")
    axes[-1].set_xlabel("Training examples")
    fig.savefig("LearningCurve_{}.png".format(clf.name))
    fig.clf()



    # Generate the training weight dictionary 
    # (using weights derived on testing sample would be cheating)            

    tmp_weight_dic = df_train["fromtop_new"].value_counts().to_dict()    
    weight_dic = {}
    for k,v in tmp_weight_dic.iteritems():
        weight_dic[k] = float(len(X_train))/v 

    # and apply to both samples
    weights_train = np.vectorize(weight_dic.get)(df_train["fromtop_new"].values)
    weights_test  = np.vectorize(weight_dic.get)(df_test["fromtop_new"].values)

    # Generate category matrix
    matrix = np.zeros((len(clf.classes),len(clf.classes)))
    for true_class in clf.classes:        
        num = float( len(df_test.loc[ (df_test["fromtop_new"] == true_class),"fromtop"]))
        for found_class in clf.classes:            
            matrix[true_class][found_class] = len(df_test.loc[ (df_test["fromtop_new"] == true_class) & (df_test["output"] == found_class),"fromtop"])/num
            
    # Plot the category matrix
    fig, ax = plt.subplots()
    min_val, max_val, diff = 0., float(len(clf.classes)), 1.

    #imshow portion
    ax.imshow(matrix, 
              interpolation='nearest',
              cmap=plt.get_cmap("summer")
    )

    print matrix

    #text portion
    ind_array = np.arange(min_val, max_val, diff)
    x, y = np.meshgrid(ind_array, ind_array)

    for x_val, y_val in zip(x.flatten(), y.flatten()):
        x_pos = int(x_val)
        y_pos = int(y_val)
        print x_val, y_val
        c = "{0:.2f}".format(matrix[int(y_val), int(x_val)])
        ax.text(x_val, y_val, c, va='center', ha='center')

    ax.set_xticks(clf.classes)
    ax.set_yticks(clf.classes)
    ax.set_xticklabels( [clf.class_names[c] for c in clf.classes])
    ax.set_yticklabels( [clf.class_names[c] for c in clf.classes])

    ax.text(0.6, -0.1, 'Reco Class',
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='black', fontsize=15)

    ax.text(-0.1, 0.6, 'True \n Class',
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='black', fontsize=15)

    plt.show()
    plt.savefig("matrix.png")
    
    features = sorted(zip(clf.input_vars, clf.model.feature_importances_), key = lambda x:x[1])    
    for f in features:
        print "{0: <15}: {1:.4f}".format(f[0],f[1])



    #rocplot(clf, df_test)

    # Plot different reco probaility distribtiuons for each true class
    for true_class in clf.classes:

        plt.clf()

        min_prob = min([min( df_test.loc[ df_test["fromtop_new"] == true_class, "proba_{0}".format(reco_class) ]) for reco_class in clf.classes])
        max_prob = max([max( df_test.loc[ df_test["fromtop_new"] == true_class, "proba_{0}".format(reco_class) ]) for reco_class in clf.classes])

        colors = ['black', 'red','blue','green','orange','green','magenta']

        for reco_class in clf.classes:
            
            # Test Sample
            prob = df_test.loc[ df_test["fromtop_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="{0} proba (Test)".format(clf.class_names[reco_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls="-",
                     color = colors[reco_class],
                     normed=True)

            # Train Sample
            prob = df_train.loc[ df_train["fromtop_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="{0} proba (Train)".format(clf.class_names[reco_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls=':', 
                     color = colors[reco_class],
                     normed=True)

            plt.title("True {0} Events".format(clf.class_names[true_class]))
            plt.xlabel("Probability", fontsize=16)
            plt.ylabel("Events", fontsize=16)        
            plt.legend(loc=1)
            plt.xlim(min_prob,max_prob)
            plt.show()
            plt.savefig("{0}_probas.png".format(clf.class_names[true_class]))


    # Plot different classfiers outputs for all true classes
    for reco_class in clf.classes:

        plt.clf()

        min_prob = min(df_test[  "proba_{0}".format(reco_class) ]) 
        max_prob = max(df_test[  "proba_{0}".format(reco_class) ])

        colors = ['black', 'red','blue','green','orange','green','magenta']

        for true_class in clf.classes:
            
            # Test Sample
            prob = df_test.loc[ df_test["fromtop_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="True {0} (Test)".format(clf.class_names[true_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls="-",
                     color = colors[true_class],
                     normed=True)

            # Train Sample
            prob = df_train.loc[ df_train["fromtop_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="True {0} (Train)".format(clf.class_names[true_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls=':', 
                     color = colors[true_class],
                     normed=True)

        plt.title("{0} Classifier".format(clf.class_names[reco_class]))
        plt.xlabel("Probability", fontsize=16)
        plt.ylabel("Events", fontsize=16)        
        plt.legend(loc=1)
        plt.xlim(min_prob,max_prob)
        plt.show()
        plt.savefig("{0}_classifier.png".format(clf.class_names[reco_class]))

    
    # Loss function/time    
    
#    print "Calculating test scores for all iterations. Samples:", len(X_test)
#    predictor_test  = clf.model.staged_predict(X_test)	
#    predictor_test_proba  = clf.model.staged_predict_proba(X_test)	
#
#    test_scores  = [log_loss(df_test["tt_class_new"], 
#                             predictor_test_proba.next(), 
#                             normalize = True,
#                             sample_weight=weights_test) for _ in range(clf.params["n_estimators"])]
#
#    print "Calculating train scores for all iterations. Samples:", len(X_train)
#    predictor_train  = clf.model.staged_predict(X_train)	
#    predictor_train_proba  = clf.model.staged_predict_proba(X_train)	
#    train_scores  = [log_loss(df_train["tt_class_new"], 
#                              predictor_train_proba.next(), 
#                              normalize = True,
#                              sample_weight=weights_train) for _ in range(clf.params["n_estimators"])]
#
#    print "Last Train:", train_scores[-1]
#    print "Last Test:",  test_scores[-1]
#
#    plt.clf()
#
#    plt.plot(train_scores, label="Train", color = 'blue')
#    plt.plot(test_scores, label="Test", color = 'red')
#
#    plt.title('Cross Entropy', fontsize=16)
#    plt.xlabel('Iterations', fontsize=16)
#    plt.ylabel('Score', fontsize=16)
#    plt.grid(False)
#    plt.legend(loc=0)
#    plt.show()
#    plt.savefig("score.png")

    



########################################
# Data access helpers
########################################

def get_data_vars(df, varlist):        
    return df[varlist].values

def get_data_flatten(df, varlist):
    
    # tmp is a 1d-array of 1d-arrays
    # so we need to convert it to 2d array
    tmp = df[varlist].values.flatten() # 
    ret = np.vstack([tmp[i] for i in xrange(len(tmp))])
     
    return ret 
