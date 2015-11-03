import sys
import json
import random
import linecache
import operator

training_file = sys.argv[1]
model_file = sys.argv[2]

f_training = open(training_file, 'r', errors="ignore")
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
       wordPos, bio = words[i].rsplit('/', 1) #word[i]
       if bio not in classes:
          classes.append(bio)
       if length >= 2: 
          if i==0:
             wordPos1 = 'bos'
             wordPos2, bio2 = words[i+1].rsplit('/', 1) #next
          elif i==length-1:
             wordPos2 = 'eos'
             wordPos1, bio1 = words[i-1].rsplit('/', 1) #previous
          else:
             wordPos1, bio1 = words[i-1].rsplit('/', 1) #previous
             wordPos2, bio2 = words[i+1].rsplit('/', 1) #next
       elif length == 1:
            wordPos1 = 'bos'
            wordPos2 = 'eos'
       if len(wordPos) > 2:
           words3.add('_CURR_' + wordPos.upper())
       else:
           words3.add('_CURR_' + wordPos)
       if len(wordPos2) > 2:
           words3.add('_NEX_' + wordPos2.upper())
       else:
           words3.add('_NEX_' + wordPos2)
       if len(wordPos1) > 2:
           words3.add('_PRE_' + wordPos1.upper())
       else:
           words3.add('_PRE_' + wordPos1)
       if i != 0 and length != 1:
          words3.add("_" + bio1)


for word in words3:
   for theclass in classes:
         weight[theclass  + word] = 0 #weight vector
         catchWeight[theclass  + word] = 0 #catchWeight vector


for theclass in classes:
     bias[theclass] = 0
     catchBias[theclass] = 0

aaa = 1

for x in range(10):
      print("iteration" + str(aaa))
      aaa = aaa + 1
      f_training.close()
      f_training = open(training_file, 'r', errors="ignore")
      for line in f_training:         
         words = line.split()
         length = len(words)
         for i in range(length):
             wordPos, bio = words[i].rsplit('/', 1) #word[i]
             feature = {}
             for theclass in classes:
                activation[theclass] = 0
             if length >= 2: 
                if i==0:
                   wordPos1 = 'bos'
                   wordPos2, bio2 = words[i+1].rsplit('/', 1) #next
                elif i==length-1:
                   wordPos2 = 'eos'
                   wordPos1, bio1 = words[i-1].rsplit('/', 1) #previous
                else:
                   wordPos1, bio1 = words[i-1].rsplit('/', 1) #previous
                   wordPos2, bio2 = words[i+1].rsplit('/', 1) #next
             elif length == 1:
                  wordPos1 = 'bos'
                  wordPos2 = 'eos' 

             if len(wordPos) > 2:
                feature[0] = "_CURR_" + wordPos.upper()
             else:
                feature[0] = "_CURR_" + wordPos
             if i != 0:
                 if len(wordPos1) > 2:
                    feature[3] = "_PRE_" + wordPos1.upper()
                 else:
                    feature[3] = "_PRE_" + wordPos1  
             if i != (length - 1):
                 if len(wordPos2) > 2:
                     feature[1] = "_NEX_" + wordPos2.upper()
                 else:
                     feature[1] = "_NEX_" + wordPos2     
             if i != 0 and length != 1:
                 feature[2] = "_" + bio1
             for theclass in classes:
                 for v in feature.values():
                          activation[theclass] += weight[theclass+ v]
                 activation[theclass] = activation[theclass] + bias[theclass] 
             predictClass = max(activation.items(), key = operator.itemgetter(1))[0]
             if predictClass != bio:
                  for w in feature.values():  
                        weight[predictClass  + w] -= 1     
                        weight[bio+ w] += 1
                        catchWeight[predictClass + w] -= c
                        catchWeight[bio+ w] += c
                  bias[predictClass] = bias[predictClass] - 1
                  bias[bio] = bias[bio] + 1
                  catchBias[predictClass] = catchBias[predictClass] - c 
                  catchBias[bio] = catchBias[bio] + c 
             c = c + 1
      for a in bias.keys():
         bias[a] = bias[a] - catchBias[a] / c


for i in weight.keys():
      weight[i] = weight[i] - catchWeight[i] / c

json.dump(weight, f_model)


f_training.close()
f_model.close()


