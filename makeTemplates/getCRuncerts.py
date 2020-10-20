#!/usr/bin/python

import os,sys,time,math

systematicList = ['pileup','jec','jer','btag','mistag','tau21','taupt','toppt','pdfNew','muRFcorrdNew','trigeff','jsf']
includeNB0 = False
discrim = 'minMlbST'
templateYields = 'templates_PreApp/yields_'+discrim+'_36p814fb_rebinned_stat0p3.txt' 
ttbarYields = 'ttbar_PreApp/yields_'+discrim+'_36p814fb_rebinned_stat0p3.txt'
wjetsYields = 'wjets_PreApp/yields_'+discrim+'_36p814fb_rebinned_stat0p3.txt'
"""NOTE: Need to have the yield files above from theta templates, not combine!!!!!!!!"""

lumiSys = 0.026 #lumi uncertainty
eltrigSys = 0.0 #electron trigger uncertainty
mutrigSys = 0.0 #muon trigger uncertainty
elIdSys = 0.02 #electron id uncertainty
muIdSys = 0.03 #muon id uncertainty
elIsoSys = 0.01 #electron isolation uncertainty
muIsoSys = 0.01 #muon isolation uncertainty
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

"""Read the template yields of top and ewk processes for all categories"""
ftemplate = open(templateYields, 'rU')
templatelines = ftemplate.readlines()
ftemplate.close()
yields_top = {}
yields_ewk = {}
ind = 0
for line in templatelines:
	if 'Systematics' in line: break
	if line.startswith('top'): 
		for yld,cat in zip(line.split('&')[1:],templatelines[ind-1].split()[1:-1]):
			yields_top[cat] = float(yld.split()[0])
	if line.startswith('ewk'): 
		for yld,cat in zip(line.split('&')[1:],templatelines[ind-2].split()[1:-1]):
			yields_ewk[cat] = float(yld.split()[0])
	ind+=1

"""Read the data/MC ratio from ttbar CR for all of its categories"""	
fttbar = open(ttbarYields, 'rU')
ttbarlines = fttbar.readlines()
fttbar.close()
dob_top = {}
data_top = {}
ind = 0
for line in ttbarlines:
	if 'Systematics' in line: break
	if line.startswith('dataOverBkg'):
		for yld,cat in zip(line.split('&')[1:],ttbarlines[ind-6].split()[1:-1]):
			newcat = 'top_'+cat.replace('_nH0','').replace('_nW0p','').replace('isE','E').replace('isM','M')
			dob_top[newcat] = float(yld.split()[0])
	elif line.startswith('data') or line.startswith('DATA'):
		for yld,cat in zip(line.split('&')[1:],ttbarlines[ind-5].split()[1:-1]):
			newcat = 'top_'+cat.replace('_nH0','').replace('_nW0p','').replace('isE','E').replace('isM','M')
			data_top[newcat] = float(yld.split()[0])
	ind+=1

"""Read the data/MC ratio from wjets CR for all of its categories"""		
fwjets = open(wjetsYields, 'rU')
wjetslines = fwjets.readlines()
fwjets.close()
dob_ewk = {}
data_ewk = {}
ind = 0
for line in wjetslines:
	if 'Systematics' in line: break
	if line.startswith('dataOverBkg'): 
		for yld,cat in zip(line.split('&')[1:],wjetslines[ind-6].split()[1:-1]):
			newcat = 'ewk_'+cat.replace('_nH0','').replace('_nB0','').replace('isE','E').replace('isM','M')
			dob_ewk[newcat] = float(yld.split()[0])
	elif line.startswith('data') or line.startswith('DATA'): 
		for yld,cat in zip(line.split('&')[1:],wjetslines[ind-5].split()[1:-1]):
			newcat = 'ewk_'+cat.replace('_nH0','').replace('_nB0','').replace('isE','E').replace('isM','M')
			data_ewk[newcat] = float(yld.split()[0])
	ind+=1

"""Sum yields of SR categories to match the CR categories"""			
yields = {}
if includeNB0: yields['top_E_nB0']  = sum([yields_top[cat] for cat in yields_top.keys() if 'isE' in cat and cat.endswith('nB0')])
yields['top_E_nB1']  = sum([yields_top[cat] for cat in yields_top.keys() if 'isE' in cat and cat.endswith('nB1')])
yields['top_E_nB2']  = sum([yields_top[cat] for cat in yields_top.keys() if 'isE' in cat and cat.endswith('nB2')])
yields['top_E_nB3p'] = sum([yields_top[cat] for cat in yields_top.keys() if 'isE' in cat and cat.endswith('nB3p')])
yields['top_E_nH1b'] = sum([yields_top[cat] for cat in yields_top.keys() if 'isE' in cat and 'nH1b' in cat])
yields['top_E_nH2b'] = sum([yields_top[cat] for cat in yields_top.keys() if 'isE' in cat and 'nH2b' in cat])
yields['ewk_E_nW0']  = sum([yields_ewk[cat] for cat in yields_ewk.keys() if 'isE' in cat and 'nW0_' in cat])
yields['ewk_E_nW1p'] = sum([yields_ewk[cat] for cat in yields_ewk.keys() if 'isE' in cat and 'nW1p_' in cat])
yields['ewk_E_nH1b'] = sum([yields_ewk[cat] for cat in yields_top.keys() if 'isE' in cat and 'nH1b' in cat])
yields['ewk_E_nH2b'] = sum([yields_ewk[cat] for cat in yields_top.keys() if 'isE' in cat and 'nH2b' in cat])

