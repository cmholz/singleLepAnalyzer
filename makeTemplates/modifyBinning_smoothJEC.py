#!/usr/bin/python

import os,sys,time,math,fnmatch
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from array import array
from weights import *
from modSyst_split import *
from utils import *
from ROOT import *
start_time = time.time()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Run as:
# > python modifyBinning.py
# 
# Optional arguments:
# -- statistical uncertainty threshold
#
# Notes:
# -- Finds certain root files in a given directory and rebins all histograms in each file
# -- A selection of subset of files in the input directory can be done below under "#Setup the selection ..."
# -- A custom binning choice can also be given below and this choice can be activated by giving a stat unc 
#    threshold larger than 100% (>1.) in the argument
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#cutString = 'splitLess/'#BB_templates/'
templateDir = os.getcwd()+'/templatesCR_June2020TT2017/'

rebinCombine = True
smoothLOWESS = True

scaleLumi = False
#lumiScaleCoeffEl = 2530./2600.
#lumiScaleCoeffMu = 2621./2690.
lumiscale = 2318./2258.

sigName = 'TT' #MAKE SURE THIS WORKS FOR YOUR ANALYSIS PROPERLY!!!!!!!!!!!
if 'BB' in templateDir: sigName = 'BB'
skipcode = 'bW'
if sigName == 'BB': skipcode = 'tW'
dataName = 'DATA'
upTag = '__plus'
downTag = '__minus'
if rebinCombine:
    upTag = 'Up'
    downTag = 'Down'

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

#Setup the selection of the files to be rebinned: HiggsTagTemplate_tW1p0_bZ0p0_bH0p0_BBM1800.root
rfiles = [file for file in findfiles(templateDir, '*.root') if 'rebinned' in file and '0p3' in file and 'smoothed' not in file and skipcode in file and 'BKGNORM' not in file and 'Combine' not in file and 'plots' not in file] 
if rebinCombine: 
    #rfiles = [file for file in findfiles(templateDir, '*.root') if '_Combine_' in file and 'rebinned' in file and '0p3' in file and 'smoothed' not in file and skipcode in file and 'BKGNORM' not in file]
    rfiles = [file for file in findfiles(templateDir, '*.root') if '_Combine_' in file and 'rebinned' in file and '0p3' in file and 'smoothed' not in file and skipcode in file]	
tfile = TFile(rfiles[0])

iRfile=0
yieldsAll = {}
yieldsErrsAll = {}
yieldsSystErrsAll = {}
checkscale = True
for rfile in rfiles: 
	print "SMOOTHING FILE:",rfile
	tfiles = {}
	outputRfiles = {}
	tfiles[iRfile] = TFile(rfile)	
        allhists = [hist.GetName() for hist in tfiles[iRfile].GetListOfKeys()]

        if smoothLOWESS: outputRfiles[iRfile] = TFile(rfile.replace('.root','_smoothedLOWESS.root'),'RECREATE')     
        else: outputRfiles[iRfile] = TFile(rfile.replace('.root','_smoothed.root'),'RECREATE')     

	print "PROGRESS:"
	rebinnedHists = {}
	for hist in allhists:

            rebinnedHists[hist]=tfiles[iRfile].Get(hist)
            rebinnedHists[hist].SetDirectory(0)

            if 'jec' not in hist and 'jer' not in hist: rebinnedHists[hist].Write()   


        jecUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'jec2017'+upTag in k.GetName()]
        jerUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'jer2017'+upTag in k.GetName()]

        for hist in jecUphists+jerUphists:
            #print hist

            if 'qcd' in hist: # don't bother
                rebinnedHists[hist].Write()
                rebinnedHists[hist.replace(upTag,downTag)].Write()
            else:

                if smoothLOWESS: ## Local regression method
                    frac = 0.5

                    up = rebinnedHists[hist].Clone()
                    down = rebinnedHists[hist.replace(upTag,downTag)].Clone()
                    central = rebinnedHists[hist.replace('__jec2017'+upTag,'').replace('__jer2017'+upTag,'')]
                    
                    upratio = up.Clone('upratio')
                    upratio.Divide(central)
                    
                    dnratio = down.Clone('dnratio')
                    dnratio.Divide(central)
                    
                    upgraph = TGraph()
                    dngraph = TGraph()
                    
                    for ibin in range(1,up.GetNbinsX()+1):
                        upgraph.SetPoint(ibin-1, upratio.GetXaxis().GetBinCenter(ibin), upratio.GetBinContent(ibin))
                        dngraph.SetPoint(ibin-1, dnratio.GetXaxis().GetBinCenter(ibin), dnratio.GetBinContent(ibin))
                    
                    upratio.Delete()
                    dnratio.Delete()

                    upsmooth = TGraphSmooth("normal")
                    dnsmooth = TGraphSmooth("normal")

                    upgraph = upsmooth.SmoothLowess(upgraph,"",frac)
                    dngraph = dnsmooth.SmoothLowess(dngraph,"",frac)

                    for ibin in range(1,up.GetNbinsX()+1):
                        newupratio = upgraph.Eval(up.GetXaxis().GetBinCenter(ibin))
                        newdnratio = dngraph.Eval(down.GetXaxis().GetBinCenter(ibin))
                        centralval = central.GetBinContent(ibin)
                        up.SetBinContent(ibin, newupratio*centralval)
                        down.SetBinContent(ibin, newdnratio*centralval)

                    if central.Integral() > 0 and up.Integral() > 0:
                        up.Write()
                        down.Write()
                    else:
                        rebinnedHists[hist].Write()
                        rebinnedHists[hist.replace(upTag,downTag)].Write()

                else: ## smooth with 5-bin rolling average window
                    upsum = 0
                    downsum = 0
                    centralsum = 0
                    for ibin in range(1,up.GetNbinsX()+1):
                        upsum = 0
                        downsum = 0
                        centralsum = 0
                        for jbin in range(ibin-2,ibin+3):
                            if jbin < 0 or jbin > up.GetNbinsX(): continue
                    
                            upsum += up.GetBinContent(jbin)
                            downsum += down.GetBinContent(jbin)
                            centralsum += central.GetBinContent(jbin)
                        
                        if centralsum != 0:
                            upratio = upsum/centralsum
                            downratio = downsum/centralsum
                        else:
                            # leave things alone if the central value was 0 (ex: QCD)
                            upratio = up.GetBinContent(ibin)
                            downratio = down.GetBinContent(ibin)

                        up.SetBinContent(ibin, central.GetBinContent(ibin)*upratio)
                        down.SetBinContent(ibin, central.GetBinContent(ibin)*downratio)

                    up.Write()
                    down.Write()
			
	tfiles[iRfile].Close()
	outputRfiles[iRfile].Close()
	iRfile+=1
tfile.Close()
print ">> Smoothing Done!"

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))



