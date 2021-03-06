# -*- coding: utf-8 -*-
# qcl
# Read wiki-raw input, output the hit count of articles

import os
import sys
import Queue
import simplejson as json
from datetime import datetime
from projizzWorker import Manager
from projizzReadNGramModel import readModel

def main(modelPath,inputPath,outputPath):
    ngram,models = readModel(modelPath)
    files = Queue.Queue(0)
    print "Read %d %d-gram models" % (len(models),ngram)

    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)

    def workerFunction(jobObj,tid,args):
        a = datetime.now()
        print "worker #%02d start read file %s" % (tid,jobObj)
        f = open(os.path.join(inputPath,jobObj),"r")
        content = json.load(f)
        f.close()
        diff = datetime.now() - a
        print "worker #%02d read file %s, use [%d.%d s]" % (tid,jobObj,diff.seconds,diff.microseconds)
        results = {}
        count = 0
        for subFilename in content:
            ngs = content[subFilename]
            count += 1
            result = {}
            for model in models:
                mn = models[model]
                #result[model] = 0
                for ng in ngs:
                    if ng in mn:
                        if not model in result:
                            result[model] = 0
                        result[model]+=1

            if count % 100 == 0:
                print "worker #%02d scan %d files" % (tid,count)

            results[subFilename] = result
        
        a = datetime.now()
        print "worker #%02d start write file %s" % (tid,jobObj)
        f = open(os.path.join(outputPath,jobObj),"w")
        json.dump(results,f)
        f.close()
        diff = datetime.now() - a
        print "worker #%02d  write file %s, use [%d.%d s]" % (tid,jobObj,diff.seconds,diff.microseconds)


    for filename in os.listdir(inputPath):
        if ".json" in filename:
            files.put(filename)

    manager = Manager(25)
    manager.setJobQueue(files)
    manager.setWorkerFunction(workerFunction)
    manager.startWorking()
    

if __name__ == "__main__":
    if len(sys.argv) > 3:
        modelPath = sys.argv[1]
        inputPath = sys.argv[2]
        outputPath= sys.argv[3]
        main(modelPath,inputPath,outputPath)
    else:
        print "$ python ./ngramRawRun.py [ModelFilePath] [inputRawDataPath] [answerOutputPath]"