if includeNB0: yields['top_M_nB0']  = sum([yields_top[cat] for cat in yields_top.keys() if 'isM' in cat and cat.endswith('nB0')])
yields['top_M_nB1']  = sum([yields_top[cat] for cat in yields_top.keys() if 'isM' in cat and cat.endswith('nB1')])
yields['top_M_nB2']  = sum([yields_top[cat] for cat in yields_top.keys() if 'isM' in cat and cat.endswith('nB2')])
yields['top_M_nB3p'] = sum([yields_top[cat] for cat in yields_top.keys() if 'isM' in cat and cat.endswith('nB3p')])
yields['top_M_nH1b'] = sum([yields_top[cat] for cat in yields_top.keys() if 'isM' in cat and 'nH1b' in cat])
yields['top_M_nH2b'] = sum([yields_top[cat] for cat in yields_top.keys() if 'isM' in cat and 'nH2b' in cat])
yields['ewk_M_nW0']  = sum([yields_ewk[cat] for cat in yields_ewk.keys() if 'isM' in cat and 'nW0_' in cat])
yields['ewk_M_nW1p'] = sum([yields_ewk[cat] for cat in yields_ewk.keys() if 'isM' in cat and 'nW1p_' in cat])
yields['ewk_M_nH1b'] = sum([yields_ewk[cat] for cat in yields_top.keys() if 'isM' in cat and 'nH1b' in cat])
yields['ewk_M_nH2b'] = sum([yields_ewk[cat] for cat in yields_top.keys() if 'isM' in cat and 'nH2b' in cat])

"""Get the deviation (from 1) of data/MC in CRs"""
dataOverBkg = {}
for cat in dob_top.keys(): dataOverBkg[cat] = abs(1-dob_top[cat])
for cat in dob_ewk.keys(): dataOverBkg[cat] = abs(1-dob_ewk[cat])
# if includeNB0: 
# 	dataOverBkg['top_E_nB0'] = abs(1-[dob_top[cat] for cat in dob_top.keys() if 'isE' in cat and cat.endswith('nB0')][0])
# 	dataOverBkg['top_M_nB0'] = abs(1-[dob_top[cat] for cat in dob_top.keys() if 'isM' in cat and cat.endswith('nB0')][0])
# dataOverBkg['top_E_nB1'] = abs(1-[dob_top[cat] for cat in dob_top.keys() if 'isE' in cat and cat.endswith('nB1')][0])
# dataOverBkg['top_M_nB1'] = abs(1-[dob_top[cat] for cat in dob_top.keys() if 'isM' in cat and cat.endswith('nB1')][0])
# dataOverBkg['top_E_nB2p']= abs(1-[dob_top[cat] for cat in dob_top.keys() if 'isE' in cat and cat.endswith('nB2p')][0])
# dataOverBkg['top_M_nB2p']= abs(1-[dob_top[cat] for cat in dob_top.keys() if 'isM' in cat and cat.endswith('nB2p')][0])
# 
# dataOverBkg['ewk_E_nW0'] = abs(1-[dob_ewk[cat] for cat in dob_ewk.keys() if 'isE' in cat and 'nW0_' in cat][0])
# dataOverBkg['ewk_M_nW0'] = abs(1-[dob_ewk[cat] for cat in dob_ewk.keys() if 'isM' in cat and 'nW0_' in cat][0])
# dataOverBkg['ewk_E_nW1p']= abs(1-[dob_ewk[cat] for cat in dob_ewk.keys() if 'isE' in cat and 'nW1p_' in cat][0])
# dataOverBkg['ewk_M_nW1p']= abs(1-[dob_ewk[cat] for cat in dob_ewk.keys() if 'isM' in cat and 'nW1p_' in cat][0])

