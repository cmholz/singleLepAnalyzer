#!/usr/bin/python

import os,sys,time,math,datetime
from numpy import linspace
import ROOT as R
from weights import *
from samples import *
import pickle

R.gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

if len(sys.argv)>2: isTTbarCR=int(sys.argv[2])
else: isTTbarCR = False # else it is Wjets

if isTTbarCR: 
	from analyzeTTJetsCR import *
else:
	from analyzeWJetsCR import *
		       
bkgStackList = ['WJets','ZJets','VV','TTW','TTZ','TTJets','T','QCD']
wjetList  = ['WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500']
zjetList  = ['DY50']
vvList    = ['WW','WZ','ZZ']
ttwList   = ['TTWl','TTWq']
ttzList   = ['TTZl','TTZq']
#ttjetList = ['TTJetsPH']
ttjetList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt']
tList     = ['Tt','Ts','TtW','TbtW']

dataList = ['DataERRC','DataERRD','DataEPRD','DataMRRC','DataMRRD','DataMPRD']

whichSignal = 'TT' #TT, BB, or T53T53
signalMassRange = [700,1800]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='T53T53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='T53T53': decays = [''] #decays to tWtW 100% of the time

#topList = ['TTJetsPH','TTWl','TTZl','TTWq','TTZq','Tt','Ts','TtW','TbtW']
topList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt','TTWl','TTZl','TTWq','TTZq','Tt','Ts','TtW','TbtW']
ewkList = ['DY50','WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500','WW','WZ','ZZ']
qcdList = ['QCDht100','QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']

scaleSignalXsecTo1pb = False # this has to be "True" if you are making templates for limit calculation!!!!!!!!
doAllSys = True
systematicList = ['pileup','jec','jer','jmr','jms','btag','tau21','pdf','pdfNew','muR','muF','muRFcorrd','toppt','jsf','muRFenv','muRFcorrdNew','muRFdecorrdNew']
normalizeRENORM_PDF = True #normalize the renormalization/pdf uncertainties to nominal templates
doQ2sys = True
q2UpList   = ['TTWl','TTZl','TTWq','TTZq','TTJetsPHQ2U','Tt','TtW','TtWQ2U','TbtWQ2U']
q2DownList = ['TTWl','TTZl','TTWq','TTZq','TTJetsPHQ2D','Tt','TtW','TtWQ2D','TbtWQ2D']

cutString  = ''#'lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
if isTTbarCR: pfix='ttbar_JECv7JSF_2016_2_15'
else: pfix='wjets_JECv7JSF_2016_2_15'
iPlot='minMlb'

outDir = os.getcwd()+'/'
outDir+=pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+outDir+'/'+cutString)
outDir+='/'+cutString

isEMlist =['E','M']
if isTTbarCR: 
	nWtaglist = ['0p']
	nbtaglist = ['0','1','2p']
else: 
	nWtaglist = ['0','1p']
	nbtaglist = ['0']

def negBinCorrection(hist): #set negative bin contents to zero and adjust the normalization
	norm0=hist.Integral()
	for iBin in range(0,hist.GetNbinsX()+2):
		if hist.GetBinContent(iBin)<0: hist.SetBinContent(iBin,0)
	if hist.Integral()!=0 and norm0>0: hist.Scale(norm0/hist.Integral())

def overflow(hist):
	nBinsX=hist.GetXaxis().GetNbins()
	content=hist.GetBinContent(nBinsX)+hist.GetBinContent(nBinsX+1)
	error=math.sqrt(hist.GetBinError(nBinsX)**2+hist.GetBinError(nBinsX+1)**2)
	hist.SetBinContent(nBinsX,content)
	hist.SetBinError(nBinsX,error)
	hist.SetBinContent(nBinsX+1,0)
	hist.SetBinError(nBinsX+1,0)

lumiSys = 0.046 #4.6% lumi uncertainty
trigSys = 0.05 #5% trigger uncertainty (increased from 3 to 5% after trigger OR suggestion)
lepIdSys = 0.01 #1% lepton id uncertainty
lepIsoSys = 0.01 #1% lepton isolation uncertainty
topXsecSys = 0.#0.055 #5.5% top x-sec uncertainty
ewkXsecSys = 0.#0.05 #5% ewk x-sec uncertainty
qcdXsecSys = 0.#0.50 #50% qcd x-sec uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)
topModelingSys = { #top modeling uncertainty from ttbar CR (correlated across e/m)
			     'top_0_0' :0.,#0.11,
			     'top_0_1' :0.,#0.11,
			     'top_0_2' :0.,#0.11,
			     'top_0_2p':0.,#0.11,
			     'top_0_3p':0.,#0.19,
			     'top_1p_0' :0.,#0.11,
			     'top_1p_1' :0.,#0.11,
			     'top_1p_2' :0.,#0.11,
			     'top_1p_2p':0.,#0.11,
			     'top_1p_3p':0.,#0.19,
			     'top_0p_0' :0.,#0.11,
			     'top_0p_1' :0.,#0.11,
			     'top_0p_2' :0.,#0.11,
			     'top_0p_2p':0.,#0.11,
			     'top_0p_3p':0.,#0.19,
			     }
ewkModelingSys = { #ewk modeling uncertainty from wjets CR (correlated across e/m)		
			     'ewk_0_0' :0.,#0.24,
			     'ewk_0_1' :0.,#0.24,
			     'ewk_0_2' :0.,#0.24,
			     'ewk_0_2p':0.,#0.24,
			     'ewk_0_3p':0.,#0.24,
			     'ewk_1p_0' :0.,#0.24,
			     'ewk_1p_1' :0.,#0.24,
			     'ewk_1p_2' :0.,#0.24,
			     'ewk_1p_2p':0.,#0.24,
			     'ewk_1p_3p':0.,#0.24,
			     'ewk_0p_0' :0.,#0.24,
			     'ewk_0p_1' :0.,#0.24,
			     'ewk_0p_2' :0.,#0.24,
			     'ewk_0p_2p':0.,#0.24,
			     'ewk_0p_3p':0.,#0.24,
			     }
addSys = {} #additional uncertainties for specific processes
for nWtag in nWtaglist:
	for nbtag in nbtaglist:
		addSys['top_'+nWtag+'_'+nbtag]   =math.sqrt(topModelingSys['top_'+nWtag+'_'+nbtag]**2+topXsecSys**2)
		addSys['TTJets_'+nWtag+'_'+nbtag]=math.sqrt(topModelingSys['top_'+nWtag+'_'+nbtag]**2+topXsecSys**2)
		addSys['T_'+nWtag+'_'+nbtag]     =math.sqrt(topModelingSys['top_'+nWtag+'_'+nbtag]**2+topXsecSys**2)
		addSys['TTW_'+nWtag+'_'+nbtag]   =math.sqrt(topModelingSys['top_'+nWtag+'_'+nbtag]**2+topXsecSys**2)
		addSys['TTZ_'+nWtag+'_'+nbtag]   =math.sqrt(topModelingSys['top_'+nWtag+'_'+nbtag]**2+topXsecSys**2)
		addSys['ewk_'+nWtag+'_'+nbtag]  =math.sqrt(ewkModelingSys['ewk_'+nWtag+'_'+nbtag]**2+ewkXsecSys**2)
		addSys['WJets_'+nWtag+'_'+nbtag]=math.sqrt(ewkModelingSys['ewk_'+nWtag+'_'+nbtag]**2+ewkXsecSys**2)
		addSys['ZJets_'+nWtag+'_'+nbtag]=math.sqrt(ewkModelingSys['ewk_'+nWtag+'_'+nbtag]**2+ewkXsecSys**2)
		addSys['VV_'+nWtag+'_'+nbtag]   =math.sqrt(ewkModelingSys['ewk_'+nWtag+'_'+nbtag]**2+ewkXsecSys**2)
		addSys['qcd_'+nWtag+'_'+nbtag]=qcdXsecSys
		addSys['QCD_'+nWtag+'_'+nbtag]=qcdXsecSys

def round_sig(x,sig=2):
	try:
		return round(x, sig-int(math.floor(math.log10(abs(x))))-1)
	except:
		return round(x,5)
			 
# def addSystematicUncertainties(hist,modelingUnc): #for plots (bin by bin uncertainty)
# 	for ibin in range(1,hist.GetNbinsX()+1):
# 		contentsquared = hist.GetBinContent(ibin)**2
# 		error = hist.GetBinError(ibin)**2
# 		error += corrdSys*corrdSys*contentsquared  #correlated uncertainties
# 		error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
# 		#if hist.GetName().split('_')[-1] in ttjetList: 
# 		if hist.GetName().endswith('top'):
# 			error += topXsecSys*topXsecSys*contentsquared # cross section
# 		#if hist.GetName().split('_')[-1] in wjetList:
# 		if hist.GetName().endswith('ewk'):
# 			error += ewkXsecSys*ewkXsecSys*contentsquared # cross section
# 		if hist.GetName().endswith('qcd'): error += qcdXsecSys*qcdXsecSys*contentsquared # cross section
# 		hist.SetBinError(ibin,math.sqrt(error))

