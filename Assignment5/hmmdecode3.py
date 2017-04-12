# -*- coding: utf-8 -*- 

import sys
import codecs
import math

#Reading file
#HMM Model File
f1 = open("hmmmodel.txt").read().split('\n')
length = len(f1)-1

#Total Number of Tags
tot_tags = int(f1[0])

#writing tags to a list
var = f1[1].split(' ')

#Writing transition data from file to transition dictionary
transition = {}
for i in range(3,length):
	temp = f1[i].split(' ')
	if(len(temp) == 1):
		key = temp[0]
		continue
	while(len(temp) != 1 and temp[0] != "Emission" and temp[1] != "probabilities"):
		if key not in transition:
			transition[key] = {temp[0]:float(temp[1])}
		else:
			transition[key].update({temp[0]:float(temp[1])})
		break
	if(temp[0] == "Emission" and temp[1] == "probabilities"):
		line_number = i
		break

#Writing emission data to emission dictionary
emission = {}
length = len(f1)-1-i
for i in range(i+1,length):
	temp = f1[i].split(' ')
	if(len(temp) == 1):
		key = temp[0]
		continue
	while(len(temp) != 1):
		if key not in emission:
			emission[key] = {temp[0]:float(temp[1])}
		else:
			emission[key].update({temp[0]:float(temp[1])})
		break

#Catalan_corpus_dev_raw File
fname2 = sys.argv[1]
f2 = open(fname2).read().split('\n')

#writing to hmmoutput.txt
f4 = open('hmmoutput.txt','w')

#Viterbi function
def viterbi_func(sen,length):
	viterbi = {}
	backpointer = {}
	#initialization step
	for i in range(len(var)):
		trans = transition['Q0'][var[i]] 
		if sen[0] not in emission:
			prod = math.log(trans)
		else:
			if(var[i] not in emission[sen[0]]):
					continue
			else:
				emiss = emission[sen[0]][var[i]]
				prod = math.log(trans) + math.log(emiss)

		viterbi[var[i]] = prod
	# maximum = None
	# for k1,v1 in viterbi.items():
	# 	if(v1 > maximum):
	# 		maximum = viterbi[k1]
	# 		tag = k1
	tag = max(viterbi, key=viterbi.get)
	value = viterbi[tag]
	f4.write(sen[0]+"/"+tag)

	#recursion step
	for i in range(1,len(sen)):
		viterbi.clear()
		for j in range(len(var)):
			trans = transition[tag][var[j]]
			if sen[i] not in emission:
				prod = math.log(trans) + value
			else:
				if(var[j] not in emission[sen[i]]):
					continue
				else:
					emiss = emission[sen[i]][var[j]]
					prod = math.log(trans) + math.log(emiss) + value
			viterbi[var[j]] = prod
		# maximum = None
		# for k1,v1 in viterbi.items():
		# 	if(viterbi[k1] > maximum):
		# 		maximum = viterbi[k1]
		# 		tag = k1
 
		tag = max(viterbi, key=viterbi.get)	
		value = viterbi[tag]
		f4.write(" "+sen[i]+"/"+tag)
	f4.write('\n')

		
#Calling Viterbi Algorithm function for every line

for i in range(len(f2)-1):
	sen = f2[i].split(' ')
	length = len(sen)
	viterbi_func(sen,length)