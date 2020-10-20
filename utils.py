#!/usr/bin/python

import os,sys,math,string
from ROOT import *

def isEqual(a, b):
    try:
        return a.upper() == b.upper()
    except AttributeError:
        return a == b

def contains(a, b):
    try:
        return b.upper() in a.upper()
    except AttributeError:
        return b in a

def cleanEOSpath(path): 
    #if path starts with /eos/uscms remove it. 
    if string.find(path,'/eos/uscms',0,10) == 0:
        return path[10:]
    elif string.find(path,'root://cmseos.fnal.gov/',0,23) == 0:
        return path[23:]
    else:
        return path

def striplist(alist): 
	#takes a list of strings, returns a version of the list with 
	#whitespace stripped from all entries.
	ret = []
	for item in alist:
		ret.append(item.strip())
	return ret

def EOSpathExists(path,file): 
    #returns a bool true iff the path exists and has contents
    xrd = 'xrdfs root://cmseos.fnal.gov/'
    path = cleanEOSpath(path)
    return len(os.popen(xrd+' ls '+path+' | grep "'+file+'"').readlines()) > 0


def EOSlist_root_files(Dir): 
    #ls Dir/*.root, returns a list of the root file names that it finds (without the path) 
    xrd = 'xrdfs root://cmseos.fnal.gov/'
    Dir = cleanEOSpath(Dir)
    items = os.popen(xrd+' ls -u '+Dir).readlines() #they have a \n at the end 
    items2 = striplist(items)
    rootlist = []
    for item in items2:
        if string.rfind(item,'root',-4) != -1:
            rootlist.append(item)
    return rootlist

def readTreeNominal(sample,step1Dir):
        pathstring0 = sample+'_hadd.root'
        pathstring1 = sample+'_1_hadd.root'
        if not EOSpathExists(step1Dir[23:]+'/',pathstring0) and not EOSpathExists(step1Dir[23:]+'/',pathstring1):
                print "Error: path does not exist! Aborting ... no",pathstring0,"nor",pathstring1
                os._exit(1)
        rootfiles = EOSlist_root_files(step1Dir[23:])

        tChain = TChain('ljmet')
        for i in range(0,len(rootfiles)):
                if sample not in rootfiles[i]: continue
                tChain.Add(rootfiles[i])
        return tChain

def readTreeShift(sample,shift,step1Dir):
        pathstring0 = sample+'_hadd.root'
        pathstring1 = sample+'_1_hadd.root'
        if not EOSpathExists(step1Dir[23:]+'/',pathstring0) and not EOSpathExists(step1Dir[23:]+'/',pathstring1):
                print "Error: path does not exist! Aborting ... no",pathstring0,"nor",pathstring1
                os._exit(1)
        rootfiles = EOSlist_root_files(step1Dir[23:])

        tChain = TChain('ljmet_'+shift)
        for i in range(0,len(rootfiles)):
                if sample not in rootfiles[i]: continue
                tChain.Add(rootfiles[i])
        return tChain

##############################################################################

def normByBinWidth(h,perNGeV):
        h.SetBinContent(0,0)
        h.SetBinContent(h.GetNbinsX()+1,0)
        h.SetBinError(0,0)
        h.SetBinError(h.GetNbinsX()+1,0)

        for bin in range(1,h.GetNbinsX()+1):
                width=float(h.GetBinWidth(bin))
                width = width/perNGeV   # could do events / 100 GeV or such, or events / 0.01

                content=h.GetBinContent(bin)
                error=h.GetBinError(bin)

                h.SetBinContent(bin, content/width)
                h.SetBinError(bin, error/width)

def poissonNormByBinWidth(tgae,hist,perNGeV):
        alpha = 1. - 0.6827
        for ibin in range(0,tgae.GetN()):
                width = float(hist.GetBinWidth(ibin+1))
                width = width/perNGeV   # could do events / 100 GeV or such, or events / 0.01
                X = tgae.GetX()[ibin]
                N = tgae.GetY()[ibin]
                L = 0
                if N != 0: L = Math.gamma_quantile(alpha/2.,N,1.)
                U = Math.gamma_quantile_c(alpha/2.,N+1,1)
                tgae.SetPoint(ibin,X,N/width)
                tgae.SetPointEYlow(ibin,(N-L)/width)
                tgae.SetPointEYhigh(ibin,(U-N)/width)

def poissonErrors(tgae):
	alpha = 1. - 0.6827
	for ibin in range(0,tgae.GetN()):
		N = tgae.GetY()[ibin]
		L = 0
		if N != 0: L = Math.gamma_quantile(alpha/2.,N,1.)
		U = Math.gamma_quantile_c(alpha/2.,N+1,1)
		tgae.SetPointEYlow(ibin,N-L)
		tgae.SetPointEYhigh(ibin,U-N)

def negBinCorrection(h): #set negative bin contents to zero and adjust the normalization
	norm0=h.Integral()
	for iBin in range(0,h.GetNbinsX()+2):
		if h.GetBinContent(iBin)<0: h.SetBinContent(iBin,0)
	if h.Integral()!=0 and norm0>0: h.Scale(norm0/h.Integral())

def overflow(h):
	nBinsX=h.GetXaxis().GetNbins()
	content=h.GetBinContent(nBinsX)+h.GetBinContent(nBinsX+1)
	error=math.sqrt(h.GetBinError(nBinsX)**2+h.GetBinError(nBinsX+1)**2)
	h.SetBinContent(nBinsX,content)
	h.SetBinError(nBinsX,error)
	h.SetBinContent(nBinsX+1,0)
	h.SetBinError(nBinsX+1,0)
	    
##############################################################################
#Printing tables

from math import log10, floor, ceil

def round_sig(x, sig):
    if x==0: return 0

    result=round(x, sig-int(floor(log10(x)))-1)
    if ceil(log10(x)) >= sig: result=int(result)
    return result

def format(number):
    return str(number)
    
def getMaxWidth(table, index):
    #Get the maximum width of the given column index
    max=0
    for row in table:
        try:
            n=len(format(row[index]))
            if n>max: max=n
        except: pass
    return max

def printTable(table,out=sys.stdout):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """
    col_paddings = []

    maxColumns=0
    for row in table:
        if len(row)>maxColumns: maxColumns=len(row)

    for i in range(maxColumns):
        col_paddings.append(getMaxWidth(table, i))
        
    for row in table:
        # left col
        if row[0]=='break': row[0]='-'*(sum(col_paddings)+(2*len(col_paddings)))
        print >> out, format(row[0]).ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format(row[i]).ljust(col_paddings[i] + 2)
            print >> out, col,
        print >> out

##############################################################################

if __name__=='__main__':

    table=[["A","B","C"],[1,2,3],[4,5],[6],['break'],['a long string','short',7,8]]
    printTable(table)
