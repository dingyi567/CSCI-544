import sys
import json
import random
import linecache
import operator


training_file = sys.argv[1]
model_file = sys.argv[2]

f_training = open(training_file, 'r')
f_model = open(model_file, 'w')


array = []
weight = {}
catchWeight = {}
activation = {}
bias = {}
catchBias = {}
c = 1
tagClass = ["it's", "its", "you're", "your", "they're", "their", "loose", "lose", "to", "too"]



def test(w, i, words):
  for tag in tagClass:
    if w == tag:  
      return 5
  if w == "it" and words[i + 1].lower() == "'s": 
    return 1
  elif w == "you" and words[i + 1].lower() =="'re": 
    return 2
  elif w == "they" and words[i + 1].lower() == "'re" : 
    return 3
  else: 
    return 4

#initialize tag class and word3
sentence = f_training.read().decode(errors = 'ignore').encode(errors = 'ignore')
words = sentence.split()
_length = len(words)
flagi = 0
for i in range(_length):

  if flagi == 1:
    flagi = 0
    continue

  flag = test(words[i].lower(), i, words)


  if flag != 4:
    word = words[i].lower()
    if flag == 5:
      for tag in tagClass:
        if tag == word:
           tag = word
           break
      j = i + 1
      k = i + 2
      length = _length  
      
    elif flag == 1 or flag == 2 or flag==3:
      j = i + 2
      k = i + 3
      length = _length - 1
      if flag == 1: tag = "it's"
      if flag == 2: tag = "your're"
      if flag == 3: tag = "they're"
      flagi = 1 

    if length >1:
      if i == 0:
         wordl1 = 'bos1'
         wordl2 = 'bos2'
      elif i == 1:
         wordl1 = 'bos1'
         wordl2 = words[i-1].lower()######################33
      else:
         wordl1 = words[i-2].lower()
         wordl2 = words[i-1].lower()

      if length - i == 2:
         wordr1 = words[j].lower()
         wordr2 = 'eos2'
      elif length - i == 1:
         wordr1 = 'eos1'
         wordr2 = 'eos2'
      else:
         wordr1 = words[j].lower()
         wordr2 = words[k].lower()
    elif length == 1:
         wordl1 = 'bos1'
         wordl2 = 'bos2'
         wordr1 = 'eos1'
         wordr2 = 'eos2'
    
    if tag == "it's" or tag == "its":
       temp1 = "it's"
       temp2 = "its"
    if tag == "you're" or tag ==  "your":
       temp1 = "you're"
       temp2 = "your"
    if tag == "they're" or tag ==  "their":
       temp1 = "they're"
       temp2 = "their"
    if tag == "loose" or tag ==  "lose":
       temp1 = "loose"
       temp2 = "lose"
    if tag == "to" or  tag == "too":
       temp1 = "to"
       temp2 = "too"
     
    weight[temp1 + "l:" + wordl1] = 0 
    weight[temp2 + "l:" + wordl1] = 0 
    weight[temp1 + "l:" + wordl2] = 0 
    weight[temp2 + "l:" + wordl2] = 0 
    weight[temp1 + "r:" + wordr1] = 0 
    weight[temp2 + "r:" + wordr1] = 0 
    weight[temp1 + "r:" + wordr2] = 0 
    weight[temp2 + "r:" + wordr2] = 0 
    weight[temp1 + "c:" + word] = 0 
    weight[temp2 + "c:" + word] = 0 

    catchWeight[temp1 + "l:" + wordl1] = 0 
    catchWeight[temp2 + "l:" + wordl1] = 0 
    catchWeight[temp1 + "l:" + wordl2] = 0 
    catchWeight[temp2 + "l:" + wordl2] = 0 
    catchWeight[temp1 + "r:" + wordr1] = 0 
    catchWeight[temp2 + "r:" + wordr1] = 0 
    catchWeight[temp1 + "r:" + wordr2] = 0 
    catchWeight[temp2 + "r:" + wordr2] = 0 
    catchWeight[temp1 + "c:" + word] = 0 
    catchWeight[temp2 + "c:" + word] = 0 
 

