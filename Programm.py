# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import random
import matplotlib
import keras
import tensorflow
tensorflow.sqrt(4.)
random.seed(0)

def minkowskiDist(v1, v2, p):
    """ v1 and v2 are equal-length arrays of numbers, we normalieze every
        observation of each featuresvector and then
       Returns Minkowski distance of order p between v1 and v2
     """
       
    dist = 0.0
    for i in range(len(v1)):
        v1[i] = keras.activations.sigmoid(v1[i])
        v2[i] = keras.activations.sigmoid(v2[i])
        dist += abs(v1[i] - v2[i])**p
    return dist**(1/p)

class Messwert(object):
    featureNames = ('g_type', 'time1', 'time2', 'vorschub')
    def __init__(self, g_type, time1, time2, vorschub, erfolg):
        self.g_type =float(g_type) 
        self.time1 = float(time1)
        self.time2 = float(time2)
        self.label = erfolg
        self.vorschub = float(vorschub)
        self.featureVec = [self.g_type, self.time1, self.time2, self.vorschub]
    def distance(self, other):
        return minkowskiDist(self.featureVec, other.featureVec, 2)
    def getVorschub(self):
        return self.vorschub
    def getTime1(self):
        return self.featureVec[2]
    def getTime2(self):
        return self.featureVec[3]
    def getType(self):
        return self.g_Type
    def getFeatures(self):
        return self.featureVec[:]
    def getLabel(self):
        return self.label
        
def getData(fname):
    data = {}
    data['g_type']=[]  #here to fit the lab data in, default, assume that we have 5 in each observation
    data['time1'],data['time2'],data['vorschub'],data['erfolg'] = [],[],[],[]

    #data['class'], data['survived'], data['age'] = [], [], []  data['gender'], data['name'] = [], []

    f = open(fname)
    line = f.readline()
    try:
        while line != '':
            split = line.split(',')
            data['g_type'].append(int(split[0]))
            data['time1'].append(float(split[1]))
            data['time2'].append(float(split[2]))
            data['vorschub'].append(float(split[3]))
            data['erfolg'].append(int(split[4]))
            line = f.readline()
    except:
        pass
    return data
                
def buildExamples(fileName):
    data = getData(fileName)
    examples = []
    try:
        for i in range(len(data['g_type'])):
            mw = Messwert(data['g_type'][i], data['time1'][i], data['time2'][i],data['vorschub'][i], data['erfolg'][i] )
            examples.append(mw)
    except:
        pass
    print('Finish processing', len(examples), 'Messwert\n')    
    return examples





###############################    
examples = buildExamples('data_2.txt')   #here insert file name 
###############################






def accuracy(truePos, falsePos, trueNeg, falseNeg):
    numerator = truePos + trueNeg
    denominator = truePos + trueNeg + falsePos + falseNeg
    return numerator/denominator

def sensitivity(truePos, falseNeg):
    try:
        return truePos/(truePos + falseNeg)
    except ZeroDivisionError:
        return float('nan')
    
def specificity(trueNeg, falsePos):
    try:
        return trueNeg/(trueNeg + falsePos)
    except ZeroDivisionError:
        return float('nan')
    
def posPredVal(truePos, falsePos):
    try:
        return truePos/(truePos + falsePos)
    except ZeroDivisionError:
        return float('nan')
    
def negPredVal(trueNeg, falseNeg):
    try:
        return trueNeg/(trueNeg + falseNeg)
    except ZeroDivisionError:
        return float('nan')

       
def getStats(truePos, falsePos, trueNeg, falseNeg, toPrint = True):
    accur = accuracy(truePos, falsePos, trueNeg, falseNeg)
    sens = sensitivity(truePos, falseNeg)
    spec = specificity(trueNeg, falsePos)
    ppv = posPredVal(truePos, falsePos)
    if toPrint:
        print(' Accuracy =', round(accur, 3))
        print(' Sensitivity =', round(sens, 3))
        print(' Specificity =', round(spec, 3))
        print(' Pos. Pred. Val. =', round(ppv, 3))
    return (accur, sens, spec, ppv)

   
def findKNearest(example, exampleSet, k):
    kNearest, distances = [], []
  ####two list containing first k examples and their distances####
    for i in range(k):
        kNearest.append(exampleSet[i])
        distances.append(example.distance(exampleSet[i]))
    maxDist = max(distances) #Get maximum distance for startting
   ###consider every point
   ###then we start to
    for e in exampleSet[k:]:
        dist = example.distance(e)
        if dist < maxDist:
            #replace farther neighbor by this one
            maxIndex = distances.index(maxDist)   #return the position in list
            kNearest[maxIndex] = e
            distances[maxIndex] = dist
            maxDist = max(distances)
            #then e is the farthest in list kNearest
            #iterating on, kNearst will be left only k element
            #then we need to conduct a vote of 3
    #print(len(kNearest))
    return kNearest, distances

erfolgreich = []
unerfolgreich = [] 
    
