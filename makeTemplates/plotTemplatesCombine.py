#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from ROOT import *
from weights import *
from modSyst import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumi=35.9
lumi2017=41.5
lumi2018=59.7
lumiInTemplates2016=str(targetlumi/1000).replace('.','p')
lumiInTemplates2017=str(targetlumi2017/1000).replace('.','p') # 1/fb
lumiInTemplates2018=str(targetlumi2018/1000).replace('.','p')


 
iPlot='HT'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
region='PS' #SR,TTCR,WJCR
if len(sys.argv)>2: region=str(sys.argv[2])
isCategorized=False
if len(sys.argv)>3: isCategorized=bool(eval(sys.argv[3]))
pfix2016='templates'+region
pfix2017='templates'+region
pfix2018='templates'+region
if not isCategorized: 
	pfix2016='kinematics'+region
	pfix2017='kinematics'+region
        pfix2018='kinematics'+region
pfix2016+='_June2020TT'
pfix2017+='_June2020TT'
pfix2018+='_Jun2020TT'



if len(sys.argv)>4: pfix=str(sys.argv[4])
#templateDir=os.getcwd()+'/'+pfix+'/'
templateDir2016='/uscms_data/d3/cholz/CMSSW_10_2_10/src/tptp_2016/makeTemplates/'+pfix2016+'/'
templateDir2017='/uscms_data/d3/bluetke/MVATraining/CMSSW_10_2_16/src/singleLepAnalyzer/makeTemplates/'+pfix2017+'/'
#templateDir2018='/uscms_data/d3/jmanagan/CMSSW_10_2_10/src/tptp_2018/makeTemplates/'+pfix2018+'/'
templateDir2018='/uscms_data/d3/jmoberg/CMSSW_10_2_16/src/singleLepAnalyzer/makeTemplates/'+pfix2018+'/'

print 'Plotting',region,'is categorized?',isCategorized

isRebinned=''#_rebinned_stat0p3' #post for ROOT file names
if len(sys.argv)>7: isRebinned='_rebinned_stat'+str(sys.argv[7])
BRstr=''
if isCategorized:
	BRstr='bW0p5_tZ0p25_tH0p25_'
	if 'BB' in pfix: BRstr = 'tW0p5_bZ0p25_bH0p25_'
saveKey = '' # tag for plot names

sig1='TTM1200' #  choose the 1st signal to plot
sig1leg='T#bar{T} (1.2 TeV)'
sig2='TTM1500' #  choose the 2nd signal to plot
sig2leg='T#bar{T} (1.5 TeV)'
if 'BB' in pfix2016:
	sig1 = sig1.replace('TT','BB')
	sig2 = sig2.replace('TT','BB')
	sig1leg = sig1leg.replace('T#bar{T}','B#bar{B}')
	sig2leg = sig2leg.replace('T#bar{T}','B#bar{B}')
if 'BB' in pfix2017:
        sig1 = sig1.replace('TT','BB')
        sig2 = sig2.replace('TT','BB')
        sig1leg = sig1leg.replace('T#bar{T}','B#bar{B}')
        sig2leg = sig2leg.replace('T#bar{T}','B#bar{B}')
if 'BB' in pfix2018:
        sig1 = sig1.replace('TT','BB')
        sig2 = sig2.replace('TT','BB')
        sig1leg = sig1leg.replace('T#bar{T}','B#bar{B}')
        sig2leg = sig2leg.replace('T#bar{T}','B#bar{B}')
#print 'sig1leg: ', sig1leg
drawNormalized = False # STACKS CAN'T DO THIS...bummer
scaleSignals = True
if not isCategorized and 'CR' not in region: scaleSignals = True
sigScaleFact = 400
if 'SR' in region: sigScaleFact = 10
if 'Nm1' in iPlot: sigScaleFact = sigScaleFact/5
print 'Scaling signals?',scaleSignals
print 'Scale factor = ',sigScaleFact

