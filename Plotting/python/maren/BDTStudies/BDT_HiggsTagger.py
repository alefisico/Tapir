import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import pandas
import root_numpy
from matplotlib.colors import LogNorm

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import log_loss

import os
import pickle
import math
import ROOT


#################################################
#Define helper functions
#################################################

def make_sclearn_arrays(files):

	a = []
	b = []

	for l in files:
		f = ROOT.TFile.Open(l, "READ")
		ttree = f.Get("t2")
		for ev in ttree:
			inter = [ev.mass,ev.nsub,ev.bbtag,ev.btagf,ev.btags]
			a.append(inter)
			b.append(ev.fromhiggs)
		f.Close()

	return a,b


def new_class(c):

    if c == 0:
        return 0
    elif c == 1:
        return 1

def datagen(sel, brs, infname, n_chunks=10):

    brs2 = brs.append("fromhiggs")

    f = ROOT.TFile.Open(infname, "READ")
    entries = f.Get("t2").GetEntries()
    f.Close()

    # Initialize
    step = entries/n_chunks
    i_start = 0

    # Generate data forever
    while True:
        
        d = root_numpy.root2array(infname, treename="t2", branches=brs2, selection = sel, start=i_start, stop = i_start + step)

        i_start += step

        # roll over
        if i_start + step >= entries:
            i_start = 0
            
        df = pandas.DataFrame(d)
         

        df["fromhiggs_new"] = df.apply(lambda x:new_class(x["fromhiggs"]),axis=1)


        # Shuffle
        df = df.iloc[np.random.permutation(len(df))]
                
        yield df

def make_decision_boundaries(bdt,anp,bnp,name):
	plot_colors = "br"
	plot_step = 0.02
	class_names = "OH"
	plt.figure(figsize=(5, 5))
	x_min, x_max = anp[:, 0].min() - 1, anp[:, 0].max() + 1
	y_min, y_max = anp[:, 1].min() - 1, anp[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
	                     np.arange(y_min, y_max, plot_step))

	Z = bdt.predict(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)
	cs = plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
	plt.axis("tight")

	# Plot the training points
	for i, n, c in zip(range(2), class_names, plot_colors):
	    idx = np.where(bnp == i)
	    plt.scatter(anp[idx, 0], anp[idx, 1],
	                c=c, cmap=plt.cm.Paired,
	                s=20, edgecolor='k',
	                label="%s" % n)
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)
	plt.legend(loc='upper right')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('Decision Boundary')

	plt.tight_layout()
	plt.show()
	plt.savefig("{}BDT_Decision_Boundary_{}.png".format(output_dir,name))

def make_decision_score(bdt,anp,bnp,name):
	plot_colors = "br"
	plot_step = 0.02
	class_names = "OH"
	plt.figure(figsize=(5, 5))
	twoclass_output = bdt.decision_function(anp)
	plot_range = (twoclass_output.min(), twoclass_output.max())
	for i, n, c in zip(range(2), class_names, plot_colors):
	    plt.hist(twoclass_output[bnp == i],
	             bins=10,
	             range=plot_range,
	             facecolor=c,
	             label='Class %s' % n,
	             alpha=.5,
	             edgecolor='k')
	x1, x2, y1, y2 = plt.axis()
	plt.axis((x1, x2, y1, y2 * 1.2))
	plt.legend(loc='upper right')
	plt.ylabel('Samples')
	plt.xlabel('Score')
	plt.title('Decision Scores')

	plt.tight_layout()
	plt.show()
	plt.savefig("{}BDT_Decision_Score_{}.png".format(output_dir,name))

def calc_roc(h1, h2, rebin=1):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Rebin(rebin)
    h2.Rebin(rebin)

    roc = np.zeros((h1.GetNbinsX()+2, 2))
    e1 = ROOT.Double(0)
    e2 = ROOT.Double(0)


    rc = ROOT.TGraph(h1.GetNbinsX()+2)
    for i in range(0, h1.GetNbinsX()+2):
        I1 = h1.Integral(0, h1.GetNbinsX()+2)
        I2 = h2.Integral(0, h2.GetNbinsX()+2)
        if I1>0 and I2>0:
            esig = float(h1.Integral(i, h1.GetNbinsX()+2)) / I1
            ebkg = float(h2.Integral(i, h2.GetNbinsX()+2)) / I2
            rc.SetPoint(i,esig,ebkg)
    rc.SetPoint(h1.GetNbinsX()+3,0,0)
    return rc

