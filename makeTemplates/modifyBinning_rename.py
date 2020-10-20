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

cutString = 'splitLess/'#BB_templates/'
templateDir = os.getcwd()+'/templates_ARC/'+cutString #BoostedHiggs/'+cutString

scaleLumi = False
#lumiScaleCoeffEl = 2530./2600.
#lumiScaleCoeffMu = 2621./2690.
lumiscale = 2318./2258.

sigName = 'TT' #MAKE SURE THIS WORKS FOR YOUR ANALYSIS PROPERLY!!!!!!!!!!!
skipcode = 'bW'
if sigName == 'BB': skipcode = 'tW'
dataName = 'DATA'
upTag = '__plus'
downTag = '__minus'

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

#Setup the selection of the files to be rebinned: HiggsTagTemplate_tW1p0_bZ0p0_bH0p0_BBM1800.root
rfiles = [file for file in findfiles(templateDir, '*.root') if 'rebinned' in file and skipcode in file]

tfile = TFile(rfiles[0])

iRfile=0
yieldsAll = {}
yieldsErrsAll = {}
yieldsSystErrsAll = {}
checkscale = True
for rfile in rfiles: 
	print "RENAMING FILE:",rfile
	tfiles = {}
	outputRfiles = {}
	tfiles[iRfile] = TFile(rfile)	
        allhists = [hist.GetName() for hist in tfiles[iRfile].GetListOfKeys()]

	outputRfiles[iRfile] = TFile(rfile.replace('.root','_renamed.root'),'RECREATE')

        #signame = ((rfile.split('/')[-1]).split('_')[-1]).split('.')[0]
        #signame = signame.replace('TTM','TpTp_M-').replace('BBM','BpBp_M-')
        #if 'M-800' in signame or 'M-900' in signame or 'M-700' in signame: signame = signame.replace('M-','M-0')

	print "PROGRESS:"
	rebinnedHists = {}
	for hist in allhists:
            #print hist
            rebinnedHists[hist]=tfiles[iRfile].Get(hist)
            rebinnedHists[hist].SetDirectory(0)
            #if scaleLumi and 'DATA' not in hist: 
            #if 'DATA' in hist: 
                #if 'El' in hist: lumiscale = lumiScaleCoeffEl
                #else: lumiscale = lumiScaleCoeffMu
                #if checkscale: print 'original integral =',rebinnedHists[hist].Integral()
                #rebinnedHists[hist].Scale(lumiscale)
                #if checkscale: print 'new integral =',rebinnedHists[hist].Integral()
                #checkscale = False

            if 'muRFcorrdNewEWK' not in hist and 'QCD__jsf' not in hist and 'SingleTop__jsf' not in hist and 'TTbar__jsf' not in hist and 'sig__jsf' not in hist: rebinnedHists[hist].Write()   
            #if 'DYJets__jsf' not in hist and 'SingleTop__jsf' not in hist and 'Diboson__jsf' not in hist and signame+'__jsf' not in hist: rebinnedHists[hist].Write()		    

        muRUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'muRFcorrdNewEWK'+upTag in k.GetName()]
        newMuRFNameBase = 'muRFcorrdNew'
        for hist in muRUphists:
                    
            if 'EWK__' in hist: newMuRFName = newMuRFNameBase+'Ewk1L'
            
        #     if 'Diboson' in hist: continue
        #     if 'TTbar__' in hist: newMuRFName = newMuRFNameBase+'TTbar'
        #     if 'WJets__' in hist: newMuRFName = newMuRFNameBase+'WJets'
        #     if 'SingleTop__' in hist: newMuRFName = newMuRFNameBase+'SingleTop'
        #     if 'DYJets__' in hist: newMuRFName = newMuRFNameBase+'DYJets'
        #     if 'QCD__' in hist: newMuRFName = newMuRFNameBase+'QCD'
        #     if sigName == 'TT' and 'TpTp' in hist: newMuRFName = newMuRFNameBase+'TpTp'
        #     if sigName == 'BB' and 'BpBp' in hist: newMuRFName = newMuRFNameBase+'BpBp'
            muRFcorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muRFcorrdNewEWK'+upTag,newMuRFName+upTag))
            muRFcorrdNewDnHist = rebinnedHists[hist.replace(upTag,downTag)].Clone(hist.replace('muRFcorrdNewEWK'+upTag,newMuRFName+downTag))
            muRFcorrdNewUpHist.Write()
            muRFcorrdNewDnHist.Write()
			
	tfiles[iRfile].Close()
	outputRfiles[iRfile].Close()
	iRfile+=1
tfile.Close()
print ">> Renaming Done!"

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))



