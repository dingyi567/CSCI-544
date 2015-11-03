import sys
import json
import random
import linecache
import operator
from subprocess import call

training_file = sys.argv[1]
model_file = sys.argv[2]

f_training = open(training_file, 'r')
f_model = open(model_file, 'w')

classes = []
array = []
weight = {}
catchWeight = {}
activation = {}
bias = {}
catchBias = {}
c = 1
words3 = set()

#initialize tag class and word3
for line in f_training:
   words = line.split()
   length = len(words)
   for i in range(length):
       word, tag = words[i].rsplit('/', 1) #word[i]
       if tag not in classes:
          classes.append(tag)
       if length >= 2: 
          if i==0:
             word1 = 'bos'
             word2, tag2 = words[i+1].rsplit('/', 1) #next
          elif i==length-1:
             word2 = 'eos'
             word1, tag1 = words[i-1].rsplit('/', 1) #previous
          else:
             word1, tag1 = words[i-1].rsplit('/', 1) #previous
             word2, tag2 = words[i+1].rsplit('/', 1) #next
       elif length == 1:
            word1 = 'bos'
            word2 = 'eos' 
       words3.add('_CURR_' + word.lower())
       words3.add('_PRE_' + word1.lower())
       words3.add('_NEX_' + word2.lower())

for word in words3:
   for theclass in classes:
         weight[theclass  + word] = 0 #weight vector
         catchWeight[theclass  + word] = 0 #catchWeight vector

for theclass in classes:
     bias[theclass] = 0
     catchBias[theclass] = 0


aaa = 1
f_training.seek(0,0)
linecount = sum(1 for line in f_training)

for x in range(5):
      print("iteration" + str(aaa))
      aaa = aaa + 1
      array = random.sample(range(1, linecount+1), linecount)
      for y in array:
         try:
             line = linecache.getline(training_file, y)
         except IndexError:
             print("y:" + str(y))          
         words = line.split()
         length = len(words)
         for i in range(length):
             word, tag = words[i].rsplit('/', 1) #word[i]
             feature = {}
             for theclass in classes:
                activation[theclass] = 0
             if length >= 2: 
               if i==0:
                  word1 = 'bos'
                  word2, tag2 = words[i+1].rsplit('/', 1) #next
               elif i==length-1:
                  word2 = 'eos'
                  word1, tag1 = words[i-1].rsplit('/', 1) #previous
               else:
                  word1, tag1 = words[i-1].rsplit('/', 1) #previous
                  word2, tag2 = words[i+1].rsplit('/', 1) #next
             elif length == 1:
                 word1 = 'bos'
                 word2 = 'eos' 
             feature[0] = "_CURR_" + word.lower()
             feature[1] = "_PRE_" + word1.lower()
             feature[2] = "_NEX_" + word2.lower()
             for theclass in classes:
                 for v in feature.values():
                     activation[theclass] += weight[theclass+ v]
                 activation[theclass] = activation[theclass] + bias[theclass] 
             predictClass = max(activation.items(), key = operator.itemgetter(1))[0]
             if predictClass != tag:
                  for w in feature.values():  
                        weight[predictClass  + w] -= 1     
                        weight[tag+ w] += 1
                        catchWeight[predictClass + w] -= c
                        catchWeight[tag+ w] += c
                  bias[predictClass] = bias[predictClass] - 1
                  bias[tag] = bias[tag] + 1
                  catchBias[predictClass] = catchBias[predictClass] - c 
                  catchBias[tag] = catchBias[tag] + c 
             c = c + 1
      for a in bias.keys():
         bias[a] = bias[a] - catchBias[a] / c
     
for i in weight.keys():
      weight[i] = weight[i] - catchWeight[i] / c

json.dump(weight, f_model)


f_training.close()
f_model.close()


