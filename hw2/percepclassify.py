import json
import math
import sys
import operator
import os


model_file = sys.argv[1]

f_model = open(model_file, 'r')
f_test = open("temporary.txt", 'w')
f_test.write(sys.stdin.read())
f_test.close()
f_test = open("temporary.txt", 'r')

weight = {}
activation = {}
classes = [] 

weight = json.load(f_model)

for k in weight.keys():
    tag1, tag2 = k.split("_", 1)
    if tag1 not in classes:
       classes.append(tag1)

for line in f_test: #for each training example
  feature = {} #feature vector for each training example 
  text = line.lower()
  words = text.split()
  for theclass in classes:
      activation[theclass] = 0
  for word in words:
     for theclass in classes:
         if (theclass + "_" + word) in weight.keys():
            feature[word] = feature.get(word, 0) + 1 #feature vector
            break
  for k, v in feature.items():
     for theclass in classes:
         activation[theclass] = activation[theclass] + v * weight[theclass + "_" + k]
  predictClass = max(activation.items(), key = operator.itemgetter(1))[0]
  print(predictClass)

 

f_model.close()
f_test.close()
os.remove("temporary.txt")