bkgProcList = ['ewk','top','qcd']
if '53' in sig1: bkgHistColors = {'top':kRed-9,'ewk':kBlue-7,'qcd':kOrange-5} #X53X53
elif 'HTB' in sig1: bkgHistColors = {'ttbar':kGreen-3,'wjets':kPink-4,'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #HTB
else: bkgHistColors = {'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #TT

if len(isRebinned)>0: systematicList = ['pileup','prefire','jec','muRFcorrdNewTop','muRFcorrdNewEwk','muRFcorrdNewQCD','btag','jsf','Teff','Tmis','Heff','Hmis','Zeff','Zmis','Weff','Wmis','Beff','Bmis','Jeff','Jmis','jer','ltag']
else: systematicList = ['muRFcorrd','pileup','prefire','jsf','jec','btag','Teff','Tmis','Heff','Hmis','Zeff','Zmis','Weff','Wmis','Beff','Bmis','Jeff','Jmis','jer','ltag']

doAllSys = True
print 'doAllSys: ',doAllSys,'systematicList: ',systematicList
addCRsys = False
doNormByBinWidth=False
if len(isRebinned)>0 and 'stat1p1' not in isRebinned: doNormByBinWidth = True
doOneBand = True
# MAY NEED TO RE-INDENT PART/ALL OF CODE FROM HERE TO CORRESPONDING COMMENT!!!!!
if not doAllSys: doOneBand = True # Don't change this!
blind = False
if len(sys.argv)>5: blind=bool(eval(sys.argv[5]))
yLog  = False
if len(sys.argv)>6: yLog=bool(eval(sys.argv[6]))
print 'Plotting blind?',blind,' yLog?',yLog
if yLog: scaleSignals = False
doRealPull = False
if doRealPull: doOneBand=False
compareShapes = False
if compareShapes: blind,yLog=True,False
histrange = {}

isEMlist =['E','M']
algolist = ['all']
if 'algos' in region or 'SR' in region or isCategorized: 
	#print 'I think algos is in the region'
	algolist = ['DeepAK8']#,'BEST','DeepAK8DC']
taglist = ['all']
if isCategorized == True: 
	if 'CR' in region: taglist=['dnnLargeT','dnnLargeH','dnnLargeW','dnnLargeZ','dnnLargeB','dnnLargeJwjet','dnnLargeJttbar'] 
	elif 'BB' in pfix: taglist=['taggedtWtW','taggedbZtW','taggedbHtW','notVbH','notVbZ','notVtW',
					'notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
	elif 'TT' in pfix: taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW',
					'notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
	#isEMlist = ['L']
	#taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtZ','notVbW','notVtH',
	#	 'notV3W0Z0H0T',
	#	 'notV2W0Z0H0T','notV2pW0Z0H1pT','notV2pW0Z1pH0pT','notV2pW1pZ0pH0pT',
	#	 'notV1W0Z0H0T','notV1W0Z1H0T','notV1W0Z0H1pT','notV1W0Z1H1pT','notV1W0Z2pH0pT','notV1W1Z0H0pT','notV1W1Z1pH0pT','notV1W2pZ0pH0pT',
	#	 'notV0W0Z0H0T','notV0W0Z1H0T','notV0W0Z0H1pT','notV0W0Z1H1pT','notV0W0Z2pH0pT','notV0W1Z0H0pT','notV0W1Z1pH0pT','notV0W2pZ0pH0pT']

print taglist, algolist

tagList = []
if isCategorized and iPlot != 'YLD':
	for item in list(itertools.product(taglist,algolist)):
		tag = [item[0],item[1]]
		tagList.append(tag)
else: tagList = list(itertools.product(taglist,algolist))

lumiSys = 0.025 # lumi uncertainty
trigSys = 0.05 # trigger uncertainty, now really reco uncertainty 
lepIdSys = 0.02 # lepton id uncertainty
lepIsoSys = 0.015 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2) #cheating while total e/m values are close

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error

def formatUpperHist(histogram,th1hist):
	histogram.GetXaxis().SetLabelSize(0)
	lowside = th1hist.GetBinLowEdge(1)
	if iPlot=='ST': lowside = th1hist.GetBinLowEdge(8)-50.0
	highside = th1hist.GetBinLowEdge(th1hist.GetNbinsX()+1)
	if iPlot=='dnnLargest': highside = th1hist.GetBinLowEdge(7)-0.1
	histogram.GetXaxis().SetRangeUser(lowside,highside)
# def formatUpperHist(histogram):
# 	histogram.GetXaxis().SetLabelSize(0)
# 	histogram.GetXaxis().SetRangeUser(histrange[0],histrange[1])
	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.04)
		histogram.GetYaxis().SetTitleSize(0.05)
		histogram.GetYaxis().SetTitleOffset(1.1)
		histogram.GetXaxis().SetNdivisions(506)
		if 'YLD' in iPlot: histogram.GetXaxis().LabelsOption("u")
	else:
		histogram.GetYaxis().SetLabelSize(0.05)
		histogram.GetYaxis().SetTitleSize(0.06)
		histogram.GetYaxis().SetTitleOffset(.82)

	if 'nB0_' in histogram.GetName() and 'minMlb' in histogram.GetName(): histogram.GetXaxis().SetTitle("min[M(l,j)], j#neqb [GeV]")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.00101)
	if 'H1b' in histogram.GetName(): histogram.SetMinimum(0.000101)
	if 'H2b' in histogram.GetName(): histogram.SetMinimum(0.0000101)
	if not yLog: 
		if region == 'SR' and isCategorized: histogram.SetMinimum(0.000101);
		else: histogram.SetMinimum(0.25)		
	if yLog:
		uPad.SetLogy()
		if not doNormByBinWidth: histogram.SetMaximum(500*histogram.GetMaximum())
		else: 
			histogram.SetMaximum(200*histogram.GetMaximum())
		if iPlot=='YLD': 
			histogram.SetMaximum(200*histogram.GetMaximum())
			histogram.SetMinimum(0.1)

		
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.15)
	histogram.GetXaxis().SetTitleSize(0.18)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)
	if 'YLD' in iPlot: histogram.GetXaxis().LabelsOption("u")
	if iPlot=='ST': histogram.GetXaxis().SetRangeUser(600,5000)
	if iPlot=='dnnLargest': histogram.GetXaxis().SetRangeUser(0,6)

	histogram.GetYaxis().SetLabelSize(0.15)
	histogram.GetYaxis().SetTitleSize(0.145)
	histogram.GetYaxis().SetTitleOffset(.3)
	if not doRealPull: histogram.GetYaxis().SetTitle('Data/Bkg')
	else: histogram.GetYaxis().SetTitle('#frac{(data-bkg)}{std. dev.}')
# MAY NEED TO RE-INDENT ALL CODE ABOVE HERE TO CORRESPONDING COMMENT!!!
	histogram.GetYaxis().SetNdivisions(7)
	if doRealPull: histogram.GetYaxis().SetRangeUser(-2.99,2.99)
	if doRealPull: histogram.GetYaxis().SetRangeUser(-2.99,2.99)
	elif yLog and doNormByBinWidth: histogram.GetYaxis().SetRangeUser(0.1,1.9)
	else: histogram.GetYaxis().SetRangeUser(0.1,1.9)
	histogram.GetYaxis().CenterTitle()

