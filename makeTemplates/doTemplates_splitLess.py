#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools
from ROOT import gROOT,TFile
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from weights import *
from modSyst_split import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

iPlot = 'ST'
region='SR' #PS,SR,TTCR,WJCR
isCategorized=True
cutString='splitLess'#lep40_MET60_DR0_1jet200_2jet100'
if region=='SR': pfix='templates_'
if region=='TTCR': pfix='ttbar_'
if region=='WJCR': pfix='wjets_'
if region=='HCR': pfix='higgs_'
if region=='CR': pfix='templatesCR_'
if region=='CRall': pfix='control_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+='BB_NewEl'
#pfix+='ST_2016_11_13_wJSF'
outDir = os.getcwd()+'/'+pfix+'/'+cutString
inDir = os.getcwd()+'/'+pfix+'/'

scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = True
lumiScaleCoeff = 35867./36814.
doAllSys = True
doQ2sys = False
if not doAllSys: doQ2sys = False
addCRsys = False
systematicList = ['pileup','jec','jer','tau21','jmr','jms','muR','muF','muRFcorrd','jsf','toppt','trigeff','btag','mistag','taupt']#,,'topsf'
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes signal processes only !!!!
		       
bkgProcList = ['TTJets','T','WJets','ZJets','VV','QCD']
wjetList  = ['WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500']
zjetList  = ['DYMG']
vvList    = ['WW','WZ','ZZ']
ttjetList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt']
tList     = ['Tt','Tbt','Ts','TtW','TbtW']

bkgGrupList = ['TTJets','WJets','top','ZJets','ewk','qcd']
topList = ttjetList+tList #ttwList+ttzList+
ewkList = wjetList+zjetList+vvList #
qcdList = ['QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']
dataList = ['DataERRBCDEFGH','DataMRRBCDEFGH']

#q2UpList   = ['TTJetsPHQ2U','Tt','Ts','TtWQ2U','TbtWQ2U']+ttwList+ttzList
#q2DownList = ['TTJetsPHQ2D','Tt','Ts','TtWQ2D','TbtWQ2D']+ttwList+ttzList
q2ttUpList   = ['TTJetsPHQ2U']
q2ttDownList = ['TTJetsPHQ2D']
q2stUpList   = ['Tt','Ts','TtWQ2U','TbtWQ2U']#,'TTJetsPHQ2U'
q2stDownList = ['Tt','Ts','TtWQ2D','TbtWQ2D']#,'TTJetsPHQ2D'

whichSignal = 'BB' #TT, BB, or X53X53
signalMassRange = [800,1800]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time

doBRScan = True
BRs={}
nBRconf=1
if whichSignal=='TT':
	BRs['BW']=[0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]#
	BRs['TH']=[0.25,0.5,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]#
	BRs['TZ']=[0.25,0.5,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]#
	nBRconf=len(BRs['BW'])
elif whichSignal=='BB':
	BRs['TW']=[0.50,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8]#
	BRs['BH']=[0.25,0.5,0.0,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2]#
	BRs['BZ']=[0.25,0.5,0.0,0.0,1.0,0.8,0.6,0.4,0.2,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0]#
	nBRconf=len(BRs['TW'])
if not doBRScan: nBRconf=1

isEMlist =['E','M']
if region=='SR': nHtaglist=['0','1b','2b']
elif 'CR' in region:
	if region=='HCR': nHtaglist=['1b','2b']
	elif region=='CR': nHtaglist=['0','1p']
	elif region=='CRall': nHtaglist=['0','1b','2b']
	else: nHtaglist=['0']
else: nHtaglist = ['0p']

if region=='TTCR' or region=='HCR' or region=='CR': nWtaglist = ['0p']
else: nWtaglist=['0','0p','1p']

if region=='WJCR': nbtaglist = ['0']
elif region=='HCR' or region=='CR': nbtaglist = ['0','1p']
elif region=='TTCR': nbtaglist = ['1','2','3p']
else: nbtaglist=['0','1','1p','2','3p']
if not isCategorized: 	
	nHtaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	if region=='WJCR': nbtaglist = ['0']
	if region=='TTCR': nbtaglist = ['1p']
	if region=='HCR': 
		nHtaglist = ['1p']
		nbtaglist = ['1p']
njetslist=['3p']
if region=='PS': njetslist=['3p']
print 'EMlist = ',isEMlist
print 'Hlist = ',nHtaglist
print 'Wlist = ',nWtaglist
print 'blist = ',nbtaglist

