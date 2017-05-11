############################################################
# Module  : feature representation
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import math
import numpy as np
from scripts import *
from scripts.graph import *

############################################################
'''
	@Use: given set of pairs and feature representation function
		  phi of each word, and a function that combines
		  the pair of words, output the X matrix
	@Input:  - xs  :: [(String,String)]	  
			 - phi :: String -> numpy.array
			 - op  :: numpy.array -> numpy.array -> numpy.array

	@Output: - X :: numpy.array 
				dim : n x m   where n is the number of examples
							  and m is number of features
'''
def to_X(xs, phi, op):
	return np.array([ op(phi(s),phi(t)) for s,t in xs ])

def to_x(phi,op):
	def fn(s,t):
		return op(phi(s),phi(t)).reshape(1,-1)
	return fn

############################################################
'''
	combine two phis
'''
def phi_subtract(phi1, phi2):
	return phi1 - phi2

def phi_concat(phi1, phi2):
	return np.concatenate((phi1,phi2), axis = 0)

def phi_add(phi1, phi2):
	return phi1 + phi2

def phi_dot(phi1,phi2):
	v = np.dot(phi1,phi2)
	w = np.append(v,1.0)
	return w

############################################################
'''
	@Use: given affective norm over all words
		  output affective representation of this word
		  if word not in norm, then default to 0.0
'''
def phi_baseline(NORM,w2idx):
  
  def fn(s):

    vec = [0.0]*len(w2idx)

    for cat,k in w2idx.iteritems():
    	if s in NORM[cat]:
    		vec[k] = NORM[cat][s]

    return np.array(vec)

  return fn


