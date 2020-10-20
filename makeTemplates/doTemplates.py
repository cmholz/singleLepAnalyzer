#!/usr:wq/bin/python

import os,sys,time,math,datetime,pickle,itertools,fnmatch
from ROOT import gROOT,TFile,TH1F
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from weights import *
from modSyst import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

region='PS' #PS,SR,TTCR,WJCR
isCategorized=False
pfix='templates'+region
if not isCategorized: pfix='kinematics'+region
pfix+='_June2020TT'
outDir = os.getcwd()+'/'+pfix+'/'

doCombineTemplates = False 
if isCategorized: doCombineTemplates = True
removeThreshold = 0.015
zero = 1e-12

scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = False
lumiScaleCoeff = 35867./59690.
doAllSys = True
addCRsys = False
doPDF = True
systematicList = ['muRFcorrd','trigeffEl','trigeffMu','pileup','jec','btag','jsf','Teff','Tmis','Heff','Hmis','Zeff','Zmis','Weff','Wmis','Beff','Bmis','Jeff','Jmis','jer','ltag']#,'toppt']
if isCategorized: systematicList = ['muRFcorrd','muR','muF','trigeffEl','trigeffMu','pileup','jec','btag','jsf','Teff','Tmis','Heff','Hmis','Zeff','Zmis','Weff','Wmis','Beff','Bmis','Jeff','Jmis','jer','ltag']
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes signal processes only !!!!
		       
bkgGrupList = ['top','ewk','qcd']
bkgProcList = ['TTJets','WJets','ZJets','VV','qcd','TTV','T']
bkgProcs = {}
bkgProcs['WJets']  = ['WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500']#'WJetsMG200',
bkgProcs['ZJets']  = ['DYMG400','DYMG600','DYMG800','DYMG1200','DYMG2500'] #'DYMG200',
bkgProcs['VV']     = ['WW','WZ','ZZ']
bkgProcs['TTV']    = ['TTWl','TTZl','TTHB','TTHnoB']#,'TTWq']#,'TTZq']
bkgProcs['TTJets'] = ['TTJetsSemiLep0','TTJetsSemiLep700','TTJetsSemiLep1000','TTJetsHad0','TTJetsHad700','TTJetsHad1000',
                      'TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000','TTJetsPH700mtt','TTJetsPH1000mtt']
#['TTJetsPH700mtt','TTJetsPH1000mtt','TTJetsHad0','TTJetsHad700','TTJetsHad1000','TTJetsSemiLep0','TTJetsSemiLep700','TTJetsSemiLep1000','TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000']#['TTJetsPS0','TTJetsPS700','TTJetsPS1000','TTJets0','TTJets700','TTJets1000','TTJetsPH700mtt','TTJetsPH1000mtt']

bkgProcs['T']      = ['Tt','Tbt','Ts','TtW','TbtW'] #'Tbs'
bkgProcs['qcd'] = ['QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000'] #'QCDht300',
bkgProcs['top'] = bkgProcs['TTJets']+bkgProcs['T']+bkgProcs['TTV']
bkgProcs['ewk'] = bkgProcs['WJets']+bkgProcs['ZJets']+bkgProcs['VV'] 
dataList = [
	'DataEBCDEFG',
	'DataMBCDEFG'
	#'Data18EG',
	#'Data18MU',
	]

topptProcs = ['top','TTJets']

whichSignal = 'TT' #HTB, TT, BB, or X53X53
massList = range(900,1800+1,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in massList for chiral in ['left','right']]
#print 'I made it here!'
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays

doBRScan = False
if isCategorized and 'SR' in region: doBRScan = True
elif isCategorized and 'CR' in region: doBRScan = True

BRs={}
if whichSignal=='TT':
	BRs['BW']=[0.50]#,0.0,1.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
	BRs['TH']=[0.25]#,0.5,0.0,1.0,0.0]#,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
	BRs['TZ']=[0.25]#,0.5,0.0,0.0,1.0]#,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
	nBRconf=len(BRs['BW'])