tempsig2016='templates_'+iPlot+'_'+sig1+'_'+BRstr+lumiInTemplates2016+'fb'+isRebinned+'.root'
tempsig2017='templates_'+iPlot+'_'+sig1+'_'+BRstr+lumiInTemplates2017+'fb'+isRebinned+'.root'#+'_Data18.root'
tempsig2018='templates_'+iPlot+'_'+sig1+'_'+BRstr+lumiInTemplates2018+'fb'+isRebinned+'.root'
RFile1 = TFile(templateDir2016+tempsig2016.replace(sig1,sig1))
print templateDir2016+tempsig2016.replace(sig1,sig1)
RFile2 = TFile(templateDir2016+tempsig2016.replace(sig1,sig2))
RFile3 = TFile(templateDir2017+tempsig2017.replace(sig1,sig1))
RFile4 = TFile(templateDir2017+tempsig2017.replace(sig1,sig2))
RFile5 = TFile(templateDir2018+tempsig2018.replace(sig1,sig1))
RFile6 = TFile(templateDir2018+tempsig2018.replace(sig1,sig2))
print RFile1
print RFile2
print RFile3
print RFile4
print RFile5
print RFile6
bkghists = {}
bkghistsmerged = {}
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
for tag in tagList:
	tagStr=tag[0]+'_'+tag[1]
	for isEM in isEMlist:
		histPrefix2016=iPlot+'_'+lumiInTemplates2016+'fb_'
                print 'hisPrefix:'+histPrefix2016
                histPrefix2017=iPlot+'_'+lumiInTemplates2017+'fb_'
                print 'hisPrefix:'+histPrefix2017
                histPrefix2018=iPlot+'_'+lumiInTemplates2018+'fb_'
                print 'hisPrefix:'+histPrefix2018
		catStr='is'+isEM+'_'+tagStr
		histPrefix2016+=catStr
		histPrefix2017+=catStr
                histPrefix2018+=catStr
		totBkg = 0.
		for proc in bkgProcList: 
			try: 				
				#print RFile1.ls()
				#print histPrefix+'__'+proc
				bkghists[proc+catStr] = RFile1.Get(histPrefix2016+'__'+proc).Clone()+RFile3.Get(histPrefix2017+'__'+proc).Clone()+RFile5.Get(histPrefix2018+'__'+proc).Clone()
				totBkg += bkghists[proc+catStr].Integral()
			except:
				print "There is no "+proc+"!!!!!!!!"
				print "tried to open "+histPrefix2016+'__'+proc
				pass
		print 'HERE: '+histPrefix2016+'__DATA and '+histPrefix2017+'__DATA and '+histPrefix2018+'__DATA'
		hData = RFile1.Get(histPrefix2016+'__DATA').Clone()+RFile3.Get(histPrefix2017+'__DATA').Clone()+RFile5.Get(histPrefix2018+'__DATA').Clone()
		histrange = [hData.GetBinLowEdge(1),hData.GetBinLowEdge(hData.GetNbinsX()+1)]
		gaeData = TGraphAsymmErrors(hData.Clone(hData.GetName().replace('DATA','gaeDATA')))
		hsig1 = RFile1.Get(histPrefix2016+'__sig').Clone(histPrefix2016+'__sig1')+RFile3.Get(histPrefix2017+'__sig').Clone(histPrefix2017+'__sig1')+RFile5.Get(histPrefix2018+'__sig').Clone(histPrefix2018+'__sig1')
		hsig2 = RFile2.Get(histPrefix2016+'__sig').Clone(histPrefix2016+'__sig2')+RFile4.Get(histPrefix2017+'__sig').Clone(histPrefix2017+'__sig2')+RFile6.Get(histPrefix2018+'__sig').Clone(histPrefix2018+'__sig1')
                #hsig3 = RFile3.Get(histPrefix2018+'__sig').Clone(histPrefix2018+'__sig1')
                #hsig4 = RFile4.Get(histPrefix2018+'__sig').Clone(histPrefix2018+'__sig2')
		hsig1.Scale(xsec[sig1])
		hsig2.Scale(xsec[sig2])
                #hsig3.Scale(xsec[sig1])
                #hsig4.Scale(xsec[sig2])
		if doNormByBinWidth:
			poissonNormByBinWidth(gaeData,hData)
			for proc in bkgProcList:
				try: normByBinWidth(bkghists[proc+catStr])
				except: pass
			normByBinWidth(hsig1)
			normByBinWidth(hsig2)
			normByBinWidth(hData)
		else: poissonErrors(gaeData)
		# Yes, there are easier ways using the TH1's but
		# it would be rough to swap objects lower down

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass
		gaeBkgHT = TGraphAsymmErrors(bkgHT.Clone("gaeBkgHT"))

		#if doNormByBinWidth: poissonNormByBinWidth(gaeBkgHT,bkgHT)
		#else: poissonErrors(gaeBkgHT)

		#yvals = gaeBkgHT.GetY()
		#print 'bkgHT = ',bkgHT.GetBinContent(25),'+/-',bkgHT.GetBinError(25)
		#print 'gaeBkgHT = ',yvals[24],'+',gaeBkgHT.GetErrorYhigh(24),'-',gaeBkgHT.GetErrorYlow(24)

		if doAllSys:
			for syst in systematicList:
				for ud in ['minus','plus']:
					for proc in bkgProcList:
						try: 
							systHists[proc+catStr+syst+ud] = RFile1.Get(histPrefix2016+'__'+proc+'__'+syst+'__'+ud).Clone()+RFile3.Get(histPrefix2017+'__'+proc+'__'+syst+'__'+ud).Clone()+RFile5.Get(histPrefix2018+'__'+proc+'__'+syst+'__'+ud).Clone()
							if doNormByBinWidth: normByBinWidth(systHists[proc+catStr+syst+ud])
						except: 
							print 'FAILED to open '+proc+'_'+syst+'_'+ud+'_'
							pass

		totBkgTemp1[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
		
		for ibin in range(1,bkghists[bkgProcList[0]+catStr].GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorStatUp = gaeBkgHT.GetErrorYhigh(ibin-1)**2
			errorStatDn = gaeBkgHT.GetErrorYlow(ibin-1)**2
			errorNorm = 0.

			if doAllSys:
				for syst in systematicList:
					for proc in bkgProcList:
						try:
							errorPlus = systHists[proc+catStr+syst+'plus'].GetBinContent(ibin)-bkghists[proc+catStr].GetBinContent(ibin)
							errorMinus = bkghists[proc+catStr].GetBinContent(ibin)-systHists[proc+catStr+syst+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass

			totBkgTemp1[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
			totBkgTemp1[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
			totBkgTemp2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
			totBkgTemp2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
			totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatUp))
			totBkgTemp3[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatDn))
		
		bkgHTgerr = totBkgTemp3[catStr].Clone()

		scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
		scaleFact2 = int(bkgHT.GetMaximum()/hsig2.GetMaximum()) - int(bkgHT.GetMaximum()/hsig2.GetMaximum()) % 10
		if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
		if scaleFact2==0: scaleFact2=int(bkgHT.GetMaximum()/hsig2.GetMaximum())
		if scaleFact1==0: scaleFact1=1
		if scaleFact2==0: scaleFact2=1
		if sigScaleFact>0:
			scaleFact1=sigScaleFact
			scaleFact2=sigScaleFact*2
		if not scaleSignals:
			scaleFact1=1
			scaleFact2=1
		hsig1.Scale(scaleFact1)
		hsig2.Scale(scaleFact2)

                ############################################################
		############## Making Plots of e+jets, mu+jets and e/mu+jets 
                ############################################################
		
		drawQCD = False
		try: drawQCD = bkghists['qcd'+catStr].Integral()/bkgHT.Integral()>.005 #don't plot QCD if it is less than 0.5%
		except: pass

		stackbkgHT = THStack("stackbkgHT","")
		bkgProcListNew = bkgProcList[:]
		if region=='WJCR':
			bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
		for proc in bkgProcListNew:
			try: 
				if drawQCD or proc!='qcd': stackbkgHT.Add(bkghists[proc+catStr])
			except: pass

		sig1Color= kBlack
		sig2Color= kBlack
		if '53' in sig1:
			sig1Color= kBlack
			sig2Color= kBlack
			
		for proc in bkgProcList:
			try: 
				bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetLineWidth(2)
			except: pass
		hsig1.SetLineColor(sig1Color)
		hsig1.SetFillStyle(0)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(sig2Color)
		hsig2.SetLineStyle(7)#5)
		hsig2.SetFillStyle(0)
		hsig2.SetLineWidth(3)
		
		gaeData.SetMarkerStyle(20)
		gaeData.SetMarkerSize(1.2)
		gaeData.SetLineWidth(2)
		gaeData.SetMarkerColor(kBlack)
		gaeData.SetLineColor(kBlack)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(kBlack)

		gStyle.SetOptStat(0)
		c1 = TCanvas("c1","c1",1200,1000)
		gStyle.SetErrorX(0.5)
		yDiv=0.25
		if blind == True: yDiv=0.01
		# for some reason the markers at 0 don't show with this setting:
		uMargin = 0.00001
		if blind == True: uMargin = 0.12
		rMargin=.04
		# overlap the pads a little to hide the error bar gap:
		uPad={}
		if yLog and not blind: uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
		else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.08)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(.105)
		uPad.Draw()
		if blind == False:
			lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
			lPad.SetTopMargin(0)
			lPad.SetBottomMargin(.4)
			lPad.SetRightMargin(rMargin)
			lPad.SetLeftMargin(.105)
			lPad.SetGridy()
			lPad.Draw()
		if not doNormByBinWidth: hData.SetMaximum(1.4*max(hData.GetMaximum(),bkgHT.GetMaximum()))
		hData.SetMinimum(0.015)
		hData.SetTitle("")
		# this is super important now!! gaeData has badly defined (negative) maximum
		gaeData.SetMaximum(1.6*max(gaeData.GetMaximum(),bkgHT.GetMaximum()))
		gaeData.SetMinimum(0.015)
		gaeData.SetTitle("")
		if doNormByBinWidth:
			if iPlot == 'DnnTprime': gaeData.GetYaxis().SetTitle("< Events / 0.01 >")
			else: gaeData.GetYaxis().SetTitle("< Events / 1 GeV >")
		else: gaeData.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(gaeData,hData)
		uPad.cd()
		gaeData.SetTitle("")
		if compareShapes: 
			hsig1.Scale(totBkg/hsig1.Integral())
			hsig2.Scale(totBkg/hsig2.Integral())
		if not blind: gaeData.Draw("apz")
		if blind: 
			hsig1.SetMinimum(0.015)
			if doNormByBinWidth:
				if iPlot == 'DnnTprime': hsig1.GetYaxis().SetTitle("< Events / 0.01 >")
				else: hsig1.GetYaxis().SetTitle("< Events / 1 GeV >")
			else: hsig1.GetYaxis().SetTitle("Events / bin")
			hsig1.SetMaximum(1.5*hData.GetMaximum())
			if iPlot=='Tau21Nm1': hsig1.SetMaximum(1.5*hData.GetMaximum())
			formatUpperHist(hsig1,hsig1)
			hsig1.Draw("HIST")
		if doNormByBinWidth:
			if iPlot == 'DnnTprime': hData.GetYaxis().SetTitle("< Events / 0.01 >")
			else: hData.GetYaxis().SetTitle("< Events / 1 GeV >")
		else: hData.GetYaxis().SetTitle("Events / bin")
		
		stackbkgHT.Draw("SAME HIST")
		hsig1.Draw("SAME HIST")
		hsig2.Draw("SAME HIST")
		if not blind: gaeData.Draw("PZ") #redraw data so its not hidden
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")
		
		chLatex = TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.06)
		if blind: chLatex.SetTextSize(0.04)
		chLatex.SetTextAlign(21) # align center
		flvString = ''
		tagString = ''
		if isEM=='E': flvString+='e+jets'
		if isEM=='M': flvString+='#mu+jets'
		tagString = ''
		algoString = ''
		if isCategorized: tagString = tag[0]
		if isCategorized or 'algos' in region: algoString = tag[1]
		if tagString.endswith(', '): tagString = tagString[:-2]		
		if algoString.endswith(', '): algoString = algoString[:-2]		
		if iPlot != 'deltaRAK8': chLatex.DrawLatex(0.28, 0.84, flvString)
		else: chLatex.DrawLatex(0.75,0.84,flvString)
		if iPlot != 'YLD': 
			chLatex.DrawLatex(0.28, 0.78, algoString)
			chLatex.DrawLatex(0.28, 0.72, tagString)

		if drawQCD: 
			leg = TLegend(0.45,0.52,0.95,0.87)
			if iPlot == 'deltaRAK8': leg = TLegend(0.15,0.52,0.55,0.82)
		if not drawQCD or blind: 
			leg = TLegend(0.45,0.64,0.95,0.89)
			if iPlot == 'deltaRAK8': leg = TLegend(0.12,0.65,0.62,0.89)
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetNColumns(2)
		leg.SetTextFont(62)#42)
		scaleFact1Str = ' x'+str(scaleFact1)
		scaleFact2Str = ' x'+str(scaleFact2)
		if not scaleSignals:
			scaleFact1Str = ''
			scaleFact2Str = ''
		if drawQCD:
			if not blind: 
				#leg.AddEntry(0, "", "")
				leg.AddEntry(gaeData,"Data","pel")  #left
				leg.AddEntry(bkghists['qcd'+catStr],"QCD","f") #right
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")  #left
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f") #right
				except: pass
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l") #left
				try: leg.AddEntry(bkghists['ewk'+catStr],"EW","f") #right
				except: pass
				#leg.AddEntry(0, "", "") #left
				leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #right
			else:
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")  #left
				leg.AddEntry(bkghists['qcd'+catStr],"QCD","f") #right
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l") #left
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f") #right
				except: pass
				leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
				try: leg.AddEntry(bkghists['ewk'+catStr],"EW","f") #right
				except: pass
				
		if not drawQCD:
			if not blind: 
				leg.AddEntry(gaeData,"Data","pel") #left 
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f") #right
				except: pass
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l") #left
				try: leg.AddEntry(bkghists['ewk'+catStr],"EW","f") #right
				except: pass
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l") #left
				leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #right
			else:
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l") #left
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f") #right
				except: pass
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l") #left
				try: leg.AddEntry(bkghists['ewk'+catStr],"EW","f") #right
				except: pass
				#leg.AddEntry(0, "", "") #left
				leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #right


		leg.Draw("same")

		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.05)
		if blind: prelimTex.SetTextSize(0.05)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.94,str(lumi+lumi2017+lumi2018)+" fb^{-1} (13 TeV)")

		prelimTex2=TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.08)
		if blind: prelimTex2.SetTextSize(0.08)
		prelimTex2.DrawLatex(0.12,0.93,"CMS")

		prelimTex3=TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(12)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.055)
		if blind: prelimTex3.SetTextSize(0.055)
		prelimTex3.SetLineWidth(2)
		if not blind: prelimTex3.DrawLatex(0.23,0.945,"Work in progress") #"Preliminary")
		if blind: prelimTex3.DrawLatex(0.26,0.945,"Work in progress") #"Preliminary")

		if blind == False and not doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			pull.Divide(hData, bkgHT)
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pull.SetBinError(binNo,hData.GetBinError(binNo)/bkgHT.GetBinContent(binNo))
			pull.SetMaximum(3)
			pull.SetMinimum(0)
			pull.SetFillColor(1)
			pull.SetLineColor(1)
			pull.SetMarkerStyle(20)
			formatLowerHist(pull)
			pull.Draw("E0")
			
			BkgOverBkg = pull.Clone("bkgOverbkg")
			BkgOverBkg.Divide(bkgHT, bkgHT)
			pullUncBandTot=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			if not doOneBand: pullUncBandTot.SetFillStyle(3001)
			else: pullUncBandTot.SetFillStyle(3344)
			pullUncBandTot.SetFillColor(1)
			pullUncBandTot.SetLineColor(1)
			pullUncBandTot.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			pullUncBandTot.Draw("SAME E2")
			
			pullUncBandNorm=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandNorm.SetFillStyle(3001)
			pullUncBandNorm.SetFillColor(2)
			pullUncBandNorm.SetLineColor(2)
			pullUncBandNorm.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
			
			pullUncBandStat=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandStat.SetFillStyle(3001)
			pullUncBandStat.SetFillColor(3)
			pullUncBandStat.SetLineColor(3)
			pullUncBandStat.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandStat.Draw("SAME E2")

			pullLegend=TLegend(0.14,0.87,0.85,0.96)
			SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
			pullLegend.SetShadowColor(0)
			pullLegend.SetNColumns(3)
			pullLegend.SetFillColor(0)
			pullLegend.SetFillStyle(0)
			pullLegend.SetLineColor(0)
			pullLegend.SetLineStyle(0)
			pullLegend.SetBorderSize(0)
			pullLegend.SetTextFont(42)
			if not doOneBand: pullLegend.AddEntry(pullUncBandStat , "Bkg. uncert. (shape syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandNorm , "Bkg. uncert. (shape #oplus norm. syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus all syst.)" , "f")
			else: 
				if doAllSys: pullLegend.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus syst.)" , "f")
				else: pullLegend.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus lumi)" , "f")
			pullLegend.Draw("SAME")
			pull.Draw("SAME E0")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			formatUpperHist(hData,hData)
			lPad.cd()
			pull=hData.Clone("pull")
			for binNo in range(1,hData.GetNbinsX()+1):
				# case for data < MC:
				dataerror = gaeData.GetErrorYhigh(binNo-1)
				MCerror = totBkgTemp3[catStr].GetErrorYlow(binNo-1)
				# case for data > MC: 
				if(hData.GetBinContent(binNo) > bkgHT.GetBinContent(binNo)):
					dataerror = gaeData.GetErrorYlow(binNo-1)
					MCerror = totBkgTemp3[catStr].GetErrorYhigh(binNo-1)
				pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+dataerror**2))
			pull.SetMaximum(3)
			pull.SetMinimum(-3)
			if '53' in sig1:
				pull.SetFillColor(2)
				pull.SetLineColor(2)
			else:
				pull.SetFillColor(kGray+2)
				pull.SetLineColor(kGray+2)
			formatLowerHist(pull)
			pull.Draw("HIST")

		#c1.Write()
		savePrefix = templateDir2016+templateDir2016.split('/')[-2]+'Combineplots/'#I think you will want to change templateDir here to match which data is being analyzed!!!!!!!
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix2016+isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if doRealPull: savePrefix+='_pull'
		if doNormByBinWidth: savePrefix+='_NBBW'
		if drawNormalized: savePrefix+='_norm'
		if yLog: savePrefix+='_logy'
		if blind: savePrefix+='_blind'
		if compareShapes: savePrefix+='_shp'

		if doOneBand:
			c1.SaveAs(savePrefix+"totBand.pdf")
			c1.SaveAs(savePrefix+"totBand.png")
			#c1.SaveAs(savePrefix+"totBand.eps")
			#c1.SaveAs(savePrefix+"totBand.root")
			#c1.SaveAs(savePrefix+"totBand.C")
		else:
			c1.SaveAs(savePrefix+".pdf")
			c1.SaveAs(savePrefix+".png")
			#c1.SaveAs(savePrefix+".eps")
			#c1.SaveAs(savePrefix+".root")
			#c1.SaveAs(savePrefix+".C")
		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass
					
	# Making plots for e+jets/mu+jets combined #

	histPrefixE2016 = iPlot+'_'+lumiInTemplates2016+'fb_isE_'+tagStr
	histPrefixM2016 = iPlot+'_'+lumiInTemplates2016+'fb_isM_'+tagStr
        histPrefixE2017 = iPlot+'_'+lumiInTemplates2017+'fb_isE_'+tagStr
        histPrefixM2017 = iPlot+'_'+lumiInTemplates2017+'fb_isM_'+tagStr
        histPrefixE2018 = iPlot+'_'+lumiInTemplates2018+'fb_isE_'+tagStr
        histPrefixM2018 = iPlot+'_'+lumiInTemplates2018+'fb_isM_'+tagStr
	totBkgMerged = 0.
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFile1.Get(histPrefixE2016+'__'+proc).Clone() + RFile3.Get(histPrefixE2017+'__'+proc).Clone() + RFile5.Get(histPrefixE2018+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFile1.Get(histPrefixM2016+'__'+proc).Clone())
			bkghistsmerged[proc+'isL'+tagStr].Add(RFile3.Get(histPrefixM2017+'__'+proc).Clone())
                        bkghistsmerged[proc+'isL'+tagStr].Add(RFile5.Get(histPrefixM2018+'__'+proc).Clone())
                        
			totBkgMerged += bkghistsmerged[proc+'isL'+tagStr].Integral()
		except:
			print("Failed try on line 723")
			pass
	hDatamerged = RFile1.Get(histPrefixE2016+'__DATA').Clone()+RFile3.Get(histPrefixE2017+'__DATA').Clone()+RFile5.Get(histPrefixE2018+'__DATA').Clone()
	hsig1merged = RFile1.Get(histPrefixE2016+'__sig').Clone(histPrefixE2016+'__sig1merged')+RFile3.Get(histPrefixE2017+'__sig').Clone(histPrefixE2017+'__sig1merged')+RFile5.Get(histPrefixE2018+'__sig').Clone(histPrefixE2018+'__sig1merged')
	hsig2merged = RFile2.Get(histPrefixE2016+'__sig').Clone(histPrefixE2016+'__sig2merged')+RFile4.Get(histPrefixE2017+'__sig').Clone(histPrefixE2017+'__sig2merged')+RFile6.Get(histPrefixE2018+'__sig').Clone(histPrefixE2018+'__sig2merged')
	hDatamerged.Add(RFile1.Get(histPrefixM2016+'__DATA').Clone())
	hDatamerged.Add(RFile3.Get(histPrefixM2017+'__DATA').Clone())
        hDatamerged.Add(RFile5.Get(histPrefixM2018+'__DATA').Clone())
	hsig1merged.Add(RFile1.Get(histPrefixM2016+'__sig').Clone())
	hsig1merged.Add(RFile3.Get(histPrefixM2017+'__sig').Clone())
        hsig1merged.Add(RFile5.Get(histPrefixM2018+'__sig').Clone())
	hsig2merged.Add(RFile2.Get(histPrefixM2016+'__sig').Clone())
	hsig2merged.Add(RFile4.Get(histPrefixM2017+'__sig').Clone())
        hsig2merged.Add(RFile6.Get(histPrefixM2018+'__sig').Clone())
	hsig1merged.Scale(xsec[sig1])
	hsig2merged.Scale(xsec[sig2])
        histrange = [hDatamerged.GetBinLowEdge(1),hDatamerged.GetBinLowEdge(hDatamerged.GetNbinsX()+1)]
	gaeDatamerged = TGraphAsymmErrors(hDatamerged.Clone(hDatamerged.GetName().replace("DATA","gaeDATA")))
	if doNormByBinWidth:
		poissonNormByBinWidth(gaeDatamerged,hDatamerged)
		for proc in bkgProcList:
			try: normByBinWidth(bkghistsmerged[proc+'isL'+tagStr])
			except: pass
		normByBinWidth(hsig1merged)
		normByBinWidth(hsig2merged)
		normByBinWidth(hDatamerged)
	else: poissonErrors(gaeDatamerged)
	# Yes, there are easier ways using the TH1's but
	# it would be rough to swap objects lower down	

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass
	gaeBkgHTmerged = TGraphAsymmErrors(bkgHTmerged.Clone("gaeBkgHTmerged"))

	#if doNormByBinWidth: poissonNormByBinWidth(gaeBkgHTmerged,bkgHTmerged)
	#else: poissonErrors(gaeBkgHTmerged)

	if doAllSys:
		for syst in systematicList:
			for ud in ['minus','plus']:
				for proc in bkgProcList:
					try: 
						systHists[proc+'isL'+tagStr+syst+ud] = systHists[proc+'isE_'+tagStr+syst+ud].Clone()
						systHists[proc+'isL'+tagStr+syst+ud].Add(systHists[proc+'isM_'+tagStr+syst+ud])
					except: pass

	totBkgTemp1['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
	totBkgTemp2['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
	totBkgTemp3['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))
	
	for ibin in range(1,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatUp = gaeBkgHTmerged.GetErrorYhigh(ibin-1)**2
		errorStatDn = gaeBkgHTmerged.GetErrorYlow(ibin-1)**2
		errorNorm = 0.

		if doAllSys:
			for syst in systematicList:
				for proc in bkgProcList:
					try:
						errorPlus = systHists[proc+'isL'+tagStr+syst+'plus'].GetBinContent(ibin)-bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)
						errorMinus = bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)-systHists[proc+'isL'+tagStr+syst+'minus'].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass

		totBkgTemp1['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
		totBkgTemp1['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
		totBkgTemp2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
		totBkgTemp2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatUp))
		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatDn))
	
	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()

	scaleFact1merged = int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) % 10
	scaleFact2merged = int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) % 10
	if scaleFact1merged==0: scaleFact1merged=int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum())
	if scaleFact2merged==0: scaleFact2merged=int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum())
	if scaleFact1merged==0: scaleFact1merged=1
	if scaleFact2merged==0: scaleFact2merged=1
	if sigScaleFact>0:
		scaleFact1merged=sigScaleFact
		scaleFact2merged=sigScaleFact*2
	if not scaleSignals:
		scaleFact1merged=1
		scaleFact2merged=1
	hsig1merged.Scale(scaleFact1merged)
	hsig2merged.Scale(scaleFact2merged)
	
	drawQCDmerged = False
	try: drawQCDmerged = bkghistsmerged['qcdisL'+tagStr].Integral()/bkgHTmerged.Integral()>.005
	except: pass

	stackbkgHTmerged = THStack("stackbkgHTmerged","")
	bkgProcListNew = bkgProcList[:]
	if region=='WJCR':
		bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
	for proc in bkgProcListNew:
		try: 
			if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
		except: pass
	hsig1merged.SetLineColor(sig1Color)
	hsig1merged.SetFillStyle(0)
	hsig1merged.SetLineWidth(3)
	hsig2merged.SetLineColor(sig2Color)
	hsig2merged.SetLineStyle(7)#5)
	hsig2merged.SetFillStyle(0)
	hsig2merged.SetLineWidth(3)
	
	gaeDatamerged.SetMarkerStyle(20)
	gaeDatamerged.SetMarkerSize(1.2)
	gaeDatamerged.SetLineWidth(2)
	gaeDatamerged.SetMarkerColor(kBlack)
	gaeDatamerged.SetLineColor(kBlack)

	bkgHTgerrmerged.SetFillStyle(3004)
	bkgHTgerrmerged.SetFillColor(kBlack)

	gStyle.SetOptStat(0)
	c1merged = TCanvas("c1merged","c1merged",1200,1000)
	gStyle.SetErrorX(0.5)
	yDiv=0.25
	if blind == True: yDiv=0.01
	uMargin = 0.00001
	if blind == True: uMargin = 0.12
	rMargin=.04
	uPad={}
	if yLog and not blind: uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
	else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
	uPad.SetTopMargin(0.08)
	uPad.SetBottomMargin(uMargin)
	uPad.SetRightMargin(rMargin)
	uPad.SetLeftMargin(.105)
	uPad.Draw()
	if blind == False:
		lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
		lPad.SetTopMargin(0)
		lPad.SetBottomMargin(.4)
		lPad.SetRightMargin(rMargin)
		lPad.SetLeftMargin(.105)
		lPad.SetGridy()
		lPad.Draw()
	gaeDatamerged.SetMaximum(1.6*max(gaeDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	if iPlot=='PrunedHNm1': gaeDatamerged.SetMaximum(1.7*max(gaeDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	gaeDatamerged.SetMinimum(0.015)
	if doNormByBinWidth:
		if iPlot == 'DnnTprime': gaeDatamerged.GetYaxis().SetTitle("< Events / 0.01 >")
		else: gaeDatamerged.GetYaxis().SetTitle("< Events / 1 GeV >")
	else: gaeDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(gaeDatamerged,hData)
	uPad.cd()
	gaeDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if compareShapes: 
		hsig1merged.Scale(totBkgMerged/hsig1merged.Integral())
		hsig2merged.Scale(totBkgMerged/hsig2merged.Integral())
	if not blind: gaeDatamerged.Draw("apz")
	if blind: 
		hsig1merged.SetMinimum(0.015)
		if doNormByBinWidth:
			if iPlot == 'DnnTprime': hsig1merged.GetYaxis().SetTitle("< Events / 0.01 >")
			else: hsig1merged.GetYaxis().SetTitle("< Events / 1 GeV >")
		else: hsig1merged.GetYaxis().SetTitle("Events / bin")
		hsig1merged.SetMaximum(1.5*hDatamerged.GetMaximum())
		if iPlot=='Tau21Nm1': hsig1merged.SetMaximum(1.5*hDatamerged.GetMaximum())
		formatUpperHist(hsig1merged,hsig1merged)
		hsig1merged.Draw("HIST")
	stackbkgHTmerged.Draw("SAME HIST")
	hsig1merged.Draw("SAME HIST")
	hsig2merged.Draw("SAME HIST")
	if not blind: gaeDatamerged.Draw("PZ") #redraw data so its not hidden
	uPad.RedrawAxis()
	bkgHTgerrmerged.Draw("SAME E2")

	chLatexmerged = TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.06)
	if blind: chLatexmerged.SetTextSize(0.04)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'e/#mu+jets'
	tagString = ''
	algoString = ''
	if isCategorized: tagString = tag[0]
	if isCategorized or 'algos' in region: algoString = tag[1]
	if tagString.endswith(', '): tagString = tagString[:-2]
	if algoString.endswith(', '): algoString = algoString[:-2]
	if iPlot != 'deltaRAK8': chLatexmerged.DrawLatex(0.28, 0.85, flvString)
	else: chLatexmerged.DrawLatex(0.75,0.85,flvString)
	if iPlot != 'YLD':
		chLatexmerged.DrawLatex(0.28, 0.78, algoString)
		chLatexmerged.DrawLatex(0.28, 0.72, tagString)

	if drawQCDmerged: 
		legmerged = TLegend(0.45,0.52,0.95,0.87)
		if iPlot == 'deltaRAK8': legmerged = TLegend(0.15,0.52,0.55,0.82)
	if not drawQCDmerged or blind: 
		legmerged = TLegend(0.45,0.64,0.95,0.89)
		if iPlot == 'deltaRAK8': legmerged = TLegend(0.12,0.65,0.62,0.90)
	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(2)
	legmerged.SetTextFont(62)#42)
	scaleFact1Str = ' x'+str(scaleFact1)
	scaleFact2Str = ' x'+str(scaleFact2)
	if not scaleSignals:
		scaleFact1Str = ''
		scaleFact2Str = ''
	if drawQCDmerged:
		if not blind: 
				#legmerged.AddEntry(0, "", "")
			legmerged.AddEntry(gaeDatamerged,"Data","pel")  #left
			legmerged.AddEntry(bkghistsmerged['qcdisL'+tagStr],"QCD","f") #right
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")  #left
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f") #right
			except: pass
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l") #left
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EW","f") #right
			except: pass
			#legmerged.AddEntry(0, "", "") #left
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #right
		else:
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")  #left
			legmerged.AddEntry(bkghistsmerged['qcdisL'+tagStr],"QCD","f") #right
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l") #left
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f") #right
			except: pass
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #left
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EW","f") #right
			except: pass
				
	if not drawQCDmerged:
		if not blind: 
			legmerged.AddEntry(gaeDatamerged,"Data","pel") #left 
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f") #right
			except: pass
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l") #left
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EW","f") #right
			except: pass
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l") #left
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #right
		else:
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l") #left
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f") #right
			except: pass
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l") #left
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EW","f") #right
			except: pass
			#legmerged.AddEntry(0, "", "") #left
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #right
	legmerged.Draw("same")

	prelimTex=TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.05)
	if blind: prelimTex.SetTextSize(0.05)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.95,0.94,str(lumi+lumi2017+lumi2018)+" fb^{-1} (13 TeV)")
	
	prelimTex2=TLatex()
	prelimTex2.SetNDC()
	prelimTex2.SetTextFont(61)
	prelimTex2.SetLineWidth(2)
	prelimTex2.SetTextSize(0.08)
	if blind: prelimTex2.SetTextSize(0.08)
	prelimTex2.DrawLatex(0.12,0.93,"CMS")
	
	prelimTex3=TLatex()
	prelimTex3.SetNDC()
	prelimTex3.SetTextAlign(12)
	prelimTex3.SetTextFont(52)
	prelimTex3.SetTextSize(0.055)
	if blind: prelimTex3.SetTextSize(0.055)
	prelimTex3.SetLineWidth(2)
	if not blind: prelimTex3.DrawLatex(0.23,0.945,"Work in progress") #"Preliminary")
	if blind: prelimTex3.DrawLatex(0.26,0.945,"Work in progress") #"Preliminary")
	
	if blind == False and not doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		pullmerged.Divide(hDatamerged, bkgHTmerged)
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pull.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(0)
		pullmerged.SetFillColor(1)
		pullmerged.SetLineColor(1)
		pullmerged.SetMarkerStyle(20)
		formatLowerHist(pullmerged)
		pullmerged.Draw("E0")
		
		BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
		BkgOverBkgmerged.Divide(bkgHTmerged, bkgHTmerged)
		pullUncBandTotmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncTotmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		if not doOneBand: pullUncBandTotmerged.SetFillStyle(3001)
		else: pullUncBandTotmerged.SetFillStyle(3344)
		pullUncBandTotmerged.SetFillColor(1)
		pullUncBandTotmerged.SetLineColor(1)
		pullUncBandTotmerged.SetMarkerSize(0)
		gStyle.SetHatchesLineWidth(1)
		pullUncBandTotmerged.Draw("SAME E2")
		
		pullUncBandNormmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncNormmerged"))
		for binNo in range(0,hData.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandNormmerged.SetFillStyle(3001)
		pullUncBandNormmerged.SetFillColor(2)
		pullUncBandNormmerged.SetLineColor(2)
		pullUncBandNormmerged.SetMarkerSize(0)
		gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
		
		pullUncBandStatmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandStatmerged.SetFillStyle(3001)
		pullUncBandStatmerged.SetFillColor(3)
		pullUncBandStatmerged.SetLineColor(3)
		pullUncBandStatmerged.SetMarkerSize(0)
		gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandStatmerged.Draw("SAME E2")

		pullLegendmerged=TLegend(0.14,0.87,0.85,0.96)
		SetOwnership( pullLegendmerged, 0 )   # 0 = release (not keep), 1 = keep
		pullLegendmerged.SetShadowColor(0)
		pullLegendmerged.SetNColumns(3)
		pullLegendmerged.SetFillColor(0)
		pullLegendmerged.SetFillStyle(0)
		pullLegendmerged.SetLineColor(0)
		pullLegendmerged.SetLineStyle(0)
		pullLegendmerged.SetBorderSize(0)
		pullLegendmerged.SetTextFont(42)
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandStat , "Bkg. uncert. (shape syst.)" , "f")
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg. uncert. (shape #oplus norm. syst.)" , "f")
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus all syst.)" , "f")
		else: 
			if doAllSys: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus syst.)" , "f")
			else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus lumi)" , "f")
		pullLegendmerged.Draw("SAME")
		pullmerged.Draw("SAME E0")
		lPad.RedrawAxis()

	if blind == False and doRealPull:
		formatUpperHist(hDatamerged,hDatamerged)
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			# case for data < MC:
			dataerror = gaeDatamerged.GetErrorYhigh(binNo-1)
			MCerror = totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)
			# case for data > MC:
			if(hDatamerged.GetBinContent(binNo) > bkgHTmerged.GetBinContent(binNo)):
				dataerror = gaeDatamerged.GetErrorYlow(binNo-1)
				MCerror = totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)
			pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+dataerror**2))
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(-3)
		if '53' in sig1:
			pullmerged.SetFillColor(2)
			pullmerged.SetLineColor(2)
		else:
			pullmerged.SetFillColor(kGray+2)
			pullmerged.SetLineColor(kGray+2)
		formatLowerHist(pullmerged)
		pullmerged.Draw("HIST")

	#c1merged.Write()
	savePrefixmerged = templateDir2016+templateDir2016.split('/')[-2]+'Combineplots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE2016.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if doRealPull: savePrefixmerged+='_pull'
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if drawNormalized: savePrefix+='_norm'
	if yLog: savePrefixmerged+='_logy'
	if blind: savePrefixmerged+='_blind'
	if compareShapes: savePrefixmerged+='_shp'

	if doOneBand: 
		c1merged.SaveAs(savePrefixmerged+"totBand.pdf")
		c1merged.SaveAs(savePrefixmerged+"totBand.png")
		#c1merged.SaveAs(savePrefixmerged+"totBand.eps")
		c1merged.SaveAs(savePrefixmerged+"totBand.root")
		#c1merged.SaveAs(savePrefixmerged+"totBand.C")
	else: 
		c1merged.SaveAs(savePrefixmerged+".pdf")
		c1merged.SaveAs(savePrefixmerged+".png")
		#c1merged.SaveAs(savePrefixmerged+".eps")
		#c1merged.SaveAs(savePrefixmerged+".root")
		#c1merged.SaveAs(savePrefixmerged+".C")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass

RFile1.Close()
RFile2.Close()
RFile3.Close()
RFile4.Close()
RFile5.Close()
RFile6.Close()
print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