catList = []
tagList = []
regiontag =''
for item in list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist,njetslist)):
	if isCategorized:
		if 'b' in item[1]:
			if item[2] != '0p': continue
			if region == 'CRall':
				if item[3] != '0' and item[3] != '1p': continue
			else:
				if item[3] != '1p' and region != 'WJCR' and region != 'HCR' and region != 'CR': continue
		elif 'b' not in item[1]:
			if region == 'CRall':
				if item[2] == '0' and item[3] != '0': continue
				elif item[2] == '1p' and item[3] != '0': continue
				elif item[2] == '0p' and (item[3] == '0' or item[3] == '1p'): continue
			else:
				if item[2] == '0p' and region != 'TTCR' and region != 'HCR' and region != 'CR': continue
				if item[3] == '1p' and region != 'CR': continue
		if 'CR' in region: regiontag = 'isCR'
		else: regiontag = 'isSR'

	catList.append('_is'+item[0]+'_nH'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4])
	if item[0] == 'E': tagList.append('nH'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4])

print catList
print tagList

lumiSys = math.sqrt(0.026**2 + 0.05**2) #lumi uncertainty plus higgs prop.
eltrigSys = 0.01 #electron trigger uncertainty
mutrigSys = 0.01 #muon trigger uncertainty
elIdSys = 0.02 #electron id uncertainty
muIdSys = 0.03 #muon id uncertainty
elIsoSys = 0.01 #electron isolation uncertainty
muIsoSys = 0.01 #muon isolation uncertainty

elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

for tag in tagList:
	modTag = tag[tag.find('nW'):]
	modelingSys['data_'+modTag] = 0.
	modelingSys['qcd_'+modTag] = 0.
	modelingSys['ZJets_'+modTag] = 0.
	if not addCRsys: modelingSys['ewk_'+modTag],modelingSys['top_'+modTag] = 0.,0.

