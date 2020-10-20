#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from ROOT import *
from weights import *
from modSyst import *
from utils import *
from array import *

gROOT.SetBatch(1)
start_time = time.time()

lumi=35.9 #for plots
targetlumi = 35867.
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

region='CR' #SR,TTCR,WJCR
isCategorized=False
iPlot='HT'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString=''#lep40_MET60_DR0_1jet200_2jet100'
if region=='SR': pfix='templates_'#+iPlot
elif region=='WJCR': pfix='wjets_'#+iPlot
elif region=='TTCR': pfix='ttbar_'#+iPlot
elif region=='HCR': pfix='higgs_'#+iPlot
elif region=='CR': pfix='templatesCR_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+='ARC'
if len(sys.argv)>2: region=str(sys.argv[2])
if len(sys.argv)>3: pfix=str(sys.argv[3])
pfix = 'fitWJetsLine'
templateDir=os.getcwd()+'/'+pfix+'/'+cutString+'/'

isRebinned=''#_rebinned_stat0p3' #post for ROOT file names
saveKey = '' # tag for plot names

sig1='Hptb500' #  choose the 1st signal to plot
sig1leg='H^{#pm} (0.5 TeV)'
sig2='Hptb1000' #  choose the 2nd signal to plot
sig2leg='H^{#pm} (1.0 TeV)'
drawNormalized = False # STACKS CAN'T DO THIS...bummer
scaleSignals = False
if not isCategorized and 'CR' not in region: scaleSignals = True
sigScaleFact = 100
if 'SR' in region: sigScaleFact = 50
if 'Nm1' in iPlot: sigScaleFact = sigScaleFact/5
print 'Scaling signals?',scaleSignals
print 'Scale factor = ',sigScaleFact
tempsig='templates_'+iPlot+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

bkgProcList = ['tt2b','ttbb','ttb','ttcc','ttlf','top','ewk','qcd']

bkgHistColors = {'tt2b':kRed+3,'ttbb':kRed,'ttb':kRed-3,'ttcc':kRed-5,'ttlf':kRed-7,'top':kBlue,'ewk':kMagenta-2,'qcd':kOrange+5,'ttbar':kRed} #HTB


#bkgProcList = ['top','ewk','qcd']
#if '53' in sig1: bkgHistColors = {'top':kRed-9,'ewk':kBlue-7,'qcd':kOrange-5} #X53X53
#elif 'HTB' in sig1: bkgHistColors = {'ttbar':kGreen-3,'wjets':kPink-4,'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #HTB
#else: bkgHistColors = {'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #TT

systematicList = ['tau21','jmr','jms','pileup','jec','jer','muRFcorrdNewTop','muRFcorrdNewEwk','muRFcorrdNewQCD','pdfNew','toppt','btag','mistag','trigeff','taupt']
if 'WJCRnoJSF' in pfix or 'WJCRwSFs' in pfix or 'TTCRwNewWgt' in pfix: systematicList = ['tau21','pileup','jec','jer','muRFcorrdNew','pdfNew','toppt']
if 'WJCRwJSF' in pfix: systematicList = ['tau21','pileup','jec','jer','muRFcorrdNew','pdfNew','toppt','jsf']
if 'TTCRnoJSF' in pfix: systematicList = ['tau21','pileup','jec','jer','muRFcorrdNew','pdfNew']

doAllSys = False
doQ2sys  = False
if not doAllSys: doQ2sys = False
addCRsys = False
doNormByBinWidth=True
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = False
yLog  = True
if yLog: scaleSignals = False
doRealPull = False
if doRealPull: doOneBand=False
compareShapes = False
if compareShapes: blind,yLog=True,False
histrange = {}

isEMlist =['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['1','2','2p','3p']
njetslist = ['3','4','5','6p']
if not isCategorized: 
	nbtaglist = ['0']
	njetslist = ['3p']
if iPlot=='YLD':
	isCategorized=0
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	njetslist = ['0p']
tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))

