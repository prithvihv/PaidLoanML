import numpy as np
import pandas as pd
import datetime as dt
import csv
import copy
import pickle

data = pd.read_csv("./Loan payments data.csv")
pkl_filename = "Model.pkl"

def savemodel():
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    data['loan_status'] = le.fit_transform(data['loan_status'])
    data['Gender'] = le.fit_transform(data['Gender'])
    data['education'] = le.fit_transform(data['education'])
    data['due_date'] = pd.to_datetime((data['due_date']), format="%m/%d/%Y")
    data['effective_date'] = pd.to_datetime(
        (data['effective_date']), format="%m/%d/%Y")
    data['paid_off_time'] = pd.to_datetime(
        (data['paid_off_time']), format="%m/%d/%Y %H:%M")
    data2 = data
    data2.drop('Loan_ID', axis=1, inplace=True)
    data3 = copy.deepcopy(data2)
    label_loan_status = data2.pop('loan_status')
    label_past_due_days = data2.pop('past_due_days')
    data2.drop('effective_date', axis=1, inplace=True)
    data2.drop('due_date', axis=1, inplace=True)
    data2.drop('paid_off_time', axis=1, inplace=True)
    from sklearn.model_selection import train_test_split
    data_train, data_test, label_train, label_test = train_test_split(
        data2, label_loan_status, test_size=0.2, random_state=16)
    from sklearn.linear_model import LogisticRegression
    logis = LogisticRegression()
    logis.fit(data_train, label_train)
    logis_score_train = logis.score(data_train, label_train)
    print("Training score: ", logis_score_train)
    logis_score_test = logis.score(data_test, label_test)
    print("Testing score: ", logis_score_test)
    with open(pkl_filename, 'wb') as file:
        pickle.dump(logis, file)
    print("wrote to local")


def loadModel():
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model


def predict(principal, term, age, education, gender):
    Model = loadModel()
    y = Model.predict(
        [[principal, term, age, education, gender]])
    # return processAnswer(y)
    print(processAnswer(y))


def processAnswer(num):
    if(num == 2):
        return 'paidOff'
    elif(num == 1):
        return 'collection'
    return 'collection_paidoff'


def fixdata():
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    data['loan_status'] = le.fit_transform(data['loan_status'])
    data['Gender'] = le.fit_transform(data['Gender'])
    data['education'] = le.fit_transform(data['education'])
    data['past_due_days'] = data['past_due_days'].fillna(0)
    data['due_date'] = pd.to_datetime((data['due_date']), format="%m/%d/%Y")
    data['effective_date'] = pd.to_datetime(
        (data['effective_date']), format="%m/%d/%Y")
    data['paid_off_time'] = pd.to_datetime(
        (data['paid_off_time']), format="%m/%d/%Y %H:%M")
    # if statement here
    data['past_due_days'] = (data['paid_off_time'].sub(
        data['due_date'], axis=0)).dt.days

    #row = ['2', ' Marie', ' California']

    print("started")
    with open('./Loan payments data.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
    i = 0
    j = 0
    for row in lines:
        if j == 0:
            j = +1
            continue
        row[7] = data['past_due_days'][i]
        i = i+1
        if i == 301:
            break

    with open('./Loan payments data.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    print("done")
    readFile.close()
    writeFile.close()


# savemodel()
predict(1000,30,50,0,0)
