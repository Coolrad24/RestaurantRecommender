from re import X
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import sklearn
from sklearn import *
import csv

#get data from our database in csv format
Data=[]
with open('database.csv','r') as d:
    
    reader=csv.reader(d)
    for r in reader:
        Data.append(r)
del Data[0]

testData=[]
Names=[]
links=[]
for d in Data:
    Names.append(d[0])
    links.append(d[len(d)-1])
    tempData=[]
    for i in range(1,4):
        tempData.append(int(d[i]))
    testData.append(tempData)
testNames=[]
for i in range(len(Names)+1):
    testNames.append(i)
del testNames [0]

model=svm.SVC()
model.fit(testData,testNames)



