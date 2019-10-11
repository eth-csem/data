import glob
import numpy as np
from obspy import read

#==========================================================
#- Readers for different datasets.
#==========================================================

def read_rays(dataset):

	evlo=[]
	evla=[]
	stlo=[]
	stla=[]

	fid=open('../Data/'+dataset+'/rays.txt','r')

	for line in fid:
		evla.append(float(line.split()[0]))
		evlo.append(float(line.split()[1]))
		stla.append(float(line.split()[2]))
		stlo.append(float(line.split()[3]))

	fid.close()

	return evlo, evla, stlo, stla


#==========================================================
#- Count distinct pairs. 
#==========================================================

def count_distinct_pairs(la,lo):

	pairs=[]

	for k in range(len(la)):
		pair=(float(la[k]),float(lo[k]))
		if pair not in pairs:
			pairs.append(pair)

	return len(pairs)