def KNearestClassify(training, testSet, label, k):  
    """Assumes training & testSet lists of examples, k an int
       Predicts whether each example in testSet has label
       Returns number of true positives, false positives,
          true negatives, and false negatives"""
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    for testCase in testSet:
        nearest, distances = findKNearest(testCase, training, k)
        #conduct vote
        numMatch = 0
        for i in range(len(nearest)):
            if nearest[i].getLabel() == label:
                numMatch += 1
                
        if numMatch > k//2: #guess label
            if testCase.getLabel() == label:
                truePos += 1
                erfolgreich.append(testCase)
                #print('e=',erfolgreich[-1].time1,erfolgreich[-1].vorschub)
            else:
                falsePos += 1
                unerfolgreich.append(testCase)
        else: #guess not label
            if testCase.getLabel() != label:
                trueNeg += 1
                unerfolgreich.append(testCase)
                #print('úe=',unerfolgreich[-1].vorschub)
            else:
                falseNeg += 1
                unerfolgreich.append(testCase)
    return truePos, falsePos, trueNeg, falseNeg


def leaveOneOut(examples, method, toPrint = True):
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    for i in range(len(examples)):
        testCase = examples[i]
        trainingData = examples[0:i] + examples[i+1:]
        results = method(trainingData, [testCase])
        #print(trainingSet,testSet)
        truePos += results[0]
        falsePos += results[1]
        trueNeg += results[2]
        falseNeg += results[3]
    if toPrint:
        getStats(truePos, falsePos, trueNeg, falseNeg)
    return truePos, falsePos, trueNeg, falseNeg



# testing classfication    
#knn = lambda training, testSet: KNearestClassify(training, testSet,'erfolg', 3)
knn = lambda training, testSet: KNearestClassify(training, testSet,1,3)###choose k here

print('Average of Leave one out testing using KNN (k=3)')
truePos, falsePos, trueNeg, falseNeg =\
      leaveOneOut(examples, knn)

###################plotting
x=[]
y=[]
for i in erfolgreich:
    x.append(i.time1)
    y.append(i.g_type)

matplotlib.pyplot.plot(x,y,'.b')
xx,yy =[],[] 
for i in unerfolgreich:
    xx.append(i.time1)
    yy.append(i.g_type)
matplotlib.pyplot.plot(xx,yy,'.r')
print('blue dot means erfolg')
matplotlib.pyplot.show()

print('le=',len(erfolgreich),'lu=',len(unerfolgreich))

######################


import sklearn.linear_model
erf = []
unerf = [] 


             
def split80_20(examples):
    sampleIndices = random.sample(range(len(examples)),
                                  len(examples)//5)
    trainingSet, testSet = [], []
    for i in range(len(examples)):
        if i in sampleIndices:
            testSet.append(examples[i])
        else:
            trainingSet.append(examples[i])
    return trainingSet, testSet

def randomSplits(examples, method, numSplits, toPrint = True):
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    random.seed(0)
    for t in range(numSplits):
        trainingSet, testSet = split80_20(examples)
        results = method(trainingSet, testSet)
        truePos += results[0]
        falsePos += results[1]
        trueNeg += results[2]
        falseNeg += results[3]
    getStats(truePos/numSplits, falsePos/numSplits,
             trueNeg/numSplits, falseNeg/numSplits, toPrint)
    return truePos/numSplits, falsePos/numSplits,\
             trueNeg/numSplits, falseNeg/numSplits
             

def buildModel(examples, toPrint = True):
    featureVecs, labels = [],[]
    for e in examples:
        featureVecs.append(e.getFeatures())
        labels.append(e.getLabel())
    LogisticRegression = sklearn.linear_model.LogisticRegression
    model = LogisticRegression(solver='lbfgs').fit(featureVecs, labels)
    ##apply solver to discard warnings
    if toPrint:
        print('model.classes_ =', model.classes_)
        for i in range(len(model.coef_)):
            print('For label', model.classes_[1])
            for j in range(len(model.coef_[0])):
                print('   ', Messwert.featureNames[j], '=',
                      model.coef_[0][j])
    return model


def applyModel(model, testSet, label, prob = 0.5):
    testFeatureVecs = [e.getFeatures() for e in testSet]
    probs = model.predict_proba(testFeatureVecs)
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    for i in range(len(probs)):
        if probs[i][1] > prob:
            if testSet[i].getLabel() == label:
                truePos += 1
                erf.append(testSet[i])

            else:
                falsePos += 1
                erf.append(testSet[i])
        else:
            if testSet[i].getLabel() != label:
                trueNeg += 1
                unerf.append(testSet[i])
            else:
                falseNeg += 1
                unerf.append(testSet[i])


    return truePos, falsePos, trueNeg, falseNeg

def lr(trainingData, testData, prob = 0.580):    #to change thread of judgement
    model = buildModel(trainingData, True)
    results = applyModel(model, testData, 1, prob)
    return results


#print('Average of Leave-One-Out testing using LR')
#truePos, falsePos, trueNeg, falseNeg = leaveOneOut(examples, lr)

#print('Average of Leave-One-Out testing using LR')
#truePos, falsePos, trueNeg, falseNeg =\
#      leaveOneOut(examples, lr)
#     

#trainingSet, testSet = split80_20(examples)
#model = buildModel(trainingSet, True)

##numSplits = 10
numSplits = 5
print('Average of', numSplits, '80/20 splits LR')
truePos, falsePos, trueNeg, falseNeg =\
      randomSplits(examples, lr, numSplits)

print('le=',len(erf),'ue=',len(unerf))
        
a,b,aa,bb=[],[],[],[]
for i in erf:
    a.append(i.time1)
    b.append(i.g_type)
matplotlib.pyplot.plot(a,b,'.g')
for i in unerf:
    aa.append(i.time1)
    bb.append(i.g_type)    
matplotlib.pyplot.plot(aa,bb,'.y')
print('green dot means erfolg')
matplotlib.pyplot.show()