###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeThetaCats(datahists,sighists,bkghists,discriminant):

	## This function categorizes the events into electron/muon --> 0/1p W-tag! --> 1/2p b-tag (the same as Cat1, but there is no 4p/3p jets requirement here)
	## Input  histograms (datahists,sighists,bkghists) must have corresponding histograms returned from analyze.py##

	## INITIALIZE DICTIONARIES FOR YIELDS AND THEIR UNCERTAINTIES ##
	yieldTable = {}
	yieldStatErrTable = {} #what is actually stored in this is the square of the uncertainty
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				yieldTable[histoPrefix]={}
				yieldStatErrTable[histoPrefix]={}
				if doAllSys:
					for systematic in systematicList:
						for ud in ['Up','Down']:
							yieldTable[histoPrefix+systematic+ud]={}
							
				if doQ2sys:
					yieldTable[histoPrefix+'q2Up']={}
					yieldTable[histoPrefix+'q2Down']={}

	## WRITING HISTOGRAMS IN ROOT FILE ##
	i=0
	for signal in sigList:
		outputRfile = R.TFile(outDir+'/templates_'+discriminant+'_'+signal+'_'+lumiStr+'fb.root','RECREATE')
		hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
		hwjets,hzjets,httjets,ht,httw,httz,hvv={},{},{},{},{},{},{}
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag

					#Group processes
					hwjets[str(i)] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix+'_WJets')
					hzjets[str(i)] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix+'_ZJets')
					httjets[str(i)] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix+'_TTJets')
					ht[str(i)] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix+'_T')
					httw[str(i)] = bkghists[histoPrefix+'_'+ttwList[0]].Clone(histoPrefix+'_TTW')
					httz[str(i)] = bkghists[histoPrefix+'_'+ttzList[0]].Clone(histoPrefix+'_TTZ')
					hvv[str(i)] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix+'_VV')
					for bkg in ttjetList:
						if bkg!=ttjetList[0]: httjets[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in wjetList:
						if bkg!=wjetList[0]: hwjets[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in ttwList:
						if bkg!=ttwList[0]: httw[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in ttzList:
						if bkg!=ttzList[0]: httz[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in tList:
						if bkg!=tList[0]: ht[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in zjetList:
						if bkg!=zjetList[0]: hzjets[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in vvList:
						if bkg!=vvList[0]: hvv[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
					#Group QCD processes
					hqcd[str(i)] = bkghists[histoPrefix+'_'+qcdList[0]].Clone(histoPrefix+'__qcd')
					for bkg in qcdList: 
						if bkg!=qcdList[0]: hqcd[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
					#Group EWK processes
					hewk[str(i)] = bkghists[histoPrefix+'_'+ewkList[0]].Clone(histoPrefix+'__ewk')
					for bkg in ewkList:
						if bkg!=ewkList[0]: hewk[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
					#Group TOP processes
					htop[str(i)] = bkghists[histoPrefix+'_'+topList[0]].Clone(histoPrefix+'__top')
					for bkg in topList:
						if bkg!=topList[0]: htop[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
					#get signal
					hsig[str(i)] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
					for decay in decays:
						if decay!=decays[0]: hsig[str(i)].Add(sighists[histoPrefix+'_'+signal+decay])

					#systematics
					if doAllSys:
						for systematic in systematicList:
							if systematic=='pdfNew' or systematic=='muRFcorrdNew' or systematic=='muRFdecorrdNew': continue
							for ud in ['Up','Down']:
								if systematic!='toppt':
									hqcd[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
									hewk[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
									htop[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+topList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
									hsig[systematic+ud+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
									for bkg in qcdList: 
										if bkg!=qcdList[0]: hqcd[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
									for bkg in ewkList: 
										if bkg!=ewkList[0]: hewk[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
									for bkg in topList: 
										if bkg!=topList[0]: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
									for decay in decays:
										if decay!=decays[0]: hsig[systematic+ud+str(i)].Add(sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decay])
								if systematic=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
									htop[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ttjetList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
									for bkg in ttjetList: 
										if bkg!=ttjetList[0]: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
									for bkg in topList: 
										if bkg not in ttjetList: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix+'_'+bkg])

						htop['muRFcorrdNewUp'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFcorrdNew__plus')
						htop['muRFcorrdNewDown'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFcorrdNew__minus')
						hewk['muRFcorrdNewUp'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFcorrdNew__plus')
						hewk['muRFcorrdNewDown'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFcorrdNew__minus')
						hqcd['muRFcorrdNewUp'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFcorrdNew__plus')
						hqcd['muRFcorrdNewDown'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFcorrdNew__minus')
						hsig['muRFcorrdNewUp'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFcorrdNew__plus')
						hsig['muRFcorrdNewDown'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFcorrdNew__minus')

						htop['muRFdecorrdNewUp'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFdecorrdNew__plus')
						htop['muRFdecorrdNewDown'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFdecorrdNew__minus')
						hewk['muRFdecorrdNewUp'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFdecorrdNew__plus')
						hewk['muRFdecorrdNewDown'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFdecorrdNew__minus')
						hqcd['muRFdecorrdNewUp'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFdecorrdNew__plus')
						hqcd['muRFdecorrdNewDown'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFdecorrdNew__minus')
						hsig['muRFdecorrdNewUp'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFdecorrdNew__plus')
						hsig['muRFdecorrdNewDown'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFdecorrdNew__minus')

						# nominal,renormWeights[4],renormWeights[2],renormWeights[1],renormWeights[0],renormWeights[5],renormWeights[3]
						histPrefixList = ['','muRUp','muRDown','muFUp','muFDown','muRFcorrdUp','muRFcorrdDown']
						for ibin in range(1,htop[str(i)].GetNbinsX()+1):
							weightListTop = [htop[item+str(i)].GetBinContent(ibin) for item in histPrefixList]	
							weightListEwk = [hewk[item+str(i)].GetBinContent(ibin) for item in histPrefixList]	
							weightListQcd = [hqcd[item+str(i)].GetBinContent(ibin) for item in histPrefixList]	
							weightListSig = [hsig[item+str(i)].GetBinContent(ibin) for item in histPrefixList]
							indTopRFcorrdUp = weightListTop.index(max(weightListTop))
							indTopRFcorrdDn = weightListTop.index(min(weightListTop))
							indEwkRFcorrdUp = weightListEwk.index(max(weightListEwk))
							indEwkRFcorrdDn = weightListEwk.index(min(weightListEwk))
							indQcdRFcorrdUp = weightListQcd.index(max(weightListQcd))
							indQcdRFcorrdDn = weightListQcd.index(min(weightListQcd))
							indSigRFcorrdUp = weightListSig.index(max(weightListSig))
							indSigRFcorrdDn = weightListSig.index(min(weightListSig))

							indTopRFdecorrdUp = weightListTop.index(max(weightListTop[:-2]))
							indTopRFdecorrdDn = weightListTop.index(min(weightListTop[:-2]))
							indEwkRFdecorrdUp = weightListEwk.index(max(weightListEwk[:-2]))
							indEwkRFdecorrdDn = weightListEwk.index(min(weightListEwk[:-2]))
							indQcdRFdecorrdUp = weightListQcd.index(max(weightListQcd[:-2]))
							indQcdRFdecorrdDn = weightListQcd.index(min(weightListQcd[:-2]))
							indSigRFdecorrdUp = weightListSig.index(max(weightListSig[:-2]))
							indSigRFdecorrdDn = weightListSig.index(min(weightListSig[:-2]))
							
							htop['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdUp]+str(i)].GetBinContent(ibin))
							htop['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdDn]+str(i)].GetBinContent(ibin))
							hewk['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+str(i)].GetBinContent(ibin))
							hewk['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+str(i)].GetBinContent(ibin))
							hqcd['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+str(i)].GetBinContent(ibin))
							hqcd['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+str(i)].GetBinContent(ibin))
							hsig['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdUp]+str(i)].GetBinContent(ibin))
							hsig['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdDn]+str(i)].GetBinContent(ibin))
							htop['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdUp]+str(i)].GetBinContent(ibin))
							htop['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdDn]+str(i)].GetBinContent(ibin))
							hewk['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+str(i)].GetBinContent(ibin))
							hewk['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+str(i)].GetBinContent(ibin))
							hqcd['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+str(i)].GetBinContent(ibin))
							hqcd['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+str(i)].GetBinContent(ibin))
							hsig['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+str(i)].GetBinContent(ibin))
							hsig['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+str(i)].GetBinContent(ibin))

							htop['muRFcorrdNewUp'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdUp]+str(i)].GetBinError(ibin))
							htop['muRFcorrdNewDown'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdDn]+str(i)].GetBinError(ibin))
							hewk['muRFcorrdNewUp'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+str(i)].GetBinError(ibin))
							hewk['muRFcorrdNewDown'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+str(i)].GetBinError(ibin))
							hqcd['muRFcorrdNewUp'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+str(i)].GetBinError(ibin))
							hqcd['muRFcorrdNewDown'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+str(i)].GetBinError(ibin))
							hsig['muRFcorrdNewUp'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdUp]+str(i)].GetBinError(ibin))
							hsig['muRFcorrdNewDown'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdDn]+str(i)].GetBinError(ibin))
							htop['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdUp]+str(i)].GetBinError(ibin))
							htop['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdDn]+str(i)].GetBinError(ibin))
							hewk['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+str(i)].GetBinError(ibin))
							hewk['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+str(i)].GetBinError(ibin))
							hqcd['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+str(i)].GetBinError(ibin))
							hqcd['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+str(i)].GetBinError(ibin))
							hsig['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+str(i)].GetBinError(ibin))
							hsig['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+str(i)].GetBinError(ibin))
			
						for pdfInd in range(100):
							hqcd['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__pdf'+str(pdfInd))
							hewk['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__pdf'+str(pdfInd))
							htop['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+topList[0]].Clone(histoPrefix+'__top__pdf'+str(pdfInd))
							hsig['pdf'+str(pdfInd)+'_'+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
							for bkg in qcdList: 
								if bkg!=qcdList[0]: hqcd['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
							for bkg in ewkList: 
								if bkg!=ewkList[0]: hewk['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
							for bkg in topList: 
								if bkg!=topList[0]: htop['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
							for decay in decays:
								if decay!=decays[0]:hsig['pdf'+str(pdfInd)+'_'+str(i)].Add(sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay])
						htop['pdfNewUp'+str(i)] = htop['pdf0_'+str(i)].Clone(histoPrefix+'__top__pdfNew__plus')
						htop['pdfNewDown'+str(i)] = htop['pdf0_'+str(i)].Clone(histoPrefix+'__top__pdfNew__minus')
						hewk['pdfNewUp'+str(i)] = hewk['pdf0_'+str(i)].Clone(histoPrefix+'__ewk__pdfNew__plus')
						hewk['pdfNewDown'+str(i)] = hewk['pdf0_'+str(i)].Clone(histoPrefix+'__ewk__pdfNew__minus')
						hqcd['pdfNewUp'+str(i)] = hqcd['pdf0_'+str(i)].Clone(histoPrefix+'__qcd__pdfNew__plus')
						hqcd['pdfNewDown'+str(i)] = hqcd['pdf0_'+str(i)].Clone(histoPrefix+'__qcd__pdfNew__minus')
						hsig['pdfNewUp'+str(i)] = hsig['pdf0_'+str(i)].Clone(histoPrefix+'__sig__pdfNew__plus')
						hsig['pdfNewDown'+str(i)] = hsig['pdf0_'+str(i)].Clone(histoPrefix+'__sig__pdfNew__minus')
						for ibin in range(1,htop['pdfNewUp'+str(i)].GetNbinsX()+1):
							weightListTop = [htop['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
							weightListEwk = [hewk['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
							weightListQcd = [hqcd['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
							weightListSig = [hsig['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
							indTopPDFUp = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[83]
							indTopPDFDn = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[15]
							indEwkPDFUp = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[83]
							indEwkPDFDn = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[15]
							indQcdPDFUp = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[83]
							indQcdPDFDn = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[15]
							indSigPDFUp = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[83]
							indSigPDFDn = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[15]
							
							htop['pdfNewUp'+str(i)].SetBinContent(ibin,htop['pdf'+str(indTopPDFUp)+'_'+str(i)].GetBinContent(ibin))
							htop['pdfNewDown'+str(i)].SetBinContent(ibin,htop['pdf'+str(indTopPDFDn)+'_'+str(i)].GetBinContent(ibin))
							hewk['pdfNewUp'+str(i)].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFUp)+'_'+str(i)].GetBinContent(ibin))
							hewk['pdfNewDown'+str(i)].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFDn)+'_'+str(i)].GetBinContent(ibin))
							hqcd['pdfNewUp'+str(i)].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFUp)+'_'+str(i)].GetBinContent(ibin))
							hqcd['pdfNewDown'+str(i)].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFDn)+'_'+str(i)].GetBinContent(ibin))
							hsig['pdfNewUp'+str(i)].SetBinContent(ibin,hsig['pdf'+str(indSigPDFUp)+'_'+str(i)].GetBinContent(ibin))
							hsig['pdfNewDown'+str(i)].SetBinContent(ibin,hsig['pdf'+str(indSigPDFDn)+'_'+str(i)].GetBinContent(ibin))

							htop['pdfNewUp'+str(i)].SetBinError(ibin,htop['pdf'+str(indTopPDFUp)+'_'+str(i)].GetBinError(ibin))
							htop['pdfNewDown'+str(i)].SetBinError(ibin,htop['pdf'+str(indTopPDFDn)+'_'+str(i)].GetBinError(ibin))
							hewk['pdfNewUp'+str(i)].SetBinError(ibin,hewk['pdf'+str(indEwkPDFUp)+'_'+str(i)].GetBinError(ibin))
							hewk['pdfNewDown'+str(i)].SetBinError(ibin,hewk['pdf'+str(indEwkPDFDn)+'_'+str(i)].GetBinError(ibin))
							hqcd['pdfNewUp'+str(i)].SetBinError(ibin,hqcd['pdf'+str(indQcdPDFUp)+'_'+str(i)].GetBinError(ibin))
							hqcd['pdfNewDown'+str(i)].SetBinError(ibin,hqcd['pdf'+str(indQcdPDFDn)+'_'+str(i)].GetBinError(ibin))
							hsig['pdfNewUp'+str(i)].SetBinError(ibin,hsig['pdf'+str(indSigPDFUp)+'_'+str(i)].GetBinError(ibin))
							hsig['pdfNewDown'+str(i)].SetBinError(ibin,hsig['pdf'+str(indSigPDFDn)+'_'+str(i)].GetBinError(ibin))
								
					if doQ2sys:
						htop['q2Up'+str(i)] = bkghists[histoPrefix+'_'+q2UpList[0]].Clone(histoPrefix+'__top__q2__plus')
						htop['q2Down'+str(i)] = bkghists[histoPrefix+'_'+q2DownList[0]].Clone(histoPrefix+'__top__q2__minus')
						for ind in range(1,len(q2UpList)):
							htop['q2Up'+str(i)].Add(bkghists[histoPrefix+'_'+q2UpList[ind]])
							htop['q2Down'+str(i)].Add(bkghists[histoPrefix+'_'+q2DownList[ind]])
					
					#Group data processes
					hdata[str(i)] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
					for dat in dataList:
						if dat!=dataList[0]: hdata[str(i)].Add(datahists[histoPrefix+'_'+dat])

					#prepare yield table
					yieldTable[histoPrefix]['top']    = htop[str(i)].Integral()
					yieldTable[histoPrefix]['ewk']    = hewk[str(i)].Integral()
					yieldTable[histoPrefix]['qcd']    = hqcd[str(i)].Integral()
					yieldTable[histoPrefix]['totBkg'] = htop[str(i)].Integral()+hewk[str(i)].Integral()+hqcd[str(i)].Integral()
					yieldTable[histoPrefix]['data']   = hdata[str(i)].Integral()
					yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
					yieldTable[histoPrefix]['WJets']  = hwjets[str(i)].Integral()
					yieldTable[histoPrefix]['ZJets']  = hzjets[str(i)].Integral()
					yieldTable[histoPrefix]['VV']     = hvv[str(i)].Integral()
					yieldTable[histoPrefix]['TTW']    = httw[str(i)].Integral()
					yieldTable[histoPrefix]['TTZ']    = httz[str(i)].Integral()
					yieldTable[histoPrefix]['TTJets'] = httjets[str(i)].Integral()
					yieldTable[histoPrefix]['T']      = ht[str(i)].Integral()
					yieldTable[histoPrefix]['QCD']    = hqcd[str(i)].Integral()
					yieldTable[histoPrefix][signal]   = hsig[str(i)].Integral()
					
					#+/- 1sigma variations of shape systematics
					if doAllSys:
						for systematic in systematicList:
							for ud in ['Up','Down']:
								yieldTable[histoPrefix+systematic+ud]['top']    = htop[systematic+ud+str(i)].Integral()
								if systematic!='toppt':
									yieldTable[histoPrefix+systematic+ud]['ewk']    = hewk[systematic+ud+str(i)].Integral()
									yieldTable[histoPrefix+systematic+ud]['qcd']    = hqcd[systematic+ud+str(i)].Integral()
									yieldTable[histoPrefix+systematic+ud]['totBkg'] = htop[systematic+ud+str(i)].Integral()+hewk[systematic+ud+str(i)].Integral()+hqcd[systematic+ud+str(i)].Integral()
									yieldTable[histoPrefix+systematic+ud][signal]   = hsig[systematic+ud+str(i)].Integral()
								
					if doQ2sys:
						yieldTable[histoPrefix+'q2Up']['top']    = htop['q2Up'+str(i)].Integral()
						yieldTable[histoPrefix+'q2Down']['top']    = htop['q2Down'+str(i)].Integral()

					#prepare MC yield error table
					yieldStatErrTable[histoPrefix]['top']    = 0.
					yieldStatErrTable[histoPrefix]['ewk']    = 0.
					yieldStatErrTable[histoPrefix]['qcd']    = 0.
					yieldStatErrTable[histoPrefix]['totBkg'] = 0.
					yieldStatErrTable[histoPrefix]['data']   = 0.
					yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.
					yieldStatErrTable[histoPrefix]['WJets']  = 0.
					yieldStatErrTable[histoPrefix]['ZJets']  = 0.
					yieldStatErrTable[histoPrefix]['VV']     = 0.
					yieldStatErrTable[histoPrefix]['TTW']    = 0.
					yieldStatErrTable[histoPrefix]['TTZ']    = 0.
					yieldStatErrTable[histoPrefix]['TTJets'] = 0.
					yieldStatErrTable[histoPrefix]['T']      = 0.
					yieldStatErrTable[histoPrefix]['QCD']    = 0.
					yieldStatErrTable[histoPrefix][signal]   = 0.

					for ibin in range(1,hsig[str(i)].GetXaxis().GetNbins()+1):
						yieldStatErrTable[histoPrefix]['top']    += htop[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['ewk']    += hewk[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['qcd']    += hqcd[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['totBkg'] += htop[str(i)].GetBinError(ibin)**2+hewk[str(i)].GetBinError(ibin)**2+hqcd[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['data']   += hdata[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['WJets']  += hwjets[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['ZJets']  += hzjets[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['VV']     += hvv[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['TTW']    += httw[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['TTZ']    += httz[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['TTJets'] += httjets[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['T']      += ht[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix]['QCD']    += hqcd[str(i)].GetBinError(ibin)**2
						yieldStatErrTable[histoPrefix][signal]   += hsig[str(i)].GetBinError(ibin)**2

					#scale signal cross section to 1pb
					if scaleSignalXsecTo1pb: hsig[str(i)].Scale(1./xsec[signal])
					#write theta histograms in root file, avoid having processes with no event yield (to make theta happy) 
					if hsig[str(i)].Integral() > 0:  
						hsig[str(i)].Write()
						if doAllSys:
							for systematic in systematicList:
								if systematic=='toppt': continue
								if scaleSignalXsecTo1pb: 
									hsig[systematic+'Up'+str(i)].Scale(1./xsec[signal])
									hsig[systematic+'Down'+str(i)].Scale(1./xsec[signal])
								if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
									hsig[systematic+'Up'+str(i)].Scale(hsig[str(i)].Integral()/hsig[systematic+'Up'+str(i)].Integral())
									hsig[systematic+'Down'+str(i)].Scale(hsig[str(i)].Integral()/hsig[systematic+'Down'+str(i)].Integral())
								hsig[systematic+'Up'+str(i)].Write()
								hsig[systematic+'Down'+str(i)].Write()
							for pdfInd in range(100): hsig['pdf'+str(pdfInd)+'_'+str(i)].Write()
					if htop[str(i)].Integral() > 0:  
						htop[str(i)].Write()
						if doAllSys:
							for systematic in systematicList:
								if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
									htop[systematic+'Up'+str(i)].Scale(htop[str(i)].Integral()/htop[systematic+'Up'+str(i)].Integral())
									htop[systematic+'Down'+str(i)].Scale(htop[str(i)].Integral()/htop[systematic+'Down'+str(i)].Integral())  
								htop[systematic+'Up'+str(i)].Write()
								htop[systematic+'Down'+str(i)].Write()
							for pdfInd in range(100): htop['pdf'+str(pdfInd)+'_'+str(i)].Write()
						if doQ2sys:
							htop['q2Up'+str(i)].Write()
							htop['q2Down'+str(i)].Write()
					if hewk[str(i)].Integral() > 0:  
						hewk[str(i)].Write()
						if doAllSys:
							for systematic in systematicList:
								if systematic=='toppt': continue
								if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
									hewk[systematic+'Up'+str(i)].Scale(hewk[str(i)].Integral()/hewk[systematic+'Up'+str(i)].Integral())
									hewk[systematic+'Down'+str(i)].Scale(hewk[str(i)].Integral()/hewk[systematic+'Down'+str(i)].Integral())  
								hewk[systematic+'Up'+str(i)].Write()
								hewk[systematic+'Down'+str(i)].Write()
							for pdfInd in range(100): hewk['pdf'+str(pdfInd)+'_'+str(i)].Write()
					if hqcd[str(i)].Integral() > 0:  
						hqcd[str(i)].Write()
						if doAllSys:
							for systematic in systematicList:
								if systematic == 'pdf' or systematic == 'pdfNew' or systematic == 'muR' or systematic == 'muF' or systematic == 'muRFcorrd' or systematic=='toppt': continue
								hqcd[systematic+'Up'+str(i)].Write()
								hqcd[systematic+'Down'+str(i)].Write()
							for pdfInd in range(100): hqcd['pdf'+str(pdfInd)+'_'+str(i)].Write()
					hdata[str(i)].Write()
					i+=1
		outputRfile.Close()
	
	stdout_old = sys.stdout
	logFile = open(outDir+'/yields_'+discriminant+'_'+lumiStr+'fb_.txt','a')
	sys.stdout = logFile

	## PRINTING YIELD TABLE WITH STATISTICAL UNCERTAINTIES ##
	#first print table without background grouping
	ljust_i = 1
	print 'CUTS:',cutString
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for bkg in bkgStackList: print bkg.ljust(ljust_i),
	print 'data'.ljust(ljust_i),
	print
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
				for bkg in bkgStackList:
					print str(yieldTable[histoPrefix][bkg]).ljust(ljust_i),
				print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
				print

	print 'YIELDS ERRORS'
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
				for bkg in bkgStackList:
					print str(math.sqrt(yieldStatErrTable[histoPrefix][bkg])).ljust(ljust_i),
				print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
				print

	#now print with top,ewk,qcd grouping
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	print 'ewk'.ljust(ljust_i),
	print 'top'.ljust(ljust_i),
	print 'qcd'.ljust(ljust_i),
	print 'data'.ljust(ljust_i),
	print
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
				print str(yieldTable[histoPrefix]['ewk']).ljust(ljust_i),
				print str(yieldTable[histoPrefix]['top']).ljust(ljust_i),
				print str(yieldTable[histoPrefix]['qcd']).ljust(ljust_i),
				print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
				print

	print 'YIELDS ERRORS'
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
				print str(math.sqrt(yieldStatErrTable[histoPrefix]['ewk'])).ljust(ljust_i),
				print str(math.sqrt(yieldStatErrTable[histoPrefix]['top'])).ljust(ljust_i),
				print str(math.sqrt(yieldStatErrTable[histoPrefix]['qcd'])).ljust(ljust_i),
				print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
				print

	#print yields for signals
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for sig in sigList: print sig.ljust(ljust_i),
	print
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
				for sig in sigList:
					print str(yieldTable[histoPrefix][sig]).ljust(ljust_i),
				print

	print 'YIELDS ERRORS'
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
				for sig in sigList:
					print str(math.sqrt(yieldStatErrTable[histoPrefix][sig])).ljust(ljust_i),
				print
				
	#print for AN tables
	print
	print "FOR AN (errors are statistical+normalization systematics): "
	print
	print 'YIELDS ELECTRON+JETS'.ljust(20*ljust_i), 
	for isEM in ['isE']:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
	print
	for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		print process.ljust(ljust_i),
		for isEM in ['E']:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					if process=='dataOverBkg':
						dataTemp = yieldTable[histoPrefix]['data']+1e-20
						dataTempErr = yieldStatErrTable[histoPrefix]['data']
						totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
						totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
						totBkgTempErr += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
						totBkgTempErr += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
						totBkgTempErr += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
						totBkgTempErr += (corrdSys*totBkgTemp)**2
						dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
						print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
					else:
						yieldtemp = yieldTable[histoPrefix][process]
						yielderrtemp = yieldStatErrTable[histoPrefix][process]
						if process=='totBkg': 
							yielderrtemp += (corrdSys*yieldtemp)**2
							yielderrtemp += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
							yielderrtemp += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
							yielderrtemp += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
						elif process in sigList: 
							yielderrtemp += (corrdSys*yieldtemp)**2
						elif process!='data': 
							yielderrtemp += (corrdSys*yieldtemp)**2
							yielderrtemp += (addSys[process+'_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix][process])**2
						if process=='data': print ' & '+str(int(yieldtemp)),
						elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
						else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		print '\\\\',
		print
	print
	print 'YIELDS MUON+JETS'.ljust(20*ljust_i), 
	for isEM in ['isM']:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
	print
	for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		print process.ljust(ljust_i),
		for isEM in ['M']:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					if process=='dataOverBkg':
						dataTemp = yieldTable[histoPrefix]['data']+1e-20
						dataTempErr = yieldStatErrTable[histoPrefix]['data']
						totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
						totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
						totBkgTempErr += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
						totBkgTempErr += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
						totBkgTempErr += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
						totBkgTempErr += (corrdSys*totBkgTemp)**2
						dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
						print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
					else:
						yieldtemp = yieldTable[histoPrefix][process]
						yielderrtemp = yieldStatErrTable[histoPrefix][process]
						if process=='totBkg': 
							yielderrtemp += (corrdSys*yieldtemp)**2
							yielderrtemp += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
							yielderrtemp += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
							yielderrtemp += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
						elif process in sigList: 
							yielderrtemp += (corrdSys*yieldtemp)**2
						elif process!='data': 
							yielderrtemp += (corrdSys*yieldtemp)**2
							yielderrtemp += (addSys[process+'_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix][process])**2
						if process=='data': print ' & '+str(int(yieldtemp)),
						elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
						else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		print '\\\\',
		print
		
	#print for AN tables systematics
	if doAllSys:
		print
		print "FOR AN (shape systematic percentaces): "
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
		print
		for process in ['ewk','top']+sigList:
			print process.ljust(ljust_i),
			print
			for ud in ['Up','Down']:
				for systematic in systematicList:
					if systematic=='toppt' and process!='top': continue
					print (systematic+ud).ljust(ljust_i),
					for isEM in isEMlist:
						for nWtag in nWtaglist:
							for nBtag in nbtaglist:
								histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
								print ' & '+str(round_sig(yieldTable[histoPrefix+systematic+ud][process]/yieldTable[histoPrefix][process],2)),
					print '\\\\',
					print
				if process!='top': continue
				print ('q2'+ud).ljust(ljust_i),
				for isEM in isEMlist:
					for nWtag in nWtaglist:
						for nBtag in nbtaglist:
							histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
							print ' & '+str(round_sig(yieldTable[histoPrefix+'q2'+ud][process]/yieldTable[histoPrefix][process],2)),
				print '\\\\',
				print
		
	print
	print "FOR PAS (errors are statistical+normalization systematics): " #combines e/m channels
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for nWtag in nWtaglist:
		for nBtag in nbtaglist:
			print ('tags00'+nWtag+'_nB'+nBtag).ljust(ljust_i),
	print
	for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		print process.ljust(ljust_i),
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_isE_nW'+nWtag+'_nB'+nBtag
				if process=='dataOverBkg':
					dataTemp = yieldTable[histoPrefix]['data']+yieldTable[histoPrefix.replace('_isE','_isM')]['data']+1e-20
					dataTempErr = yieldStatErrTable[histoPrefix]['data']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['data']
					totBkgTemp = yieldTable[histoPrefix]['totBkg']+yieldTable[histoPrefix.replace('_isE','_isM')]['totBkg']+1e-20
					totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['totBkg'] # statistical error squared
					totBkgTempErr += (addSys['top_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					totBkgTempErr += (addSys['ewk_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					totBkgTempErr += (addSys['qcd_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					totBkgTempErr += (corrdSys*totBkgTemp)**2
					dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
					print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
				else:
					yieldtemp = yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]
					yielderrtemp = yieldStatErrTable[histoPrefix][process]++yieldStatErrTable[histoPrefix.replace('_isE','_isM')][process]
					if process=='totBkg': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys['top_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						yielderrtemp += (addSys['ewk_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						yielderrtemp += (addSys['qcd_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					elif process in sigList: 
						yielderrtemp += (corrdSys*yieldtemp)**2
					elif process!='data': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys[process+'_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					if process=='data': print ' & '+str(int(yieldtemp)),
					elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
					else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		print '\\\\',
		print
		
	sys.stdout = stdout_old
	logFile.close()

###########################################################
################ CATEGORIZATION DECAYS ####################
###########################################################
def makeThetaCatsIndDecays(datahists,sighists,bkghists,discriminant):

	## This function categorizes the events into electron/muon --> 0/1p W-tag! --> 1/2p b-tag (the same as Cat1, but there is no 4p/3p jets requirement here)
	## Input  histograms (datahists,sighists,bkghists) must have corresponding histograms returned from analyze.py##

	## INITIALIZE DICTIONARIES FOR YIELDS AND THEIR UNCERTAINTIES ##
	yieldTable = {}
	yieldStatErrTable = {} #what is actually stored in this is the square of the uncertainty
	for isEM in isEMlist:
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
				yieldTable[histoPrefix]={}
				yieldStatErrTable[histoPrefix]={}
				if doAllSys:
					for systematic in systematicList:
						for ud in ['Up','Down']:
							yieldTable[histoPrefix+systematic+ud]={}
							
				if doQ2sys:
					yieldTable[histoPrefix+'q2Up']={}
					yieldTable[histoPrefix+'q2Down']={}

	## WRITING HISTOGRAMS IN ROOT FILE ##
	i=0
	for decay in decays:
		for signal in sigList:
			outputRfile = R.TFile(outDir+'/templates_'+discriminant+'_'+signal+decay+'_'+lumiStr+'fb.root','RECREATE')
			hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
			hwjets,hzjets,httjets,ht,httw,httz,hvv={},{},{},{},{},{},{}
			for isEM in isEMlist:
				for nWtag in nWtaglist:
					for nBtag in nbtaglist:
						histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag

						#Group processes
						hwjets[str(i)] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix+'_WJets')
						hzjets[str(i)] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix+'_ZJets')
						httjets[str(i)] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix+'_TTJets')
						ht[str(i)] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix+'_T')
						httw[str(i)] = bkghists[histoPrefix+'_'+ttwList[0]].Clone(histoPrefix+'_TTW')
						httz[str(i)] = bkghists[histoPrefix+'_'+ttzList[0]].Clone(histoPrefix+'_TTZ')
						hvv[str(i)] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix+'_VV')
						for bkg in ttjetList:
							if bkg!=ttjetList[0]: httjets[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
						for bkg in wjetList:
							if bkg!=wjetList[0]: hwjets[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
						for bkg in ttwList:
							if bkg!=ttwList[0]: httw[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
						for bkg in ttzList:
							if bkg!=ttzList[0]: httz[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
						for bkg in tList:
							if bkg!=tList[0]: ht[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
						for bkg in zjetList:
							if bkg!=zjetList[0]: hzjets[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
						for bkg in vvList:
							if bkg!=vvList[0]: hvv[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
						#Group QCD processes
						hqcd[str(i)] = bkghists[histoPrefix+'_'+qcdList[0]].Clone(histoPrefix+'__qcd')
						for bkg in qcdList: 
							if bkg!=qcdList[0]: hqcd[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
						#Group EWK processes
						hewk[str(i)] = bkghists[histoPrefix+'_'+ewkList[0]].Clone(histoPrefix+'__ewk')
						for bkg in ewkList:
							if bkg!=ewkList[0]: hewk[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
						#Group TOP processes
						htop[str(i)] = bkghists[histoPrefix+'_'+topList[0]].Clone(histoPrefix+'__top')
						for bkg in topList:
							if bkg!=topList[0]: htop[str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					
						#get signal
						hsig[str(i)] = sighists[histoPrefix+'_'+signal+decay].Clone(histoPrefix+'__sig')

						#systematics
						if doAllSys:
							for systematic in systematicList:
								if systematic=='pdfNew' or systematic=='muRFcorrdNew' or systematic=='muRFdecorrdNew': continue
								for ud in ['Up','Down']:
									if systematic!='toppt':
										hqcd[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
										hewk[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
										htop[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+topList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
										hsig[systematic+ud+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decay].Clone(histoPrefix+'__sig__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
										for bkg in qcdList: 
											if bkg!=qcdList[0]: hqcd[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
										for bkg in ewkList: 
											if bkg!=ewkList[0]: hewk[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
										for bkg in topList: 
											if bkg!=topList[0]: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
									if systematic=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
										htop[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ttjetList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
										for bkg in ttjetList: 
											if bkg!=ttjetList[0]: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
										for bkg in topList: 
											if bkg not in ttjetList: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix+'_'+bkg])

							htop['muRFcorrdNewUp'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFcorrdNew__plus')
							htop['muRFcorrdNewDown'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFcorrdNew__minus')
							hewk['muRFcorrdNewUp'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFcorrdNew__plus')
							hewk['muRFcorrdNewDown'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFcorrdNew__minus')
							hqcd['muRFcorrdNewUp'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFcorrdNew__plus')
							hqcd['muRFcorrdNewDown'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFcorrdNew__minus')
							hsig['muRFcorrdNewUp'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFcorrdNew__plus')
							hsig['muRFcorrdNewDown'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFcorrdNew__minus')

							htop['muRFdecorrdNewUp'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFdecorrdNew__plus')
							htop['muRFdecorrdNewDown'+str(i)] = htop['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__top__muRFdecorrdNew__minus')
							hewk['muRFdecorrdNewUp'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFdecorrdNew__plus')
							hewk['muRFdecorrdNewDown'+str(i)] = hewk['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__ewk__muRFdecorrdNew__minus')
							hqcd['muRFdecorrdNewUp'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFdecorrdNew__plus')
							hqcd['muRFdecorrdNewDown'+str(i)] = hqcd['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__qcd__muRFdecorrdNew__minus')
							hsig['muRFdecorrdNewUp'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFdecorrdNew__plus')
							hsig['muRFdecorrdNewDown'+str(i)] = hsig['muRFcorrdUp'+str(i)].Clone(histoPrefix+'__sig__muRFdecorrdNew__minus')

							# nominal,renormWeights[4],renormWeights[2],renormWeights[1],renormWeights[0],renormWeights[5],renormWeights[3]
							histPrefixList = ['','muRUp','muRDown','muFUp','muFDown','muRFcorrdUp','muRFcorrdDown']
							for ibin in range(1,htop[str(i)].GetNbinsX()+1):
								weightListTop = [htop[item+str(i)].GetBinContent(ibin) for item in histPrefixList]	
								weightListEwk = [hewk[item+str(i)].GetBinContent(ibin) for item in histPrefixList]	
								weightListQcd = [hqcd[item+str(i)].GetBinContent(ibin) for item in histPrefixList]	
								weightListSig = [hsig[item+str(i)].GetBinContent(ibin) for item in histPrefixList]
								indTopRFcorrdUp = weightListTop.index(max(weightListTop))
								indTopRFcorrdDn = weightListTop.index(min(weightListTop))
								indEwkRFcorrdUp = weightListEwk.index(max(weightListEwk))
								indEwkRFcorrdDn = weightListEwk.index(min(weightListEwk))
								indQcdRFcorrdUp = weightListQcd.index(max(weightListQcd))
								indQcdRFcorrdDn = weightListQcd.index(min(weightListQcd))
								indSigRFcorrdUp = weightListSig.index(max(weightListSig))
								indSigRFcorrdDn = weightListSig.index(min(weightListSig))

								indTopRFdecorrdUp = weightListTop.index(max(weightListTop[:-2]))
								indTopRFdecorrdDn = weightListTop.index(min(weightListTop[:-2]))
								indEwkRFdecorrdUp = weightListEwk.index(max(weightListEwk[:-2]))
								indEwkRFdecorrdDn = weightListEwk.index(min(weightListEwk[:-2]))
								indQcdRFdecorrdUp = weightListQcd.index(max(weightListQcd[:-2]))
								indQcdRFdecorrdDn = weightListQcd.index(min(weightListQcd[:-2]))
								indSigRFdecorrdUp = weightListSig.index(max(weightListSig[:-2]))
								indSigRFdecorrdDn = weightListSig.index(min(weightListSig[:-2]))
							
								htop['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdUp]+str(i)].GetBinContent(ibin))
								htop['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdDn]+str(i)].GetBinContent(ibin))
								hewk['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+str(i)].GetBinContent(ibin))
								hewk['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+str(i)].GetBinContent(ibin))
								hqcd['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+str(i)].GetBinContent(ibin))
								hqcd['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+str(i)].GetBinContent(ibin))
								hsig['muRFcorrdNewUp'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdUp]+str(i)].GetBinContent(ibin))
								hsig['muRFcorrdNewDown'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdDn]+str(i)].GetBinContent(ibin))
								htop['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdUp]+str(i)].GetBinContent(ibin))
								htop['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdDn]+str(i)].GetBinContent(ibin))
								hewk['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+str(i)].GetBinContent(ibin))
								hewk['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+str(i)].GetBinContent(ibin))
								hqcd['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+str(i)].GetBinContent(ibin))
								hqcd['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+str(i)].GetBinContent(ibin))
								hsig['muRFdecorrdNewUp'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+str(i)].GetBinContent(ibin))
								hsig['muRFdecorrdNewDown'+str(i)].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+str(i)].GetBinContent(ibin))

								htop['muRFcorrdNewUp'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdUp]+str(i)].GetBinError(ibin))
								htop['muRFcorrdNewDown'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdDn]+str(i)].GetBinError(ibin))
								hewk['muRFcorrdNewUp'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+str(i)].GetBinError(ibin))
								hewk['muRFcorrdNewDown'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+str(i)].GetBinError(ibin))
								hqcd['muRFcorrdNewUp'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+str(i)].GetBinError(ibin))
								hqcd['muRFcorrdNewDown'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+str(i)].GetBinError(ibin))
								hsig['muRFcorrdNewUp'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdUp]+str(i)].GetBinError(ibin))
								hsig['muRFcorrdNewDown'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdDn]+str(i)].GetBinError(ibin))
								htop['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdUp]+str(i)].GetBinError(ibin))
								htop['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdDn]+str(i)].GetBinError(ibin))
								hewk['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+str(i)].GetBinError(ibin))
								hewk['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+str(i)].GetBinError(ibin))
								hqcd['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+str(i)].GetBinError(ibin))
								hqcd['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+str(i)].GetBinError(ibin))
								hsig['muRFdecorrdNewUp'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+str(i)].GetBinError(ibin))
								hsig['muRFdecorrdNewDown'+str(i)].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+str(i)].GetBinError(ibin))

							for pdfInd in range(100):
								hqcd['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__pdf'+str(pdfInd))
								hewk['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__pdf'+str(pdfInd))
								htop['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+topList[0]].Clone(histoPrefix+'__top__pdf'+str(pdfInd))
								hsig['pdf'+str(pdfInd)+'_'+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
								for bkg in qcdList: 
									if bkg!=qcdList[0]: hqcd['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
								for bkg in ewkList: 
									if bkg!=ewkList[0]: hewk['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
								for bkg in topList: 
									if bkg!=topList[0]: htop['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
							htop['pdfNewUp'+str(i)] = htop['pdf0_'+str(i)].Clone(histoPrefix+'__top__pdfNew__plus')
							htop['pdfNewDown'+str(i)] = htop['pdf0_'+str(i)].Clone(histoPrefix+'__top__pdfNew__minus')
							hewk['pdfNewUp'+str(i)] = hewk['pdf0_'+str(i)].Clone(histoPrefix+'__ewk__pdfNew__plus')
							hewk['pdfNewDown'+str(i)] = hewk['pdf0_'+str(i)].Clone(histoPrefix+'__ewk__pdfNew__minus')
							hqcd['pdfNewUp'+str(i)] = hqcd['pdf0_'+str(i)].Clone(histoPrefix+'__qcd__pdfNew__plus')
							hqcd['pdfNewDown'+str(i)] = hqcd['pdf0_'+str(i)].Clone(histoPrefix+'__qcd__pdfNew__minus')
							hsig['pdfNewUp'+str(i)] = hsig['pdf0_'+str(i)].Clone(histoPrefix+'__sig__pdfNew__plus')
							hsig['pdfNewDown'+str(i)] = hsig['pdf0_'+str(i)].Clone(histoPrefix+'__sig__pdfNew__minus')
							for ibin in range(1,htop['pdfNewUp'+str(i)].GetNbinsX()+1):
								weightListTop = [htop['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
								weightListEwk = [hewk['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
								weightListQcd = [hqcd['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
								weightListSig = [hsig['pdf'+str(pdfInd)+'_'+str(i)].GetBinContent(ibin) for pdfInd in range(100)]
								indTopPDFUp = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[83]
								indTopPDFDn = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[15]
								indEwkPDFUp = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[83]
								indEwkPDFDn = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[15]
								indQcdPDFUp = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[83]
								indQcdPDFDn = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[15]
								indSigPDFUp = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[83]
								indSigPDFDn = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[15]
								htop['pdfNewUp'+str(i)].SetBinContent(ibin,htop['pdf'+str(indTopPDFUp)+'_'+str(i)].GetBinContent(ibin))
								htop['pdfNewDown'+str(i)].SetBinContent(ibin,htop['pdf'+str(indTopPDFDn)+'_'+str(i)].GetBinContent(ibin))
								hewk['pdfNewUp'+str(i)].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFUp)+'_'+str(i)].GetBinContent(ibin))
								hewk['pdfNewDown'+str(i)].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFDn)+'_'+str(i)].GetBinContent(ibin))
								hqcd['pdfNewUp'+str(i)].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFUp)+'_'+str(i)].GetBinContent(ibin))
								hqcd['pdfNewDown'+str(i)].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFDn)+'_'+str(i)].GetBinContent(ibin))
								hsig['pdfNewUp'+str(i)].SetBinContent(ibin,hsig['pdf'+str(indSigPDFUp)+'_'+str(i)].GetBinContent(ibin))
								hsig['pdfNewDown'+str(i)].SetBinContent(ibin,hsig['pdf'+str(indSigPDFDn)+'_'+str(i)].GetBinContent(ibin))
								
						if doQ2sys:
							htop['q2Up'+str(i)] = bkghists[histoPrefix+'_'+q2UpList[0]].Clone(histoPrefix+'__top__q2__plus')
							htop['q2Down'+str(i)] = bkghists[histoPrefix+'_'+q2DownList[0]].Clone(histoPrefix+'__top__q2__minus')
							for ind in range(1,len(q2UpList)):
								htop['q2Up'+str(i)].Add(bkghists[histoPrefix+'_'+q2UpList[ind]])
								htop['q2Down'+str(i)].Add(bkghists[histoPrefix+'_'+q2DownList[ind]])
					
						#Group data processes
						hdata[str(i)] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
						for dat in dataList:
							if dat!=dataList[0]: hdata[str(i)].Add(datahists[histoPrefix+'_'+dat])

						#prepare yield table
						yieldTable[histoPrefix]['top']    = htop[str(i)].Integral()
						yieldTable[histoPrefix]['ewk']    = hewk[str(i)].Integral()
						yieldTable[histoPrefix]['qcd']    = hqcd[str(i)].Integral()
						yieldTable[histoPrefix]['totBkg'] = htop[str(i)].Integral()+hewk[str(i)].Integral()+hqcd[str(i)].Integral()
						yieldTable[histoPrefix]['data']   = hdata[str(i)].Integral()
						yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
						yieldTable[histoPrefix]['WJets']  = hwjets[str(i)].Integral()
						yieldTable[histoPrefix]['ZJets']  = hzjets[str(i)].Integral()
						yieldTable[histoPrefix]['VV']     = hvv[str(i)].Integral()
						yieldTable[histoPrefix]['TTW']    = httw[str(i)].Integral()
						yieldTable[histoPrefix]['TTZ']    = httz[str(i)].Integral()
						yieldTable[histoPrefix]['TTJets'] = httjets[str(i)].Integral()
						yieldTable[histoPrefix]['T']      = ht[str(i)].Integral()
						yieldTable[histoPrefix]['QCD']    = hqcd[str(i)].Integral()
						yieldTable[histoPrefix][signal]   = hsig[str(i)].Integral()
					
						#+/- 1sigma variations of shape systematics
						if doAllSys:
							for systematic in systematicList:
								for ud in ['Up','Down']:
									yieldTable[histoPrefix+systematic+ud]['top']    = htop[systematic+ud+str(i)].Integral()
									if systematic!='toppt':
										yieldTable[histoPrefix+systematic+ud]['ewk']    = hewk[systematic+ud+str(i)].Integral()
										yieldTable[histoPrefix+systematic+ud]['qcd']    = hqcd[systematic+ud+str(i)].Integral()
										yieldTable[histoPrefix+systematic+ud]['totBkg'] = htop[systematic+ud+str(i)].Integral()+hewk[systematic+ud+str(i)].Integral()+hqcd[systematic+ud+str(i)].Integral()
										yieldTable[histoPrefix+systematic+ud][signal]   = hsig[systematic+ud+str(i)].Integral()
								
						if doQ2sys:
							yieldTable[histoPrefix+'q2Up']['top']    = htop['q2Up'+str(i)].Integral()
							yieldTable[histoPrefix+'q2Down']['top']    = htop['q2Down'+str(i)].Integral()

						#prepare MC yield error table
						yieldStatErrTable[histoPrefix]['top']    = 0.
						yieldStatErrTable[histoPrefix]['ewk']    = 0.
						yieldStatErrTable[histoPrefix]['qcd']    = 0.
						yieldStatErrTable[histoPrefix]['totBkg'] = 0.
						yieldStatErrTable[histoPrefix]['data']   = 0.
						yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.
						yieldStatErrTable[histoPrefix]['WJets']  = 0.
						yieldStatErrTable[histoPrefix]['ZJets']  = 0.
						yieldStatErrTable[histoPrefix]['VV']     = 0.
						yieldStatErrTable[histoPrefix]['TTW']    = 0.
						yieldStatErrTable[histoPrefix]['TTZ']    = 0.
						yieldStatErrTable[histoPrefix]['TTJets'] = 0.
						yieldStatErrTable[histoPrefix]['T']      = 0.
						yieldStatErrTable[histoPrefix]['QCD']    = 0.
						yieldStatErrTable[histoPrefix][signal]   = 0.

						for ibin in range(1,hsig[str(i)].GetXaxis().GetNbins()+1):
							yieldStatErrTable[histoPrefix]['top']    += htop[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['ewk']    += hewk[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['qcd']    += hqcd[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['totBkg'] += htop[str(i)].GetBinError(ibin)**2+hewk[str(i)].GetBinError(ibin)**2+hqcd[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['data']   += hdata[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['WJets']  += hwjets[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['ZJets']  += hzjets[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['VV']     += hvv[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['TTW']    += httw[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['TTZ']    += httz[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['TTJets'] += httjets[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['T']      += ht[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix]['QCD']    += hqcd[str(i)].GetBinError(ibin)**2
							yieldStatErrTable[histoPrefix][signal]   += hsig[str(i)].GetBinError(ibin)**2

						#scale signal cross section to 1pb
						if scaleSignalXsecTo1pb: hsig[str(i)].Scale(1./xsec[signal])
						BRcoeff = 1.
						if decay[:2]!=decay[2:]: BRcoeff = 2.
						hsig[str(i)].Scale(1./(BRcoeff*BR[decay[:2]]*BR[decay[2:]]))
						#write theta histograms in root file, avoid having processes with no event yield (to make theta happy) 
						if hsig[str(i)].Integral() > 0:  
							hsig[str(i)].Write()
							if doAllSys:
								for systematic in systematicList:
									if systematic=='toppt': continue
									if scaleSignalXsecTo1pb: 
										hsig[systematic+'Up'+str(i)].Scale(1./xsec[signal])
										hsig[systematic+'Down'+str(i)].Scale(1./xsec[signal])
									hsig[systematic+'Up'+str(i)].Scale(1./(BRcoeff*BR[decay[:2]]*BR[decay[2:]]))
									hsig[systematic+'Down'+str(i)].Scale(1./(BRcoeff*BR[decay[:2]]*BR[decay[2:]]))
									if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
										hsig[systematic+'Up'+str(i)].Scale(hsig[str(i)].Integral()/hsig[systematic+'Up'+str(i)].Integral())
										hsig[systematic+'Down'+str(i)].Scale(hsig[str(i)].Integral()/hsig[systematic+'Down'+str(i)].Integral())
									hsig[systematic+'Up'+str(i)].Write()
									hsig[systematic+'Down'+str(i)].Write()
								for pdfInd in range(100): hsig['pdf'+str(pdfInd)+'_'+str(i)].Write()
						if htop[str(i)].Integral() > 0:  
							htop[str(i)].Write()
							if doAllSys:
								for systematic in systematicList:
									if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
										htop[systematic+'Up'+str(i)].Scale(htop[str(i)].Integral()/htop[systematic+'Up'+str(i)].Integral())
										htop[systematic+'Down'+str(i)].Scale(htop[str(i)].Integral()/htop[systematic+'Down'+str(i)].Integral())  
									htop[systematic+'Up'+str(i)].Write()
									htop[systematic+'Down'+str(i)].Write()
								for pdfInd in range(100): htop['pdf'+str(pdfInd)+'_'+str(i)].Write()
							if doQ2sys:
								htop['q2Up'+str(i)].Write()
								htop['q2Down'+str(i)].Write()
						if hewk[str(i)].Integral() > 0:  
							hewk[str(i)].Write()
							if doAllSys:
								for systematic in systematicList:
									if systematic=='toppt': continue
									if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
										hewk[systematic+'Up'+str(i)].Scale(hewk[str(i)].Integral()/hewk[systematic+'Up'+str(i)].Integral())
										hewk[systematic+'Down'+str(i)].Scale(hewk[str(i)].Integral()/hewk[systematic+'Down'+str(i)].Integral()) 
									hewk[systematic+'Up'+str(i)].Write()
									hewk[systematic+'Down'+str(i)].Write()
								for pdfInd in range(100): hewk['pdf'+str(pdfInd)+'_'+str(i)].Write()
						if hqcd[str(i)].Integral() > 0:  
							hqcd[str(i)].Write()
							if doAllSys:
								for systematic in systematicList:
									if systematic == 'pdf' or systematic == 'pdfNew' or systematic == 'muR' or systematic == 'muF' or systematic == 'muRFcorrd' or systematic=='toppt': continue
									hqcd[systematic+'Up'+str(i)].Write()
									hqcd[systematic+'Down'+str(i)].Write()
								for pdfInd in range(100): hqcd['pdf'+str(pdfInd)+'_'+str(i)].Write()
						hdata[str(i)].Write()
						i+=1
			outputRfile.Close()
	
		stdout_old = sys.stdout
		logFile = open(outDir+'/yields_'+discriminant+'_'+lumiStr+'fb_'+decay+'.txt','a')
		sys.stdout = logFile

		## PRINTING YIELD TABLE WITH STATISTICAL UNCERTAINTIES ##
		#first print table without background grouping
		ljust_i = 1
		print 'CUTS:',cutString
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for bkg in bkgStackList: print bkg.ljust(ljust_i),
		print 'data'.ljust(ljust_i),
		print
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
					for bkg in bkgStackList:
						print str(yieldTable[histoPrefix][bkg]).ljust(ljust_i),
					print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
					print

		print 'YIELDS ERRORS'
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
					for bkg in bkgStackList:
						print str(math.sqrt(yieldStatErrTable[histoPrefix][bkg])).ljust(ljust_i),
					print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
					print

		#now print with top,ewk,qcd grouping
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		print 'ewk'.ljust(ljust_i),
		print 'top'.ljust(ljust_i),
		print 'qcd'.ljust(ljust_i),
		print 'data'.ljust(ljust_i),
		print
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
					print str(yieldTable[histoPrefix]['ewk']).ljust(ljust_i),
					print str(yieldTable[histoPrefix]['top']).ljust(ljust_i),
					print str(yieldTable[histoPrefix]['qcd']).ljust(ljust_i),
					print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
					print

		print 'YIELDS ERRORS'
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
					print str(math.sqrt(yieldStatErrTable[histoPrefix]['ewk'])).ljust(ljust_i),
					print str(math.sqrt(yieldStatErrTable[histoPrefix]['top'])).ljust(ljust_i),
					print str(math.sqrt(yieldStatErrTable[histoPrefix]['qcd'])).ljust(ljust_i),
					print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
					print

		#print yields for signals
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for sig in sigList: print sig.ljust(ljust_i),
		print
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
					for sig in sigList:
						print str(yieldTable[histoPrefix][sig]).ljust(ljust_i),
					print

		print 'YIELDS ERRORS'
		for isEM in isEMlist:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
					for sig in sigList:
						print str(math.sqrt(yieldStatErrTable[histoPrefix][sig])).ljust(ljust_i),
					print
				
		#print for AN tables
		print
		print "FOR AN (errors are statistical+normalization systematics): "
		print
		print 'YIELDS ELECTRON+JETS'.ljust(20*ljust_i), 
		for isEM in ['isE']:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
		print
		for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
			print process.ljust(ljust_i),
			for isEM in ['E']:
				for nWtag in nWtaglist:
					for nBtag in nbtaglist:
						histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
						if process=='dataOverBkg':
							dataTemp = yieldTable[histoPrefix]['data']+1e-20
							dataTempErr = yieldStatErrTable[histoPrefix]['data']
							totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
							totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
							totBkgTempErr += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
							totBkgTempErr += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
							totBkgTempErr += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
							totBkgTempErr += (corrdSys*totBkgTemp)**2
							dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
							print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
						else:
							yieldtemp = yieldTable[histoPrefix][process]
							yielderrtemp = yieldStatErrTable[histoPrefix][process]
							if process=='totBkg': 
								yielderrtemp += (corrdSys*yieldtemp)**2
								yielderrtemp += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
								yielderrtemp += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
								yielderrtemp += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
							elif process in sigList: 
								yielderrtemp += (corrdSys*yieldtemp)**2
							elif process!='data': 
								yielderrtemp += (corrdSys*yieldtemp)**2
								yielderrtemp += (addSys[process+'_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix][process])**2
							if process=='data': print ' & '+str(int(yieldtemp)),
							elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
							else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
			print '\\\\',
			print
		print
		print 'YIELDS MUON+JETS'.ljust(20*ljust_i), 
		for isEM in ['isM']:
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
		print
		for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
			print process.ljust(ljust_i),
			for isEM in ['M']:
				for nWtag in nWtaglist:
					for nBtag in nbtaglist:
						histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
						if process=='dataOverBkg':
							dataTemp = yieldTable[histoPrefix]['data']+1e-20
							dataTempErr = yieldStatErrTable[histoPrefix]['data']
							totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
							totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
							totBkgTempErr += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
							totBkgTempErr += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
							totBkgTempErr += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
							totBkgTempErr += (corrdSys*totBkgTemp)**2
							dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
							print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
						else:
							yieldtemp = yieldTable[histoPrefix][process]
							yielderrtemp = yieldStatErrTable[histoPrefix][process]
							if process=='totBkg': 
								yielderrtemp += (corrdSys*yieldtemp)**2
								yielderrtemp += (addSys['top_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['top'])**2
								yielderrtemp += (addSys['ewk_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['ewk'])**2
								yielderrtemp += (addSys['qcd_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix]['qcd'])**2
							elif process in sigList: 
								yielderrtemp += (corrdSys*yieldtemp)**2
							elif process!='data': 
								yielderrtemp += (corrdSys*yieldtemp)**2
								yielderrtemp += (addSys[process+'_'+nWtag+'_'+nBtag]*yieldTable[histoPrefix][process])**2
							if process=='data': print ' & '+str(int(yieldtemp)),
							elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
							else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
			print '\\\\',
			print
		
		#print for AN tables systematics
		if doAllSys:
			print
			print "FOR AN (shape systematic percentaces): "
			print
			print 'YIELDS'.ljust(20*ljust_i), 
			for isEM in isEMlist:
				for nWtag in nWtaglist:
					for nBtag in nbtaglist:
						print (isEM+'_nW'+nWtag+'_nB'+nBtag).ljust(ljust_i),
			print
			for process in ['ewk','top']+sigList:
				print process.ljust(ljust_i),
				print
				for ud in ['Up','Down']:
					for systematic in systematicList:
						if systematic=='toppt' and process!='top': continue
						print (systematic+ud).ljust(ljust_i),
						for isEM in isEMlist:
							for nWtag in nWtaglist:
								for nBtag in nbtaglist:
									histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
									print ' & '+str(round_sig(yieldTable[histoPrefix+systematic+ud][process]/yieldTable[histoPrefix][process],2)),
						print '\\\\',
						print
					if process!='top': continue
					print ('q2'+ud).ljust(ljust_i),
					for isEM in isEMlist:
						for nWtag in nWtaglist:
							for nBtag in nbtaglist:
								histoPrefix=discriminant+'_'+lumiStr+'fb_is'+isEM+'_nW'+nWtag+'_nB'+nBtag
								print ' & '+str(round_sig(yieldTable[histoPrefix+'q2'+ud][process]/yieldTable[histoPrefix][process],2)),
					print '\\\\',
					print
		
		print
		print "FOR PAS (errors are statistical+normalization systematics): " #combines e/m channels
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for nWtag in nWtaglist:
			for nBtag in nbtaglist:
				print ('tags00'+nWtag+'_nB'+nBtag).ljust(ljust_i),
		print
		for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
			print process.ljust(ljust_i),
			for nWtag in nWtaglist:
				for nBtag in nbtaglist:
					histoPrefix=discriminant+'_'+lumiStr+'fb_isE_nW'+nWtag+'_nB'+nBtag
					if process=='dataOverBkg':
						dataTemp = yieldTable[histoPrefix]['data']+yieldTable[histoPrefix.replace('_isE','_isM')]['data']+1e-20
						dataTempErr = yieldStatErrTable[histoPrefix]['data']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['data']
						totBkgTemp = yieldTable[histoPrefix]['totBkg']+yieldTable[histoPrefix.replace('_isE','_isM')]['totBkg']+1e-20
						totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['totBkg'] # statistical error squared
						totBkgTempErr += (addSys['top_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						totBkgTempErr += (addSys['ewk_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						totBkgTempErr += (addSys['qcd_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						totBkgTempErr += (corrdSys*totBkgTemp)**2
						dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
						print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
					else:
						yieldtemp = yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]
						yielderrtemp = yieldStatErrTable[histoPrefix][process]++yieldStatErrTable[histoPrefix.replace('_isE','_isM')][process]
						if process=='totBkg': 
							yielderrtemp += (corrdSys*yieldtemp)**2
							yielderrtemp += (addSys['top_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
							yielderrtemp += (addSys['ewk_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
							yielderrtemp += (addSys['qcd_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						elif process in sigList: 
							yielderrtemp += (corrdSys*yieldtemp)**2
						elif process!='data': 
							yielderrtemp += (corrdSys*yieldtemp)**2
							yielderrtemp += (addSys[process+'_'+nWtag+'_'+nBtag]*(yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						if process=='data': print ' & '+str(int(yieldtemp)),
						elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
						else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
			print '\\\\',
			print
		
		sys.stdout = stdout_old
		logFile.close()

datahists = {}
bkghists  = {}
sighists  = {}
for isEM in isEMlist:
	for nWtag in nWtaglist:
		for nbtag in nbtaglist:
			print "LOADING: ",isEM+'_nW'+nWtag+'_nB'+nbtag
			datahists.update(pickle.load(open(outDir+'/'+isEM+'_nW'+nWtag+'_nB'+nbtag+'/datahists.p','rb')))
			bkghists.update(pickle.load(open(outDir+'/'+isEM+'_nW'+nWtag+'_nB'+nbtag+'/bkghists.p','rb')))
			sighists.update(pickle.load(open(outDir+'/'+isEM+'_nW'+nWtag+'_nB'+nbtag+'/sighists.p','rb')))
# for key in bkghists.keys(): bkghists[key].Scale(2263./2215.)
# for key in sighists.keys(): sighists[key].Scale(2263./2215.)

print "MAKING CATEGORIES FOR TOTAL SIGNALS ..."
makeThetaCats(datahists,sighists,bkghists,iPlot)
print "MAKING CATEGORIES FOR DECAY CHANNELS ..."
if len(decays)>1: makeThetaCatsIndDecays(datahists,sighists,bkghists,iPlot)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


