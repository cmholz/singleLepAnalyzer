#!/usr/bin/python

import os,sys,time,math,fnmatch,gc
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from array import array
from weights import *
from modSyst import *
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
# -- A custom binning choice can also be given by manually filling "xbinsList[chn]" for each channel
#    with the preferred choice of binning
# -- If no rebinning is wanted, but want to add PDF and R/F uncertainties, use a stat unc threshold 
#    that is larger than 100% (i.e, >1.)
# -- If CR and SR templates are in the same file and single bins are required for CR templates,
#    this can be done with "singleBinCR" bool (assumes that the CR templates contain "isCR" tags!).
# -- Use "removalKeys" to remove specific systematics from the output file.
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#print 'Checking garbage collection:',gc.isenabled()
#gc.set_debug(gc.DEBUG_LEAK)

iPlot='minMlbST'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
folder = ''
if len(sys.argv)>2: folder=str(sys.argv[2])
cutString = 'splitLess'#'lep30_MET150_NJets4_DR1_1jet450_2jet150'
templateDir = os.getcwd()+'/'+folder+'/'+cutString
combinefile = 'templates_'+iPlot+'_36p814fb.root'

rebinCombine = False #else rebins theta templates
doStatShapes = True
normalizeRENORM = True #only for signals
normalizePDF    = True #only for signals
#X53X53, TT, BB, HTB, etc --> this is used to identify signal histograms for combine templates when normalizing the pdf and muRF shapes to nominal!!!!
sigName = 'TT' #MAKE SURE THIS WORKS FOR YOUR ANALYSIS PROPERLY!!!!!!!!!!!
if len(sys.argv)>4: sigName=str(sys.argv[4])
brcode = 'bW'
if sigName == 'BB': brcode = 'tW'
massList = range(800,1800+1,100)
sigProcList = [sigName+'M'+str(mass) for mass in massList]
if sigName=='TT' or sigName=='BB': 
	sigProcList = [sigName+'M'+str(mass) for mass in massList]
	if not rebinCombine: sigProcList = [sigName+'M'+str(mass) for mass in massList]
bkgProcList = ['TTbar','SingleTop','EWK','QCD'] #put the most dominant process first #'WJets','DYJets','ewk',
era = "13TeV"

stat = 0.3 #statistical uncertainty requirement (enter >1.0 for no rebinning; i.g., "1.1")
singleBinCR = False
if len(sys.argv)>3: stat=float(sys.argv[3])

if rebinCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'

addCRsys = False
addShapes = True
lumiSys = math.sqrt(0.026**2 + 0.05**2) #lumi uncertainty + higgs prop
eltrigSys = 0.01 #electron trigger uncertainty
mutrigSys = 0.01 #muon trigger uncertainty
elIdSys = 0.02 #electron id uncertainty
muIdSys = 0.03 #muon id uncertainty
elIsoSys = 0.01 #electron isolation uncertainty
muIsoSys = 0.01 #muon isolation uncertainty
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

removalKeys = {} # True == keep, False == remove
removalKeys['btag__']    = True
removalKeys['mistag__']  = True
removalKeys['trigeff__'] = False
removalKeys['muR__']       = False
removalKeys['muF__']       = False
removalKeys['muRFcorrd__'] = False
removalKeys['q2__'] = False
removalKeys['jsf__'] = True

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

#Setup the selection of the files to be rebinned:          
print templateDir
rfiles = [file for file in findfiles(templateDir, '*.root') if 'rebinned' not in file and brcode in file and combinefile not in file and '_'+iPlot+'_' in file.split('/')[-1]]
if rebinCombine: rfiles = [templateDir+'/'+combinefile]

for rfile in rfiles:
	if sigName=='TT' and 'TTM1000_bW0p5_tZ0p25_tH0p25' in rfile: tfile = TFile(rfile)
	if sigName=='BB' and 'BBM1000_tW0p5_bZ0p25_bH0p25' in rfile: tfile = TFile(rfile)
print tfile
datahists = [k.GetName() for k in tfile.GetListOfKeys() if '__'+dataName in k.GetName()]
channels = [hist[hist.find('fb_')+3:hist.find('__')] for hist in datahists if 'isL_' not in hist]
allhists = {chn:[hist.GetName() for hist in tfile.GetListOfKeys() if chn in hist.GetName()] for chn in channels}

totBkgHists = {}
for hist in datahists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	totBkgHists[channel]=tfile.Get(hist.replace('__'+dataName,'__'+bkgProcList[0])).Clone()
	for proc in bkgProcList:
		if proc == bkgProcList[0]: continue
		try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__'+proc)))
		except: 
			print "Missing",proc,"for category:",hist
			print "WARNING! Skipping this process!!!!"
			pass

