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


for line in f_test:       
    words = line.split()
    length = len(words)
    for i in range(length):
        word = words[i] #word[i] 
        feature = {}
        for theclass in classes:
           activation[theclass] = 0
        if length >= 2: 
          if i>=1 and i<=length-2:
             word1= words[i-1]#previous
             word2= words[i+1] #next
          elif i==0:
             word1 = 'bos'
             word2= words[i+1] #next
          elif i==length-1:
             word2 = 'eos'
             word1= words[i-1] #previous
        elif length == 1:
            word1 = 'bos'
            word2 = 'eos' 
        feature[0] = "_CURR_" + word.lower()
        feature[1] = "_PRE_" + word1.lower()
        feature[2] = "_NEX_" + word2.lower()
        for theclass in classes:
            for v in feature.values():
                  if (theclass + v) in weight.keys():
                     activation[theclass] += weight[theclass  + v]
        predictClass = max(activation.items(), key = operator.itemgetter(1))[0]
        if i == length - 1:
            print(word + '/' + predictClass + ' ')
        else:
             print(word + '/' + predictClass + ' ', end="")          


     
f_model.close()
f_test.close()
os.remove("temporary.txt")