lumiSys = math.sqrt(0.025**2 + 0.05**2) # lumi uncertainty plus higgs prop
trigSys = 0.01 # trigger uncertainty, now really reco uncertainty
lepIdSys = 0.03 # lepton id uncertainty
lepIsoSys = 0.01 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2) #cheating while total e/m values are close

for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	for proc in bkgProcList:
		if proc in ['ttbar','tt2b','ttbb','ttb','ttcc','ttlf']: 
			modelingSys[proc+'_'+modTag] = math.sqrt(0.042**2+0.027**2)
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module
		for proc in bkgProcList:
			modelingSys[proc+'_'+modTag] = 0.

# for tag in tagList:
# 	tagStr='nH'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
# 	modTag = tagStr[tagStr.find('nH'):tagStr.find('nJ')-3]	
# 	modelingSys['data_'+modTag] = 0.
# 	if not addCRsys: #else CR uncertainties are defined in modSyst.py module
# 		for proc in bkgProcList:
# 			modelingSys[proc+'_'+modTag] = 0.

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)
	histogram.GetXaxis().SetRangeUser(histrange[0],histrange[1])
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
		histogram.GetYaxis().SetTitleOffset(.71)

	if 'nB0_' in histogram.GetName() and 'minMlb' in histogram.GetName(): histogram.GetXaxis().SetTitle("min[M(l,j)], j#neqb [GeV]")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.00101)
	if 'H1b' in histogram.GetName(): histogram.SetMinimum(0.000101)
	if 'H2b' in histogram.GetName(): histogram.SetMinimum(0.0000101)
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		if not doNormByBinWidth: histogram.SetMaximum(200*histogram.GetMaximum())
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
	#histogram.GetXaxis().SetTitle("S_{T} (GeV)")
	if 'YLD' in iPlot: histogram.GetXaxis().LabelsOption("u")

	histogram.GetYaxis().SetLabelSize(0.15)
	histogram.GetYaxis().SetTitleSize(0.145)
	histogram.GetYaxis().SetTitleOffset(.3)
	if not doRealPull: histogram.GetYaxis().SetTitle('Data/Bkg')
	else: histogram.GetYaxis().SetTitle('#frac{(data-bkg)}{std. dev.}')
	histogram.GetYaxis().SetNdivisions(7)
	if doRealPull: histogram.GetYaxis().SetRangeUser(-2.99,2.99)
	elif yLog and doNormByBinWidth: histogram.GetYaxis().SetRangeUser(0.1,1.9)
	else: histogram.GetYaxis().SetRangeUser(0.4,1.6)
	histogram.GetYaxis().CenterTitle()

