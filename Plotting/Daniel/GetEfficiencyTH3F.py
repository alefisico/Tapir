import ROOT
import copy

def THNFtoTH1F(histo3D):
    nx = histo3D.GetNbinsX()
    ny = histo3D.GetNbinsY()
    nz = histo3D.GetNbinsZ()
    if histo3D.GetDimension() == 1:
        nbins = (nx+2) 
    elif histo3D.GetDimension() == 2:
        nbins = (nx+2)*(ny+2) 
    elif histo3D.GetDimension() == 3:
        nbins = (nx+2)*(ny+2)*(nz+2) 
    else:
        print("EROR dimension", histo3D.GetDimension())
    histo1D = ROOT.TH1F("histo1D","",nbins-2,0,nbins-2)
    histo1D.Sumw2()
    if histo3D.fN != histo1D.fN:
        print("histo3D.fN",histo3D.fN)
        print("histo1D.fN",histo1D.fN)
        print("must be identical!")
    for i in range(histo1D.fN):
        histo1D.GetSumw2()[i] = histo3D.GetSumw2()[i]
        histo1D.GetArray()[i] = histo3D.GetArray()[i]
        #print(i,histo1D.GetSumw2()[i])
    return copy.copy(histo1D)

def TH1FtoTHNF(histo1D,histo3D):
    if histo3D.fN != histo1D.fN:
        print("histo3D.fN",histo3D.fN)
        print("histo1D.fN",histo1D.fN)
        print("must be identical!")
        return
    for i in range(histo1D.fN):
        histo3D.GetSumw2()[i] = histo1D.GetSumw2()[i]
        histo3D.GetArray()[i] = histo1D.GetArray()[i]
    return copy.copy(histo3D)

def reFillTH3F(histo3D):
    nZbins = histo3D.GetZaxis().GetNbins()
    nYbins = histo3D.GetYaxis().GetNbins()
    nXbins = histo3D.GetXaxis().GetNbins()
    hret = histo3D.Clone("reFilled_"+histo3D.GetName())
    hret.Reset()
    hret.Sumw2()
    print hret
    for z in range(0,nZbins+2):
        for x in range(0, nXbins+2):
            for y in range(0, nYbins+2):
                hret.SetBinContent(x,y,z,histo3D.GetBinContent(x,y,z))
                hret.SetBinError(x,y,z,histo3D.GetBinError(x,y,z))
    return copy.copy(hret)
                
                
def GetEfficiencyTHNF(num,den):

    ## Convert THNF num and den histo to TH1F
    num_1d = THNFtoTH1F(num)
    den_1d = THNFtoTH1F(den)
    
    ## Calculate the effienciency
    nbins = num_1d.GetNbinsX()
    eff = ROOT.TEfficiency(num_1d,den_1d);

    ## Convert TEffiency in TH1F
    eff_1d = num_1d.Clone("eff")
    eff_1d.Reset()
    for i in range(nbins+2):
        #print "setting",i,"to",eff.GetEfficiency(i),"+-",(eff.GetEfficiencyErrorUp(i)+eff.GetEfficiencyErrorLow(i))/2,"(",eff.GetEfficiencyErrorUp(i),"+",eff.GetEfficiencyErrorLow(i),")"
        eff_1d.SetBinContent(i,eff.GetEfficiency(i))
        if eff.GetEfficiency(i) != 0:
            eff_1d.SetBinError(i,(eff.GetEfficiencyErrorUp(i)+eff.GetEfficiencyErrorLow(i))/2)
    print("Done")
    
    ## Convert TH1F in THNF
    eff = den.Clone("eff_data")
    eff.Reset()
    eff = TH1FtoTHNF(eff_1d, eff)
    
    return copy.copy(eff)


if __name__ == "__main__":
    ## Generate num and den THNF histo
    xmax = 5
    ymax = 5
    zmax = 5
    num_data = ROOT.TH3F("num_data","",xmax,0,xmax,ymax,0,ymax,zmax,0,zmax)
    den_data = ROOT.TH3F("den_data","",xmax,0,xmax,ymax,0,ymax,zmax,0,zmax)

    k=1
    for i in range(1,xmax+1):
        for j in range(1,ymax+1):
            for k in range(1,zmax):
                val = i * j * k
                num_data.SetBinContent(i,j,k,5*0.5132412*(val))
                den_data.SetBinContent(i,j,k,5*0.5132412*(val))

    num_data.Sumw2()
    den_data.Sumw2()

    ## Get Efficiency
    eff_data = GetEfficiencyTHNF(num_data, den_data)
    print eff_data
    ## Plot and checks
    print("num:",num_data.GetBinContent(2,2,2))
    print("den:",den_data.GetBinContent(2,2,2))
    print("eff:",eff_data.GetBinContent(2,2,2)," +/- ", eff_data.GetBinError(2,2,2))

    print("num:",num_data.GetBinContent(4,4,4))
    print("den:",den_data.GetBinContent(4,4,4))
    print("eff:",eff_data.GetBinContent(4,4,4)," +/- ", eff_data.GetBinError(2,2,2))

    
    print("num:",num_data.GetBinContent(5,5,5))
    print("den:",den_data.GetBinContent(5,5,5))
    print("eff:",eff_data.GetBinContent(5,5,5)," +/- ", eff_data.GetBinError(5,5,5))

    c1 = ROOT.TCanvas("c1","c1",600,600)
    c1.cd()
    eff_data.Draw("LEGO")
    c1.Update()

    eff_refilled = reFillTH3F(eff_data)
    out = ROOT.TFile("out_test_thnfeff.root","RECREATE")
    eff_data.Write()
    eff_refilled.Write()
    out.Close()

    raw_input("Press ret to quit")
