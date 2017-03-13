import ROOT, sys

infile = open(sys.argv[1]).readlines()

bad_files = []
for line in infile:
    if not "root" in line:
        continue
    line = line.split()[0]
    print "trying", line
    f = None 
    try:
        f = ROOT.TFile.Open("root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat" + line)
        if not f or f.IsZombie():
            raise Exception("is zombie")
    except Exception as e:
        print "BAD", line
        bad_files += [line]
        print e
    if f:
        f.Close()