SigHists = {}
for hist in datahists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	try: SigHists[channel]=tfile.Get(hist.replace('__'+dataName,'__sig')).Clone()
	except: 
		print 'No signal for channel:',channel
		pass 

xbinsListTemp = {}
for chn in totBkgHists.keys():
	if ('H1b' not in chn and 'H2b' not in chn and 'H1p' not in chn) or iPlot != 'minMlbST':
		#print 'Channel',chn,'integral is',totBkgHists[chn].Integral()

		if 'isE' not in chn: continue
		#if 'nH0_nW0_nB0' not in chn: continue
		xbinsListTemp[chn]=[tfile.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile.Get(datahists[0]).GetXaxis().GetNbins())]
		Nbins = tfile.Get(datahists[0]).GetNbinsX()
		totTempBinContent_E = 0.
		totTempBinContent_M = 0.
		totTempBinErrSquared_E = 0.
		totTempBinErrSquared_M = 0.
		totTempSigContent_E = 0;
		totTempSigContent_M = 0;
		for iBin in range(1,Nbins+1):			
			totTempBinContent_E += totBkgHists[chn].GetBinContent(Nbins+1-iBin)
			totTempBinContent_M += totBkgHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
			totTempBinErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
			totTempBinErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
			try:
				totTempSigContent_E += SigHists[chn].GetBinContent(Nbins+1-iBin)
				totTempSigContent_M += SigHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
			except: pass
			#print 'totTempBinContent =',totTempBinContent_E,' ',totTempBinContent_M,', totTempBinErrSquared =',totTempBinErrSquared_E,' ',totTempBinErrSquared_M
			#print 'totTempSigContent =',totTempSigContent_E,' ',totTempSigContent_M

			if totTempBinContent_E>0. and totTempBinContent_M>0.:				
				if 'CR' in templateDir or 'ttbar' in templateDir or 'wjets' in templateDir or 'higgs' in templateDir or (totTempSigContent_E>0. and totTempSigContent_M>0):
					if math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E<=stat and math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M<=stat:
						totTempBinContent_E = 0.
						totTempBinContent_M = 0.
						totTempBinErrSquared_E = 0.
						totTempBinErrSquared_M = 0.
						totTempSigContent_E = 0.
						totTempSigContent_M = 0.
						#print 'Appending bin edge',totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin)
						xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
		if xbinsListTemp[chn][-1]!=0: xbinsListTemp[chn].append(0)
		if totBkgHists[chn].GetBinContent(1)==0. or totBkgHists[chn.replace('isE','isM')].GetBinContent(1)==0.: 
			if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
		elif totBkgHists[chn].GetBinError(1)/totBkgHists[chn].GetBinContent(1)>stat or totBkgHists[chn.replace('isE','isM')].GetBinError(1)/totBkgHists[chn.replace('isE','isM')].GetBinContent(1)>stat: 
			if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
		xbinsListTemp[chn.replace('isE','isM')]=xbinsListTemp[chn]
		if stat>1.0:
			xbinsListTemp[chn] = [tfile.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile.Get(datahists[0]).GetXaxis().GetNbins())]
			for iBin in range(1,Nbins+1): 
				xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
			xbinsListTemp[chn.replace('isE','isM')] = xbinsListTemp[chn]
	else:
		if 'isE' not in chn: continue

		#print 'Channel',chn,'integral is',totBkgHists[chn].Integral()
		
		index = 8
		#if 'ttbar' in templateDir: index = 4
		#if 'wjets' in templateDir: index = 2
		if 'higgs' in templateDir: index = 0
		if 'CR' in templateDir: index = 2
		xbinsListTemp[chn]=[tfile.Get(datahists[index]).GetXaxis().GetBinUpEdge(tfile.Get(datahists[index]).GetXaxis().GetNbins())]
		Nbins = tfile.Get(datahists[index]).GetNbinsX()
		totTempBinContent_E = 0.
		totTempBinContent_M = 0.
		totTempBinErrSquared_E = 0.
		totTempBinErrSquared_M = 0.
		totTempSigContent_E = 0;
		totTempSigContent_M = 0;
		for iBin in range(1,Nbins+1):
			totTempBinContent_E += totBkgHists[chn].GetBinContent(Nbins+1-iBin)
			totTempBinContent_M += totBkgHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
			totTempBinErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
			totTempBinErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
			try:
				totTempSigContent_E += SigHists[chn].GetBinContent(Nbins+1-iBin)
				totTempSigContent_M += SigHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
			except: pass
			if totTempBinContent_E>0. and totTempBinContent_M>0.:
				if 'CR' in templateDir or 'ttbar' in templateDir or 'wjets' in templateDir or 'higgs' in templateDir or SigHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin) < 1351.0 or (totTempSigContent_E>0. and totTempSigContent_M>0.):
					if math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E<=stat and math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M<=stat:
						totTempBinContent_E = 0.
						totTempBinContent_M = 0.
						totTempBinErrSquared_E = 0.
						totTempBinErrSquared_M = 0.
						totTempSigContent_E = 0.
						totTempSigContent_M = 0.
						xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
		if xbinsListTemp[chn][-1]!=0: xbinsListTemp[chn].append(0)
		if totBkgHists[chn].GetBinContent(1)==0. or totBkgHists[chn.replace('isE','isM')].GetBinContent(1)==0.: 
			if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
		elif totBkgHists[chn].GetBinError(1)/totBkgHists[chn].GetBinContent(1)>stat or totBkgHists[chn.replace('isE','isM')].GetBinError(1)/totBkgHists[chn.replace('isE','isM')].GetBinContent(1)>stat: 
			if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
		xbinsListTemp[chn.replace('isE','isM')]=xbinsListTemp[chn]
		if stat>1.0:
			xbinsListTemp[chn] = [tfile.Get(datahists[8]).GetXaxis().GetBinUpEdge(tfile.Get(datahists[8]).GetXaxis().GetNbins())]
			for iBin in range(1,Nbins+1): 
				xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
			xbinsListTemp[chn.replace('isE','isM')] = xbinsListTemp[chn]

