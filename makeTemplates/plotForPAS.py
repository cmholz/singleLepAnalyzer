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

lumi=2.3 #for plots
lumiInTemplates=str(targetlumi/1000).replace('.','p') # 1/fb

discriminant = 'minMlb'
cutString=''#finalsel'
saveKey = ''#'_topPtSystOnly'

m1 = '800'
sig1='TTM'+m1 # choose the 1st signal to plot
sig1leg='TT (0.8 TeV)'
m2 = '1200'
sig2='TTM'+m2 # choose the 2nd signal to plot
sig2leg='TT (1.2 TeV)'
scaleSignals = False

systematicList = ['pileup','jec','jer','btag','mistag','tau21','pdfNew','muRFcorrdNew','taupt','jsf','jmr','jms']
doAllSys = True
doQ2sys  = False
if not doAllSys: doQ2sys = False # I assume you don't want Q^2 as well if you are not doing the other shape systematics! (this is just to change one bool)

isRebinned='_rebinned_stat0p3'#post fix for file names if the name changed b/c of rebinning or some other process
doNormByBinWidth=True # not tested, may not work out of the box
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = False
yLog  = True
doRealPull = True
if doRealPull: doOneBand=False

templateDir=os.getcwd()+'/templates_minMlb_PaperARC_fixes/'+cutString+'/'
tempsig='templates_'+discriminant+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'	

isEMlist =['E','M']
nttaglist=['0p']
nWtaglist=['0','1p']
nbtaglist=['0','1','2','3p']
tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist))

lumiSys = 0.023 #2.7% lumi uncertainty
trigSys = 0.05 #5% trigger uncertainty
lepIdSys = 0.01 #1% lepton id uncertainty
lepIsoSys = 0.01 #1% lepton isolation uncertainty
topXsecSys = 0.#0.055 #5.5% top x-sec uncertainty --> covered by PDF and muRF uncertainties
ewkXsecSys = 0.#0.05 #5% ewk x-sec uncertainty --> covered by PDF and muRF uncertainties
qcdXsecSys = 0.#0.50 #50% qcd x-sec uncertainty --> covered by PDF and muRF uncertainties
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)
topModelingSys = { #top modeling uncertainty from ttbar CR (correlated across e/m)
			     'top_nT0p_nW0_nB0' :0.125,
			     'top_nT0p_nW0_nB1' :0.080,
			     'top_nT0p_nW0_nB2' :0.055,
			     'top_nT0p_nW0_nB2p':0.055,
			     'top_nT0p_nW0_nB3p':0.055,
			     'top_nT0p_nW1p_nB0' :0.125,
			     'top_nT0p_nW1p_nB1' :0.080,
			     'top_nT0p_nW1p_nB2' :0.055,
			     'top_nT0p_nW1p_nB2p':0.055,
			     'top_nT0p_nW1p_nB3p':0.055,
			     }
ewkModelingSys = { #ewk modeling uncertainty from wjets CR (correlated across e/m)		
			     'ewk_nT0p_nW0_nB0' :0.208,
			     'ewk_nT0p_nW0_nB1' :0.208,
			     'ewk_nT0p_nW0_nB2' :0.208,
			     'ewk_nT0p_nW0_nB2p':0.208,
			     'ewk_nT0p_nW0_nB3p':0.208,
			     'ewk_nT0p_nW1p_nB0' :0.038,
			     'ewk_nT0p_nW1p_nB1' :0.038,
			     'ewk_nT0p_nW1p_nB2' :0.038,
			     'ewk_nT0p_nW1p_nB2p':0.038,
			     'ewk_nT0p_nW1p_nB3p':0.038,
			     }

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	if 'top' in hist.GetName(): error += topXsecSys*topXsecSys*contentsquared # cross section
	if 'ewk' in hist.GetName(): error += ewkXsecSys*ewkXsecSys*contentsquared # cross section
	if 'qcd' in hist.GetName(): error += qcdXsecSys*qcdXsecSys*contentsquared # cross section
	return error

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)

	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.08)
		histogram.GetXaxis().SetTitleSize(0.08)
		#histogram.GetXaxis().SetTitle(xTitle)
		histogram.GetYaxis().SetLabelSize(0.08)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(1.2)
		histogram.GetXaxis().SetNdivisions(506)
	else:
		histogram.GetYaxis().SetLabelSize(0.05)
		histogram.GetYaxis().SetTitleSize(0.07)
		histogram.GetYaxis().SetTitleOffset(.71)

	if 'nB0' in histogram.GetName() and 'minMlb' in histogram.GetName(): histogram.GetXaxis().SetTitle("min[M(l,j)] [GeV]")
	else: histogram.GetXaxis().SetTitle("min[M(l,b)] [GeV]")
	#histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(5.01e-5)
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		if not doNormByBinWidth: histogram.SetMaximum(200*histogram.GetMaximum())
		else: histogram.SetMaximum(25*histogram.GetMaximum())
		
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.15)
	histogram.GetXaxis().SetTitleSize(0.18)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)
	#histogram.GetXaxis().SetTitle("S_{T} (GeV)")

	histogram.GetYaxis().SetLabelSize(0.15)
	histogram.GetYaxis().SetTitleSize(0.16)
	histogram.GetYaxis().SetTitleOffset(.33)
	if not doRealPull: histogram.GetYaxis().SetTitle('Data/Bkg')
	else: histogram.GetYaxis().SetTitle('#frac{(data-bkg)}{std. dev.}')
	histogram.GetYaxis().SetNdivisions(5)
	#if doRealPull: histogram.GetYaxis().SetRangeUser(min(-1.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(1.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	if doRealPull: histogram.GetYaxis().SetRangeUser(-1.99,1.99)
	else: histogram.GetYaxis().SetRangeUser(0,2.99)
	histogram.GetYaxis().CenterTitle()

