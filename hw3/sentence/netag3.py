import json
import math
import sys
import operator
import os
import codecs

model_file = sys.argv[1]
test_file = sys.argv[2]

f_model = open(model_file, 'r')
f_test = open(test_file, 'r')


weight = {}
activation = {}
tagClass = ["it's", "its", "you're", "your", "they're", "their", "loose", "lose", "to", "too"]

weight = json.load(f_model)

def test(w, i, words):
  for tag in tagClass:
    if w == tag:  
      #print 5, w, tag
      return 5

  if w == "it" and words[i + 1].lower() == "'s": 
    return 1
  elif w == "you" and words[i + 1].lower() =="'re": 
    return 2
  elif w == "they" and words[i + 1].lower() == "'re" : 
    #print 3, w, words[i+1]
    return 3
  else: 
    return 4

def testCase(w):
  result = []
  for ch in w:
    if ch.isupper():
      result.append("u")
    else:
      result.append("l")
  return result

def testCase1(w1, w2):
  result = []
  for ch in w1:
    if ch.isupper():
      result.append("u")
    else:
      result.append("l")

  for ch in w2:
    if ch.isupper():
      result.append("u")
    else:
      result.append("l")

  return result

def printResult(w, formatt):
  formatt.reverse()
  for i in range(len(w)):
    if formatt.pop() == "u":
      sys.stdout.write(w[i].upper())
    else:
      sys.stdout.write(w[i].lower())

  sys.stdout.write(' ')
  sys.stdout.flush() 


sentence = f_test.read().decode(errors = 'ignore').encode(errors = 'ignore')#decode
words = sentence.split()
_length = len(words)
flagi = 0


for i in range(_length):
  if flagi == 1:
    flagi = 0
    continue

  flagPrint = 0
  flag = test(words[i].lower(), i, words)
  format = []
  
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
      format = testCase(words[i])

      
    elif flag == 1 or flag == 2 or flag==3:
      j = i + 2
      k = i + 3
      length = _length - 1
      if flag == 1: tag = "it's"
      if flag == 2: tag = "your're"
      if flag == 3: tag = "they're"
      format = testCase1(words[i], words[i+1])
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
           wordl2 = words[i-1].lower()
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
       if v1 in weight.keys():
          activation[temp1] += weight[v1]
    for v2 in feature2.values():
       if v2 in weight.keys():
          activation[temp2] += weight[v2]

    predict = max(activation.items(), key = operator.itemgetter(1))[0]

    if predict != tag:
      format = testCase(predict)
    printResult(predict, format)
    flagPrint = 1
     
  if flagPrint == 0:
      sys.stdout.write(words[i])
      sys.stdout.write(' ')
      sys.stdout.flush()


f_model.close()
f_test.close()



