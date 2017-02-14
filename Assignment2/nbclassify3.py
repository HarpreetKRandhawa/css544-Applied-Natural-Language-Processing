import re
import string
import math
import sys

#Opening Ignore.txt
IgnoreWords = []
f5 = open('Ignore.txt').read().split('\n')
for i in range(len(f5)):
    IgnoreWords.append(f5[i])

#Opening nbmodel.txt
f1 = open('nbmodel.txt').read().split('\n')

#Extracting prior probabilities from nbmodel.txt
score = []
for i in range(0,4):
    score.append(float(f1[i]))

#Computing log of prior probabilities
for i in range(len(score)):
    score[i] = math.log(score[i])

#Extracting the conditional probabilities from nbmodel.txt
condt_prob = {}
for i in range(4,len(f1)-1):
    a = f1[i].split(' ')
    key = a[0]
    value = a[1:]
    condt_prob[key]=value

for k,v in condt_prob.items(): 
    for i in range(len(v)):
        v[i] = float(v[i])

#Opening test-data document
fname = sys.argv[1]
f2 = open(fname).read().split('\n')

#Storing test-data in dict d1
d1 = {}
for i in range(len(f2)-1):
    a = f2[i].split(' ',1)
    key = a[0]
    value = a[1]
    value = str.lower(value)
    v = re.split(r'[/.,; ]',value)
    v = list(set(v))
    d1[key] = v

for v in d1.values():
    for i in range(len(v)):
        v[i] = v[i].translate(str.maketrans("","", string.punctuation))

#Eliminating the Stop words and storing new dict d2
word = []
d2 = {}
for k,v in d1.items():
    for i in range(len(v)):
        if(len(v[i])>2 and v[i].isdigit()==False and (re.match(r'[1-9]+[A-Za-z]*',v[i]) is None) and (re.match(r'[A-Za-z]+[1-9]+',v[i]) is None) and v[i] not in IgnoreWords):
            word = v[i]
            if k not in d2.keys():
                d2.setdefault(k, [])
                d2[k].append(word)
            else:
                d2[k].append(word)

#Writing to nboutput.txt
f3 = open('nboutput.txt','w')

#Copying score list to another
t = []
for i in range(len(score)):
    t.append(score[i])

#Assigning max probability and writing to nboutput
for k1,v1 in d2.items():
    for i in range(len(v1)):
        w = v1[i]
        for k2,v2 in condt_prob.items():
            if k2 == w:
                score[0] += math.log(v2[0])
                score[1] += math.log(v2[1])
                score[2] += math.log(v2[2])
                score[3] += math.log(v2[3])
    argmax = max(score)
    if argmax == score[0]:
        f3.write(k1+' '+'truthful positive'+'\n')
    elif argmax == score[1]:
        f3.write(k1+' '+'truthful negative'+'\n')
    elif argmax == score[2]:
        f3.write(k1+' '+'deceptive positive'+'\n')
    elif argmax == score[3]:
        f3.write(k1+' '+'deceptive negative'+'\n')
    for i in range(len(score)):
        score[i] = t[i]

