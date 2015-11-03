import os
import glob

list_of_files=glob.glob('/home/dingyi/Downloads/SPAM_training/*.txt')

with open("spam_training.txt", 'w') as fout:
  for fileName in list_of_files:
    fin = open(fileName, 'r', errors='ignore')
    name1, name2 = fileName.split('.', 1)
    name3, name4 = name1.rsplit('/', 1)
    fout.writelines(name4 + ' ')
    data = fin.read()
    data = data.replace("\n", "")
    fout.write(data + '\n')
    fin.close()

fout.close()


dingyi567
