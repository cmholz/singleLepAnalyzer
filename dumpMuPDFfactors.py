import os,sys
execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

dirlist = [ 
'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8',
]

from ROOT import TFile, TH1

for sample in dirlist:
    print('---------------------'+sample+'--------------------------')
    runlist = EOSlistdir('/store/user/jmanagan/FWLJMET102X_1lep2018mupdf_072919/'+sample+'/singleLep2017/')
    if len(runlist) > 1: 
        print('PROBLEM: more than 1 crab directory, SKIPPING')
        continue

    rfile = TFile.Open('root://cmseos.fnal.gov//store/user/jmanagan/FWLJMET102X_1lep2018mupdf_072919/'+sample+'/singleLep2017/'+str(runlist[0])+'/0000/'+sample+'_1.root')
    hist = rfile.Get("mcweightanalyzer/weightHist")
    integral = hist.GetBinContent(5) + hist.GetBinContent(7)
    newpdf = hist.GetBinContent(2)

    print(str(round(newpdf,3))+'. # from integral '+str(integral))

    muhist = rfile.Get("mcweightanalyzer/muRFcounts")
    #print('MuRF nominal yield = '+str(round(muhist.GetBinContent(1),3)))

    muvars = []
    for ibin in range(1,muhist.GetNbinsX()+1): muvars.append(muhist.GetBinContent(ibin))
    muvars.sort()
    
    print('MuRF up yield = '+str(round(muvars[6],3)))
    print('MuRF dn yield = '+str(round(muvars[0],3)))
    
    pdfhist = rfile.Get("mcweightanalyzer/pdfcounts")
    #print('PDF nominal yield = '+str(round(pdfhist.GetBinContent(1),3)))

    pdfvars = []
    for ibin in range(1,pdfhist.GetNbinsX()+1): pdfvars.append(pdfhist.GetBinContent(ibin))
    pdfvars.sort()

    print('PDF up yield = '+str(round(pdfvars[83],3)))
    print('PDF dn yield = '+str(round(pdfvars[15],3)))

    print('MUup scale factor = '+str(round(muhist.GetBinContent(1)/muvars[6],3)))
    print('MUdn scale factor = '+str(round(muhist.GetBinContent(1)/muvars[0],3)))
    print('PDFup scale factor = '+str(round(pdfhist.GetBinContent(1)/pdfvars[83],3)))
    print('PDFdn scale factor = '+str(round(pdfhist.GetBinContent(1)/pdfvars[15],3)))





