'''
clus_reader.py

Read and interpret results of cluster.py

ex:

> cr = ClusReader('../results/tgts100.adj-adj.adj-adjp.k25.pkl')
> hard = cr.hard_clustering()
> c2w = cr.clus2words(hard)
> cr.nearest_words('hot')

'''

import sys
import cPickle as pkl
import numpy as np

class ClusReader:
    def __init__(self, clusfile):
        self.clusfile = clusfile
        with open(clusfile,'r') as fin:
            self.vocab, self.m = pkl.load(fin)
        self.w2i = {w: i for i,w in enumerate(self.vocab)}
        self.N, self.k = self.m.shape

        # normalize
        denom = np.sqrt(np.sum((self.m*self.m),axis=1))
        denom = np.array([d if d>0 else 1. for d in denom])[np.newaxis].T
        self.m_norm = self.m / denom

    def hard_clustering(self):
        y = np.argmax(self.m, axis=1)
        return {w: set([yy]) for w,yy in zip(self.vocab, y)}

    def clus2words(self, words2clus):
        c2w = {}
        for w,cset in words2clus.items():
            for c in cset:
                cc = c2w.get(c, set([]))
                cc.add(w)
                c2w[c] = cc
        return c2w

    def soft_clustering(self, thr=0.0035):
        mask = self.m >= thr
        w2c = {}
        for i, clusprobs in enumerate(self.m):
            cnums = set([np.argmax(clusprobs)])
            cnums |= set([j for j,b in enumerate(mask[i]) if b])
            w2c[self.vocab[i]] = cnums
        return w2c

    def nearest_words(self, word, n=5):
        if word not in self.w2i:
            sys.stderr.write('Word %s not found in vocab\n' % word)
            return None
        wvec = self.m_norm[self.w2i[word]]
        sims = np.argsort(-self.m_norm.dot(wvec))
        numfound = 0
        neighbors = []
        for i in sims:
            if self.vocab[i] != word:
                neighbors.append(self.vocab[i])
                numfound += 1
            if numfound >= n:
                break
        return neighbors

    def near_to_vec(self, v, n=5):
        if sum(v*v)==0.:
            v_norm = v
        else:
            v_norm = v / np.sqrt((v*v).sum())
        sims = np.argsort(-self.m_norm.dot(v_norm))
        return [self.vocab[i] for i in sims[:n]]

    def w2v(self, word):
        if word not in self.w2i:
            return None
        return self.m_norm[self.w2i[word]]
