import csv 
import math
import random
from re import L 

starfile = "star_data.csv"

def read(file):
    data = []
    with open(file,'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            if row[0] != "Temperature (K)":
                temp, lum, rad, mag, tp, cl, spect = row 
                data.append((math.log(float(temp)),math.log(float(lum)),math.log(float(rad)),float(mag),int(tp)))
    return data 

data = read(starfile)

k = 6

def initial(k,file): 
    ls = []
    max = len(file)
    for i in range (0,k):
        rand = int(random.random() * max)
        while rand in ls:
            rand = int(random.random() * max)
        ls.append(rand)
    distinct = [] 
    for j in ls:
        distinct.append([file[j]])
    return distinct

starting = initial(k,data)

def avg(setinfo):
    temp,lum,rad,mag,tp = 0.0,0.0,0.0,0.0,0.0
    for i in setinfo: 
        t,l,r,m,type = i 
        temp = temp + t
        lum = lum + l
        rad = rad + r
        mag = mag + m 
    temp = temp/len(setinfo)
    lum = lum/len(setinfo)
    rad = rad/len(setinfo)
    mag = mag/len(setinfo)
    return temp,lum,rad,mag 

def mean(individual,setinfo):
    temp, lum, rad, mag, tp = individual
    t, l, r, m = avg(setinfo)
    error = math.pow( math.pow(t-temp,2) + math.pow(l-lum,2) + math.pow(r-rad,2) + math.pow(m-mag,2),1)
    return error

def sort(sets,file):
    means = [] 
    for i in range(0,len(sets)):
        means.append([])
    for i in file:
        minerror = 1000
        bestset = 0 
        for x in range (0,len(sets)):
            error = mean(i,sets[x])
            if error < minerror:
                minerror = error
                bestset = x 
        means[bestset].append(i)        
    return means


newmeans = sort(starting,data) 
second = sort(newmeans, data)

while newmeans != second:
    newmeans = second 
    second = sort(newmeans,data) 


for i in second:
    print("Avg")
    print(avg(i))
    print("Ind")
    for j in i:
        temp, lum, rad, mag, tp = j
        print(tp, temp,lum,rad,mag)
    print('--------------------------------------')