for theclass in tagClass:
     bias[theclass] = 0
     catchBias[theclass] = 0

aaa = 1

for x in range(10):
    print("iteration" + str(aaa))
    aaa = aaa + 1
    f_training.close()
    f_training = open(training_file, 'r')
    sentence = f_training.read().decode(errors = 'ignore').encode(errors = 'ignore')
    words = sentence.split()
    _length = len(words)
    flagi = 0
    for i in range(_length):

      if flagi == 1:
        flagi = 0
        continue

      flag = test(words[i].lower(), i, words)

      if flag != 4:
        word = words[i].lower()
        if flag == 5:
          for tag in tagClass:
            if tag == word:
               tag = word
               break
          j = i + 1
          k = i + 2
          length = _length  
          
        elif flag == 1 or flag == 2 or flag==3:
          j = i + 2
          k = i + 3
          length = _length - 1
          if flag == 1: tag = "it's"
          if flag == 2: tag = "your're"
          if flag == 3: tag = "they're"
          flagi = 1 


        feature1 = {}
        feature2 = {}
        activation = {}
        if length >1:
          if i == 0:
             wordl1 = 'bos1'
             wordl2 = 'bos2'
          elif i == 1:
             wordl1 = 'bos1'
             wordl2 = words[i-1].lower()#####################
          else:
             wordl1 = words[i-2].lower()
             wordl2 = words[i-1].lower()

          if length - i == 2:
             wordr1 = words[j].lower()
             wordr2 = 'eos2'
          elif length - i == 1:
             wordr1 = 'eos1'
             wordr2 = 'eos2'
          else:
             wordr1 = words[j].lower()
             wordr2 = words[k].lower()
        elif length == 1:
             wordl1 = 'bos1'
             wordl2 = 'bos2'
             wordr1 = 'eos1'
             wordr2 = 'eos2'
  
        if tag == "it's" or tag == "its":
           temp1 = "it's"
           temp2 = "its"
        if tag == "you're" or tag ==  "your":
           temp1 = "you're"
           temp2 = "your"
        if tag == "they're" or tag ==  "their":
           temp1 = "they're"
           temp2 = "their"
        if tag == "loose" or tag ==  "lose":
           temp1 = "loose"
           temp2 = "lose"
        if tag == "to" or  tag == "too":
           temp1 = "to"
           temp2 = "too"

        activation[temp1] = 0
        activation[temp2] = 0

        feature1[0] = temp1 + "l:" + wordl1
        feature2[0] = temp2 + "l:" + wordl1
        feature1[1] = temp1 + "l:" + wordl2
        feature2[1] = temp2 + "l:" + wordl2
        feature1[2] = temp1 + "r:" + wordr1
        feature2[2] = temp2 + "r:" + wordr1
        feature1[3] = temp1 + "r:" + wordr2
        feature2[3] = temp2 + "r:" + wordr2
        feature1[4] = temp1 + "c:" + word
        feature2[4] = temp2 + "c:" + word

        for v1 in feature1.values():
            activation[temp1] += weight[v1]
        for v2 in feature2.values():
            activation[temp2] += weight[v2]

        activation[temp1] +=  bias[temp1] 
        activation[temp2] +=  bias[temp2] 
        predict = max(activation.items(), key = operator.itemgetter(1))[0]
        if predict != tag:
            if predict != temp1:
               temp = temp1
               temp1 = temp2
               temp2 = temp
            for w in feature1.values():  
               weight[w] -= 1     
               catchWeight[w] -= c
            for w in feature2.values():
               weight[w] += 1
               catchWeight[w] += c
            bias[temp1] -= 1
            bias[temp2] += 1
            catchBias[temp1] -= c 
            catchBias[temp2] += c 
        c = c + 1
    for a in bias.keys():
       bias[a] = bias[a] - catchBias[a] / c


for i in weight.keys():
      weight[i] = weight[i] - catchWeight[i] / c

json.dump(weight, f_model)


f_training.close()
f_model.close()



