# -*- coding: utf-8 -*-
# qcl
# Build prefix-tree model.
# merge all patterns into a prefix tree, then write to patternTree.json
import operator
import sys
import os
import simplejson as json
import pickle
from nltk import word_tokenize
from nltk.util import ngrams

from textblob_aptagger import PerceptronTagger

pos = []
f = open("../naive_model/patternsByRelations.log","r")
max_len = 0
max_ptn = []
max_rls = ""

tagger = PerceptronTagger()

tree = {}

word_freq = {}
ptns = []

count = 0
dup = 0
for line in f:
    relationship = line.split("\t")[0]
    g = open("../naive_model/PbR/%s.txt" % (relationship),"r")

    print relationship

    for l in g:
        ws = l[:-1].lower().replace(";","").split()
        count += 1

        #p = l[:-1].lower().replace(";","")
        #if not p in ptns:
        #    ptns.append(p)

        #print ws
        for w in ws:
            if "[[" in w or "*" in w:
                if not w in pos:
                    pos.append(w)
        t = tree
        for w in ws:
            if not w in t:
                t[w] = {}
            t = t[w]

            if not w in word_freq:
                word_freq[w] = 0
            word_freq[w] += 1

        if "_rls_" in t:
            dup += 1
            if not relationship in t["_rls_"]:
                t["_rls_"].append(relationship)
            if len(t["_rls_"]) > max_len:
                max_len = len(t["_rls_"])
                max_rls = t["_rls_"]
                max_ptn = ws
        else:
            t["_rls_"] = [relationship]
        t["_ptn_"] = l[:-1]

    g.close()
f.close()

#h = open("./patternTree.json","w")
#json.dump(tree,h)
#h.close()

# some testing code here.
#print pos
#print count,dup
#print tree["has"]["released"]["on"]["_rls_"]
#print max_len,max_ptn,max_rls
#print tree.keys()
#print len(tree.keys())


#wf = sorted(word_freq.items(),key=lambda x:x[1],reverse=True)
#gg = 0
#zz = []
#for w,c in wf:
#    gg += 1
#    print w,c
#    if gg > 30:
#        break
#    else:
#        zz.append(w)

#for p in ptns:
#    t = False
#    for z in zz:
#        if z in p:
#            t = True
#            break
#    if not t:
#        print p

#print zz