del SigHists
del totBkgHists
tfile.Close()
del tfile

print "==> Here is the binning I found with",stat*100,"% uncertainty threshold: "
print "//"*40
xbinsList = {}
for chn in xbinsListTemp.keys():
	xbinsList[chn] = []
	for bin in range(len(xbinsListTemp[chn])): xbinsList[chn].append(xbinsListTemp[chn][len(xbinsListTemp[chn])-1-bin])
	if 'isCR' in chn and singleBinCR: xbinsList[chn] = [xbinsList[chn][0],xbinsList[chn][-1]]
	print chn,"=",xbinsList[chn]
print "//"*40

xbins = {}
for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

#os._exit(1)

muSFsUp = {'TTM800':0.750,'TTM900':0.750,'TTM1000':0.749,'TTM1100':0.749,'TTM1200':0.748,'TTM1300':0.747,'TTM1400':0.746,'TTM1500':0.745,'TTM1600':0.744,'TTM1700':0.743,'TTM1800':0.741}
muSFsDn = {'TTM800':1.303,'TTM900':1.303,'TTM1000':1.304,'TTM1100':1.305,'TTM1200':1.307,'TTM1300':1.309,'TTM1400':1.311,'TTM1500':1.313,'TTM1600':1.315,'TTM1700':1.317,'TTM1800':1.319}
pdfSFsUp = {'TTM800':0.908,'TTM900':0.902,'TTM1000':0.890,'TTM1100':0.889,'TTM1200':0.895,'TTM1300':0.895,'TTM1400':0.888,'TTM1500':0.897,'TTM1600':0.905,'TTM1700':0.885,'TTM1800':0.872}
pdfSFsDn = {'TTM800':1.106,'TTM900':1.104,'TTM1000':1.099,'TTM1100':1.099,'TTM1200':1.093,'TTM1300':1.098,'TTM1400':1.102,'TTM1500':1.099,'TTM1600':1.122,'TTM1700':1.121,'TTM1800':1.133}

if sigName == 'BB':
	muSFsUp = {'BBM800':0.750,'BBM900':0.750,'BBM1000':0.749,'BBM1100':0.749,'BBM1200':0.748,'BBM1300':0.747,'BBM1400':0.746,'BBM1500':0.745,'BBM1600':0.744,'BBM1700':0.743,'BBM1800':0.741}
	muSFsDn = {'BBM800':1.303,'BBM900':1.303,'BBM1000':1.304,'BBM1100':1.305,'BBM1200':1.307,'BBM1300':1.309,'BBM1400':1.310,'BBM1500':1.313,'BBM1600':1.315,'BBM1700':1.317,'BBM1800':1.319}
	pdfSFsUp = {'BBM800':0.909,'BBM900':0.903,'BBM1000':0.889,'BBM1100':0.889,'BBM1200':0.895,'BBM1300':0.895,'BBM1400':0.889,'BBM1500':0.897,'BBM1600':0.904,'BBM1700':0.884,'BBM1800':0.872}
	pdfSFsDn = {'BBM800':1.106,'BBM900':1.104,'BBM1000':1.100,'BBM1100':1.099,'BBM1200':1.093,'BBM1300':1.097,'BBM1400':1.102,'BBM1500':1.099,'BBM1600':1.121,'BBM1700':1.122,'BBM1800':1.132}


