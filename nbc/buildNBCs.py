# -*- coding: utf-8 -*-
# qcl
# build naive bayes models from dir

import os
import sys
import projizz
import multiprocessing

def trainModel(jobid,relation,inputpath,outputPath):
    print "%d -> train %s" % (jobid,relation)
    instances = []
    filepath = os.path.join(inputpath,"%s.pos" % (relation))
    if os.path.exists(filepath):
        posInstances = projizz.jsonRead( filepath )
        for data in posInstances:
            instances.append( (data["text"], data["label"]) )
    filepath = os.path.join(inputpath,"%s.neg" % (relation))
    if os.path.exists(filepath):
        negInstances = projizz.jsonRead( filepath )
        for data in negInstances:
            instances.append( (data["text"], data["label"]) )

    if len(instances) == 0:
        print "Cannot build %s.nbc because there are no training data." % (relation)

    classifier = projizz.NaiveBayesClassifier(instances)
    classifier.save( os.path.join(outputPath,"%s.nbc" % (relation)) )
    print "%d -> Write to %s %s.nbc" % (jobid,outputPath,relation)

def buildModels(inputpath,outputPath):

    projizz.checkPath(outputPath)

    cpuCount = multiprocessing.cpu_count()
    if cpuCount > 8:
        cpuCount = 8

    pool = multiprocessing.Pool(processes=cpuCount) 
    t = 0

    relations = projizz.getYagoRelation()
    for relation in relations:
        if relation == "produced":
            continue
        pool.apply_async(trainModel, (t,relation,inputpath,outputPath))
        t += 1
    pool.close()
    pool.join()

    print "Done training all classifiers"

if __name__ == "__main__":
    if len(sys.argv) > 2:
        modelsDir = sys.argv[1]
        outputPath = sys.argv[2]
        buildModels(modelsDir,outputPath)
    else:
        print "$ python ./buildNBCs.py [inpu model dir] [output model dir]"
