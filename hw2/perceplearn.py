import sys
import json
import operator
import linecache
import random 
import argparse

training_file = sys.argv[1]
model_file = sys.argv[2]

f = open(training_file, 'r')
f_m = open(model_file, 'w')

words3 = set()
classes = []
array = []
classCode = {}
weight = {}
catchWeight = {}
activation = {}
bias = {}
catchBias = {}
c = 1

for line in f: #create vocabulary, count the class
  prex, text3 = line.split(' ',1) 
  text3 = text3.lower()
  words3.update(text3.split())
  if prex not in classes:
      classes.append(prex)
  
f.seek(0,0)
linecount = sum(1 for line in f)


for theclass in classes:
     bias[theclass] = 0
     catchBias[theclass] = 0
for word in words3:
      for theclass in classes:
         weight[theclass + '_' + word] = 0 #weight vector
         catchWeight[theclass + '_' + word] = 0 #catchWeight vector

aaa = 1
for x in range(10):
      print("iteration" + str(aaa))
      aaa = aaa + 1
      array = random.sample(range(1, linecount+1), linecount)
      for y in array:
         try:
             line = linecache.getline(training_file, y)
         except IndexError:
             print("y:" + str(y))         
         feature = {} #feature vector for each training example
         className, text = line.split(' ', 1)
         text = text.lower()
         words = text.split()
         for theclass in classes:
            activation[theclass] = 0
         for word in words:
            if word in words3:
               feature[word] = feature.get(word, 0) + 1 #feature vector
         for k, v in feature.items():
             for theclass in classes:
                 activation[theclass] = activation[theclass] + v * weight[theclass + "_" + k]
         for theclass in classes:
             activation[theclass] += bias[theclass]
         predictClass = max(activation.items(), key = operator.itemgetter(1))[0]
         if predictClass != className:
            for word in feature.keys():
                weight[predictClass + '_' + word] -= feature[word]
                weight[className + '_' + word] += feature[word]
                catchWeight[predictClass + '_' + word] -= c * feature[word]
                catchWeight[className + '_' + word] += c * feature[word]
            bias[predictClass] = bias[predictClass] - 1
            bias[className] = bias[className] + 1
            catchBias[predictClass] = catchBias[predictClass] - c 
            catchBias[className] = catchBias[className] + c 
         c = c + 1
      for a in bias.keys():
         bias[a] = bias[a] - catchBias[a] / c
     
  
for i in weight.keys():
      weight[i] = weight[i] - catchWeight[i] / c


json.dump(weight, f_m)

f.close()
f_m.close()