def negBinCorrection(hist): #set negative bin contents to zero and adjust the normalization
	norm0=hist.Integral()
	for iBin in range(0,hist.GetNbinsX()+2):
		if hist.GetBinContent(iBin)<0: hist.SetBinContent(iBin,0)
	if hist.Integral()!=0: hist.Scale(norm0/hist.Integral())

def normByBinWidth(result):
	result.SetBinContent(0,0)
	result.SetBinContent(result.GetNbinsX()+1,0)
	result.SetBinError(0,0)
	result.SetBinError(result.GetNbinsX()+1,0)
	
	for bin in range(1,result.GetNbinsX()+1):
		width=result.GetBinWidth(bin)
		content=result.GetBinContent(bin)
		error=result.GetBinError(bin)
		
		result.SetBinContent(bin, content/width)
		result.SetBinError(bin, error/width)

RFile1 = TFile(templateDir+tempsig.replace(sig1,sig1))
RFile2 = TFile(templateDir+tempsig.replace(sig1,sig2))
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
for tag in tagList:
	for isEM in isEMlist:
		histPrefix=discriminant+'_'+lumiInTemplates+'fb_'
		tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
		catStr='is'+isEM+'_'+tagStr
		histPrefix+=catStr
		print histPrefix
		hTOP = RFile1.Get(histPrefix+'__top').Clone()
		try: hEWK = RFile1.Get(histPrefix+'__ewk').Clone()
		except:
			print "There is no EWK!!!!!!!!"
			print "Skipping EWK....."
			pass
		try: hQCD = RFile1.Get(histPrefix+'__qcd').Clone()
		except:
			print "There is no QCD!!!!!!!!"
			print "Skipping QCD....."
			pass
		hData = RFile1.Get(histPrefix+'__DATA').Clone()
		hsig1 = RFile1.Get(histPrefix+'__sig').Clone(histPrefix+'__sig1')
		hsig2 = RFile2.Get(histPrefix+'__sig').Clone(histPrefix+'__sig2')
		hsig1.Scale(xsec[sig1])
		hsig2.Scale(xsec[sig2])
		if doNormByBinWidth:
			normByBinWidth(hTOP)
			try: normByBinWidth(hEWK)
			except: pass
			try: normByBinWidth(hQCD)
			except: pass
			normByBinWidth(hsig1)
			normByBinWidth(hsig2)
			normByBinWidth(hData)

		if doAllSys:
			for sys in systematicList:
				print sys
				for ud in ['minus','plus']:
					systHists['top'+catStr+sys+ud] = RFile1.Get(histPrefix+'__top__'+sys+'__'+ud).Clone()
					if doNormByBinWidth: normByBinWidth(systHists['top'+catStr+sys+ud])
					try: 
						systHists['ewk'+catStr+sys+ud] = RFile1.Get(histPrefix+'__ewk__'+sys+'__'+ud).Clone()
						if doNormByBinWidth: normByBinWidth(systHists['ewk'+catStr+sys+ud])
					except: pass
					try: 
						systHists['qcd'+catStr+sys+ud] = RFile1.Get(histPrefix+'__qcd__'+sys+'__'+ud).Clone()
						if doNormByBinWidth: normByBinWidth(systHists['qcd'+catStr+sys+ud])
					except: pass
		if doQ2sys:
			for ud in ['minus','plus']:
				systHists['top'+catStr+'q2'+ud] = RFile1.Get(histPrefix+'__top__q2__'+ud).Clone()
				if doNormByBinWidth: normByBinWidth(systHists['top'+catStr+'q2'+ud])
				systHists['q2'+catStr+ud] = systHists['top'+catStr+'q2'+ud].Clone()
				try:
					systHists['ewk'+catStr+'q2'+ud] = RFile1.Get(histPrefix+'__ewk').Clone()
					if doNormByBinWidth: normByBinWidth(systHists['ewk'+catStr+'q2'+ud])
					systHists['q2'+catStr+ud].Add(systHists['ewk'+catStr+'q2'+ud])
				except: pass
				try:
					systHists['qcd'+catStr+'q2'+ud] = RFile1.Get(histPrefix+'__qcd').Clone()
					if doNormByBinWidth: normByBinWidth(systHists['qcd'+catStr+'q2'+ud])
					systHists['q2'+catStr+ud].Add(systHists['qcd'+catStr+'q2'+ud])
				except: pass

		bkgHT = hTOP.Clone()
		try: bkgHT.Add(hEWK)
		except: pass
		try: bkgHT.Add(hQCD)
		except: pass

		totBkgTemp1[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
		
		for ibin in range(1,hTOP.GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorStatOnly = bkgHT.GetBinError(ibin)**2
			errorNorm = getNormUnc(hTOP,ibin,topModelingSys['top_'+tagStr])
			try: errorNorm += getNormUnc(hEWK,ibin,ewkModelingSys['ewk_'+tagStr])
			except: pass
			try: errorNorm += getNormUnc(hQCD,ibin,0.0)
			except: pass

			for sys in systematicList:
				if doAllSys:	
					errorPlus = systHists['top'+catStr+sys+'plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
					errorMinus = hTOP.GetBinContent(ibin)-systHists['top'+catStr+sys+'minus'].GetBinContent(ibin)
					if errorPlus > 0: errorUp += errorPlus**2
					else: errorDn += errorPlus**2
					if errorMinus > 0: errorDn += errorMinus**2
					else: errorUp += errorMinus**2
					if sys!='toppt':
						try:
							errorPlus = systHists['ewk'+catStr+sys+'plus'].GetBinContent(ibin)-hEWK.GetBinContent(ibin)
							errorMinus = hEWK.GetBinContent(ibin)-systHists['ewk'+catStr+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass
						try:
							errorPlus = systHists['qcd'+catStr+sys+'plus'].GetBinContent(ibin)-hQCD.GetBinContent(ibin)
							errorMinus = hQCD.GetBinContent(ibin)-systHists['qcd'+catStr+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass													
			if doQ2sys: 
				errorPlus = systHists['top'+catStr+'q2plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
				errorMinus = hTOP.GetBinContent(ibin)-systHists['top'+catStr+'q2minus'].GetBinContent(ibin)
				if errorPlus > 0: errorUp += errorPlus**2
				else: errorDn += errorPlus**2
				if errorMinus > 0: errorDn += errorMinus**2
				else: errorUp += errorMinus**2

			totBkgTemp1[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
			totBkgTemp1[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
			totBkgTemp2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
			totBkgTemp2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
			totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
			totBkgTemp3[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
		
		bkgHTgerr = totBkgTemp3[catStr].Clone()

		scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
		scaleFact2 = int(bkgHT.GetMaximum()/hsig2.GetMaximum()) - int(bkgHT.GetMaximum()/hsig2.GetMaximum()) % 10
		if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
		if scaleFact2==0: scaleFact2=int(bkgHT.GetMaximum()/hsig2.GetMaximum())
		if scaleFact1==0: scaleFact1=1
		if scaleFact2==0: scaleFact2=1
		if not scaleSignals:
			scaleFact1=1
			scaleFact2=1
# 			else:
# 				scaleFact1=25
# 				scaleFact2=25
		hsig1.Scale(scaleFact1)
		hsig2.Scale(scaleFact2)
		
		drawQCD = False
		try: drawQCD = hQCD.Integral()/bkgHT.Integral()>.005 #don't plot QCD if it is less than 0.5%
		except: pass

		stackbkgHT = THStack("stackbkgHT","")#"CMS Preliminary, 5 fb^{-1} at #sqrt{s} = 13 TeV;H_{T} (GeV)")
		try: stackbkgHT.Add(hTOP)
		except: pass
		try: stackbkgHT.Add(hEWK)
		except: pass
		try: 
			if drawQCD: stackbkgHT.Add(hQCD)
		except: pass

		topColor = kAzure+8
		ewkColor = kMagenta-2
		qcdColor = kOrange+5
		sig1Color= kBlack
		sig2Color= kBlack
		if '53' in sig1: 
			topColor = kRed-9
			ewkColor = kBlue-7
			qcdColor = kOrange-5
			sig1Color= kBlack
			sig2Color= kBlack
			
		hTOP.SetLineColor(topColor)
		hTOP.SetFillColor(topColor)
		hTOP.SetLineWidth(2)
		try: 
			hEWK.SetLineColor(ewkColor)
			hEWK.SetFillColor(ewkColor)
			hEWK.SetLineWidth(2)
		except: pass
		try:
			hQCD.SetLineColor(qcdColor)
			hQCD.SetFillColor(qcdColor)
			hQCD.SetLineWidth(2)
		except: pass
		hsig1.SetLineColor(sig1Color)
		hsig1.SetFillStyle(0)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(sig2Color)
		hsig2.SetLineStyle(7)#5)
		hsig2.SetFillStyle(0)
		hsig2.SetLineWidth(3)
		
		hData.SetMarkerStyle(20)
		hData.SetMarkerSize(1.2)
		hData.SetLineWidth(2)
		hData.SetMarkerColor(kBlack)
		hData.SetLineColor(kBlack)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(kBlack)

		gStyle.SetOptStat(0)
		c1 = TCanvas("c1","c1",600,500)
		gStyle.SetErrorX(0.5)
		yDiv=0.25
		if blind == True: yDiv=0.1
		uMargin = 0
		if blind == True: uMargin = 0.15
		rMargin=.04
		uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.10)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(.12)
		uPad.Draw()
		if blind == False:
			lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
			lPad.SetTopMargin(0)
			lPad.SetBottomMargin(.4)
			lPad.SetRightMargin(rMargin)
			lPad.SetLeftMargin(.12)
			lPad.SetGridy()
			lPad.Draw()
		if not doNormByBinWidth: hData.SetMaximum(1.2*max(hData.GetMaximum(),bkgHT.GetMaximum()))
		hData.SetMinimum(0.015)
		hData.SetTitle("")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("Events / 1 GeV")
		else: hData.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(hData)
		uPad.cd()
		hData.SetTitle("")
		if not blind: hData.Draw("E1")
		if blind: 
			hsig1.SetMinimum(0.015)
			if doNormByBinWidth: hsig1.GetYaxis().SetTitle("Events / 1 GeV")
			else: hsig1.GetYaxis().SetTitle("Events / bin")
			formatUpperHist(hsig1)
			hsig1.SetMaximum(hData.GetMaximum())
			hsig1.Draw("HIST")
		stackbkgHT.Draw("SAME HIST")
		hsig1.Draw("SAME HIST")
		hsig2.Draw("SAME HIST")
		if not blind: hData.Draw("SAME E1") #redraw data so its not hidden
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")
		
		chLatex = TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.06)
		chLatex.SetTextAlign(11) # align right
		chString = ''
		if isEM=='E': chString+='e+jets'
		if isEM=='M': chString+='#mu+jets'
		if tag[0]!='0p': 
			if 'p' in tag[0]: chString+=', #geq'+tag[0][:-1]+' t'
			else: chString+=', '+tag[0]+' t'
		if 'p' in tag[1]: chString+=', #geq'+tag[1][:-1]+' W'
		else: chString+=', '+tag[1]+' W'
		if 'p' in tag[2]: chString+=', #geq'+tag[2][:-1]+' b'
		else: chString+=', '+tag[2]+' b'
		chLatex.DrawLatex(0.16, 0.82, chString)

		if drawQCD: leg = TLegend(0.492,0.532,0.952,0.881)
		if not drawQCD: leg = TLegend(0.492,0.612,0.952,0.881)
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
			leg.AddEntry(hQCD,"QCD","f")
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			try: leg.AddEntry(hEWK,"EWK","f")
			except: pass
			if not blind: leg.AddEntry(hData,"DATA")
			try: leg.AddEntry(hTOP,"TOP","f")
			except: pass
			leg.AddEntry(0, "", "")
			#leg.AddEntry(bkgHTgerr,"MC uncert. (stat. #oplus syst.)","f")
			leg.AddEntry(bkgHTgerr,"Bkg uncert.","f")
		if not drawQCD:
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			try: leg.AddEntry(hEWK,"EWK","f")
			except: pass
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			try: leg.AddEntry(hTOP,"TOP","f")
			except: pass
			if not blind: leg.AddEntry(hData,"DATA")
			#leg.AddEntry(bkgHTgerr,"MC uncert. (stat. #oplus syst.)","f")
			leg.AddEntry(bkgHTgerr,"Bkg uncert.","f")
		leg.Draw("same")

		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.07)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.10)
		prelimTex2.DrawLatex(0.12,0.92,"CMS")

		prelimTex3=TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.075)
		prelimTex3.SetLineWidth(2)
		#if not blind: prelimTex3.DrawLatex(0.24,0.975,"Preliminary")
		#if blind: prelimTex3.DrawLatex(0.29175,0.9364,"Preliminary")

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
			pull.Draw("E1")
			
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
			
			if doQ2sys:
				pullQ2up=systHists['q2'+catStr+'plus'].Clone("pullQ2Up")
				pullQ2up.Divide(systHists['q2'+catStr+'plus'], bkgHT)
				pullQ2up.SetFillColor(0)
				pullQ2up.SetLineColor(6)
				pullQ2up.SetLineWidth(3)
				#pullQ2up.Draw("SAME HIST")
			
				pullQ2dn=systHists['q2'+catStr+'minus'].Clone("pullQ2Dn")
				pullQ2dn.Divide(systHists['q2'+catStr+'minus'], bkgHT)
				pullQ2dn.SetFillColor(0)
				pullQ2dn.SetLineColor(6)
				pullQ2dn.SetLineWidth(3)
				pullQ2dn.SetLineStyle(5)
				#pullQ2dn.Draw("SAME HIST")

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
			if not doOneBand: pullLegend.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
			else: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
			#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
			#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
			pullLegend.Draw("SAME")
			pull.Draw("SAME")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			for binNo in range(1,hData.GetNbinsX()+1):
				if hData.GetBinContent(binNo)!=0:
					MCerror = 0.5*(totBkgTemp3[catStr].GetErrorYhigh(binNo-1)+totBkgTemp3[catStr].GetErrorYlow(binNo-1))
					pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hData.GetBinError(binNo)**2))
				else: pull.SetBinContent(binNo,0.)
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
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plotsForPaperHalved/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned+saveKey
		if doRealPull: savePrefix+='_pull'
		if doNormByBinWidth: savePrefix+='_NBBW'
		if yLog: savePrefix+='_logy'

		if doOneBand:
			c1.SaveAs(savePrefix+"totBand.pdf")
			c1.SaveAs(savePrefix+"totBand.png")
			c1.SaveAs(savePrefix+"totBand.root")
			c1.SaveAs(savePrefix+"totBand.C")
		else:
			c1.SaveAs(savePrefix+".pdf")
			c1.SaveAs(savePrefix+".png")
			c1.SaveAs(savePrefix+".root")
			c1.SaveAs(savePrefix+".C")
		try: del hTOP
		except: pass
		try: del hEWK
		except: pass
		try: del hQCD
		except: pass
					
	#plot e/m combined
	histPrefixE = discriminant+'_'+lumiInTemplates+'fb_isE_'+tagStr
	histPrefixM = discriminant+'_'+lumiInTemplates+'fb_isM_'+tagStr
	hTOPmerged = RFile1.Get(histPrefixE+'__top').Clone()
	hTOPmerged.Add(RFile1.Get(histPrefixM+'__top'))
	try: 
		hEWKmerged = RFile1.Get(histPrefixE+'__ewk').Clone()
		hEWKmerged.Add(RFile1.Get(histPrefixM+'__ewk'))
	except:pass
	try: 
		hQCDmerged = RFile1.Get(histPrefixE+'__qcd').Clone()
		hQCDmerged.Add(RFile1.Get(histPrefixM+'__qcd').Clone())
	except:pass
	hDatamerged = RFile1.Get(histPrefixE+'__DATA').Clone()
	hsig1merged = RFile1.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig1merged')
	hsig2merged = RFile2.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig2merged')
	hDatamerged.Add(RFile1.Get(histPrefixM+'__DATA').Clone())
	hsig1merged.Add(RFile1.Get(histPrefixM+'__sig').Clone())
	hsig2merged.Add(RFile2.Get(histPrefixM+'__sig').Clone())
	hsig1merged.Scale(xsec[sig1])
	hsig2merged.Scale(xsec[sig2])
	if doNormByBinWidth:
		normByBinWidth(hTOPmerged)
		normByBinWidth(hEWKmerged)
		try: normByBinWidth(hQCDmerged)
		except: pass
		normByBinWidth(hsig1merged)
		normByBinWidth(hsig2merged)
		normByBinWidth(hDatamerged)

	if doAllSys:
		for sys in systematicList:
			for ud in ['minus','plus']:
				systHists['toplep'+tagStr+sys+ud] = systHists['topisE_'+tagStr+sys+ud].Clone()
				systHists['toplep'+tagStr+sys+ud].Add(systHists['topisM_'+tagStr+sys+ud])
				try: 
					systHists['ewklep'+tagStr+sys+ud] = systHists['ewkisE_'+tagStr+sys+ud].Clone()
					systHists['ewklep'+tagStr+sys+ud].Add(systHists['ewkisM_'+tagStr+sys+ud])
				except: pass
				try: 
					systHists['qcdlep'+tagStr+sys+ud] = systHists['qcdisE_'+tagStr+sys+ud].Clone()
					systHists['qcdlep'+tagStr+sys+ud].Add(systHists['qcdisM_'+tagStr+sys+ud])
				except: pass
	if doQ2sys:
		for ud in ['minus','plus']:
			systHists['toplep'+tagStr+'q2'+ud] = systHists['topisE_'+tagStr+'q2'+ud].Clone()
			systHists['toplep'+tagStr+'q2'+ud].Add(systHists['topisM_'+tagStr+'q2'+ud])
			systHists['q2lep'+tagStr+'q2'+ud] = systHists['toplep'+tagStr+'q2'+ud].Clone()
			try:
				systHists['ewklep'+tagStr+'q2'+ud] = systHists['ewkisE_'+tagStr+'q2'+ud].Clone()
				systHists['ewklep'+tagStr+'q2'+ud].Add(systHists['ewkisM_'+tagStr+'q2'+ud])
				systHists['q2lep'+tagStr+'q2'+ud].Add(systHists['ewklep'+tagStr+'q2'+ud])
			except: pass
			try:
				systHists['qcdlep'+tagStr+'q2'+ud] = systHists['qcdisE_'+tagStr+'q2'+ud].Clone()
				systHists['qcdlep'+tagStr+'q2'+ud].Add(systHists['qcdisM_'+tagStr+'q2'+ud])
				systHists['q2lep'+tagStr+'q2'+ud].Add(systHists['qcdlep'+tagStr+'q2'+ud])
			except: pass

	bkgHTmerged = hTOPmerged.Clone()
	try: bkgHTmerged.Add(hEWKmerged)
	except: pass
	try: bkgHTmerged.Add(hQCDmerged)
	except: pass

	totBkgTemp1['lep'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
	totBkgTemp2['lep'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
	totBkgTemp3['lep'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))
	
	for ibin in range(1,hTOPmerged.GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatOnly = bkgHTmerged.GetBinError(ibin)**2
		errorNorm = getNormUnc(hTOPmerged,ibin,topModelingSys['top_'+tagStr])
		try: errorNorm += getNormUnc(hEWKmerged,ibin,ewkModelingSys['ewk_'+tagStr])
		except: pass
		try: errorNorm += getNormUnc(hQCDmerged,ibin,0.0)
		except: pass

		for sys in systematicList:
			if doAllSys:	
				errorPlus = systHists['toplep'+tagStr+sys+'plus'].GetBinContent(ibin)-hTOPmerged.GetBinContent(ibin)
				errorMinus = hTOPmerged.GetBinContent(ibin)-systHists['toplep'+tagStr+sys+'minus'].GetBinContent(ibin)
				if errorPlus > 0: errorUp += errorPlus**2
				else: errorDn += errorPlus**2
				if errorMinus > 0: errorDn += errorMinus**2
				else: errorUp += errorMinus**2
				if sys!='toppt':
					try:
						errorPlus = systHists['ewklep'+tagStr+sys+'plus'].GetBinContent(ibin)-hEWKmerged.GetBinContent(ibin)
						errorMinus = hEWKmerged.GetBinContent(ibin)-systHists['ewklep'+tagStr+sys+'minus'].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass
					try:
						errorPlus = systHists['qcdlep'+tagStr+sys+'plus'].GetBinContent(ibin)-hQCDmerged.GetBinContent(ibin)
						errorMinus = hQCDmerged.GetBinContent(ibin)-systHists['qcdlep'+tagStr+sys+'minus'].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass													
		if doQ2sys: 
			errorPlus = systHists['toplep'+tagStr+'q2plus'].GetBinContent(ibin)-hTOPmerged.GetBinContent(ibin)
			errorMinus = hTOPmerged.GetBinContent(ibin)-systHists['toplep'+tagStr+'q2minus'].GetBinContent(ibin)
			if errorPlus > 0: errorUp += errorPlus**2
			else: errorDn += errorPlus**2
			if errorMinus > 0: errorDn += errorMinus**2
			else: errorUp += errorMinus**2

		totBkgTemp1['lep'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
		totBkgTemp1['lep'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
		totBkgTemp2['lep'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
		totBkgTemp2['lep'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
		totBkgTemp3['lep'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
		totBkgTemp3['lep'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
	
	bkgHTgerrmerged = totBkgTemp3['lep'+tagStr].Clone()

	scaleFact1merged = int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) % 10
	scaleFact2merged = int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) % 10
	if scaleFact1merged==0: scaleFact1merged=int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum())
	if scaleFact2merged==0: scaleFact2merged=int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum())
	if scaleFact1merged==0: scaleFact1merged=1
	if scaleFact2merged==0: scaleFact2merged=1
	if not scaleSignals:
		scaleFact1merged=1
		scaleFact2merged=1
	hsig1merged.Scale(scaleFact1merged)
	hsig2merged.Scale(scaleFact2merged)
	
	drawQCDmerged = False
	try: drawQCDmerged = hQCDmerged.Integral()/bkgHTmerged.Integral()>.005
	except: pass

	stackbkgHTmerged = THStack("stackbkgHTmerged","")#"CMS Preliminary, 5 fb^{-1} at #sqrt{s} = 13 TeV;H_{T} (GeV)")
	try: stackbkgHTmerged.Add(hTOPmerged)
	except: pass
	try: stackbkgHTmerged.Add(hEWKmerged)
	except: pass
	try: 
		if drawQCDmerged: stackbkgHTmerged.Add(hQCDmerged)
	except: pass

	hTOPmerged.SetLineColor(topColor)
	hTOPmerged.SetFillColor(topColor)
	hTOPmerged.SetLineWidth(2)
	try: 
		hEWKmerged.SetLineColor(ewkColor)
		hEWKmerged.SetFillColor(ewkColor)
		hEWKmerged.SetLineWidth(2)
	except: pass
	try:
		hQCDmerged.SetLineColor(qcdColor)
		hQCDmerged.SetFillColor(qcdColor)
		hQCDmerged.SetLineWidth(2)
	except: pass
	hsig1merged.SetLineColor(sig1Color)
	hsig1merged.SetFillStyle(0)
	hsig1merged.SetLineWidth(3)
	hsig2merged.SetLineColor(sig2Color)
	hsig2merged.SetLineStyle(7)#5)
	hsig2merged.SetFillStyle(0)
	hsig2merged.SetLineWidth(3)
	
	hDatamerged.SetMarkerStyle(20)
	hDatamerged.SetMarkerSize(1.2)
	hDatamerged.SetLineWidth(2)
	hDatamerged.SetMarkerColor(kBlack)
	hDatamerged.SetLineColor(kBlack)

	bkgHTgerrmerged.SetFillStyle(3004)
	bkgHTgerrmerged.SetFillColor(kBlack)

	gStyle.SetOptStat(0)
	c1merged = TCanvas("c1merged","c1merged",600,500)
	gStyle.SetErrorX(0.5)
	yDiv=0.25
	if blind == True: yDiv=0.1
	uMargin = 0
	if blind == True: uMargin = 0.15
	rMargin=.04
	uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
	uPad.SetTopMargin(0.10)
	uPad.SetBottomMargin(uMargin)
	uPad.SetRightMargin(rMargin)
	uPad.SetLeftMargin(.12)
	uPad.Draw()
	if blind == False:
		lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
		lPad.SetTopMargin(0)
		lPad.SetBottomMargin(.4)
		lPad.SetRightMargin(rMargin)
		lPad.SetLeftMargin(.12)
		lPad.SetGridy()
		lPad.Draw()
	if not doNormByBinWidth: hDatamerged.SetMaximum(1.2*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	hDatamerged.SetMinimum(0.015)
	if doNormByBinWidth: hDatamerged.GetYaxis().SetTitle("Events / 1 GeV")
	else: hDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(hDatamerged)
	uPad.cd()
	hDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if not blind: hDatamerged.Draw("E1")
	if blind: 
		sighist1RHmerged.SetMinimum(0.015)
		if doNormByBinWidth: sighist1RHmerged.GetYaxis().SetTitle("Events / 1 GeV")
		else: sighist1RHmerged.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(sighist1RHmerged)
		sighist1RHmerged.SetMaximum(hDatamerged.GetMaximum())
		sighist1RHmerged.Draw("HIST")
	stackbkgHTmerged.Draw("SAME HIST")
	hsig1merged.Draw("SAME HIST")
	hsig2merged.Draw("SAME HIST")
	if not blind: hDatamerged.Draw("SAME E1") #redraw data so its not hidden
	uPad.RedrawAxis()
	bkgHTgerrmerged.Draw("SAME E2")

	chLatexmerged = TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.06)
	chLatexmerged.SetTextAlign(11) # align right
	chString = 'e/#mu+jets'
	if tag[0]!='0p':
		if 'p' in tag[0]: chString+=', #geq'+tag[0][:-1]+' t'
		else: chString+=', '+tag[0]+' t'
	if 'p' in tag[1]: chString+=', #geq'+tag[1][:-1]+' W'
	else: chString+=', '+tag[1]+' W'
	if 'p' in tag[2]: chString+=', #geq'+tag[2][:-1]+' b'
	else: chString+=', '+tag[2]+' b'
	chLatexmerged.DrawLatex(0.16, 0.82, chString)

	if drawQCDmerged: legmerged = TLegend(0.492,0.532,0.952,0.881)
	if not drawQCDmerged: legmerged = TLegend(0.492,0.612,0.952,0.881)
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
		legmerged.AddEntry(hQCDmerged,"QCD","f")
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		try: legmerged.AddEntry(hEWKmerged,"EWK","f")
		except: pass
		if not blind: legmerged.AddEntry(hDatamerged,"DATA")
		try: legmerged.AddEntry(hTOPmerged,"TOP","f")
		except: pass
		legmerged.AddEntry(0, "", "")
		#legmerged.AddEntry(bkgHTgerrmerged,"MC uncert. (stat. #oplus syst.)","f")
		legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert.","f")
	if not drawQCDmerged:
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		try: legmerged.AddEntry(hEWKmerged,"EWK","f")
		except: pass
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		try: legmerged.AddEntry(hTOPmerged,"TOP","f")
		except: pass
		if not blind: legmerged.AddEntry(hDatamerged,"DATA")
		#legmerged.AddEntry(bkgHTgerrmerged,"MC uncert. (stat. #oplus syst.)","f")
		legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert.","f")
	legmerged.Draw("same")

	prelimTex=TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.07)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")

	prelimTex2=TLatex()
	prelimTex2.SetNDC()
	prelimTex2.SetTextFont(61)
	prelimTex2.SetLineWidth(2)
	prelimTex2.SetTextSize(0.10)
	prelimTex2.DrawLatex(0.12,0.92,"CMS")

	prelimTex3=TLatex()
	prelimTex3.SetNDC()
	prelimTex3.SetTextAlign(13)
	prelimTex3.SetTextFont(52)
	prelimTex3.SetTextSize(0.075)
	prelimTex3.SetLineWidth(2)
	#if not blind: prelimTex3.DrawLatex(0.24,0.975,"Preliminary")
	#if blind: prelimTex3.DrawLatex(0.29175,0.9364,"Preliminary")

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
		formatLowerHist(pullmerged)
		pullmerged.Draw("E1")
		
		BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
		BkgOverBkgmerged.Divide(bkgHTmerged, bkgHTmerged)
		pullUncBandTotmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncTotmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['lep'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['lep'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
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
				pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['lep'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['lep'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandNormmerged.SetFillStyle(3001)
		pullUncBandNormmerged.SetFillColor(2)
		pullUncBandNormmerged.SetLineColor(2)
		pullUncBandNormmerged.SetMarkerSize(0)
		gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
		
		pullUncBandStatmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['lep'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['lep'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
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
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
		else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
		pullLegendmerged.Draw("SAME")
		pullmerged.Draw("SAME")
		lPad.RedrawAxis()

	if blind == False and doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			if hDatamerged.GetBinContent(binNo)!=0:
				MCerror = 0.5*(totBkgTemp3['lep'+tagStr].GetErrorYhigh(binNo-1)+totBkgTemp3['lep'+tagStr].GetErrorYlow(binNo-1))
				pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
			else: pullmerged.SetBinContent(binNo,0.)
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
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plotsForPaperHalved/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','lep')+isRebinned+saveKey
	if doRealPull: savePrefixmerged+='_pull'
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if yLog: savePrefixmerged+='_logy'

	if doOneBand: 
		c1merged.SaveAs(savePrefixmerged+"totBand.pdf")
		c1merged.SaveAs(savePrefixmerged+"totBand.png")
		c1merged.SaveAs(savePrefixmerged+"totBand.root")
		c1merged.SaveAs(savePrefixmerged+"totBand.C")
	else: 
		c1merged.SaveAs(savePrefixmerged+".pdf")
		c1merged.SaveAs(savePrefixmerged+".png")
		c1merged.SaveAs(savePrefixmerged+".root")
		c1merged.SaveAs(savePrefixmerged+".C")
	try: del hTOPmerged
	except: pass
	try: del hEWKmerged
	except: pass
	try: del hQCDmerged
	except: pass
			
RFile1.Close()
RFile2.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


