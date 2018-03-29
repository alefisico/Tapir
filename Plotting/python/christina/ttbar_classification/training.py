import matplotlib
matplotlib.use("Agg")
import numpy as np
import ROOT
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split 
import os
import glob
from sklearn.externals import joblib
import sys
import pandas as pd

### fast part: training
def training(fpath):

# load grid-control output
    os.chdir(fpath)

    count = 0
    for npfile in glob.glob("*_dataframe.csv"):
        filepath = os.path.join(fpath, npfile)
        print filepath
        if count == 0:
            d = pd.read_csv(filepath)
        else:
            d = d.append(pd.read_csv(filepath), ignore_index = True)
        count += 1

    os.chdir(sys.path[0])
    d.to_csv("dataframe.csv")

# divide dataframe in train and test sample
    d = d.sample(frac=1, random_state=0).reset_index(drop=True)
    nevt = d.shape[0]
    train = d[:int(nevt*0.9)]
    print train
    test = d[int(nevt*0.9):]
    print test

    train.to_csv("train.csv")
    test.to_csv("test.csv")

# get arrays as BDT input
    numJets = 6
    var = ["jets_btagCSV_" + str(x) for x in range(numJets)]
    X_train = np.array(train[var]) 
    X_test = np.array(test[var])
    X_train = np.sort(X_train) 
    X_test = np.sort(X_test)

    y_train = np.array(train["ttCls"])
    y_test = np.array(test["ttCls"])

   
# construct estimator for classification
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=0) 
    clf.fit(X_train, y_train)
    
    n_classes = clf.n_classes_
    print "number of classes:", n_classes
    print "mean score:", clf.score(X_train, y_train)
    print "feature importance:", clf.feature_importances_

# save model
    joblib.dump(clf, "classifier.pkl")

    """
    from sklearn import svm
    clf = svm.SVC()
    clf.fit(data_train, target_train)
    print clf.score(data_test, target_test)
    """
if __name__ == "__main__":

    training("/mnt/t3nfs01/data01/shome/creissel/tth/gc/bdt/GC7da410223313/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8")
