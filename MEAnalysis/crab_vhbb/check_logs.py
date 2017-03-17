#! /usr/bin/env python
import os
import subprocess
from ROOT import TH1F, TCanvas, TFile, TObject

sample = "ttHbb"
copy = 1
extract = 1
analyse = 0

se = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat//store/user/dsalerno"
lsprefix = "xrdfs storage01.lcg.cscs.ch ls -ltr -u /pnfs/lcg.cscs.ch/cms/trivcat/store/user/dsalerno/"
path = {
    # "QCD300":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193325",
    # "QCD500":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_194135",
    # "QCD700":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193622",
    # "QCD1000":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193740",
    # "QCD1500":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_194255",
    # "QCD2000":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193858",
    # "TTbar":"tth/VHBBHeppyV21_tthbbV9_v3_2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBBHeppyV21_tthbbV9_v3_2/160515_085747",
    # "ttHbb":"tth/VHBBHeppyV21_tthbbV9_v3_3/ttHTobb_M125_13TeV_powheg_pythia8/VHBBHeppyV21_tthbbV9_v3_3/160518_110721",
    # "ttHNon":"tth/VHBBHeppyV21_tthbbV9_v3_3/ttHToNonbb_M125_13TeV_powheg_pythia8/VHBBHeppyV21_tthbbV9_v3_3/160518_110839",

    "QCD300":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194235",
    "QCD500":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194354",
    "QCD700":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194510",
    "QCD1000":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194632",
    "QCD1500":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194746",
    "QCD2000":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194905",
    "TTbar":"tth/JoosepFeb_test3/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/JoosepFeb_test3/170315_103441",
    "ttHbb":"tth/JoosepFeb_2python_test1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/JoosepFeb_2python_test1/170316_152719",
}

endpath = "/scratch/dsalerno/tth/80x_M17/crab_JoosepFeb_2python_test1/" #CHOOSE HERE!!
destination = endpath+sample