elif whichSignal=='BB':
        BRs['TW']=[0.0,0.50,1.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
        BRs['BH']=[0.5,0.25,0.0,1.0,0.0]#,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]  # May or may not want to keep these lines, have to ask
        BRs['BZ']=[0.5,0.25,0.0,0.0,1.0]#,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
	nBRconf=len(BRs['TW'])

if not doBRScan: nBRconf=1

isEMlist = ['E','M']
#isEMlist =['E','M','L']
#isEMlist =['L']
algolist = ['all']
if isCategorized or 'algos' in region or 'SR' in region: algolist = ['DeepAK8']#,'BEST'],'DeepAK8DC']
taglist = ['all']

if isCategorized:
        if region == 'SR' or region=='SCR': 
        	if whichSignal=='TT':
			taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW','notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
		if whichSignal=='BB':
			taglist=['taggedtWtW','taggedbZtW','taggedbHtW','notVbH','notVbZ','notVtW','notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']

        elif 'CR' in region: taglist=['dnnLargeT','dnnLargeH','dnnLargeW','dnnLargeZ','dnnLargeB','dnnLargeJwjet','dnnLargeJttbar']
        else: taglist = ['all']

#tagList = list(itertools.product(taglist,algolist))
catList = ['is'+item[0]+'_'+item[1]+'_'+item[2] for item in list(itertools.product(isEMlist,taglist,algolist))]
print 'catList', catList
#tagList = [item[0] for item in list(itertools.product(taglist))]

lumiSys = 0.023 #lumi uncertainty
eltrigSys = 0.0 #electron trigger uncertainty
mutrigSys = 0.0 #muon trigger uncertainty
elIdSys = 0.02 #electron id uncertainty
muIdSys = 0.02 #muon id uncertainty
elIsoSys = 0.015 #electron isolation uncertainty
muIsoSys = 0.015 #muon isolation uncertainty

elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

if 'CR' in region: postTag = 'isCR_'
else: postTag = 'isSR_'
###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeThetaCats(datahists,sighists,bkghists,discriminant):
	yieldTable = {}
	yieldStatErrTable = {}
	for cat in catList:
		
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
		yieldTable[histoPrefix]={}
		yieldStatErrTable[histoPrefix]={}
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+syst+ud]={}
			
	for BRind in range(nBRconf):
		BRconfStr=''
		if doBRScan and whichSignal=='TT': BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
		elif doBRScan and whichSignal=='BB': BRconfStr='_tW'+str(BRs['TW'][BRind]).replace('.','p')+'_bZ'+str(BRs['BZ'][BRind]).replace('.','p')+'_bH'+str(BRs['BH'][BRind]).replace('.','p')

		print "       BR Configuration:"+BRconfStr
		#Initialize dictionaries for histograms
		hists={}
		print "RESETTING HISTS. NOW CATLIST = ",catList
		print "SIGLIST = ",sigList
		print "BRCONFSTR = ",BRconfStr
		for cat in catList:
			print "              processing cat: "+cat
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			i=BRconfStr+cat
			#Group data processes
			hists['data'+i] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
			for dat in dataList:
			      	print 'dataList member',dat,'with integral',datahists[histoPrefix+'_'+dat].Integral()
				if dat!=dataList[0]: hists['data'+i].Add(datahists[histoPrefix+'_'+dat])
			
			#Group processes
			for proc in bkgProcList+bkgGrupList:
				hists[proc+i] = bkghists[histoPrefix+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc)
				for bkg in bkgProcs[proc]:
					print 'bkgList member',histoPrefix+'_'+bkg,'with integral',bkghists[histoPrefix+'_'+bkg].Integral()
					if bkg!=bkgProcs[proc][0]: hists[proc+i].Add(bkghists[histoPrefix+'_'+bkg])

			#get signal
			for signal in sigList:
				hists[signal+i] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
				#print "Adding to hists...",signal+i
				if doBRScan: hists[signal+i].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
				for decay in decays:
					if decay!=decays[0]:
						htemp = sighists[histoPrefix+'_'+signal+decay].Clone()
						if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
						hists[signal+i].Add(htemp)
		#systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						for proc in bkgProcList+bkgGrupList:
							if syst=='toppt' and proc not in topptProcs: continue
							hists[proc+i+syst+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in bkgProcs[proc]:
								if bkg!=bkgProcs[proc][0]: hists[proc+i+syst+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
						if syst=='toppt': continue
						for signal in sigList:
							hists[signal+i+syst+ud] = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							if doBRScan: hists[signal+i+syst+ud].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
							for decay in decays:
								htemp = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decay].Clone()
								if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
								if decay!=decays[0]: hists[signal+i+syst+ud].Add(htemp)
				if doPDF:
					for pdfInd in range(100):
						for proc in bkgProcList+bkgGrupList:
							hists[proc+i+'pdf'+str(pdfInd)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__pdf'+str(pdfInd))
							for bkg in bkgProcs[proc]:
								if bkg!=bkgProcs[proc][0]: hists[proc+i+'pdf'+str(pdfInd)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
						for signal in sigList:
							hists[signal+i+'pdf'+str(pdfInd)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
							if doBRScan: hists[signal+i+'pdf'+str(pdfInd)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
							for decay in decays:
								htemp = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone()
								if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
								if decay!=decays[0]:hists[signal+i+'pdf'+str(pdfInd)].Add(htemp)
														
			#+/- 1sigma variations of shape systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						for proc in bkgGrupList+bkgProcList+sigList:
							if syst=='toppt' and proc not in topptProcs: continue
							yieldTable[histoPrefix+syst+ud][proc] = hists[proc+i+syst+ud].Integral()
			#prepare yield table
			for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldTable[histoPrefix][proc] = hists[proc+i].Integral()
			yieldTable[histoPrefix]['totBkg'] = sum([hists[proc+i].Integral() for proc in bkgGrupList])
			yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']

			#prepare MC yield error table
			for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldStatErrTable[histoPrefix][proc] = 0.
			yieldStatErrTable[histoPrefix]['totBkg'] = 0.
			yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.

			for ibin in range(1,hists[bkgGrupList[0]+i].GetXaxis().GetNbins()+1):
				for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldStatErrTable[histoPrefix][proc] += hists[proc+i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['totBkg'] += sum([hists[proc+i].GetBinError(ibin)**2 for proc in bkgGrupList])
			for key in yieldStatErrTable[histoPrefix].keys(): yieldStatErrTable[histoPrefix][key] = math.sqrt(yieldStatErrTable[histoPrefix][key])

		#scale signal cross section to 1pb
		if scaleSignalXsecTo1pb:
			print "       SCALING SIGNAL TEMPLATES TO 1pb ..."
			for signal in sigList:
				for cat in catList:
					i=BRconfStr+cat
					hists[signal+i].Scale(1./xsec[signal])
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hists[signal+i+syst+'Up'].Scale(1./xsec[signal])
							hists[signal+i+syst+'Down'].Scale(1./xsec[signal])
							if normalizeRENORM_PDF and (syst.startswith('mu') or syst=='pdf'):
								try:
									hists[signal+i+syst+'Up'].Scale(hists[signal+i].Integral()/hists[signal+i+syst+'Up'].Integral())
									hists[signal+i+syst+'Down'].Scale(hists[signal+i].Integral()/hists[signal+i+syst+'Down'].Integral())
								except:
									print "Couldn't normalize MU for",signal,i
									pass
						if doPDF:
							for pdfInd in range(100): 
								hists[signal+i+'pdf'+str(pdfInd)].Scale(1./xsec[signal])

		#Theta templates:
		print "       WRITING THETA TEMPLATES: "
		for signal in sigList:
			print "              ... "+signal
			thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+'fb'+'.root'
			thetaRfile = TFile(thetaRfileName,'RECREATE')
			for cat in catList:
				i=BRconfStr+cat
				for proc in bkgGrupList:
					if hists[proc+i].Integral() > 0:
						hists[proc+i].Write()
						if doAllSys:
							for syst in systematicList:
								if syst=='toppt' and proc not in topptProcs: continue
								hists[proc+i+syst+'Up'].Write()
								hists[proc+i+syst+'Down'].Write()
							if doPDF:
								for pdfInd in range(100): hists[proc+i+'pdf'+str(pdfInd)].Write()
				for proc in [signal]:
					hists[proc+i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' and proc not in topptProcs: continue
							hists[proc+i+syst+'Up'].Write()
							hists[proc+i+syst+'Down'].Write()
						if doPDF:
							for pdfInd in range(100): hists[proc+i+'pdf'+str(pdfInd)].Write()
				hists['data'+i].Write()
			thetaRfile.Close()

                #Combine templates:
		if doCombineTemplates:
			print "       WRITING COMBINE TEMPLATES: "
			combineRfileName = outDir+'/templates_'+discriminant+BRconfStr+'_'+lumiStr+'_Combine.root'
			combineRfile = TFile(combineRfileName,'RECREATE')
			for cat in catList:
				print "              ... "+cat
				i=BRconfStr+cat
				for signal in sigList:
					mass = [str(mass) for mass in massList if str(mass) in signal][0]
					hists[signal+i].SetName(hists[signal+i].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
					hists[signal+i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hists[signal+i+syst+'Up'].SetName(hists[signal+i+syst+'Up'].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__plus','Up'))
							hists[signal+i+syst+'Down'].SetName(hists[signal+i+syst+'Down'].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__minus','Down'))
							hists[signal+i+syst+'Up'].Write()
							hists[signal+i+syst+'Down'].Write()
						if doPDF:
							for pdfInd in range(100): 
								hists[signal+i+'pdf'+str(pdfInd)].SetName(hists[signal+i+'pdf'+str(pdfInd)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
								hists[signal+i+'pdf'+str(pdfInd)].Write()

				totBkg_ = sum([hists[proc+i].Integral() for proc in bkgGrupList])
				for proc in bkgGrupList:
					if hists[proc+i].Integral()/totBkg_ < removeThreshold:
						print proc+i,"IS EMPTY OR < "+str(removeThreshold*100)+"% OF TOTAL BKG! SKIPPING ..."
						continue
					hists[proc+i].SetName(hists[proc+i].GetName().replace('fb_','fb_'+postTag))
					if hists[proc+i].Integral() == 0: hists[proc+i].SetBinContent(1,zero)
					hists[proc+i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' and proc not in topptProcs: continue
							hists[proc+i+syst+'Up'].SetName(hists[proc+i+syst+'Up'].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
							hists[proc+i+syst+'Down'].SetName(hists[proc+i+syst+'Down'].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
							hists[proc+i+syst+'Up'].Write()
							hists[proc+i+syst+'Down'].Write()
						if doPDF:
							for pdfInd in range(100): 
								hists[proc+i+'pdf'+str(pdfInd)].SetName(hists[proc+i+'pdf'+str(pdfInd)].GetName().replace('fb_','fb_'+postTag))
								hists[proc+i+'pdf'+str(pdfInd)].Write()
				hists['data'+i].SetName(hists['data'+i].GetName().replace('fb_','fb_'+postTag).replace('DATA','data_obs'))
				hists['data'+i].Write()
			combineRfile.Close()


	        table = []
                table.append(['break'])
		table.append(['break'])
		
		#yields without background grouping
		table.append(['YIELDS']+[proc for proc in bkgProcList+['data']])
		for cat in catList:
			row = [cat]
			#print str(yieldTable[histoPrefix][proc]
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			#print str(histoPrefix),str(proc)
			for proc in bkgProcList+['data']: 
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
				print str(proc)
			table.append(row)			
		table.append(['break'])
		table.append(['break'])
		
		#yields with top,ewk,qcd grouping
		table.append(['YIELDS']+[proc for proc in bkgGrupList+['data']])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			for proc in bkgGrupList+['data']:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)
		table.append(['break'])
		table.append(['break'])
		
		#yields for signals
		table.append(['YIELDS']+[proc for proc in sigList])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			for proc in sigList:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)

		#yields for AN tables (yields in e/m channels)
		for isEM in isEMlist:
			if isEM=='E': corrdSys = elcorrdSys
			if isEM=='M': corrdSys = mucorrdSys
			if isEM=='L': corrdSys = math.sqrt(elcorrdSys*elcorrdSys + mucorrdSys*mucorrdSys)
		#	g in nHtaglist:
			table.append(['break'])
			table.append(['','is'+isEM+'_yields'])
			table.append(['break'])
			table.append(['YIELDS']+[cat for cat in catList if 'is'+isEM in cat]+['\\\\'])
			for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
				row = [proc]
				for cat in catList:
					if not ('is'+isEM in cat): continue
					histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
					yieldtemp = 0.
					yielderrtemp = 0.
					if proc=='totBkg' or proc=='dataOverBkg':
						for bkg in bkgGrupList:
							try:
								yieldtemp += yieldTable[histoPrefix][bkg]
								yielderrtemp += yieldStatErrTable[histoPrefix][bkg]**2
								yielderrtemp += (modelingSys[bkg]*yieldTable[histoPrefix][bkg])**2
							except:
								print "Missing",bkg,"for channel:",cat
								pass
						yielderrtemp += (corrdSys*yieldtemp)**2
						if proc=='dataOverBkg':
							dataTemp = yieldTable[histoPrefix]['data']+1e-20
							dataTempErr = yieldStatErrTable[histoPrefix]['data']**2
							yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
							yieldtemp = dataTemp/yieldtemp
					else:
						try:
							yieldtemp += yieldTable[histoPrefix][proc]
							yielderrtemp += yieldStatErrTable[histoPrefix][proc]**2
						except:
							print "Missing",proc,"for channel:",cat
							pass
						if proc not in sigList: yielderrtemp += (modelingSys[proc]*yieldtemp)**2
						yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp = math.sqrt(yielderrtemp)
					if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefix][proc])))
					else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
				row.append('\\\\')
				table.append(row)
		
		#yields for PAS tables (yields in e/m channels combined)
		#for nHtag in nHtaglist:
		table.append(['break'])
		table.append(['','isL'+'_yields'])
		table.append(['break'])
		table.append(['YIELDS']+[cat.replace('isE','isL') for cat in catList if 'isE' in cat]+['\\\\'])
		for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
			row = [proc]
			for cat in catList:
				if not ('isE' in cat): continue
				histoPrefixE = discriminant+'_'+lumiStr+'fb_'+cat
				histoPrefixM = histoPrefixE.replace('isE','isM')
				yieldtemp = 0.
				yieldtempE = 0.
				yieldtempM = 0.
				yielderrtemp = 0. 
				if proc=='totBkg' or proc=='dataOverBkg':
					for bkg in bkgGrupList:
						try:
							yieldtempE += yieldTable[histoPrefixE][bkg]
							yieldtempM += yieldTable[histoPrefixM][bkg]
							yieldtemp  += yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]
							yielderrtemp += yieldStatErrTable[histoPrefixE][bkg]**2+yieldStatErrTable[histoPrefixM][bkg]**2
							yielderrtemp += (modelingSys[bkg]*(yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]))**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						except:
							print "Missing",bkg,"for channel:",cat
							pass
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
					if proc=='dataOverBkg':
						dataTemp = yieldTable[histoPrefixE]['data']+yieldTable[histoPrefixM]['data']+1e-20
						dataTempErr = yieldStatErrTable[histoPrefixE]['data']**2+yieldStatErrTable[histoPrefixM]['data']**2
						yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
						yieldtemp = dataTemp/yieldtemp
				else:
					try:
						yieldtempE += yieldTable[histoPrefixE][proc]
						yieldtempM += yieldTable[histoPrefixM][proc]
						yieldtemp  += yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc]
						yielderrtemp += yieldStatErrTable[histoPrefixE][proc]**2+yieldStatErrTable[histoPrefixM][proc]**2
					except:
						print "Missing",proc,"for channel:",cat
						pass
					if proc not in sigList: yielderrtemp += (modelingSys[proc]*yieldtemp)**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
				yielderrtemp = math.sqrt(yielderrtemp)
				if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc])))
				else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
			row.append('\\\\')
			table.append(row)

		#systematics
		if doAllSys:
			table.append(['break'])
			table.append(['','Systematics'])
			table.append(['break'])
			for proc in bkgGrupList+sigList:
				table.append([proc]+[cat for cat in catList]+['\\\\'])
				for syst in sorted(systematicList):
					for ud in ['Up','Down']:
						row = [syst+ud]
						for cat in catList:
							histoPrefix = discriminant+'_'+lumiStr+'fb_'+cat
							nomHist = histoPrefix
							shpHist = histoPrefix+syst+ud
							try: row.append(' & '+str(round(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+1e-20),2)))
							except:
								if not ((syst=='toppt' and proc not in topptProcs)):
									print "Missing",proc,"for channel:",cat,"and systematic:",syst
								pass
						row.append('\\\\')
						table.append(row)
				table.append(['break'])
			
		if not addCRsys: out=open(outDir+'/yields_noCRunc_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','w')
		else: out=open(outDir+'/yields_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','w')
		printTable(table,out)

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

iPlotList = []
print 'outDir:',outDir,'catList[0][2:]',catList[0][2:]
print 'dir:',outDir+'/'+catList[0][2:]+'/','*.p'
for file in findfiles(outDir+'/'+catList[0][2:]+'/', '*.p'):
    if 'bkghists' not in file: continue
    if not os.path.exists(file.replace('bkghists','datahists')): continue
    if not os.path.exists(file.replace('bkghists','sighists')): continue
    iPlotList.append(file.split('_')[-1][:-2])
print 'Plot list:',iPlotList

checkprint = False
for iPlot in iPlotList:
	datahists = {} 
	bkghists  = {}
	sighists  = {}
	#if iPlot!='HT': continue
	print "LOADING DISTRIBUTION: "+iPlot
	for cat in catList:
		print "         ",cat[2:]
		datahists.update(pickle.load(open(outDir+'/'+cat[2:]+'/datahists_'+iPlot+'.p','rb')))
		bkghists.update(pickle.load(open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
		sighists.update(pickle.load(open(outDir+'/'+cat[2:]+'/sighists_'+iPlot+'.p','rb')))
	if scaleLumi:
		for key in bkghists.keys(): bkghists[key].Scale(lumiScaleCoeff)	    		
		for key in sighists.keys(): sighists[key].Scale(lumiScaleCoeff)
	#print sighists.keys()
	checkprint = False
        #print bkghists
        #print datahists
	#print sighists
	#print 'sighists check:'
	for key in sighists:
		if 'MET_' in key and 'TTM800' in key: print key
	print "       MAKING CATEGORIES FOR TOTAL SIGNALS ..."
        if whichSignal=='BB': 
		iPlot=iPlot.replace('Tp','Bp')
        	iPlot=iPlot.replace('DnnTTbar','DnnTTbarBB')
        	iPlot=iPlot.replace('DnnWJets','DnnWJetsBB') 
	#try:
	makeThetaCats(datahists,sighists,bkghists,iPlot)
	#except Exception as e:
	#	print(type(e))
#		print(e)
#		print 'makeThetaCats failed for iPlot:',iPlot
#		pass


print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))