postTag = 'isSR_'
###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeThetaCats(datahists,sighists,bkghists,discriminant):
	# yieldTable = {}
	# yieldStatErrTable = {}
	# for cat in catList:
	# 	histoPrefix=discriminant+'_'+lumiStr+'fb'+cat
	# 	yieldTable[histoPrefix]={}
	# 	yieldStatErrTable[histoPrefix]={}
	# 	if doAllSys:
	# 		for syst in systematicList:
	# 			for ud in ['Up','Down']:
	# 				yieldTable[histoPrefix+syst+ud]={}
			
	# 	if doQ2sys:
	# 		yieldTable[histoPrefix+'q2Up']={}
	# 		yieldTable[histoPrefix+'q2Down']={}

	for BRind in range(nBRconf):
		BRconfStr=''
		if doBRScan: 
			if whichSignal=='TT': BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
			elif whichSignal=='BB': BRconfStr='_tW'+str(BRs['TW'][BRind]).replace('.','p')+'_bZ'+str(BRs['BZ'][BRind]).replace('.','p')+'_bH'+str(BRs['BH'][BRind]).replace('.','p')
		print "       BR Configuration:"+BRconfStr
		#Initialize dictionaries for histograms
		hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
		hwjets,hzjets,httjets,ht,hvv={},{},{},{},{}
		for cat in catList:
			print "              processing cat: "+cat
			histoPrefix=discriminant+'_'+lumiStr+'fb'+cat
			histoPrefix2=discriminant+'_'+lumiStr+'fb'+cat.replace('nJ3p',regiontag)
			i=BRconfStr+cat
			
			#Group processes
			hwjets[i] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix2+'__WJets')
			hzjets[i] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix2+'__DYJets')
			httjets[i] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix2+'__TTbar')
			ht[i] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix2+'__SingleTop')
			hvv[i] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix2+'__ewk')
			for bkg in ttjetList:
				if bkg!=ttjetList[0]: httjets[i].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in wjetList:
				if bkg!=wjetList[0]: hwjets[i].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in tList:
				if bkg!=tList[0]: ht[i].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in zjetList:
				if bkg!=zjetList[0]: hzjets[i].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in vvList:
				if bkg!=vvList[0]: hvv[i].Add(bkghists[histoPrefix+'_'+bkg])
	
			#Group QCD processes
			hqcd[i] = bkghists[histoPrefix+'_'+qcdList[0]].Clone(histoPrefix2+'__QCD')
			for bkg in qcdList: 
				if bkg!=qcdList[0]: 
					hqcd[i].Add(bkghists[histoPrefix+'_'+bkg])
		
			#Group OTHER EWK processes
			hewk[i] = bkghists[histoPrefix+'_'+ewkList[0]].Clone(histoPrefix2+'__EWK')
			for bkg in ewkList:
				if bkg!=ewkList[0]: hewk[i].Add(bkghists[histoPrefix+'_'+bkg])
		
			#Group OTHER TOP processes
			htop[i] = bkghists[histoPrefix+'_'+topList[0]].Clone(histoPrefix2+'__TOP')
			for bkg in topList:
				if bkg!=topList[0]: htop[i].Add(bkghists[histoPrefix+'_'+bkg])
	
			#get signal
			for signal in sigList:
				i=BRconfStr+cat+signal
				hsig[i] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix2+'__sig')
				if doBRScan: hsig[i].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
				for decay in decays:
					if decay!=decays[0]:
						htemp = sighists[histoPrefix+'_'+signal+decay].Clone()
						if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
						hsig[i].Add(htemp)
			i=BRconfStr+cat

			#systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						if syst!='toppt':
							hqcd[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+qcdList[0]].Clone(histoPrefix2+'__QCD__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							hewk[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+ewkList[0]].Clone(histoPrefix2+'__EWK__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							#hwjets[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+wjetList[0]].Clone(histoPrefix2+'__WJets__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							httjets[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+ttjetList[0]].Clone(histoPrefix2+'__TTbar__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							ht[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+tList[0]].Clone(histoPrefix2+'__SingleTop__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							#hzjets[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+zjetList[0]].Clone(histoPrefix2+'__DYJets__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							#hvv[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+vvList[0]].Clone(histoPrefix2+'__ewk__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))

							for bkg in qcdList: 
								if bkg!=qcdList[0]: hqcd[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for bkg in ewkList: 
								if bkg!=ewkList[0]: hewk[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							#for bkg in wjetList: 
							#	if bkg!=wjetList[0]: hwjets[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for bkg in tList: 
								if bkg!=tList[0]: ht[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for bkg in ttjetList: 
								if bkg!=ttjetList[0]: httjets[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							#for bkg in vvList: 
							#	if bkg!=vvList[0]: hvv[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for signal in sigList:
								i=BRconfStr+cat+signal
								hsig[syst+ud+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decays[0]].Clone(histoPrefix2+'__sig__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
								if doBRScan: hsig[syst+ud+str(i)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
								for decay in decays:
									htemp = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decay].Clone()
									if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
									if decay!=decays[0]: hsig[syst+ud+str(i)].Add(htemp)
							i=BRconfStr+cat
						if syst=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
							httjets[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+ttjetList[0]].Clone(histoPrefix2+'__TTbar__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in ttjetList: 
								if bkg!=ttjetList[0]: httjets[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for bkg in ttjetList: 
								if bkg not in ttjetList: httjets[syst+ud+str(i)].Add(bkghists[histoPrefix+'_'+bkg])
				for pdfInd in range(100):
					hqcd['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix2+'__QCD__pdf'+str(pdfInd))
					hewk['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix2+'__EWK__pdf'+str(pdfInd))
					#hwjets['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+wjetList[0]].Clone(histoPrefix2+'__WJets__pdf'+str(pdfInd))
					httjets['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ttjetList[0]].Clone(histoPrefix2+'__TTbar__pdf'+str(pdfInd))
					#hzjets['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+zjetList[0]].Clone(histoPrefix2+'__DYJets__pdf'+str(pdfInd))
					ht['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+tList[0]].Clone(histoPrefix2+'__SingleTop__pdf'+str(pdfInd))
					#hvv['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+vvList[0]].Clone(histoPrefix2+'__ewk__pdf'+str(pdfInd))
					for bkg in qcdList: 
						if bkg!=qcdList[0]: hqcd['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for bkg in ewkList: 
						if bkg!=ewkList[0]: hewk['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					#for bkg in wjetList: 
					#	if bkg!=wjetList[0]: hwjets['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for bkg in tList: 
						if bkg!=tList[0]: ht['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for bkg in ttjetList: 
						if bkg!=ttjetList[0]: httjets['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					#for bkg in vvList: 
					#	if bkg!=vvList[0]: hvv['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for signal in sigList:
						i=BRconfStr+cat+signal
						hsig['pdf'+str(pdfInd)+'_'+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix2+'__sig__pdf'+str(pdfInd))
						if doBRScan: hsig['pdf'+str(pdfInd)+'_'+str(i)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
						for decay in decays:
							htemp = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone()
							if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
							if decay!=decays[0]:hsig['pdf'+str(pdfInd)+'_'+str(i)].Add(htemp)
					i=BRconfStr+cat
											
			if doQ2sys:
				ht['q2Up'+str(i)] = bkghists[histoPrefix+'_'+q2stUpList[0]].Clone(histoPrefix2+'__SingleTop__q2__plus')
				ht['q2Down'+str(i)] = bkghists[histoPrefix+'_'+q2stDownList[0]].Clone(histoPrefix2+'__SingleTop__q2__minus')
				for ind in range(1,len(q2stUpList)):
					ht['q2Up'+str(i)].Add(bkghists[histoPrefix+'_'+q2stUpList[ind]])
					ht['q2Down'+str(i)].Add(bkghists[histoPrefix+'_'+q2stDownList[ind]])

				httjets['q2Up'+str(i)] = bkghists[histoPrefix+'_'+q2ttUpList[0]].Clone(histoPrefix2+'__TTbar__q2__plus')
				httjets['q2Down'+str(i)] = bkghists[histoPrefix+'_'+q2ttDownList[0]].Clone(histoPrefix2+'__TTbar__q2__minus')
				for ind in range(1,len(q2ttUpList)):
					httjets['q2Up'+str(i)].Add(bkghists[histoPrefix+'_'+q2ttUpList[ind]])
					httjets['q2Down'+str(i)].Add(bkghists[histoPrefix+'_'+q2ttDownList[ind]])
	
			#Group data processes
			hdata[i] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix2+'__DATA')
			for dat in dataList:
				if dat!=dataList[0]: hdata[i].Add(datahists[histoPrefix+'_'+dat])

			# #prepare yield table
			# yieldTable[histoPrefix]['top']    = htop[i].Integral()
			# yieldTable[histoPrefix]['ewk']    = hewk[i].Integral()
			# yieldTable[histoPrefix]['qcd']    = hqcd[i].Integral()
			# yieldTable[histoPrefix]['totBkg'] = ht[i].Integral()+hwjets[i].Integral()+hqcd[i].Integral()+httjets[i].Integral()+hzjets[i].Integral()+hvv[i].Integral()
			# yieldTable[histoPrefix]['data']   = hdata[i].Integral()
			# yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
			# yieldTable[histoPrefix]['WJets']  = hwjets[i].Integral()
			# yieldTable[histoPrefix]['ZJets']  = hzjets[i].Integral()
			# yieldTable[histoPrefix]['VV']     = hvv[i].Integral()
			# yieldTable[histoPrefix]['TTJets'] = httjets[i].Integral()
			# yieldTable[histoPrefix]['T']      = ht[i].Integral()
			# yieldTable[histoPrefix]['QCD']    = hqcd[i].Integral()
			# for signal in sigList: 
			# 	i=BRconfStr+cat+signal
			# 	yieldTable[histoPrefix][signal] = hsig[i].Integral()
			# i=BRconfStr+cat
	
			# #+/- 1sigma variations of shape systematics
			# if doAllSys:
			# 	for syst in systematicList:
			# 		for ud in ['Up','Down']:
			# 			yieldTable[histoPrefix+syst+ud]['TTJets']    = httjets[syst+ud+str(i)].Integral()
			# 			if syst!='toppt':
			# 				yieldTable[histoPrefix+syst+ud]['T']    = ht[syst+ud+str(i)].Integral()
			# 				yieldTable[histoPrefix+syst+ud]['qcd']    = hqcd[syst+ud+str(i)].Integral()
			# 				yieldTable[histoPrefix+syst+ud]['ZJets']    = hzjets[syst+ud+str(i)].Integral()
			# 				yieldTable[histoPrefix+syst+ud]['VV']    = hvv[syst+ud+str(i)].Integral()
			# 				yieldTable[histoPrefix+syst+ud]['WJets']    = hwjets[syst+ud+str(i)].Integral()
			# 				yieldTable[histoPrefix+syst+ud]['totBkg'] = ht[syst+ud+str(i)].Integral()+hwjets[syst+ud+str(i)].Integral()+hqcd[syst+ud+str(i)].Integral()+httjets[syst+ud+str(i)].Integral()+hzjets[syst+ud+str(i)].Integral()+hvv[syst+ud+str(i)].Integral()
			# 				for signal in sigList: 
			# 					i=BRconfStr+cat+signal
			# 					yieldTable[histoPrefix+syst+ud][signal] = hsig[syst+ud+str(i)].Integral()
			# 				i=BRconfStr+cat
				
			# if doQ2sys:
			# 	yieldTable[histoPrefix+'q2Up']['top']    = ht['q2Up'+str(i)].Integral()
			# 	yieldTable[histoPrefix+'q2Down']['top']    = ht['q2Down'+str(i)].Integral()
			# 	yieldTable[histoPrefix+'q2Up']['TTJets']    = httjets['q2Up'+str(i)].Integral()
			# 	yieldTable[histoPrefix+'q2Down']['TTJets']    = httjets['q2Down'+str(i)].Integral()

			# #prepare MC yield error table
			# yieldStatErrTable[histoPrefix]['top']    = 0.
			# yieldStatErrTable[histoPrefix]['ewk']    = 0.
			# yieldStatErrTable[histoPrefix]['qcd']    = 0.
			# yieldStatErrTable[histoPrefix]['totBkg'] = 0.
			# yieldStatErrTable[histoPrefix]['data']   = 0.
			# yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.
			# yieldStatErrTable[histoPrefix]['WJets']  = 0.
			# yieldStatErrTable[histoPrefix]['ZJets']  = 0.
			# yieldStatErrTable[histoPrefix]['VV']     = 0.
			# yieldStatErrTable[histoPrefix]['TTJets'] = 0.
			# yieldStatErrTable[histoPrefix]['T']      = 0.
			# yieldStatErrTable[histoPrefix]['QCD']    = 0.
			# for signal in sigList: yieldStatErrTable[histoPrefix][signal] = 0.

			# for ibin in range(1,htop[i].GetXaxis().GetNbins()+1):
			# 	yieldStatErrTable[histoPrefix]['top']    += htop[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['ewk']    += hewk[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['qcd']    += hqcd[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['totBkg'] += ht[i].GetBinError(ibin)**2+hwjets[i].GetBinError(ibin)**2+hqcd[i].GetBinError(ibin)**2+httjets[i].GetBinError(ibin)**2+hzjets[i].GetBinError(ibin)**2+hvv[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['data']   += hdata[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['WJets']  += hwjets[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['ZJets']  += hzjets[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['VV']     += hvv[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['TTJets'] += httjets[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['T']      += ht[i].GetBinError(ibin)**2
			# 	yieldStatErrTable[histoPrefix]['QCD']    += hqcd[i].GetBinError(ibin)**2
			# 	for signal in sigList: 
			# 		i=BRconfStr+cat+signal
			# 		yieldStatErrTable[histoPrefix][signal] += hsig[i].GetBinError(ibin)**2
			# 	i=BRconfStr+cat
			# for key in yieldStatErrTable[histoPrefix].keys(): yieldStatErrTable[histoPrefix][key] = math.sqrt(yieldStatErrTable[histoPrefix][key])

		#scale signal cross section to 1pb
		print "SCALING SIGNAL TEMPLATES TO 1pb ..."
		if scaleSignalXsecTo1pb:
			for signal in sigList:
				thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+'fb'+'.root'
				thetaRfile = TFile(thetaRfileName,'RECREATE')
				for cat in catList:
					i=BRconfStr+cat+signal
					hsig[i].Scale(1./xsec[signal])
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hsig[syst+'Up'+str(i)].Scale(1./xsec[signal])
							hsig[syst+'Down'+str(i)].Scale(1./xsec[signal])
							if normalizeRENORM_PDF and (syst.startswith('mu') or syst=='pdf'):
								hsig[syst+'Up'+str(i)].Scale(hsig[i].Integral()/hsig[syst+'Up'+str(i)].Integral())
								hsig[syst+'Down'+str(i)].Scale(hsig[i].Integral()/hsig[syst+'Down'+str(i)].Integral())
						for pdfInd in range(100): 
							hsig['pdf'+str(pdfInd)+'_'+str(i)].Scale(1./xsec[signal])

		#Theta templates:
		print "WRITING THETA TEMPLATES: "
		for signal in sigList:
			print "              ... "+signal
			thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+'fb'+'.root'
			thetaRfile = TFile(thetaRfileName,'RECREATE')
			for cat in catList:
				i=BRconfStr+cat+signal
				if hsig[i].Integral() > 0:
					hsig[i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hsig[syst+'Up'+str(i)].Write()
							hsig[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): hsig['pdf'+str(pdfInd)+'_'+str(i)].Write()
				i=BRconfStr+cat
				if ht[i].Integral() > 0:
					ht[i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							ht[syst+'Up'+str(i)].Write()
							ht[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): ht['pdf'+str(pdfInd)+'_'+str(i)].Write()
					if doQ2sys:
						ht['q2Up'+str(i)].Write()
						ht['q2Down'+str(i)].Write()
				if httjets[i].Integral() > 0:
					httjets[i].Write()
					if doAllSys:
						for syst in systematicList:
							httjets[syst+'Up'+str(i)].Write()
							httjets[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): httjets['pdf'+str(pdfInd)+'_'+str(i)].Write()
					if doQ2sys:
						httjets['q2Up'+str(i)].Write()
						httjets['q2Down'+str(i)].Write()
				if hewk[i].Integral() > 0:
					hewk[i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hewk[syst+'Up'+str(i)].Write()
							hewk[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): hewk['pdf'+str(pdfInd)+'_'+str(i)].Write()
				# if hwjets[i].Integral() > 0:
				# 	hwjets[i].Write()
				# 	if doAllSys:
				# 		for syst in systematicList:
				# 			if syst=='toppt': continue
				# 			hwjets[syst+'Up'+str(i)].Write()
				# 			hwjets[syst+'Down'+str(i)].Write()
				# 		for pdfInd in range(100): hwjets['pdf'+str(pdfInd)+'_'+str(i)].Write()
				# if hvv[i].Integral() > 0:
				# 	hvv[i].Write()
				# 	if doAllSys:
				# 		for syst in systematicList:
				# 			if syst=='toppt': continue
				# 			hvv[syst+'Up'+str(i)].Write()
				# 			hvv[syst+'Down'+str(i)].Write()
				# 		for pdfInd in range(100): hvv['pdf'+str(pdfInd)+'_'+str(i)].Write()
				# if hzjets[i].Integral() > 0:
				# 	hzjets[i].Write()
				# 	if doAllSys:
				# 		for syst in systematicList:
				# 			if syst=='toppt': continue
				# 			hzjets[syst+'Up'+str(i)].Write()
				# 			hzjets[syst+'Down'+str(i)].Write()
				# 		for pdfInd in range(100): hzjets['pdf'+str(pdfInd)+'_'+str(i)].Write()
				if hqcd[i].Integral() > 0:
					hqcd[i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hqcd[syst+'Up'+str(i)].Write()
							hqcd[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): hqcd['pdf'+str(pdfInd)+'_'+str(i)].Write()
				hdata[i].Write()
			thetaRfile.Close()

		#Combine templates:
		'''
		print "WRITING COMBINE TEMPLATES: "
		combineRfileName = outDir+'/templates_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.root'
		combineRfile = TFile(combineRfileName,'RECREATE')
		for cat in catList:
			print "              ... "+cat
			i=BRconfStr+cat
			for signal in sigList:
				mass = [str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100) if str(mass) in signal][0]
				i=BRconfStr+cat+signal
				hsig[i].SetName(hsig[i].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
				hsig[i].Write()
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt': continue
						hsig[syst+'Up'+str(i)].SetName(hsig[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__plus','Up'))
						hsig[syst+'Down'+str(i)].SetName(hsig[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__minus','Down'))
						hsig[syst+'Up'+str(i)].Write()
						hsig[syst+'Down'+str(i)].Write()
					for pdfInd in range(100): 
						hsig['pdf'+str(pdfInd)+'_'+str(i)].SetName(hsig['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
						hsig['pdf'+str(pdfInd)+'_'+str(i)].Write()
			i=BRconfStr+cat
			htop[i].SetName(htop[i].GetName().replace('fb_','fb_'+postTag))
			htop[i].Write()
			if doAllSys:
				for syst in systematicList:
					htop[syst+'Up'+str(i)].SetName(htop[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					htop[syst+'Down'+str(i)].SetName(htop[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					htop[syst+'Up'+str(i)].Write()
					htop[syst+'Down'+str(i)].Write()
				for pdfInd in range(100): 
					htop['pdf'+str(pdfInd)+'_'+str(i)].SetName(htop['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag))
					htop['pdf'+str(pdfInd)+'_'+str(i)].Write()
			if doQ2sys:
				htop['q2Up'+str(i)].SetName(htop['q2Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
				htop['q2Down'+str(i)].SetName(htop['q2Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
				htop['q2Up'+str(i)].Write()
				htop['q2Down'+str(i)].Write()
			hewk[i].SetName(hewk[i].GetName().replace('fb_','fb_'+postTag))
			hewk[i].Write()
			if doAllSys:
				for syst in systematicList:
					if syst=='toppt': continue
					hewk[syst+'Up'+str(i)].SetName(hewk[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					hewk[syst+'Down'+str(i)].SetName(hewk[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					hewk[syst+'Up'+str(i)].Write()
					hewk[syst+'Down'+str(i)].Write()
				for pdfInd in range(100): 
					hewk['pdf'+str(pdfInd)+'_'+str(i)].SetName(hewk['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag))
					hewk['pdf'+str(pdfInd)+'_'+str(i)].Write()
			hqcd[i].SetName(hqcd[i].GetName().replace('fb_','fb_'+postTag))
			hqcd[i].Write()
			if doAllSys:
				for syst in systematicList:
					if syst=='toppt': continue
					hqcd[syst+'Up'+str(i)].SetName(hqcd[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					hqcd[syst+'Down'+str(i)].SetName(hqcd[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					hqcd[syst+'Up'+str(i)].Write()
					hqcd[syst+'Down'+str(i)].Write()
				for pdfInd in range(100): 
					hqcd['pdf'+str(pdfInd)+'_'+str(i)].SetName(hqcd['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag))
					hqcd['pdf'+str(pdfInd)+'_'+str(i)].Write()
			hdata[i].SetName(hdata[i].GetName().replace('fb_','fb_'+postTag).replace('DATA','data_obs'))
			hdata[i].Write()
		combineRfile.Close()
		'''
		# table = []
		# table.append(['CUTS:',cutString])
		# table.append(['break'])
		# table.append(['break'])
		
		# #yields without background grouping
		# table.append(['YIELDS']+[proc for proc in bkgProcList+['data']])
		# for cat in catList:
		# 	row = [cat]
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb'+cat
		# 	for proc in bkgProcList+['data']:
		# 		row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		# 	table.append(row)			
		# table.append(['break'])
		# table.append(['break'])
		
		# #yields with top,ewk,qcd grouping
		# table.append(['YIELDS']+[proc for proc in bkgGrupList+['data']])
		# for cat in catList:
		# 	row = [cat]
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb'+cat
		# 	for proc in bkgGrupList+['data']:
		# 		row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		# 	table.append(row)
		# table.append(['break'])
		# table.append(['break'])
		
		# #yields for signals
		# table.append(['YIELDS']+[proc for proc in sigList])
		# for cat in catList:
		# 	row = [cat]
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb'+cat
		# 	for proc in sigList:
		# 		row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		# 	table.append(row)

		# #yields for AN tables (yields in e/m channels)
		# for isEM in isEMlist:
		# 	if isEM=='E': corrdSys = elcorrdSys
		# 	if isEM=='M': corrdSys = mucorrdSys
		# 	for nHtag in nHtaglist:
		# 		table.append(['break'])
		# 		table.append(['','is'+isEM+'_nH'+nHtag+'_yields'])
		# 		table.append(['break'])
		# 		table.append(['YIELDS']+[cat for cat in catList if 'is'+isEM in cat and 'nH'+nHtag in cat]+['\\\\'])
		# 		for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
		# 			row = [proc]
		# 			for cat in catList:
		# 				if not ('is'+isEM in cat and 'nH'+nHtag in cat): continue
		# 				modTag = cat[cat.find('nW'):]
		# 				histoPrefix=discriminant+'_'+lumiStr+'fb'+cat
		# 				yieldtemp = 0.
		# 				yielderrtemp = 0.
		# 				if proc=='totBkg' or proc=='dataOverBkg':
		# 					for bkg in bkgGrupList:
		# 						try:
		# 							yieldtemp += yieldTable[histoPrefix][bkg]
		# 							yielderrtemp += yieldStatErrTable[histoPrefix][bkg]**2
		# 							yielderrtemp += (modelingSys[bkg+'_'+modTag]*yieldTable[histoPrefix][bkg])**2
		# 						except:
		# 							print "Missing",bkg,"for channel:",cat
		# 							pass
		# 					yielderrtemp += (corrdSys*yieldtemp)**2
		# 					if proc=='dataOverBkg':
		# 						dataTemp = yieldTable[histoPrefix]['data']+1e-20
		# 						dataTempErr = yieldStatErrTable[histoPrefix]['data']**2
		# 						yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
		# 						yieldtemp = dataTemp/yieldtemp
		# 				else:
		# 					try:
		# 						yieldtemp += yieldTable[histoPrefix][proc]
		# 						yielderrtemp += yieldStatErrTable[histoPrefix][proc]**2
		# 					except:
		# 						print "Missing",proc,"for channel:",cat
		# 						pass
		# 					if proc not in sigList: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2
		# 					yielderrtemp += (corrdSys*yieldtemp)**2
		# 				yielderrtemp = math.sqrt(yielderrtemp)
		# 				if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefix][proc])))
		# 				else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
		# 			row.append('\\\\')
		# 			table.append(row)
		
		# #yields for PAS tables (yields in e/m channels combined)
		# for nHtag in nHtaglist:
		# 	table.append(['break'])
		# 	table.append(['','isL_nH'+nHtag+'_yields'])
		# 	table.append(['break'])
		# 	table.append(['YIELDS']+[cat.replace('isE','isL') for cat in catList if 'isE' in cat and 'nH'+nHtag in cat]+['\\\\'])
		# 	for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
		# 		row = [proc]
		# 		for cat in catList:
		# 			if not ('isE' in cat and 'nH'+nHtag in cat): continue
		# 			modTag = cat[cat.find('nW'):]
		# 			histoPrefixE = discriminant+'_'+lumiStr+'fb'+cat
		# 			histoPrefixM = histoPrefixE.replace('isE','isM')
		# 			yieldtemp = 0.
		# 			yieldtempE = 0.
		# 			yieldtempM = 0.
		# 			yielderrtemp = 0. 
		# 			if proc=='totBkg' or proc=='dataOverBkg':
		# 				for bkg in bkgGrupList:
		# 					try:
		# 						yieldtempE += yieldTable[histoPrefixE][bkg]
		# 						yieldtempM += yieldTable[histoPrefixM][bkg]
		# 						yieldtemp  += yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]
		# 						yielderrtemp += yieldStatErrTable[histoPrefixE][bkg]**2+yieldStatErrTable[histoPrefixM][bkg]**2
		# 						yielderrtemp += (modelingSys[bkg+'_'+modTag]*(yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]))**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
		# 					except:
		# 						print "Missing",bkg,"for channel:",cat
		# 						pass
		# 				yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
		# 				if proc=='dataOverBkg':
		# 					dataTemp = yieldTable[histoPrefixE]['data']+yieldTable[histoPrefixM]['data']+1e-20
		# 					dataTempErr = yieldStatErrTable[histoPrefixE]['data']**2+yieldStatErrTable[histoPrefixM]['data']**2
		# 					yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
		# 					yieldtemp = dataTemp/yieldtemp
		# 			else:
		# 				try:
		# 					yieldtempE += yieldTable[histoPrefixE][proc]
		# 					yieldtempM += yieldTable[histoPrefixM][proc]
		# 					yieldtemp  += yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc]
		# 					yielderrtemp += yieldStatErrTable[histoPrefixE][proc]**2+yieldStatErrTable[histoPrefixM][proc]**2
		# 				except:
		# 					print "Missing",proc,"for channel:",cat
		# 					pass
		# 				if proc not in sigList: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
		# 				yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
		# 			yielderrtemp = math.sqrt(yielderrtemp)
		# 			if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc])))
		# 			else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
		# 		row.append('\\\\')
		# 		table.append(row)

		# #systematics
		# if doAllSys:
		# 	table.append(['break'])
		# 	table.append(['','Systematics'])
		# 	table.append(['break'])
		# 	for proc in bkgGrupList+sigList:
		# 		table.append([proc]+[cat for cat in catList]+['\\\\'])
		# 		for syst in sorted(systematicList+['q2']):
		# 			for ud in ['Up','Down']:
		# 				row = [syst+ud]
		# 				for cat in catList:
		# 					histoPrefix = discriminant+'_'+lumiStr+'fb'+cat
		# 					nomHist = histoPrefix
		# 					shpHist = histoPrefix+syst+ud
		# 					try: row.append(' & '+str(round(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+1e-20),2)))
		# 					except:
		# 						if not ((syst=='toppt' or syst=='q2') and proc!='top'):
		# 							print "Missing",proc,"for channel:",cat,"and systematic:",syst
		# 						pass
		# 				row.append('\\\\')
		# 				table.append(row)
		# 		table.append(['break'])
			
		# if not addCRsys: out=open(outDir+'/yields_noCRunc_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','w')
		# else: out=open(outDir+'/yields_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','w')
		# printTable(table,out)
		
datahists = {}
bkghists  = {}
sighists  = {}
print "WORKING DIR:",inDir
print "CREADTING DIR:",outDir
if not os.path.exists(outDir): os.system('mkdir -p '+outDir)
print "LOADING:\n"
for cat in catList:
	cat = cat[1:]
	print "         ",cat[2:]
	datahists.update(pickle.load(open(inDir+'/'+cat[2:]+'/datahists_'+iPlot+'.p','rb')))
	bkghists.update(pickle.load(open(inDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
	sighists.update(pickle.load(open(inDir+'/'+cat[2:]+'/sighists_'+iPlot+'.p','rb')))
if scaleLumi:
	for key in bkghists.keys(): bkghists[key].Scale(lumiScaleCoeff)
	for key in sighists.keys(): sighists[key].Scale(lumiScaleCoeff)

print "MAKING CATEGORIES FOR TOTAL SIGNALS ..."
makeThetaCats(datahists,sighists,bkghists,iPlot)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


