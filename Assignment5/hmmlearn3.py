# -*- coding: utf-8 -*- 

import sys
import codecs

#Reading file
fname1 = sys.argv[1]
f1 = open(fname1,'rb').read().split('\n')
print(type(f1))
#Split each sentence
f2 = []
for i in range(len(f1)-1):
	temp = f1[i].split(' ')
	f2.append(temp)
	
#Determine all tags 
tag = list()
for i in range(len(f2)):
	for j in range(len(f2[i])):
		if(f2[i][j][-2:] not in tag):
			tag.append(f2[i][j][-2:])

# Writing number of tags to hmmmodel.txt
f3 = open('hmmmodel.txt','w')
f3.write(str(len(tag))+'\n'+tag[0])
for i in range(1,len(tag)):
	f3.write(' '+tag[i])
f3.write('\n')

#Determining the tags and their counts
tag_set1 = {} 
tag_set2 = {}
tag_set3 = {}
transition = {}

for i in range(len(f2)):
	if(f2[i][0][-2:] not in tag_set1):
		tag_set1[f2[i][0][-2:]] = 1
	else:
		tag_set1[f2[i][0][-2:]] += 1
	for j in range(len(f2[i])-1):
		if (f2[i][j][-2:]) not in tag_set2:
			tag_set2[f2[i][j][-2:]] = 1
			tag_set3[f2[i][j][-2:]] = 1
		else:
			tag_set2[f2[i][j][-2:]] += 1
			tag_set3[f2[i][j][-2:]] += 1
		if (j == len(f2)-2):
			if (f2[i][j+1][-2:]) not in tag_set3:
				tag_set3[f2[i][j+1][-2:]] = 1
			else:
				tag_set3[f2[i][j+1][-2:]] += 1

		if (f2[i][j][-2:]) not in transition:
			transition[f2[i][j][-2:]] = {f2[i][j+1][-2:]:1}
		else:
			if(f2[i][j+1][-2:] not in transition[f2[i][j][-2:]]):
				transition[f2[i][j][-2:]].update({f2[i][j+1][-2:]:1})
			else:
				transition[f2[i][j][-2:]][f2[i][j+1][-2:]] += 1
 
for i in range(len(tag)):
	if(tag[i] not in tag_set1):
		tag_set1[tag[i]] = 0

#Transition Counts
initial = {}
for k,v in tag_set1.items():
	if 'Q0' not in initial:
		initial['Q0']={k:v}
	else:
		initial['Q0'].update({k:v})

for i in range(len(tag)):
	for k1,v1 in transition.items():
		if tag[i] not in transition[k1]:
			transition[k1].update({tag[i]:0})


#Transition Probability after smoothing
for k1,v1 in initial.items():
	for k2,v2 in v1.items():
		initial[k1][k2] = (float(v2+1))/(len(f2)+len(tag))

for k1,v1 in transition.items():
	for k2,v2 in v1.items():
		if k1 in tag_set2:
			transition[k1][k2] = (float(v2+1))/(tag_set2[k1]+len(tag))

#Writing output to hmmmodel.txt file
f3.write("Transition probabilities"+'\n')
for k1,v1 in initial.items():
	f3.write(k1+'\n')
	for k2,v2 in v1.items():
		f3.write(k2+' '+str(v2)+'\n')

for k1,v1 in transition.items():
	f3.write(k1+'\n')
	for k2,v2 in v1.items():
		f3.write(k2+' '+str(v2)+'\n')

#Determining the tags and their counts for emission probabilities
emission = {}

for i in range(len(f2)):
	for j in range(len(f2[i])):
		if(f2[i][j][:-3] not in emission):
			emission[f2[i][j][:-3]] = {f2[i][j][-2:] : 1}
		else:
			if f2[i][j][-2:] not in emission[f2[i][j][:-3]]:
				emission[f2[i][j][:-3]].update({f2[i][j][-2:] : 1})
			else:
				emission[f2[i][j][:-3]][f2[i][j][-2:]] += 1

for k,v in emission.items():
	k1 = k.decode('utf-8')
	print(k1)
#Emission Probability
for k1,v1 in emission.items():
	for k2,v2 in v1.items():
		if k2 in tag_set3:
			emission[k1][k2] = (float(v2))/tag_set3[k2]

#Writing output to hmmmodel.txt file
f3.write("Emission probabilities"+'\n')
for k1,v1 in emission.items():
	# k = k1.decode('utf-8')
	# f3.write(k.encode('utf-8')+'\n')
	f3.write(str(k1)+'\n')
	for k2,v2 in v1.items():
		f3.write(k2+' '+str(v2)+'\n')

#	