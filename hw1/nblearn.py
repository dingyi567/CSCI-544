import sys
import json

training_file = sys.argv[1]
model_file = sys.argv[2]
Dict = {}
d = {}
f = open(training_file, 'r')
f_m = open(model_file, 'w')

words3 = set()
classes = []

for line in f:
  prex, text3 = line.split(' ',1) 
  for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~':
     text3 = text3.replace(ch, ' ') 
  text3 = text3.lower()
  words3.update(text3.split())
  if prex not in classes:
      classes.append(prex)
  
vocabulary_size = len(set(words3))

for i in classes:
   d[i] = 0

f.close()
f = open(training_file, 'r')

for line in f:
  className, text = line.split(' ', 1)
  for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~':
     text = text.replace(ch, ' ')
 
  text = text.lower()
  words = text.split()
  for theclass in classes:
     if theclass == className:
        d[className] = d[className] + 1
        for w in words:
            Dict[className + '_' + w] = Dict.get(className + '_' + w, 0) + 1


for j in classes:
   Dict['*_' + j + '_' + 'Count'] = d[j]


Dict['~_VocabularySize'] = vocabulary_size

json.dump(Dict, f_m)

f.close()
f_m.close()





dingyi567