RFile1 = TFile(templateDir+tempsig.replace(sig1,sig1))
RFile2 = TFile(templateDir+tempsig.replace(sig1,sig2))
print RFile1
bkghists = {}
bkghistsmerged = {}
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	#tagStr = tagStr.replace('nH','nT')
	#modTag = modTag.replace('nH','nT')
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr='is'+isEM+'_'+tagStr
		histPrefix+=catStr
		print histPrefix
		totBkg = 0.
		for proc in bkgProcList: 
			try: 				
				bkghists[proc+catStr] = RFile1.Get(histPrefix+'__'+proc).Clone()
				totBkg += bkghists[proc+catStr].Integral()
			except:
				print "There is no "+proc+"!!!!!!!!"
				print "tried to open "+histPrefix+'__'+proc
				pass
		hData = RFile1.Get(histPrefix+'__DATA').Clone()
		histrange = [hData.GetBinLowEdge(1),hData.GetBinLowEdge(hData.GetNbinsX()+1)]
		gaeData = TGraphAsymmErrors(hData.Clone(hData.GetName().replace('DATA','gaeDATA')))
		hsig1 = RFile1.Get(histPrefix+'__sig').Clone(histPrefix+'__sig1')
		hsig2 = RFile2.Get(histPrefix+'__sig').Clone(histPrefix+'__sig2')
		hsig1.Scale(xsec[sig1])
		hsig2.Scale(xsec[sig2])
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

		if doNormByBinWidth: poissonNormByBinWidth(gaeBkgHT,bkgHT)
		else: poissonErrors(gaeBkgHT)

		if doAllSys:
			q2list = []
			if doQ2sys: q2list=['q2']
			#print systematicList
			for syst in systematicList+q2list:
				#print syst
				for ud in ['minus','plus']:
					for proc in bkgProcList:
						try: 
							systHists[proc+catStr+syst+ud] = RFile1.Get(histPrefix+'__'+proc+'__'+syst+'__'+ud).Clone()
							if doNormByBinWidth: normByBinWidth(systHists[proc+catStr+syst+ud])
						except: pass

		totBkgTemp1[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
		
		for ibin in range(1,bkghists[bkgProcList[0]+catStr].GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorStatUp = gaeBkgHT.GetErrorYhigh(ibin-1)**2
			errorStatDn = gaeBkgHT.GetErrorYlow(ibin-1)**2
			errorNorm = 0.
			for proc in bkgProcList:
				try: errorNorm += getNormUnc(bkghists[proc+catStr],ibin,modelingSys[proc+'_'+modTag])
				except: pass

			if doAllSys:
				q2list=[]
				if doQ2sys: q2list=['q2']
				for syst in systematicList+q2list:
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
		sig2Color= kRed
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
		gaeData.SetMaximum(1.25*max(gaeData.GetMaximum(),bkgHT.GetMaximum()))
		gaeData.SetMinimum(0.015)
		gaeData.SetTitle("")
		if doNormByBinWidth: gaeData.GetYaxis().SetTitle("Events / 1 GeV")
		else: gaeData.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(gaeData)
		uPad.cd()
		gaeData.SetTitle("")
		if compareShapes: 
			hsig1.Scale(totBkg/hsig1.Integral())
			hsig2.Scale(totBkg/hsig2.Integral())
		if not blind: gaeData.Draw("apz")
		if blind: 
			hsig1.SetMinimum(0.015)
			if doNormByBinWidth: hsig1.GetYaxis().SetTitle("Events / 1 GeV")
			else: hsig1.GetYaxis().SetTitle("Events / bin")
			hsig1.SetMaximum(hData.GetMaximum())
			if iPlot=='Tau21Nm1': hsig1.SetMaximum(1.4*hData.GetMaximum())
			formatUpperHist(hsig1)
			hsig1.Draw("HIST")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("Events / 1 GeV")
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
		if tag[0]!='0p': 
			if '1b' in tag[0]: tagString+='1b H, '
			elif '2b' in tag[0]: tagString+='2b H, '
			else: tagString+=tag[0]+' H, '
		if tag[1]!='0p': 
			if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
			else: tagString+=tag[1]+' W, '
		if tag[2]!='0p': 
			if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
			else: tagString+=tag[2]+' b, '
		if tag[3]!='3p': 
			if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
			else: tagString+=tag[3]+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]		
		chLatex.DrawLatex(0.28, 0.84, flvString)
		if iPlot != 'YLD': chLatex.DrawLatex(0.28, 0.78, tagString)

		if drawQCD: 
			leg = TLegend(0.45,0.52,0.95,0.87)
			if iPlot == 'deltaRAK8': leg = TLegend(0.15,0.52,0.55,0.82)
		if not drawQCD or blind: 
			leg = TLegend(0.45,0.64,0.95,0.89)
			if iPlot == 'deltaRAK8': leg = TLegend(0.15,0.52,0.55,0.82)
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
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			leg.AddEntry(bkghists['qcd'+catStr],"QCD","f")
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			try: leg.AddEntry(bkghists['ewk'+catStr],"EW","f")
			except: pass
			leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f")
			try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
			except: pass
			if not blind: 
				leg.AddEntry(0, "", "")
				leg.AddEntry(gaeData,"Data","pel")
				
		if not drawQCD:
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			try: leg.AddEntry(bkghists['ewk'+catStr],"EW","f")
			except: pass
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
			except: pass
			leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f")
			if not blind: leg.AddEntry(gaeData,"Data","pel")
		leg.Draw("same")

		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.05)
		if blind: prelimTex.SetTextSize(0.05)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")

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
		if not blind: prelimTex3.DrawLatex(0.23,0.945,"Preliminary")
		if blind: prelimTex3.DrawLatex(0.26,0.945,"Preliminary")

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
			formatLowerHist(pull)
			pull.Draw("E0")

			# DO A FIT to the histogram named "pull" = hData/bkgHT
			fit = False
			flat = TF1("flat","pol0",2500,5000);
			line = TF1("line","pol1",300,2700);

			line.SetLineWidth(2);

			if fit:
				fitresult = pull.Fit("line","RS")
				cov = fitresult.GetCovarianceMatrix()
				p0p0cov = cov(0,0)
				p0p1cov = cov(0,1)
				p1p1cov = cov(1,1)
				print 'covariance p0-p0 =',p0p0cov
				print 'covariance p0-p1 =',p0p1cov
				print 'covariance p1-p1 =',p1p1cov
				fitresult = pull.Fit("flat","R+S")
				cov = fitresult.GetCovarianceMatrix()
				p0p0cov = cov(0,0)
				p0p1cov = cov(0,1)
				p1p1cov = cov(1,1)
				print 'covariance p0-p0 =',p0p0cov
				print 'covariance p0-p1 =',p0p1cov
				print 'covariance p1-p1 =',p1p1cov
				'''
				****************************************
				Minimizer is Linear
				Chi2                      =      9.97134
				NDf                       =            9
				p0                        =      1.09771   +/-   0.0384644   
				p1                        = -0.000517529   +/-   9.94895e-05 
				covariance p0-p0 = 0.0014795109823
				covariance p0-p1 = -3.6104869696e-06
				covariance p1-p1 = 9.89815635815e-09
				******************************

				jsf = TF1("jsf","1.09383 - 0.00047777*x",250,730)
				jsf2 = TF1("jsf2","0.747382",720,1500);
				jsfup = TF1("jsfup","max(0.747382 + 0.164524,1.09383 - 0.000477777*x + sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06))",250,1500)
				jsfdn = TF1("jsfdn","max(0.747382 - 0.164524,1.09383 - 0.000477777*x - sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06))",250,1500)
				jsfup2 =TF1("jsfup2","0.747382 + 0.164524",725,1500);
				jsfdn2 =TF1("jsfdn2","0.747382 - 0.164524",725,1500);

				jsf0b = TF1("jsf0b","1.24507 - 0.000664768*x",350,1030)
				jsf20b = TF1("jsf20b","0.568135",1015,1500);
				jsfup0b = TF1("jsfup0b","max(0.568135 + 0.052292,1.24507 - 0.000664768*x + sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06))",350,1500)
				jsfdn0b = TF1("jsfdn0b","max(0.568135 - 0.052292,1.24507 - 0.000664768*x - sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06))",350,1500)
#				jsfup0b = TF1("jsfup0b","max(max(0.747382 + 0.164524,1.09383 - 0.000477777*x + sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06)),max(0.568135 + 0.052292,1.24507 - 0.000664768*x + sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06)))",350,1500)
#				jsfdn0b = TF1("jsfdn0b","min(max(0.747382 - 0.164524,1.09383 - 0.000477777*x - sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06)),max(0.568135 - 0.052292,1.24507 - 0.000664768*x - sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06)))",350,1500)
				jsfup20b =TF1("jsfup20b","0.568135 + 0.052292",1020,1500);
				jsfdn20b =TF1("jsfdn20b","0.568135 - 0.052292",1020,1500);

#				print 'JSFup at 250:',jsfup.Eval(250)

				jsf.SetLineColor(kRed)
				jsf.SetLineWidth(2)
				jsfup.SetLineColor(kBlue)
				jsfdn.SetLineColor(kBlue)
				jsfup.SetLineWidth(2)
				jsfdn.SetLineWidth(2)
				jsf2.SetLineColor(kRed)
				jsf2.SetLineWidth(2)
				jsfup2.SetLineColor(kBlue)
				jsfdn2.SetLineColor(kBlue)
				jsfup2.SetLineWidth(2)
				jsfdn2.SetLineWidth(2)

				pull.Draw("E1")
				jsf.Draw("same")
				jsfup.Draw("same")
				jsfdn.Draw("same")
				jsf2.Draw("same")
#				pull.Draw("E1 same")
                                '''
			
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
			#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
			#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
			pullLegend.Draw("SAME")
			pull.Draw("SAME E0")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
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
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if nttaglist[0]=='0p': savePrefix=savePrefix.replace('nt0p_','')
		if nWtaglist[0]=='0p': savePrefix=savePrefix.replace('nW0p_','')
		if nbtaglist[0]=='0p': savePrefix=savePrefix.replace('nB0p_','')
		if njetslist[0]=='0p': savePrefix=savePrefix.replace('nJ0p_','')
		if doRealPull: savePrefix+='_pull'
		if doNormByBinWidth: savePrefix+='_NBBW'
		if drawNormalized: savePrefix+='_norm'
		if yLog: savePrefix+='_logy'
		if blind: savePrefix+='_blind'
		if compareShapes: savePrefix+='_shp'

		if doOneBand:
			c1.SaveAs(savePrefix+"totBand.pdf")
			c1.SaveAs(savePrefix+"totBand.png")
			c1.SaveAs(savePrefix+"totBand.eps")
			#c1.SaveAs(savePrefix+"totBand.root")
			#c1.SaveAs(savePrefix+"totBand.C")
		else:
			c1.SaveAs(savePrefix+".pdf")
			c1.SaveAs(savePrefix+".png")
			c1.SaveAs(savePrefix+".eps")
			#c1.SaveAs(savePrefix+".root")
			#c1.SaveAs(savePrefix+".C")
		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass
					
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_isE_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_isM_'+tagStr
	totBkgMerged = 0.
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFile1.Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFile1.Get(histPrefixM+'__'+proc))
			totBkgMerged += bkghistsmerged[proc+'isL'+tagStr].Integral()
		except:pass
	hDatamerged = RFile1.Get(histPrefixE+'__DATA').Clone()
	hsig1merged = RFile1.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig1merged')
	hsig2merged = RFile2.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig2merged')
	hDatamerged.Add(RFile1.Get(histPrefixM+'__DATA').Clone())
	hsig1merged.Add(RFile1.Get(histPrefixM+'__sig').Clone())
	hsig2merged.Add(RFile2.Get(histPrefixM+'__sig').Clone())
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

	if doNormByBinWidth: poissonNormByBinWidth(gaeBkgHTmerged,bkgHTmerged)
	else: poissonErrors(gaeBkgHTmerged)

	if doAllSys:
		q2list=[]
		if doQ2sys: q2list=['q2']
		for syst in systematicList+q2list:
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
		for proc in bkgProcList:
			try: errorNorm += getNormUnc(bkghistsmerged[proc+'isL'+tagStr],ibin,modelingSys[proc+'_'+modTag])
			except: pass

		if doAllSys:
			q2list=[]
			if doQ2sys: q2list=['q2']
			for syst in systematicList+q2list:
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
	gaeDatamerged.SetMaximum(1.25*max(gaeDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	gaeDatamerged.SetMinimum(0.015)
	if doNormByBinWidth: gaeDatamerged.GetYaxis().SetTitle("Events / 1 GeV")
	else: gaeDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(gaeDatamerged)
	uPad.cd()
	gaeDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if compareShapes: 
		hsig1merged.Scale(totBkgMerged/hsig1merged.Integral())
		hsig2merged.Scale(totBkgMerged/hsig2merged.Integral())
	if not blind: gaeDatamerged.Draw("apz")
	if blind: 
		hsig1merged.SetMinimum(0.015)
		if doNormByBinWidth: hsig1merged.GetYaxis().SetTitle("Events / 1 GeV")
		else: hsig1merged.GetYaxis().SetTitle("Events / bin")
		hsig1merged.SetMaximum(hDatamerged.GetMaximum())
		if iPlot=='Tau21Nm1': hsig1merged.SetMaximum(1.4*hDatamerged.GetMaximum())
		formatUpperHist(hsig1merged)
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
	if tag[0]!='0p':
		if '1b' in tag[0]: tagString+='1b H, '
		elif '2b' in tag[0]: tagString+='2b H, '
		else: tagString+=tag[0]+' H,  '
	if tag[1]!='0p':
		if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
		else: tagString+=tag[1]+' W, '
	if tag[2]!='0p':
		if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
		else: tagString+=tag[2]+' b, '
	if tag[3]!='3p':
		if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
		else: tagString+=tag[3]+' j'
	if tagString.endswith(', '): tagString = tagString[:-2]
	chLatexmerged.DrawLatex(0.28, 0.85, flvString)
	if iPlot != 'YLD':chLatexmerged.DrawLatex(0.28, 0.78, tagString)

	if drawQCDmerged: 
		legmerged = TLegend(0.45,0.52,0.95,0.87)
		if iPlot == 'deltaRAK8': legmerged = TLegend(0.15,0.52,0.55,0.82)
	if not drawQCDmerged or blind: 
		legmerged = TLegend(0.45,0.64,0.95,0.89)
		if iPlot == 'deltaRAK8': legmerged = TLegend(0.15,0.52,0.55,0.82)
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
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		legmerged.AddEntry(bkghistsmerged['qcdisL'+tagStr],"QCD","f")
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EW","f")
		except: pass
		if not blind: 
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f")
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
			legmerged.AddEntry(0, "", "")
			legmerged.AddEntry(hDatamerged,"Data","pel")
		else:
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f")
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
	if not drawQCDmerged:
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EW","f")
		except: pass
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
		except: pass
		legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f")
		if not blind: legmerged.AddEntry(hDatamerged,"Data","pel")
	legmerged.Draw("same")

	prelimTex=TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.05)
	if blind: prelimTex.SetTextSize(0.05)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")
	
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
	if not blind: prelimTex3.DrawLatex(0.23,0.945,"Preliminary")
	if blind: prelimTex3.DrawLatex(0.26,0.945,"Preliminary")
	
	if blind == False and not doRealPull:
		lPad.cd()

		bigbins = array('d',[0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 1080, 1140, 1200, 1260, 1320, 1380, 1440, 1500, 1560, 1620, 1680, 1740, 1800, 1860, 1920, 1980, 2040, 2100, 2160, 2220, 2280, 2340, 2400, 2460, 2520, 2640, 2760, 2880, 3000, 3200, 3500, 4000, 5000])
		#Rebin(len(xbins[chn])-1,hist,xbins[chn])
		print 'hDatamerged Nbins = ',hDatamerged.GetNbinsX()

		tempData = hDatamerged.Rebin(len(bigbins)-1,'tempData',bigbins)
		tempBkg = bkgHTmerged.Rebin(len(bigbins)-1,'tempBkg',bigbins)
		print 'tempData Nbins = ',tempData.GetNbinsX()

		pullmerged = tempData.Clone("pullmerged")
		pullmerged.Divide(tempData,tempBkg)
		for binNo in range(0,tempData.GetNbinsX()+2):
			if tempBkg.GetBinContent(binNo)!=0:
				pull.SetBinError(binNo,tempData.GetBinError(binNo)/tempBkg.GetBinContent(binNo))

		# pullmerged=hDatamerged.Clone("pullmerged")
		# pullmerged.Divide(hDatamerged, bkgHTmerged)
		# for binNo in range(0,hDatamerged.GetNbinsX()+2):
		# 	if bkgHTmerged.GetBinContent(binNo)!=0:
		# 		pull.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(0)
		pullmerged.SetFillColor(1)
		pullmerged.SetLineColor(1)
		formatLowerHist(pullmerged)
		pullmerged.Draw("E0")


		# DO A FIT to the histogram named "pull" = hData/bkgHT
		fit = True
		flat = TF1("flat","pol0",2760,5000);
		line = TF1("line","pol1",300,2700);
		poly = TF1("poly","pol3",120,3500);
		#poly = TF1("poly","pol3",300,5000);

		line.SetLineWidth(2);

		if fit:
			# pullmerged.Fit("poly","R")
			fitresult = pullmerged.Fit("poly","RS")
			cov = fitresult.GetCovarianceMatrix()
			p0p0cov = cov(0,0)
			p0p1cov = cov(0,1)
			p0p2cov = cov(0,2)
			p0p3cov = cov(0,3)
			p1p1cov = cov(1,1)
			p1p2cov = cov(1,2)
			p1p3cov = cov(1,3)
			p2p2cov = cov(2,2)
			p2p3cov = cov(2,3)
			p3p3cov = cov(3,3)
			print 'covariance p0-p0 =',p0p0cov
			print 'covariance p0-p1 =',p0p1cov
			print 'covariance p0-p2 =',p0p2cov
			print 'covariance p0-p3 =',p0p3cov
			print 'covariance p1-p1 =',p1p1cov
			print 'covariance p1-p2 =',p1p2cov
			print 'covariance p1-p3 =',p1p3cov
			print 'covariance p2-p2 =',p2p2cov
			print 'covariance p2-p3 =',p2p3cov
			print 'covariance p3-p3 =',p3p3cov
			# fitresult = pullmerged.Fit("flat","R+S")
			pullmerged.Fit("flat","R+S")
			# cov = fitresult.GetCovarianceMatrix()
			# p0p0cov = cov(0,0)
			# print 'covariance p0-p0 =',p0p0cov
			'''
			****************************************
			Minimizer is Linear
			Chi2                      =      9.97134
			NDf                       =            9
			p0                        =      1.09771   +/-   0.0384644   
			p1                        = -0.000517529   +/-   9.94895e-05 
			covariance p0-p0 = 0.0014795109823
			covariance p0-p1 = -3.6104869696e-06
			covariance p1-p1 = 9.89815635815e-09
			******************************
			
			jsf = TF1("jsf","1.09383 - 0.00047777*x",250,730)
			jsf2 = TF1("jsf2","0.747382",720,1500);
			jsfup = TF1("jsfup","max(0.747382 + 0.164524,1.09383 - 0.000477777*x + sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06))",250,1500)
			jsfdn = TF1("jsfdn","max(0.747382 - 0.164524,1.09383 - 0.000477777*x - sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06))",250,1500)
			jsfup2 =TF1("jsfup2","0.747382 + 0.164524",725,1500);
			jsfdn2 =TF1("jsfdn2","0.747382 - 0.164524",725,1500);

			jsf.SetLineColor(kRed)
			jsf.SetLineWidth(2)
			jsfup.SetLineColor(kBlue)
			jsfdn.SetLineColor(kBlue)
			jsfup.SetLineWidth(2)
			jsfdn.SetLineWidth(2)
			jsf2.SetLineColor(kRed)
			jsf2.SetLineWidth(2)
			jsfup2.SetLineColor(kBlue)
			jsfdn2.SetLineColor(kBlue)
			jsfup2.SetLineWidth(2)
			jsfdn2.SetLineWidth(2)
			
			pull.Draw("E1")
			jsf.Draw("same")
			jsfup.Draw("same")
			jsfdn.Draw("same")
			jsf2.Draw("same")
			#				pull.Draw("E1 same")
			'''
		
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
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if nttaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nt0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	if doRealPull: savePrefixmerged+='_pull'
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if drawNormalized: savePrefix+='_norm'
	if yLog: savePrefixmerged+='_logy'
	if blind: savePrefixmerged+='_blind'
	if compareShapes: savePrefixmerged+='_shp'

	if doOneBand: 
		c1merged.SaveAs(savePrefixmerged+"totBand.pdf")
		c1merged.SaveAs(savePrefixmerged+"totBand.png")
		c1merged.SaveAs(savePrefixmerged+"totBand.eps")
		#c1merged.SaveAs(savePrefixmerged+"totBand.root")
		#c1merged.SaveAs(savePrefixmerged+"totBand.C")
	else: 
		c1merged.SaveAs(savePrefixmerged+".pdf")
		c1merged.SaveAs(savePrefixmerged+".png")
		c1merged.SaveAs(savePrefixmerged+".eps")
		#c1merged.SaveAs(savePrefixmerged+".root")
		#c1merged.SaveAs(savePrefixmerged+".C")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass
			
RFile1.Close()
RFile2.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


