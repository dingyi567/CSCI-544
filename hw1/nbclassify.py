import json
import math
import sys
import operator

model_file = sys.argv[1]
test_file = sys.argv[2]

f_test = open(test_file, 'r')
f_model = open(model_file, 'r')
#sys.stdout = open("spam.out", 'w')

Dict = json.load(f_model)

d = {}
P_c = {}
classes = []
N = 0 #total number of documents
correct = 0 
k = int(Dict['~_VocabularySize'])

for t, v in Dict.items():
  ClassName, WordName = t.split('_',1)
  if ClassName == '*':
     i, j = WordName.split('_', 1)
     if i not in classes:
        classes.append(i)

for CLASS1 in classes:
    N = N + Dict['*_' + CLASS1 + '_' + 'Count']
    
for CLASS in classes:
    d[CLASS] = 0
    P_c[CLASS] = math.log(Dict['*_' + CLASS + '_' + 'Count']/N)

for x, y in Dict.items(): #total number for each class
  ClassName1, WordName1 = x.split('_',1)
  if ClassName1 != '*' and ClassName1 != '~':
     d[ClassName1] = d[ClassName1] + y 

for line in f_test:
   P = {}
   w1 = ''
   for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~':
       line = line.replace(ch, ' ')
   line = line.lower()
   words = line.split()
   for s in classes:
       P_d_c =0
       for w in words:
          w1 = s + '_' + w
          if w1 in Dict:
             P_w1_c = math.log((Dict[w1] + 1) / (d[s] + k))
             P_d_c = P_d_c + P_w1_c
          else:
             P_w1_c = math.log(1 / (d[s] + k + 1 ))
             P_d_c = P_d_c + P_w1_c
       P[s] = P_d_c + P_c[s]

   Result = max(P.items(), key=operator.itemgetter(1))[0]
   print(Result)#modify


#sys.stdout.close()
f_test.close()
f_model.close()





dingyi567