if( copy ):
    listdir = lsprefix+path[sample]
    print listdir
    p = subprocess.Popen(listdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    if not os.path.exists(destination):
        os.makedirs(destination)

    for line in p.stdout.readlines():
        directory = line.split(path[sample]+"/")[1].strip()
        print "directory ", directory
        listlog = listdir+"/"+directory+"/log"
        q = subprocess.Popen(listlog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in q.stdout.readlines():
            logfile = line.split(path[sample]+"/"+directory+"/log/")[1].strip()
            #print "logfile ", logfile
            if( os.path.isfile(destination+"/"+logfile) ):
                print logfile, " already copied"
                continue
            half = logfile.split("_")[1]
            num = half.split(".")[0]
            stdoutfile = "cmsRun-stdout-"+num+".log"
            if( os.path.isfile(destination+"/"+stdoutfile) ):
                print logfile, " already extracted"
                continue
            ##copylog = "gfal-copy "+se+"/"+path[sample]+"/"+directory+"/log/"+logfile+" file://"+destination
            copylog = "xrdcp "+se+"/"+path[sample]+"/"+directory+"/log/"+logfile+" "+destination
            #print copylog
            os.system(copylog)

if( extract ):
    r = subprocess.Popen("ls "+destination, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in r.stdout.readlines():
        zipfile = line.split()[0]
        if(zipfile.find('log.tar.gz')<0):
            continue
        #print "zipfile ", zipfile
        half = zipfile.split("_")[1]
        num = half.split(".")[0]
        stdoutfile = "cmsRun-stdout-"+num+".log"
        #print "stdoutfile", stdoutfile
        if( os.path.isfile(destination+"/"+stdoutfile) ):
            print stdoutfile, " already extracted"
            continue
        unzip = "tar -C "+destination+" -zxvf "+destination+"/"+zipfile
        os.system(unzip)
    os.system("rm "+destination+"/cmsRun_*.log.tar.gz")
    os.system("rm "+destination+"/FrameworkJobReport-*.xml")   

if( analyse ):
    outf = TFile.Open(endpath+"/jobtime.root","UPDATE")
    outf.cd()
    htime_total = TH1F("htime_total","htime_total",100,0,50)
    htime_vhbb  = TH1F("htime_vhbb" ,"htime_vhbb" ,100,0,10)
    htime_mem   = TH1F("htime_mem"  ,"htime_mem"  ,100,0,50)
    hev_vhbb    = TH1F("hev_vhbb"   ,"hev_vhbb"   ,400,400,800)
    hev_mem     = TH1F("hev_mem"    ,"hev_mem"    ,200,0,200)

    h_0_7_322   = TH1F("h_0_7_322","h_0_7_322",300,0,300)
    h_0_7_122   = TH1F("h_0_7_122","h_0_7_122",300,0,300) ##
    h_0_7_421   = TH1F("h_0_7_421","h_0_7_421",300,0,300)

    h_0_8_422   = TH1F("h_0_8_422","h_0_8_422",300,0,300)    
    h_0_8_322   = TH1F("h_0_8_322","h_0_8_322",1000,0,1000)
    h_0_8_122   = TH1F("h_0_8_122","h_0_8_122",1000,0,1000) ##
    h_0_8_421   = TH1F("h_0_8_421","h_0_8_421",500,0,500)

    h_0_9_422   = TH1F("h_0_9_422","h_0_9_422",500,0,1000)
    h_0_9_322   = TH1F("h_0_9_322","h_0_9_322",500,0,500)
    h_0_9_122   = TH1F("h_0_9_122","h_0_9_122",500,0,1000) ##
    h_0_9_421   = TH1F("h_0_9_421","h_0_9_421",500,0,500)

    h_0_10_421   = TH1F("h_0_10_421","h_0_10_421",400,0,400)
    h_0_10_422   = TH1F("h_0_10_422","h_0_10_422",300,0,300)  
    h_0_10_322   = TH1F("h_0_10_322","h_0_10_322",600,0,600)

    h_0_11_421   = TH1F("h_0_11_421","h_0_11_421",300,0,300)
    h_0_11_422   = TH1F("h_0_11_422","h_0_11_422",600,0,600)
    h_0_11_322   = TH1F("h_0_11_322","h_0_11_322",300,0,300)

    h_0_12_421   = TH1F("h_0_12_421","h_0_12_421",600,0,600)
    h_0_12_422   = TH1F("h_0_12_422","h_0_12_422",600,0,600)
    h_0_12_322   = TH1F("h_0_12_322","h_0_12_322",600,0,600)
    
    h_1_7_322   = TH1F("h_1_7_322","h_1_7_322",300,0,300)
    h_1_7_122   = TH1F("h_1_7_122","h_1_7_122",300,0,300) ##
    h_1_7_421   = TH1F("h_1_7_421","h_1_7_421",300,0,300)
                       
    h_1_8_422   = TH1F("h_1_8_422","h_1_8_422",300,0,300)    
    h_1_8_322   = TH1F("h_1_8_322","h_1_8_322",1000,0,1000)
    h_1_8_122   = TH1F("h_1_8_122","h_1_8_122",1000,0,1000) ##
    h_1_8_421   = TH1F("h_1_8_421","h_1_8_421",500,0,500)
    
    h_1_9_422   = TH1F("h_1_9_422","h_1_9_422",500,0,1000)
    h_1_9_322   = TH1F("h_1_9_322","h_1_9_322",500,0,800)
    h_1_9_122   = TH1F("h_1_9_122","h_1_9_122",500,0,1000) ##
    h_1_9_421   = TH1F("h_1_9_421","h_1_9_421",500,0,500)
    
    h_1_10_421   = TH1F("h_1_10_421","h_1_10_421",1000,0,1000)
    h_1_10_422   = TH1F("h_1_10_422","h_1_10_422",300,0,300)
    h_1_10_322   = TH1F("h_1_10_322","h_1_10_322",300,0,300)

    h_1_11_421   = TH1F("h_1_11_421","h_1_11_421",300,0,300) 
    h_1_11_422   = TH1F("h_1_11_422","h_1_11_422",300,0,300)
    h_1_11_322   = TH1F("h_1_11_322","h_1_11_322",300,0,300)

    h_1_12_421   = TH1F("h_1_12_421","h_1_12_421",600,0,600)
    h_1_12_422   = TH1F("h_1_12_422","h_1_12_422",600,0,600)
    h_1_12_322   = TH1F("h_1_12_322","h_1_12_322",600,0,600)

    s = subprocess.Popen("ls "+destination, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in s.stdout.readlines():
        if(line.find('stdout') > 0):
            outfile = line.split()[0]
            #print "outfile", outfile
            f = open(destination+"/"+outfile)
            lines = f.readlines()
            hypo = -1
            cat = -1
            method = -1
            nev_vhbb =0
            nev_mem = 0
            memevent = False
            for l in lines:
                if(l.find('timeto_doVHbb') == 0):
                    time_vhbb = float(l.split()[1])/3600
                    htime_vhbb.Fill( time_vhbb )
                if(l.find('timeto_doMEM') == 0):
                    htime_mem.Fill( (float(l.split()[1]) - time_vhbb*3600)/3600 )
                if(l.find('timeto_totalJob') == 0):
                    htime_total.Fill( float(l.split()[1])/3600 )
                if(l.find('---starting EVENT') == 0):
                    nev_vhbb += 1
                    memevent = False
                if(l.find('Integrator::run started') > 0 and memevent == False ):
                    memevent = True
                    nev_mem += 1
                if(l.find('hypo=0')>0):
                    hypo = 0
                if(l.find('hypo=1')>0):
                    hypo = 1                   

                if(l.find('fh_j7_tge5')>0 or l.find('fh_j7_t4')>0):
                    cat = 7
                if(l.find('fh_j8_tge5')>0 or l.find('fh_j8_t4')>0):
                    cat = 8                    
                if(l.find('fh_jge9_tge5')>0 or l.find('fh_jge9_t4')>0):
                    cat = 9
                if(l.find('fh_j8_t3')>0 ):
                    cat = 10
                if(l.find('fh_j7_t3')>0 ):
                    cat = 11
                if(l.find('fh_jge9_t3')>0 ):
                    cat = 12

                if(l.find('conf=FH_3w2h2t')>0):
                    method = 322
                if(l.find('conf=FH_4w2h2t')>0):
                    method = 422
                if(l.find('conf=FH_4w2h1t')>0):
                    method = 421
                if(l.find('conf=FH_1w1w2h2t')>0): #not used
                    method = 122
                if(l.find('conf=FH_3w2h1t')>0): #not used
                    method = 321

                if(l.find('Job done in...............')>0):
                    half = l.split('...............')[1]
                    time = float(half.split()[0])
                    if(hypo==0):
                        if(cat==7):
                            if(method==322):
                                h_0_7_322.Fill(time)
                            if(method==122):
                                h_0_7_122.Fill(time) ##
                            if(method==421):
                                h_0_7_421.Fill(time)
                        if(cat==8):
                            if(method==422):
                                h_0_8_422.Fill(time)
                            if(method==322):
                                h_0_8_322.Fill(time)
                            if(method==122):
                                h_0_8_122.Fill(time) ##
                            if(method==421):
                                h_0_8_421.Fill(time)
                        if(cat==9):
                            if(method==422):
                                h_0_9_422.Fill(time)
                            if(method==322):
                                h_0_9_322.Fill(time)
                            if(method==122):
                                h_0_9_122.Fill(time) ##
                            if(method==421):
                                h_0_9_421.Fill(time)
                        if(cat==10):
                            if(method==421):
                                h_0_10_421.Fill(time)
                            if(method==422):
                                h_0_10_422.Fill(time)
                            if(method==322):
                                h_0_10_322.Fill(time)
                        if(cat==11):
                            if(method==421):
                                h_0_11_421.Fill(time)
                            if(method==422):
                                h_0_11_422.Fill(time)
                            if(method==322):
                                h_0_11_322.Fill(time)
                        if(cat==12):
                            if(method==421):
                                h_0_12_421.Fill(time)
                            if(method==422):
                                h_0_11_422.Fill(time)
                            if(method==322):
                                h_0_12_322.Fill(time)
                    if(hypo==1):
                        if(cat==7):
                            if(method==322):
                                h_1_7_322.Fill(time)
                            if(method==122):
                                h_1_7_122.Fill(time) ##
                            if(method==421):
                                h_1_7_421.Fill(time)
                        if(cat==8):
                            if(method==422):
                                h_1_8_422.Fill(time)
                            if(method==322):
                                h_1_8_322.Fill(time)
                            if(method==122):
                                h_1_8_122.Fill(time) ##
                            if(method==421):
                                h_1_8_421.Fill(time)
                        if(cat==9):
                            if(method==422):
                                h_1_9_422.Fill(time)
                            if(method==322):
                                h_1_9_322.Fill(time)
                            if(method==122):
                                h_1_9_122.Fill(time) ##
                            if(method==421):
                                h_1_9_421.Fill(time)
                        if(cat==10):
                            if(method==421):
                                h_1_10_421.Fill(time)
                            if(method==422):
                                h_1_10_422.Fill(time)
                            if(method==322):
                                h_1_10_322.Fill(time)
                        if(cat==11):
                            if(method==421):
                                h_1_11_421.Fill(time)
                            if(method==422):
                                h_1_11_422.Fill(time)
                            if(method==322):
                                h_1_11_322.Fill(time)
                        if(cat==12):
                            if(method==421):
                                h_1_12_421.Fill(time)
                            if(method==422):
                                h_1_11_422.Fill(time)
                            if(method==322):
                                h_1_12_322.Fill(time)

            hev_vhbb.Fill(nev_vhbb)
            hev_mem.Fill(nev_mem)
            # t = subprocess.Popen("grep 'timeto' "+destination+"/"+outfile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            # for line in t.stdout.readlines():
            #     if(line.find('totalJob') > 0):
            #         jobtime = line.split()[1]
            #         #print "jobtime ", float(jobtime)/3600
            #         htime.Fill(float(jobtime)/3600)

    treedir = outf.GetDirectory( sample)
    if(treedir==None):
        treedir = outf.mkdir( sample )

    treedir.cd()
    htime_total.Write("", TObject.kOverwrite)
    htime_vhbb.Write("", TObject.kOverwrite)
    htime_mem.Write("", TObject.kOverwrite)
    hev_vhbb.Write("", TObject.kOverwrite)
    hev_mem.Write("", TObject.kOverwrite)

    h_0_7_322.Write("", TObject.kOverwrite)
    #h_0_7_122.Write("", TObject.kOverwrite)
    h_0_7_421.Write("", TObject.kOverwrite)
    h_0_8_422.Write("", TObject.kOverwrite)
    h_0_8_322.Write("", TObject.kOverwrite)
    #h_0_8_122.Write("", TObject.kOverwrite)
    h_0_8_421.Write("", TObject.kOverwrite)
    h_0_9_422.Write("", TObject.kOverwrite)
    h_0_9_322.Write("", TObject.kOverwrite)
    #h_0_9_122.Write("", TObject.kOverwrite)
    h_0_9_421.Write("", TObject.kOverwrite)
    h_0_10_421.Write("", TObject.kOverwrite)
    h_0_10_422.Write("", TObject.kOverwrite)
    h_0_10_322.Write("", TObject.kOverwrite)
    h_0_11_421.Write("", TObject.kOverwrite)
    h_0_11_422.Write("", TObject.kOverwrite)
    h_0_11_322.Write("", TObject.kOverwrite)
    h_0_12_421.Write("", TObject.kOverwrite)
    h_0_12_422.Write("", TObject.kOverwrite)
    h_0_12_322.Write("", TObject.kOverwrite)

    h_1_7_322.Write("", TObject.kOverwrite)
    #h_1_7_122.Write("", TObject.kOverwrite)
    h_1_7_421.Write("", TObject.kOverwrite)
    h_1_8_422.Write("", TObject.kOverwrite)
    h_1_8_322.Write("", TObject.kOverwrite)
    #h_1_8_122.Write("", TObject.kOverwrite)
    h_1_8_421.Write("", TObject.kOverwrite)
    h_1_9_422.Write("", TObject.kOverwrite)
    h_1_9_322.Write("", TObject.kOverwrite)
    #h_1_9_122.Write("", TObject.kOverwrite)
    h_1_9_421.Write("", TObject.kOverwrite)
    h_1_10_421.Write("", TObject.kOverwrite)
    h_1_10_422.Write("", TObject.kOverwrite)
    h_1_10_322.Write("", TObject.kOverwrite)
    h_1_11_421.Write("", TObject.kOverwrite)
    h_1_11_422.Write("", TObject.kOverwrite)
    h_1_11_322.Write("", TObject.kOverwrite)
    h_1_12_421.Write("", TObject.kOverwrite)
    h_1_12_422.Write("", TObject.kOverwrite)
    h_1_12_322.Write("", TObject.kOverwrite)

    outf.Close()
