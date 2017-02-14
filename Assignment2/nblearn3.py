import re
import string
import math
import sys

#Training Labels
fname2 = sys.argv[2]
f2 = open(fname2).read().split('\n')
d2={}
for i in range(len(f2)-1):
    a = f2[i].split(' ',1)
    key = a[0]
    value = a[1]
    d2[key]=value

#Calculating Priors
priors = [0,0,0,0]
for value in d2.values():
    if value == "truthful positive":
        priors[0] += 1
    elif value == "truthful negative":
        priors[1] += 1
    elif value == "deceptive positive":
        priors[2] += 1
    elif value == "deceptive negative":
        priors[3] += 1

for i in range(len(priors)):
    priors[i] = priors[i]/sum(priors)

#Writing prior probabilities to nbmodel.txt file
f3 = open('nbmodel.txt','w')
for i in range(len(priors)):
    f3.write(str(priors[i])+'\n')

#Training Data
fname1 = sys.argv[1]
f1 = open(fname1).read().split('\n')
d1={}
for i in range(len(f1)-1):
    a = f1[i].split(' ',1)
    key = a[0]
    value = a[1]
    value = str.lower(value)
    v = re.split(r'[/.,; ]',value)
    v = list(set(v))
    d1[key] = v

for v in d1.values():
    for i in range(len(v)):
        v[i] = v[i].translate(str.maketrans("","", string.punctuation))

#Ignore Words data
IgnoreWords = []
f5 = open('Ignore.txt').read().split('\n')
for i in range(len(f5)):
    IgnoreWords.append(f5[i])

#Calculating Occurrence of words in each class
d3 = {}
for k2,v2 in d2.items():
    for k1,v1 in d1.items():
        if k1 == k2:
            c = v2
            for i in range(len(v1)):
                if(len(v1[i])>2 and v1[i].isdigit()==False and (re.match(r'[1-9]+[A-Za-z]*',v1[i]) is None) and (re.match(r'[A-Za-z]+[1-9]+',v1[i]) is None) and v1[i] not in IgnoreWords):
                    if v1[i] not in d3:
                        if c == "truthful positive":
                            d3[v1[i]] = [1,0,0,0]
                        elif c == "truthful negative":
                            d3[v1[i]] = [0,1,0,0]
                        elif c == "decptive positive":
                            d3[v1[i]] = [0,0,1,0]
                        elif c == "deceptive negative":
                            d3[v1[i]] = [0,0,0,1]
                    else:
                        if c == "truthful positive":
                            d3[v1[i]][0] += 1
                        elif c == "truthful negative":
                            d3[v1[i]][1] += 1
                        elif c == "deceptive positive":
                            d3[v1[i]][2] += 1
                        elif c == "deceptive negative":
                            d3[v1[i]][3] += 1

# classCount=[0,0,0,0]
#Distinct words
distinct = len(d3)

#Count of words in each class
tot = [0,0,0,0]        
for v in d3.values():
    tot[0] += v[0]
    tot[1] += v[1]
    tot[2] += v[2]
    tot[3] += v[3]

#Laplace Smoothing
for k,v in d3.items():
    for i in range(len(v)):
        v[i] += 1

#Conditional Probability Calculation
for k,v in d3.items():
    for i in range(len(v)):
        v[i] = v[i]/(distinct+tot[i])

#Writing Conditional Probabilities to the nbmodel.txt
for k,v in d3.items():
    f3.write(k+' '+str(v[0])+' '+str(v[1])+' '+str(v[2])+' '+str(v[3])+'\n')
