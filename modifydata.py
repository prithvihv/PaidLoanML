import numpy as np
import pandas as pd 
import datetime as dt
import csv


data=pd.read_csv("./Loan payments data.csv")

from sklearn import preprocessing
le=preprocessing.LabelEncoder()
data['loan_status']=le.fit_transform(data['loan_status'])
data['Gender']=le.fit_transform(data['Gender'])
data['education']=le.fit_transform(data['education'])
data['past_due_days']=data['past_due_days'].fillna(0)
data['due_date'] = pd.to_datetime((data['due_date']),format="%m/%d/%Y")
data['effective_date'] = pd.to_datetime((data['effective_date']),format="%m/%d/%Y")
data['paid_off_time'] = pd.to_datetime((data['paid_off_time']),format="%m/%d/%Y %H:%M")
#if statement here
data['past_due_days'] = (data['paid_off_time'].sub(data['due_date'], axis=0)).dt.days


#row = ['2', ' Marie', ' California']

print("started")
with open('./Loan payments data.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    lines = list(reader)
i=0
j=0
for row in lines:
    if j==0:
        j=j+1
        continue
    row[7] = data['past_due_days'][i]
    i=i+1
    if i==301:
        break

with open('./Loan payments data.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)

print("done")
readFile.close()
writeFile.close()