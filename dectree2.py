import matplotlib.pyplot as plt 
import csv 
import math
import random
import sys

# xs = []
# ys = []

# for x in range(1,101):
#     xs.append(x)
#     ys.append(x)

# plt.scatter(xs,ys)

#plt.show()

def read(file):
    data = []
    with open(file,'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            data.append(row[0:])
    return data

file = "house-votes-84.csv" 
file = 'nursery.csv'
file = sys.argv[1] 
readdata = read(file)


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
    entdict = featureentropydict(set)
    bestfeature = findhighestfeature(entdict)
    bestent = entdict.get(bestfeature)
    if bestfeature == None:
        return set[int((len(set)-1)*random.random()+1)][-1]
    tree = dict()
    feat_dict = editdata(set,bestfeature)
    for i in feat_dict: 
        entropy = baseentropy(feat_dict.get(i))
        if entropy == 0: 
            result = feat_dict.get(i)[1][len(feat_dict.get(i)[1])-1]
            treewithin = dict() 
            treewithin[i] = result 
            if bestfeature not in tree:
                tree[bestfeature] = [treewithin]
            else:
                tree[bestfeature] = tree.get(bestfeature) + [treewithin]
        else:
            treewithin = dict() 
            treewithin[i] = create_tree(feat_dict.get(i),count+2)
            if bestfeature not in tree:
                tree[bestfeature] = [treewithin]
            else:
                tree[bestfeature] = tree.get(bestfeature) + [treewithin]
    return tree


def valset(set):
    possibilities = []
    for i in range(1,len(set)):
        res = set[i][len(set[i])-1] 
        if res not in possibilities:
            possibilities.append(res)
    return possibilities

def indset(set,ind):
    possibilities = []
    for i in range(1,ind):
        res = set[i][ind] 
        if res not in possibilities:
            possibilities.append(res)
    return possibilities

def guessval(tree,row,key,vals):
    party = "indepedent"
    length = len(key) 

    while True:
        stuck = tree 
        for i in tree:
            if tree in vals:
                return tree 
            if i in key: 
               ind = key.index(i)
               val = row[ind]
               for j in tree.get(i):
                   if val in j: 
                       if j.get(val) in key:
                           print(tree)
                       tree = j.get(val)
                       if tree in vals:
                          return tree
        if stuck == tree:
            if tree in vals:
                return tree
            for i in tree:
                if i in vals:
                    return i  
                newtree = tree.get(i)[int(random.random()*len(tree.get(i)))]
                for k in newtree:
                    if k in vals:
                        return k 
                    if newtree.get(k) in vals: 
                        return newtree.get(k)
            for j in newtree:
                tree = newtree.get(j)
                if tree in vals:
                    return tree 
        if tree in vals:
            return tree 
        
        
    return None 

def accuracy(rows,set):
    tree = create_tree(set,0)
    basis = set[0] 
    vals = valset(set)
    correct = 0 
    total = 0 
    for i in rows:
        total = total + 1 
        guess = guessval(tree,i,basis,vals)
        if guess == i[len(i)-1]:
            correct = correct + 1
    return(correct/total)

def fixvals(set):
    classes = valset(set)

    avg = dict()
    for i in classes:
        avg[i] = [] 
        for j in range (0,len(set[0])-1):
            n = avg.get(i)
            n.append(dict())

    for i in range (1,len(set)):
        group = avg.get(set[i][len(set[i])-1])
        for j in range (0,len(set[i])-1):
            if set[i][j] != '?': 
                if set[i][j] not in group[j]:
                    group[j][set[i][j]] = 1 
                else:
                    group[j][set[i][j]] = group[j].get(set[i][j]) + 1  
    finals = dict()
    for i in classes:
        finals[i] = [] 
        for j in range (0,len(set[0])-1):
            n = finals.get(i)
            n.append(None)
    
    for i in avg: 
        for j in range (0,len(avg.get(i))):
            bestval = None 
            bestscore = 0 
            for k in avg.get(i)[j]:
                if avg.get(i)[j].get(k) > bestscore:
                    bestscore = avg.get(i)[j].get(k)
                    bestval = k 
            finals.get(i)[j] = bestval

    for i in set:
        for j in range(0,len(i)-1):
            if i[j] == '?':
                i[j] = finals.get((i[len(i)-1]))[j]
          
    return set

def selectdata(sdata,size,bound):
    ls = [sdata[0]]
    indices = [] 
    for k in range (1,size):
        rand = int(random.random() * bound + 1)
        while rand in indices:
            rand = int(random.random() * bound + 1)
        indices.append(rand) 
    for i in indices:
        ls.append(sdata[i])
    
    val = ls[1][-1]
    reclass = 0 
    for line in range(1,len(ls)): 
        if val != ls[line][-1] :
            reclass = 1 

    if reclass == 0:
        return selectdata(sdata,size,bound)
    return ls 

data = fixvals(readdata)

testsize = int(sys.argv[2])

mintrainsize = int(sys.argv[3])

maxtrainsize = int(sys.argv[4])

step = int(sys.argv[5])

readdata = selectdata(data,len(data),len(data)-1)

test = readdata[len(readdata)-testsize:]


inds = [] 
avg = [] 
for size in range (mintrainsize,maxtrainsize,step):
    data = selectdata(readdata[:len(readdata)-testsize],size,len(readdata)-testsize-1)
    inds.append(size) 
    avg.append(accuracy(test,data))
    #print(size)

plt.scatter(inds,avg)

plt.show()