"""Correlate the e/m channels and print the derived full CR uncertainties"""
print "FULL CR:"
for key in sorted(yields.keys()):
	if '_M_' in key: continue
	print key.replace('E_','')+': %.2f' % ((yields[key]*dataOverBkg[key]+yields[key.replace('_E_','_M_')]*dataOverBkg[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')]))
print

"""Calculate the size of the shape systematics:"""
"""Check "systematicList" above!!!!!!!"""
#Get the size of systematics for the top group in each category of the ttbar CR:
ind = 0
indtemp_top = -1#indexes to help find the corresponding numbers in the yield file
indtemp_ewk = -1
indtemp_qcd = -1
for line in ttbarlines:
	if line.split()[0]=='top' and line.split()[1].startswith('is'): indtemp_top=ind
	if line.split()[0]=='ewk' and line.split()[1].startswith('is'): indtemp_ewk=ind
	if line.split()[0]=='qcd' and line.split()[1].startswith('is'): indtemp_qcd=ind
	ind+=1

shapes_top_tt = {}
for ind in range(indtemp_top+1,indtemp_ewk-1):
	syst = ttbarlines[ind].split()[0]
	if syst.replace('__plus','').replace('__minus','') not in systematicList: continue
	shapes_top_tt[syst] = {}
	nCats = len(ttbarlines[indtemp_top].split()[1:-1])
	for catind in range(nCats): 
		catStr = ttbarlines[indtemp_top].split()[catind+1]
		systShift = float(ttbarlines[ind].split('&')[catind+1].split()[0])-1
		shapes_top_tt[syst][catStr] = systShift

#Get the size of systematics for the ewk group in each category of the wjets CR:
ind = 0
indtemp_top = -1#indexes to help find the corresponding numbers in the yield file
indtemp_ewk = -1
indtemp_qcd = -1
for line in wjetslines:
	if line.split()[0]=='top' and line.split()[1].startswith('is'): indtemp_top=ind
	if line.split()[0]=='ewk' and line.split()[1].startswith('is'): indtemp_ewk=ind
	if line.split()[0]=='qcd' and line.split()[1].startswith('is'): indtemp_qcd=ind
	ind+=1

shapes_ewk_wj = {}
for ind in range(indtemp_ewk+1,indtemp_qcd-1):
	syst = wjetslines[ind].split()[0]
	if syst.replace('__plus','').replace('__minus','') not in systematicList: continue
	shapes_ewk_wj[syst] = {}
	nCats = len(wjetslines[indtemp_ewk].split()[1:-1])
	for catind in range(nCats): 
		catStr = wjetslines[indtemp_ewk].split()[catind+1]
		systShift = float(wjetslines[ind].split('&')[catind+1].split()[0])-1
		shapes_ewk_wj[syst][catStr] = systShift

"""Calculate the total shape uncertainty percentage:
   for each systematic, check the real direction of up and down shifts
   and add "real" up (down) shifts in quadrature to get the total variation"""
total_top_Up = {}
total_top_Dn = {}
for cat in shapes_top_tt[systematicList[0]+'__minus'].keys():
	newcat = 'top_'+cat.replace('_nH0','').replace('_nW0p','').replace('isE','E').replace('isM','M')
	total_top_Up[newcat] = 0.
	total_top_Dn[newcat] = 0.
	for syst in shapes_top_tt.keys():
		if shapes_top_tt[syst][cat]>0.: total_top_Up[newcat]+=shapes_top_tt[syst][cat]**2
		if shapes_top_tt[syst][cat]<0.: total_top_Dn[newcat]+=shapes_top_tt[syst][cat]**2
	total_top_Up[newcat] = math.sqrt(total_top_Up[newcat])
	total_top_Dn[newcat] = math.sqrt(total_top_Dn[newcat])
total_ewk_Up = {}
total_ewk_Dn = {}
for cat in shapes_ewk_wj[systematicList[0]+'__minus'].keys():
	newcat = 'ewk_'+cat.replace('_nH0','').replace('_nB0','').replace('isE','E').replace('isM','M')
	total_ewk_Up[newcat] = 0.
	total_ewk_Dn[newcat] = 0.
	for syst in shapes_ewk_wj.keys():
		if shapes_ewk_wj[syst][cat]>0.: total_ewk_Up[newcat]+=shapes_ewk_wj[syst][cat]**2
		if shapes_ewk_wj[syst][cat]<0.: total_ewk_Dn[newcat]+=shapes_ewk_wj[syst][cat]**2
	total_ewk_Up[newcat] = math.sqrt(total_ewk_Up[newcat])
	total_ewk_Dn[newcat] = math.sqrt(total_ewk_Dn[newcat])

"""Take the smaller of the up/down shifts:"""
total_shape = {}
for cat in sorted(total_top_Up.keys()): 
	total_shape[cat] = min([total_top_Up[cat],total_top_Dn[cat]])
for cat in sorted(total_ewk_Up.keys()): 
	total_shape[cat] = min([total_ewk_Up[cat],total_ewk_Dn[cat]])

"""Print the shape uncertainty on the Data/MC:"""
print 'TOTAL SHAPES ON THE DATA/MC:'
unc_shape = {}
for cat in sorted(total_shape.keys()): 
	if 'top' in cat: unc_shape[cat] = dob_top[cat]*math.sqrt((1./data_top[cat]+total_shape[cat]**2))
	if 'ewk' in cat: unc_shape[cat] = dob_ewk[cat]*math.sqrt((1./data_ewk[cat]+total_shape[cat]**2))
	print cat,': %.2f' % unc_shape[cat]
print

print "NORM+SHAPE SUBSTRACTED CR:"
for key in sorted(yields.keys()):
	if '_M_' in key: continue
	normsquared  = ((elcorrdSys*yields[key]+mucorrdSys*yields[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')]))**2
	shapesquared = ((unc_shape[key]*yields[key]+unc_shape[key.replace('_E_','_M_')]*yields[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')]))**2
	shapePlusNorm = math.sqrt(normsquared+shapesquared)
	CRfull = (yields[key]*dataOverBkg[key]+yields[key.replace('_E_','_M_')]*dataOverBkg[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')])
	if CRfull<=shapePlusNorm: print key.replace('E_','')+': 0.00(totCR=%.2f,shape+norm=%.2f)' % (CRfull,shapePlusNorm)
	else: print key.replace('E_','')+': %.2f(totCR=%.2f,shape+norm=%.2f)' % (math.sqrt(CRfull**2-normsquared-shapesquared),CRfull,shapePlusNorm)
print

"""For kinematic plots, average these uncertainties across tagging categories for ewk process:"""
ewk_isE=(yields['ewk_E_nW0']*dataOverBkg['ewk_E_nW0']+yields['ewk_E_nW1p']*dataOverBkg['ewk_E_nW1p'])/(yields['ewk_E_nW0']+yields['ewk_E_nW1p'])
ewk_isM=(yields['ewk_M_nW0']*dataOverBkg['ewk_M_nW0']+yields['ewk_M_nW1p']*dataOverBkg['ewk_M_nW1p'])/(yields['ewk_M_nW0']+yields['ewk_M_nW1p'])
ewk_all=((yields['ewk_E_nW0']+yields['ewk_E_nW1p'])*ewk_isE+(yields['ewk_M_nW0']+yields['ewk_M_nW1p'])*ewk_isM)/(yields['ewk_E_nW0']+yields['ewk_E_nW1p']+yields['ewk_M_nW0']+yields['ewk_M_nW1p'])
print 'ewk_isE (full CR): %.2f' % ewk_isE
print 'ewk_isM (full CR): %.2f' % ewk_isM 
print 'ewk_isL (full CR): %.2f' % ewk_all
print

"""... and the same for top process:"""
if includeNB0: 
	top_isE=(yields['top_E_nB0']*dataOverBkg['top_E_nB0']+yields['top_E_nB1']*dataOverBkg['top_E_nB1']+yields['top_E_nB2p']*dataOverBkg['top_E_nB2p'])/(yields['top_E_nB0']+yields['top_E_nB1']+yields['top_E_nB2p'])
	top_isM=(yields['top_M_nB0']*dataOverBkg['top_M_nB0']+yields['top_M_nB1']*dataOverBkg['top_M_nB1']+yields['top_M_nB2p']*dataOverBkg['top_M_nB2p'])/(yields['top_M_nB0']+yields['top_M_nB1']+yields['top_M_nB2p'])
	top_all=((yields['top_E_nB0']+yields['top_E_nB1']+yields['top_E_nB2p'])*top_isE+(yields['top_M_nB0']+yields['top_M_nB1']+yields['top_M_nB2p'])*top_isM)/(yields['top_E_nB0']+yields['top_E_nB1']+yields['top_E_nB2p']+yields['top_M_nB0']+yields['top_M_nB1']+yields['top_M_nB2p'])
else: 
	top_isE=(yields['top_E_nB1']*dataOverBkg['top_E_nB1']+yields['top_E_nB2p']*dataOverBkg['top_E_nB2p'])/(yields['top_E_nB1']+yields['top_E_nB2p'])
	top_isM=(yields['top_M_nB1']*dataOverBkg['top_M_nB1']+yields['top_M_nB2p']*dataOverBkg['top_M_nB2p'])/(yields['top_M_nB1']+yields['top_M_nB2p'])
	top_all=((yields['top_E_nB1']+yields['top_E_nB2p'])*top_isE+(yields['top_M_nB1']+yields['top_M_nB2p'])*top_isM)/(yields['top_E_nB1']+yields['top_E_nB2p']+yields['top_M_nB1']+yields['top_M_nB2p'])
print 'top_isE (full CR): %.2f' % top_isE
print 'top_isM (full CR): %.2f' % top_isM 
print 'top_isL (full CR): %.2f' % top_all

