############################################################
# Module  : elastic net tutorial
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import r2_score
from sklearn.linear_model import ElasticNet

from app     import *
from utils   import *
from scripts import *
from scripts.graph import *
from experiments.argmax import *
from experiments.rank_all import *

############################################################
'''
	make sparse data with X,y \in R^n
'''
np.random.seed(42)

n_samples, n_features = 50, 200
X    = np.random.randn(n_samples, n_features)
coef = 3 * np.random.randn(n_features)

inds = np.arange(n_features)
np.random.shuffle(inds)
coef[inds[10:]] = 0   # sparsify

y = np.dot(X,coef)
y += 0.01 * np.random.normal((n_samples,))

'''
	split data into test and train
'''
X_train, y_train = X[:n_samples / 2], y[:n_samples / 2]
X_test,  y_test  = X[n_samples / 2:], y[n_samples / 2:]

############################################################
'''
	elastic net
'''
alpha = 0.1
net   = ElasticNet(alpha = alpha, l1_ratio = 0.7)  
y_hat = net.fit(X_train, y_train).predict(X_test)
r2_score_net = r2_score(y_test, y_hat)

############################################################
'''
	make sparse data with X \in R^n, y \in {0,1}
'''






