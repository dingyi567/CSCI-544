import json
import math
import sys
import operator
import os
import codecs

test_file = sys.argv[1]

f_model_its = open("its_model", 'r')
f_model_lose = open("lose_model", 'r')
f_model_your = open("your_model", 'r')
f_model_to = open("to_model", 'r')
f_model_their = open("their_model", 'r')
f_test = open(test_file, 'r' ,errors = 'ignore')


weight = {}
activation = {}
tagClass = ["it's", "its", "you're", "your", "they're", "their", "loose", "lose", "to", "too"]

weight_its  = json.load(f_model_its)
weight_lose = json.load(f_model_lose)
weight_your = json.load(f_model_your)
weight_to = json.load(f_model_to)
weight_their = json.load(f_model_their)


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
      print(w[i].upper(), end="")
    else:
      print(w[i].lower(), end="")
  print(" ", end="")



for line in f_test:
    words = line.split()
    _length = len(words)
    for i in range(_length):
        flag = 0
        flagPrint = 0
        format = []
        word = words[i].lower()
        for tag in tagClass:
          if tag == word:
             tag = word
             flag = 1
             break
        if flag == 1:
          j = i + 1
          k = i + 2
          length = _length   
          format = testCase(words[i])
    
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
             count_its += 1
             temp1 = "it's"
             temp2 = "its"
          elif tag == "you're" or tag ==  "your":
             count_your += 1
             temp1 = "you're"
             temp2 = "your"
          elif tag == "they're" or tag ==  "their":
             count_their += 1
             temp1 = "they're"
             temp2 = "their"
          elif tag == "loose" or tag ==  "lose":
             count_lose += 1
             temp1 = "loose"
             temp2 = "lose"
          elif tag == "to" or  tag == "too":
             count_to += 1
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
    
          if tag == "it's" or tag == "its":
            for v1 in feature1.values():
               if v1 in weight_its.keys():
                  activation[temp1] += weight_its[v1]
            for v2 in feature2.values():
               if v2 in weight_its.keys():
                  activation[temp2] += weight_its[v2]
    
          elif tag == "you're" or tag ==  "your":
            for v1 in feature1.values():
               if v1 in weight_your.keys():
                  activation[temp1] += weight_your[v1]
            for v2 in feature2.values():
               if v2 in weight_your.keys():
                  activation[temp2] += weight_your[v2]
    
          elif tag == "they're" or tag ==  "their":
            for v1 in feature1.values():
               if v1 in weight_their.keys():
                  activation[temp1] += weight_their[v1]
            for v2 in feature2.values():
               if v2 in weight_their.keys():
                  activation[temp2] += weight_their[v2]
    
          elif tag == "loose" or tag ==  "lose":
            for v1 in feature1.values():
               if v1 in weight_lose.keys():
                  activation[temp1] += weight_lose[v1]
            for v2 in feature2.values():
               if v2 in weight_lose.keys():
                  activation[temp2] += weight_lose[v2]
    
          elif tag == "to" or  tag == "too":
            for v1 in feature1.values():
               if v1 in weight_to.keys():
                  activation[temp1] += weight_to[v1]
            for v2 in feature2.values():
               if v2 in weight_to.keys():
                  activation[temp2] += weight_to[v2]
    
          predict = max(activation.items(), key = operator.itemgetter(1))[0]

     
          if predict != tag:
            #if predict == "too":
              #predict = "to"
            format = testCase(predict)
            printResult(predict, format)
            flagPrint = 1
     
        if flagPrint == 0:
           print(words[i], end="")
           print(" ", end="")

    print("\n", end="")



f_test.close()
f_model_its.close()
f_model_lose.close()
f_model_your.close()
f_model_to.close()
f_model_their.close()


