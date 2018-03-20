import sys
import math
from copy import copy, deepcopy
import numpy as np

#http://www.scipy.org/
try:
	from numpy import dot
	from numpy.linalg import norm
except:
	print ("Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?")
	sys.exit() 

def removeDuplicates(list):
	""" remove duplicates from a list """
	return set((item for item in list))


def cosine(vector1, vector2):
	""" related documents j and q are in the concept space by comparing the vectors :
		cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
	return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))


def binjaccard(vector1,vector2):
	p=0.0
	q=0.0
	r=0.0	
#	print("len(vector1)")
#	print(len(vector1))
#	print("len(vector2)")
#	print(len(vector2))
	for x in range(0,len(vector1)-1,1):
#		print("x")
#		print(x)
		if vector1[x]!=0 and vector2[x]!=0:
			p = p + 1	
		elif vector1[x]==0 and vector2[x]!=0:
			q = q + 1
		elif vector1[x]!=0 and vector2[x]==0:
			r = r + 1
	return float (float(p)/float(p+q+r))



def tf_idf(vectors):
# print vectors
        tf_idf = [] 
	#df = [0]*len(vectors[0])
        idf = [0] *len(vectors[0])
        for vector in vectors:
	#	print vector
                i=0
                for i in range(len(vector)):
                        if vector[i] !=0:
                                 idf[i] = idf[i]+1
#	print df
        i=0
        for i in range(len(idf)):
                idf[i] = 1+math.log(float(len(vectors))/float(idf[i]))
        for vector in vectors:
                tf_idf.append([m*n for m,n in zip(vector, idf)])
#	print len(vectors)
#	print len(tf_idf)
        return tf_idf
#	for k in range(0,len(df)-1):
#		idf[k] = (1 +math.log(1000/df[k]))
#	
##	for w in range(0,len(vector)-1):		
#		for x in range(0,len(idf)):
##			tfidf[w] = vector[w][x] * idf[x]
#	return tf_idf
	
