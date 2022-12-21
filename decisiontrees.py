import csv 
import math
import random
import sys
from re import L


file = sys.argv[1]

def read(file):
    data = []
    with open(file,'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return data

data = read(file)

def baseentropy(set):
    result = len(set[1]) - 1
    possibilities = []
    counts = dict()  
    total = len(set) - 1  
    for i in range(1,len(set)):
        res = set[i][result] 
        if res not in possibilities:
            possibilities.append(res)
        if res not in counts:
            counts[res] = 1 
        else:
            counts[res] = counts.get(res) + 1 
    entropy = 0 
    for j in counts: 
        count = counts.get(j)
        entropy = entropy + ((count/total) * math.log((count/total),2))
    return -1*entropy 

def valentropy(ind,val,set):
    result = len(set[1]) - 1
    possibilities = []
    counts = dict()  
    total = 0 
    for i in range(1,len(set)):
        res = set[i][result]
        if set[i][ind] == val: 
            total = total + 1
            if res not in possibilities:
                possibilities.append(res)
            if res not in counts:
                counts[res] = 1 
            else:
                counts[res] = counts.get(res) + 1 
    entropy = 0 
    for j in counts: 
        count = counts.get(j)
        entropy = entropy + ((count/total) * math.log((count/total),2))
    return -1*entropy 

def featureentropy (ind,set):
    possibilities = []
    counts = dict()  
    total = len(set) - 1  
    for i in range(1,len(set)):
        res = set[i][ind] 
        if res not in possibilities:
            possibilities.append(res)
        if res not in counts:
            counts[res] = 1 
        else:
            counts[res] = counts.get(res) + 1 
    entropy = 0 
    for j in counts: 
        count = counts.get(j)
        entropy = entropy + (count/total) * valentropy(ind,j,set)
    return entropy 

def featurelist(set):
    features = []
    for i in range(0,len(set[0])-1):
        features.append(set[0][i])
    return features

def featureentropydict(set):
    entropydict = dict()
    total_entropy = baseentropy(set)
    for i in range (0,len(set[0])-1):
        entropydict[set[0][i]] = total_entropy - featureentropy(i,set)
    return entropydict

def findhighestfeature(entropy_dict):
    greatest = 0
    feat = None 
    for i in entropy_dict:
        feat_entropy = entropy_dict.get(i)
        if feat_entropy > greatest:
            greatest = feat_entropy 
            feat = i 
    return feat 

def editdata(set,feature):
    for i in range (0,len(set[0])-1):
        if set[0][i] == feature:
            ind = i 
    possibilities = []  
    for i in range(1,len(set)):
        res = set[i][ind] 
        if res not in possibilities:
            possibilities.append(res)
    featdict = dict()
    base = [] 
    for i in range(0,len(set[0])):
        if i != ind:
            base.append(set[0][i])
    for possibility in possibilities:
        newset = [base]
        for i in set: 
            hold = []
            if i[ind] == possibility: 
                for j in range(0,len(i)):
                    if j != ind:
                        hold.append(i[j])
            if hold != []: 
                newset.append(hold)
        featdict[possibility] = newset 
    return featdict 


def create_tree(set,count):
    if count == 0: 
        base = baseentropy(set)
        outputfile.write("* Starting Entropy: " + str(base))
        outputfile.write('\n')
    entdict = featureentropydict(set)
    bestfeature = findhighestfeature(entdict)
    bestent = entdict.get(bestfeature)
    for i in range (0,count):
        outputfile.write("\t")
    outputfile.write("* " + bestfeature + "? (infomation gain: " + str(bestent) + ")")
    outputfile.write('\n')
    feat_dict = editdata(set,bestfeature)
    for i in feat_dict: 
        entropy = baseentropy(feat_dict.get(i))
        if entropy == 0: 
            result = feat_dict.get(i)[1][len(feat_dict.get(i)[1])-1]
            for x in range (0,count+1):
                outputfile.write("\t")
            outputfile.write("* " + i + " ---> " + result)
            outputfile.write('\n')
        else:
            for x in range (0,count+1):
                outputfile.write("\t")
            outputfile.write("* " + i + " (with curret entropy " + str(entropy) + ")")
            outputfile.write('\n')
            create_tree(feat_dict.get(i),count+2)


outputfile = open("treeout.txt",'w')
create_tree(data,0) 
outputfile.close()