def calc_cutbased(files,var,cutpointsmin,cutpointsmax):
	esig = []
	ebkg = []

	ntotS = 0
	ntotB = 0
	npassS = [0] * 1000
	npassB = [0] * 1000

	"""for v in var:
		npassS[v] = {}
		npassB[v] = {}
		for imin in cutpointsmin[v]:
			npassS[v][imin] = {}
			npassB[v][imin] = {}
			for imax in cutpointsmax[v]:
				npassS[v][imin][imax] = 0
				npassB[v][imin][imax] = 0
 	
	for l in files:
		f = ROOT.TFile.Open(l, "READ")
		ttree = f.Get("t2")
		for ev in ttree:
			passes = {}
			for v in var:
				passes[v] = {}
				for imin in cutpointsmin[v]:
					passes[v][imin] = {}
					for imax in cutpointsmax[v]:
						passes[v][imin][imax] = 1

			for v in var:
				ind = var.index(v)
				for imin in cutpointsmin[v]:
					for imax in cutpointsmax[v]:
						if getattr(ev,v)<imin or getattr(ev,v)>imax:
							passes[v][imin][imax] = 0

			for v in var:
				for imin in cutpointsmin[v]:
					for imax in cutpointsmax[v]:
						if passes[v][imin][imax] == 1:
							if ev.fromhiggs==1:
								npassS[v][imin][imax] += 1
							if ev.fromhiggs==0:
								npassB[v][imin][imax] += 1

			for v in var:

			if ev.fromhiggs==1:
				ntotS += 1
			if ev.fromhiggs==0:
				ntotB += 1

		f.Close()"""


	for l in files:
		f = ROOT.TFile.Open(l, "READ")
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
						for l in range(maxlength):
							for m in range(maxlength):
								if passes[var[0]][i] == 1 and passes[var[1]][j] == 1 and passes[var[2]][k] == 1 and passes[var[3]][l] == 1 and passes[var[4]][m] == 1:
									if ev.fromhiggs == 1:
										npassS[position]+= 1
									if ev.fromhiggs == 0:
										npassB[position]+= 1
								if passes[var[0]][i] == -1 or passes[var[1]][j] == -1 or passes[var[2]][k] == -1 or passes[var[3]][l] == -1 or passes[var[4]][m] == -1:
									pass
								else:
									position += 1

			#print position


			if ev.fromhiggs==1:
				ntotS += 1
			if ev.fromhiggs==0:
				ntotB += 1

		f.Close()


	for i in range(len(npassS)):
		if npassS[i] > 0 and npassB[i]>0:
			esig.append(float(npassS[i])/ntotS)
			ebkg.append(float(npassB[i])/ntotB)

	return esig,ebkg

def make_roc(bdt,anp,bnp,filesTest,var,cutpointsmin,cutpointsmax,name = ""):

	li_colors = [ROOT.kRed,ROOT.kBlue+1,ROOT.kBlack,ROOT.kOrange-1,ROOT.kViolet+1,ROOT.kGreen+1,
        ROOT.kGray,ROOT.kYellow]*10 

	bdtscoreS = ROOT.TH1F("Signal","Signal",300,-1,1)
	bdtscoreB = ROOT.TH1F("Bkg","Bkg",300,-1,1)

	res2 = bdt.predict_proba(anp)
	print res2
	res = bdt.decision_function(anp)
	print res
	for i in range(len(res)):
		if bnpt[i] == 0:
			bdtscoreB.Fill(res2[i][1])
		elif bnpt[i] == 1:
			bdtscoreS.Fill(res2[i][1])

	rocs = {}
	names = ["BDT"]
	rocs["BDT"] = calc_roc(bdtscoreS,bdtscoreB)

	esig,ebkg = calc_cutbased(filesTest,var,cutpointsmin,cutpointsmax)

	rc = ROOT.TGraph(len(esig))
	for i in range(len(esig)):
		rc.SetPoint(i,esig[i],ebkg[i])

	rc.SetMarkerSize(1.2)
	rc.SetMarkerColor(ROOT.kGreen+1)
	rc.SetMarkerStyle(20)


	mu = ROOT.TMultiGraph()

	for k in rocs.keys():
	    rocs[k].SetLineColor(li_colors[rocs.keys().index(k)])
	    rocs[k].SetLineWidth(2)
	    mu.Add(rocs[k])
	c = ROOT.TCanvas("c","c",600,600)
	c.SetLeftMargin(0.16)
	mu.Draw("ALP")
	mu.GetXaxis().SetTitle("Signal efficiency")
	mu.GetYaxis().SetTitle("Background efficiency")
	mu.GetXaxis().SetLimits(0,1)
	mu.GetYaxis().SetTitleOffset(1.2)
	mu.GetYaxis().SetRangeUser(0,1)
	legend = ROOT.TLegend(0.2,0.65,0.7,0.85)
	for k in names:
	    legend.AddEntry(rocs[k],"{}, AOC = {:0.2f}".format(k, 0.5-rocs[k].Integral()),"l")
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	legend.Draw()
	line = ROOT.TLine(0,0,1,1)
	line.Draw()
	rc.Draw("P")
	c.Print("./{}ROCCurve_HiggsBDT_{}.pdf".format(output_dir,name))
	c.Print("./{}ROCCurve_HiggsBDT_{}.png".format(output_dir,name))