iRfile=0
for rfile in rfiles: 	
	#if os.path.exists(rfile.replace('.root','_rebinned_stat'+str(stat).replace('.','p')+'.root')): continue
	print "REBINNING FILE:",rfile
	tfiles = {}
	outputRfiles = {}
	tfiles[iRfile] = TFile(rfile)	
	outputRfiles[iRfile] = TFile(rfile.replace('.root','_BKGNORM_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')	

	signame = rfile.split('/')[-1].split('_')[2]
	if 'TTM' not in signame and 'BBM' not in signame: print 'DIDNT STORE SIGNAME: ',signame

	print "PROGRESS:"
	for chn in channels:
		print "         ",chn,' hist size',len(allhists[chn])
		rebinnedHists = {}
		#Rebinning histograms
		for hist in allhists[chn]:			
			try: rebinnedHists[hist]=tfiles[iRfile].Get(hist).Rebin(len(xbins[chn])-1,hist,xbins[chn])
			except: 
				print 'making empty hist for:',hist,'in',chn
				rebinnedHists[hist]=TH1D(hist,"",len(xbins[chn])-1,xbins[chn])				
			rebinnedHists[hist].SetDirectory(0)
			# if 'sig__mu' in hist and normalizeRENORM: #normalize the renorm/fact shapes to nominal
			# 	renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__mu')]).Clone()
			# 	renormSysHist = tfiles[iRfile].Get(hist).Clone()
			# 	rebinnedHists[hist].Scale(renormNomHist.Integral()/renormSysHist.Integral())
			# if 'sig__pdf' in hist and normalizePDF: #normalize the pdf shapes to nominal
			# 	renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
			# 	renormSysHist = tfiles[iRfile].Get(hist).Clone()
			# 	rebinnedHists[hist].Scale(renormNomHist.Integral()/renormSysHist.Integral())
			if '__pdf' in hist:
				if 'Up' not in hist or 'Down' not in hist: continue
			#if '__mu' in hist: continue
			if any([item in hist and not removalKeys[item] for item in removalKeys.keys()]): continue
			rebinnedHists[hist].Write()

		##Check for empty signal bins
		#sighist = rebinnedHists[iPlot+'_36p814fb_'+chn+'__sig']
		#for ibin in range(1,sighist.GetNbinsX()+1):
		#	if sighist.GetBinContent(ibin) == 0: print 'chn = '+chn+', mass = '+sigName+', empty minMlb > '+str(sighist.GetBinLowEdge(ibin))
			

		#Constructing muRF shapes
		trighists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'trigeff'+upTag in k.GetName() and chn in k.GetName()]
		trigNameBase = 'trigeff'
		for hist in trighists:
			if 'isE_' in hist: trigName = trigNameBase+'El'
			elif 'isM_' in hist: trigName = trigNameBase+'Mu'
			else: print 'trig doesnt understand this name:'+hist
			trigUpHist = rebinnedHists[hist].Clone(hist.replace('trigeff'+upTag,trigName+upTag))
			trigUpHist.SetDirectory(0)
			trigDnHist = rebinnedHists[hist.replace(upTag,downTag)].Clone(hist.replace('trigeff'+upTag,trigName+downTag))
			trigDnHist.SetDirectory(0)
			trigUpHist.Write()
			trigDnHist.Write()

		trighists = []		

		#Constructing muRF shapes
		muRUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'muR'+upTag in k.GetName() and chn in k.GetName()]
		newMuRFNameBase = 'muRFcorrdNew'
		for hist in muRUphists:
			if 'TTbar__' in hist: newMuRFName = newMuRFNameBase+'TTbar'
			#elif 'WJets__' in hist: newMuRFName = newMuRFNameBase+'WJets'
			#elif 'DYJets__' in hist: newMuRFName = newMuRFNameBase+'DYJets'
			#elif 'ewk__' in hist: newMuRFName = newMuRFNameBase+'Ewk'
			elif 'EWK__' in hist: newMuRFName = newMuRFNameBase+'Ewk1L'
			elif 'SingleTop__' in hist: newMuRFName = newMuRFNameBase+'SingleTop'
			elif 'QCD__' in hist: newMuRFName = newMuRFNameBase+'QCD'
			elif 'sig__' in hist: newMuRFName = newMuRFNameBase+'Sig'
			elif 'top__' in hist: newMuRFName = newMuRFNameBase+'Top'
			else: print 'muRF doesnt understand this name:'+hist
			muRFcorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muR'+upTag,newMuRFName+upTag))
			muRFcorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muR'+upTag,newMuRFName+downTag))
			muRFcorrdNewUpHist.SetDirectory(0)
			muRFcorrdNewDnHist.SetDirectory(0)
			histList = [
				rebinnedHists[hist[:hist.find('__mu')]], #nominal
				rebinnedHists[hist], #renormWeights[4]
				rebinnedHists[hist.replace('muR'+upTag,'muR'+downTag)], #renormWeights[2]
				rebinnedHists[hist.replace('muR'+upTag,'muF'+upTag)], #renormWeights[1]
				rebinnedHists[hist.replace('muR'+upTag,'muF'+downTag)], #renormWeights[0]
				rebinnedHists[hist.replace('muR'+upTag,'muRFcorrd'+upTag)], #renormWeights[5]
				rebinnedHists[hist.replace('muR'+upTag,'muRFcorrd'+downTag)] #renormWeights[3]
				]
			for ibin in range(1,histList[0].GetNbinsX()+1):
				weightList = [histList[ind].GetBinContent(ibin) for ind in range(len(histList))]
				indCorrdUp = weightList.index(max(weightList))
				indCorrdDn = weightList.index(min(weightList))
	
				muRFcorrdNewUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
				muRFcorrdNewDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))
	
				muRFcorrdNewUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
				muRFcorrdNewDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
			if ('sig__mu' in hist and normalizeRENORM) or (rebinCombine and '__'+sigName in hist and '__mu' in hist and normalizeRENORM): #normalize the renorm/fact shapes to nominal
				scalefactorUp = muSFsUp[signame]
				scalefactorDn = muSFsDn[signame]
				muRFcorrdNewUpHist.Scale(scalefactorUp)   # shape-only: muRFcorrdNewUpHist.Scale(renormNomHist.Integral()/muRFcorrdNewUpHist.Integral()) 
				muRFcorrdNewDnHist.Scale(scalefactorDn)
			if ('sig__mu' not in hist and normalizeRENORM):
 				renormNomHist = histList[0]
				#print 'hist: ',hist,' SF =',renormNomHist.Integral()/muRFcorrdNewUpHist.Integral()
				muRFcorrdNewUpHist.Scale(renormNomHist.Integral()/muRFcorrdNewUpHist.Integral())
				muRFcorrdNewDnHist.Scale(renormNomHist.Integral()/muRFcorrdNewDnHist.Integral())
			muRFcorrdNewUpHist.Write()
			muRFcorrdNewDnHist.Write()

		muRUphists = []

		#Constructing PDF shapes
		pdfUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'pdf0' in k.GetName() and chn in k.GetName()]
		newPDFName = 'pdfNew'
		for hist in pdfUphists:
			pdfNewUpHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+upTag))
			pdfNewDnHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+downTag))
			pdfNewUpHist.SetDirectory(0)
			pdfNewDnHist.SetDirectory(0)
			for ibin in range(1,pdfNewUpHist.GetNbinsX()+1):
				weightList = [rebinnedHists[hist.replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
				indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
				indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
				pdfNewUpHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinContent(ibin))
				pdfNewDnHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinContent(ibin))
				pdfNewUpHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinError(ibin))
				pdfNewDnHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinError(ibin))
			if ('sig__pdf' in hist and normalizePDF) or (rebinCombine and '__'+sigName in hist and '__pdf' in hist and normalizePDF): #normalize the renorm/fact shapes to nominal
				scalefactorUp = pdfSFsUp[signame]
				scalefactorDn = pdfSFsDn[signame]
				#print 'Mass',signame,': assigning SFup =',scalefactorUp,', SFdn =',scalefactorDn
				pdfNewUpHist.Scale(scalefactorUp)
				pdfNewDnHist.Scale(scalefactorDn)
				# renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
				# pdfNewUpHist.Scale(renormNomHist.Integral()/pdfNewUpHist.Integral())
				# pdfNewDnHist.Scale(renormNomHist.Integral()/pdfNewDnHist.Integral())
			pdfNewUpHist.Write()
			pdfNewDnHist.Write()
	
		pdfUphists = []
		rebinnedHists = []
	
	tfiles[iRfile].Close()
	outputRfiles[iRfile].Close()
	tfiles[iRfile] = 'null'
	outputRfiles[iRfile] = 'null'
	iRfile+=1
	gc.collect()

print ">> Rebinning Done!"

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