#################################################
#Define parameters
#################################################

var = ["mass", "nsub", "bbtag", "btagf", "btags"]

#Cut based discriminator: Mass, Nsub, bbtag, btagF, btagS
#To be generalized for more points
cutpointsmin = {}
cutpointsmax = {}
cutpointsmin["mass"] = [-1,100]
cutpointsmin["nsub"] = [0]
cutpointsmin["bbtag"] = [-1,0.6]
cutpointsmin["btagf"] = [0.6,0.97]
cutpointsmin["btags"] = [-2,0.6]
cutpointsmax["mass"] = [600]
cutpointsmax["nsub"] = [0.7,0.9]
cutpointsmax["bbtag"] = [1]
cutpointsmax["btagf"] = [1]
cutpointsmax["btags"] = [1]


output_dir = "results/HiggsStudiesBDT_20171212/"

nestimators = 200


#Training/Test file + get np arrays
full_file_names = {}
full_file_names["Training"] = "./HiggsTaggerBDT_Cuts.root"
full_file_names["Test"] = "./HiggsTaggerBDT_Cuts_TestSample.root"

filesTraining = [full_file_names[x] for x in full_file_names.keys() if "Training" in x]
a,b = make_sclearn_arrays(filesTraining)
anp = np.array(a)
bnp = np.array(b)


filesTest = [full_file_names[x] for x in full_file_names.keys() if "Test" in x]
at,bt = make_sclearn_arrays(filesTest)
anpt = np.array(at)
bnpt = np.array(bt)


#################################################
#Train classifier
#################################################
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                         algorithm="SAMME",
                         n_estimators=nestimators)
bdt.fit(anp,bnp)


f = open("BDT.pickle","wb")
pickle.dump(bdt, f)
f.close()

# Plot the decision boundaries - Only for two variables in the BDT
# make_decision_boundaries(bdt,anp,bnp,"Training")

# Plot the two-class decision scores
make_decision_score(bdt,anp,bnp,"Training")



#################################################
#Test classifier
#################################################

#Decision scores
make_decision_score(bdt,anpt,bnpt,"Test")

#ROC curve
make_roc(bdt,anpt,bnpt,filesTest,var,cutpointsmin,cutpointsmax)


# Loss function/time    



print "Calculating test scores for all iterations. Samples:", len(anpt)

predictor_test_proba  = bdt.staged_decision_function(anpt)

test_scores  = [log_loss(bnpt, 
                         predictor_test_proba.next(), 
                         normalize = True,
                         sample_weight=None) for _ in range(nestimators)]

print "Calculating train scores for all iterations. Samples:", len(anp)

#predictor_train_proba  = bdt.staged_predict_proba(anp)
predictor_train_proba  = bdt.staged_decision_function(anp)

train_scores  = [log_loss(bnp, 
                          predictor_train_proba.next(), 
                          normalize = True,
                          sample_weight=None) for _ in range(nestimators)]

print "Last Train:", train_scores[-1]
print "Last Test:",  test_scores[-1]

print "Score", bdt.score(anpt,bnpt)

plt.clf()

plt.plot(train_scores, label="Train", color = 'blue')
plt.plot(test_scores, label="Test", color = 'red')

plt.title('Loss function', fontsize=16)
plt.xlabel('Iterations', fontsize=16)
plt.ylabel('Score', fontsize=16)
plt.grid(False)
plt.legend(loc=0)
plt.show()
plt.savefig("score.png")
