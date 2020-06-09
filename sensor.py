#!/usr/bin/env python
# coding: utf-8
import time
from gcloud import storage
import os
import xlrd
import xlwt
import gcsfs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\dell\IoF\eyes\original-aspect-237711-16bdef48f04d.json"
# In[9]:
#import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import *
import plotly.plotly as py
import plotly.graph_objs as go
import datetime
from plotly import tools
from plotly.offline import *
from flask import make_response
import plotly
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask_wtf import FlaskForm
import pandas as pd
from flask import jsonify,json
import pandas as pd
import serial
import re
import numpy as np
import sqlite3
global portPath
portPath = "COM3"
global baud
baud = 38400
global timeout
timeout = 10
global rate
rate = 15

filename = "data.csv"
global max_num_readings
max_num_readings = 5
global num_signals
num_signals = 10
str1 = "1471"
str2 = 'crab'
from functools import wraps

class callonce(object):

    def __init__(self, f):
        self.f = f
        self.called = False

    def __call__(self, *args, **kwargs):
        if not self.called:
            self.called = True
            return self.f(*args, **kwargs)
        print ('Function already called once.')
def callonce1(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not wrapper.called:
            wrapper.called = True
            return f(*args, **kwargs)
        print('Function already called once.')
    wrapper.called = False
    return wrapper
    
 
@callonce
def create_serial_obj(portPath, baud_rate, tout):
    
    return serial.Serial(portPath, baud_rate, timeout = tout)
    
def read_serial_data(serial):
    time.sleep(15)
    #serial.rtscts = True
    #serial.dsrdtr = True
    serial.flushInput()
    
    serial_data = []
    readings_left = True
    timeout_reached = False
    
    while readings_left and not timeout_reached:
        serial_line = serial.readline()
        if serial_line == '':
            timeout_reached = True
        else:
            serial_data.append(serial_line)
            if len(serial_data) == max_num_readings:
                readings_left = False
        
    return serial_data
 
def is_number(string):
   
    try:
        str(string)
        #float(string)
        return True
    except ValueError:
        return False
        
def clean_serial_data(data):
    
    clean_data = []
    line_data = []
    newlist1 = []
    newlist1.append(str1)
    for line in data:
        line = line.decode('ISO-8859-1')
        line = line.split('\r\n')

        if line != '\r\n':
            line_data = line
            
            line_data.append(str1)
            line_data.append(str2)
        else:
           
            break 
        if len(line_data) >= 2:
            clean_data.append(line_data)
             
    return clean_data           


# In[2]:


#try:

#global f
#f = 0
#if f == 0:
print("Creating serial object...")
serial_obj = create_serial_obj(portPath, baud, timeout)
#    f = 1


#except SerialException:
  #  print("COM3 Already Active")


# In[10]:

def read():
    print("Reading serial data...")
    global serial_data
    serial_data = read_serial_data(serial_obj)
    return serial_data

    #print(len(serial_data))


# In[11]:

def clean():
    print ("Cleaning data...")
    clean_data =  clean_serial_data(serial_data)
    return clean_data

# In[12]:


def newframefinal(clean_data):
    df = pd.DataFrame(clean_data)
    start = 0  # set start to 0 for slicing
    newDF = pd.DataFrame() 
    newlist = []
    for i in range(len(df.index)):
        if (i + 1) % 2 == 0:  # the modulo operation
            result = df[0].iloc[start:i+1].values.reshape(2)
            newlist.append(result)
        #resdf = pd.DataFrame(result)
        #newDF.append(resdf)
            print (result)
        
            start = i + 1 
    global dfnew
    dfnew = pd.DataFrame(newlist,columns=['Time','temperature'])
    dfnew
    currentdt = datetime.datetime.now()
    dfnew['Time'] = str(currentdt.strftime("%Y-%m-%d %H:%M:%S"))
    dfnew['ItemName']= df[3]
    dfnew['ProductID'] = df[2]
    dfnew = dfnew.set_index("ProductID")
    dfnew['temperature'] = dfnew['temperature'].astype(float)

    dfnew['price'] = df[3]
    dfnew['shelflife'] = df[3]
    dfnew['calories'] = df[3]
    dfnew['cholestrol_in_mg'] = df[3]
    dfnew['pottasium'] = df[3]
    dfnew['protiens'] = df[3]
    dfnew['vitamin_A'] = df[3]
    dfnew['vitamin_C'] = df[3]
    dfnew['Calcium'] = df[3]
    dfnew['Iron'] = df[3]
    dfnew['shelflife'] = dfnew['shelflife'].astype(float)
    dfnew['protiens'] = dfnew['protiens'].astype(float)
    dfnew['vitamin_A'] = dfnew['vitamin_A'].astype(float)
    dfnew['vitamin_C'] = dfnew['vitamin_C'].astype(float)
    dfnew['price'] = dfnew['price'].astype(float)
    for i in range(len(dfnew['ItemName'])):
        if dfnew['ItemName'].iloc[i] == 'crab':
            dfnew['calories'].iloc[i] = 0.87
            dfnew['cholestrol_in_mg'].iloc[i] = 0.78
            dfnew['pottasium'].iloc[i] = 3.29
            dfnew['protiens'].iloc[i] = 181
            dfnew['vitamin_A'].iloc[i] = 50.0
            dfnew['vitamin_C'].iloc[i] = 30
            dfnew['Calcium'].iloc[i] = 0.89
            dfnew['Iron'].iloc[i] = 0.0074
            continue
        elif dfnew['ItemName'].iloc[i] == 'oysters':
            dfnew['calories'].iloc[i] = 1.41
            dfnew['cholestrol_in_mg'].iloc[i] = 0.81
            dfnew['pottasium'].iloc[i] = 2.5
            dfnew['protiens'].iloc[i] = 228
            dfnew['vitamin_A'].iloc[i] = 0
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.04
            dfnew['Iron'].iloc[i] = 0.055
            continue
        elif dfnew['ItemName'].iloc[i] == 'scallops':
            dfnew['calories'].iloc[i] = 0.18
            dfnew['cholestrol_in_mg'].iloc[i] = None
            dfnew['pottasium'].iloc[i] = 1.8
            dfnew['protiens'].iloc[i] = 12
            dfnew['vitamin_A'].iloc[i] = 2170
            dfnew['vitamin_C'].iloc[i] = 180
            dfnew['Calcium'].iloc[i] = 0.19
            dfnew['Iron'].iloc[i] = 0.004
            continue

        elif dfnew['ItemName'].iloc[i] == 'whole lobster':
            dfnew['calories'].iloc[i] = 0.77
            dfnew['cholestrol_in_mg'].iloc[i] = 1.27
            dfnew['pottasium'].iloc[i] = 2
            dfnew['protiens'].iloc[i] = 165
            dfnew['vitamin_A'].iloc[i] = 40
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.84
            dfnew['Iron'].iloc[i] = 0.0026
            continue

        elif dfnew['ItemName'].iloc[i] == 'cod':
            dfnew['calories'].iloc[i] = 0.820
            dfnew['cholestrol_in_mg'].iloc[i] = 0.43
            dfnew['pottasium'].iloc[i] = 4.13
            dfnew['protiens'].iloc[i] = 178
            dfnew['vitamin_A'].iloc[i] = 400
            dfnew['vitamin_C'].iloc[i] = 10
            dfnew['Calcium'].iloc[i] = 0.16
            dfnew['Iron'].iloc[i] = 0.0038
            continue


        elif dfnew['ItemName'].iloc[i] == 'flatfish':
            dfnew['calories'].iloc[i] = 0.7
            dfnew['cholestrol_in_mg'].iloc[i] = 0.45
            dfnew['pottasium'].iloc[i] = 1.6
            dfnew['protiens'].iloc[i] = 124.1
            dfnew['vitamin_A'].iloc[i] = 330
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.21
            dfnew['Iron'].iloc[i] = 0.0018
            continue



        elif dfnew['ItemName'].iloc[i] == 'fatty fish':
            dfnew['calories'].iloc[i] = 1.27
            dfnew['cholestrol_in_mg'].iloc[i] = 0.66
            dfnew['pottasium'].iloc[i] = 3.33
            dfnew['protiens'].iloc[i] = 178.3
            dfnew['vitamin_A'].iloc[i] = 300
            dfnew['vitamin_C'].iloc[i] = 16
            dfnew['Calcium'].iloc[i] = 0.41
            dfnew['Iron'].iloc[i] = 0.00124
            continue

        elif dfnew['ItemName'].iloc[i] == 'lobster':
            dfnew['calories'].iloc[i] = 0.77
            dfnew['cholestrol_in_mg'].iloc[i] = 1.27
            dfnew['pottasium'].iloc[i] = 2
            dfnew['protiens'].iloc[i] = 165
            dfnew['vitamin_A'].iloc[i] = 40
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.84
            dfnew['Iron'].iloc[i] = 0.0026
            continue


        elif dfnew['ItemName'].iloc[i] == 'smoked white fish':
            dfnew['calories'].iloc[i] = 0.92
            dfnew['cholestrol_in_mg'].iloc[i] = 0.41
            dfnew['pottasium'].iloc[i] = 3.8
            dfnew['protiens'].iloc[i] = 167.6
            dfnew['vitamin_A'].iloc[i] = 1700
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.7
            dfnew['Iron'].iloc[i] = 0.0013
            continue



        elif dfnew['ItemName'].iloc[i] == 'white fish (gutted)':
            dfnew['calories'].iloc[i] = 0.92
            dfnew['cholestrol_in_mg'].iloc[i] = 0.41
            dfnew['pottasium'].iloc[i] = 3.8
            dfnew['protiens'].iloc[i] = 167.6
            dfnew['vitamin_A'].iloc[i] = 1700
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.7
            dfnew['Iron'].iloc[i] = 0.0013
            continue

        elif dfnew['ItemName'].iloc[i] == 'mussel meats':
            dfnew['calories'].iloc[i] = 0.86
            dfnew['cholestrol_in_mg'].iloc[i] = 0.280
            dfnew['pottasium'].iloc[i] = 3.2
            dfnew['protiens'].iloc[i] = 119
            dfnew['vitamin_A'].iloc[i] = 1600
            dfnew['vitamin_C'].iloc[i] = 80
            dfnew['Calcium'].iloc[i] = 0.26
            dfnew['Iron'].iloc[i] = 0.00395
            continue


        elif dfnew['ItemName'].iloc[i] == 'kippers(vacuum packed)':
            dfnew['calories'].iloc[i] = 1.95
            dfnew['cholestrol_in_mg'].iloc[i] = 0.77
            dfnew['pottasium'].iloc[i] = 4.23
            dfnew['protiens'].iloc[i] = 162.19
            dfnew['vitamin_A'].iloc[i] = 1060
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.83
            dfnew['Iron'].iloc[i] = 0.00112
            continue

        elif dfnew['ItemName'].iloc[i] == 'kippers':
            dfnew['calories'].iloc[i] = 1.95
            dfnew['cholestrol_in_mg'].iloc[i] = 0.77
            dfnew['pottasium'].iloc[i] = 4.23
            dfnew['protiens'].iloc[i] = 162.19
            dfnew['vitamin_A'].iloc[i] = 1060
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.83
            dfnew['Iron'].iloc[i] = 0.00112
            continue



        elif dfnew['ItemName'].iloc[i] == 'herring (gutted)':
            dfnew['calories'].iloc[i] = 1.95
            dfnew['cholestrol_in_mg'].iloc[i] = 0.77
            dfnew['pottasium'].iloc[i] = 4.23
            dfnew['protiens'].iloc[i] = 162.19
            dfnew['vitamin_A'].iloc[i] = 1060
            dfnew['vitamin_C'].iloc[i] = 0
            dfnew['Calcium'].iloc[i] = 0.83
            dfnew['Iron'].iloc[i] = 0.00112
            continue





        elif dfnew['ItemName'].iloc[i] == 'shrimp':
            dfnew['calories'].iloc[i] = 0.85
            dfnew['cholestrol_in_mg'].iloc[i] = 1.61
            dfnew['pottasium'].iloc[i] = 2.62
            dfnew['protiens'].iloc[i] = 201
            dfnew['vitamin_A'].iloc[i] = None
            dfnew['vitamin_C'].iloc[i] = None
            dfnew['Calcium'].iloc[i] = 0.64
            dfnew['Iron'].iloc[i] = 0.0052
            continue

        else:
            continue
    #global rate
    #j = False
    #if j == False:
        #j = True
    global rate
    for i in range(len(dfnew)):
        #dfnew['shelflife'].iloc[i] = 15
        if dfnew['temperature'].iloc[i] in range(10, 15):
            # print("true")
            dfnew['price'].iloc[i] = 15

            dfnew['shelflife'].iloc[i] = rate - 0.5
        elif dfnew['temperature'].iloc[i] in range(15, 20):
            dfnew['price'].iloc[i] = 14.5
            dfnew['shelflife'].iloc[i] = rate - 0.5
        elif dfnew['temperature'].iloc[i] in range(20, 25):
            dfnew['price'].iloc[i] = 14
            dfnew['shelflife'].iloc[i] = rate - 1
        elif dfnew['temperature'].iloc[i] in range(25, 30):
            dfnew['price'].iloc[i] = 11
            dfnew['shelflife'].iloc[i] = rate - 1.5
        elif dfnew['temperature'].iloc[i] in range(30, 35):
            dfnew['price'].iloc[i] = 10
            dfnew['shelflife'].iloc[i] = rate - 2
        elif dfnew['temperature'].iloc[i] in range(35, 40):
            dfnew['price'].iloc[i] = 8
            dfnew['shelflife'].iloc[i] = rate - 2.5
        elif dfnew['temperature'].iloc[i] in range(40, 45):
            dfnew['price'].iloc[i] = 6
            dfnew['shelflife'].iloc[i] = rate - 3
        rate = dfnew['shelflife'].iloc[i]
    return dfnew
    #return dfnew


# In[13]:


#newframefinal()


# In[14]:


def createdatabase():
    dfnew1 = dfnew[['Time','temperature','ItemName','price']]
    conn = sqlite3.connect('sense8.db')
    cursor = conn.cursor()
    print("Opened database successfully")
    try:
        dfnew1.to_sql('producttable', conn)
        dfnew.to_sql('sensortablefinalnew1',conn)


    except ValueError:
        print('already exists')
    sql = ''' INSERT INTO sensortablefinalnew1(ProductID,Time,temperature,ItemName,price,shelflife,calories,cholestrol_in_mg,pottasium,protiens,vitamin_A,vitamin_C,Calcium,Iron)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    #cur = conn.commit()
    #cur = conn.cursor()
    sql2 = ''' INSERT INTO producttable(ProductID,Time,temperature,ItemName,price)
                  VALUES(?,?,?,?,?)'''
    conn.executemany(sql, dfnew.to_records(index=True,))
    conn.executemany(sql2, dfnew1.to_records(index=True, ))
    conn.commit()
    global dfsql
    dfsql = pd.read_sql_query("SELECT * FROM sensortablefinalnew1", conn)
    conn.close()
    dfsql.to_excel("cfscnew.xls")
    client = storage.Client()
    bucket = client.get_bucket('123iof')
    bucket.blob("newcfsc.xls")
    blob = bucket.blob('updatedcfsc.xls')
    with open('cfscnew.xls', 'rb') as csv:
        blob.upload_from_file(csv)

    return dfsql


# In[15]:


#createdatabase()


# In[23]:


def price(result):
    client = storage.Client()
    bucket = client.get_bucket('123iof')
    bucket.blob("updatedcsfc.xls")
    dfne = pd.read_excel('gs://123iof/updatedcfsc.xls')
    dfne = pd.DataFrame(dfne)
    dfne['ProductID'] = dfne["ProductID"].astype(str)
    currentdt = datetime.datetime.now()

    #serial_obj.close()
    global newlocdf
    newlocdf =  dfne.loc[dfne['ProductID'] == str(result)]
    time = newlocdf['Time'].values
    temp = newlocdf['temperature'].values
    layout = go.Layout(title='Days vs Temperature', xaxis=dict(title='Days'), yaxis=dict(title='Temperature'))
    trace = go.Scatter(x=time, y=temp)

    data = [trace]

    fig = go.Figure(data=data, layout=layout)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def table():
    global dfn
    dfn = newlocdf.iloc[:,:5]
    layout = go.Layout(title='Products stats', xaxis=dict(title='Days'), yaxis=dict(title='Temperature'))
    trace = go.Table(
        header=dict(values=list(['ProductID','Time','temperature','ItemName']),
                    fill=dict(color='#228B22'),
                    align=['left'] * 5),
        cells=dict(values=[dfn.ProductID, dfn.Time, dfn.temperature, dfn.ItemName],
                   fill=dict(color='#F5F8FF'),
                   align=['left'] * 5))

    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON1
def tableshelf():
    global dfn
    dfn = newlocdf.iloc[:,:7]
    layout = go.Layout(title='Products stats', xaxis=dict(title='Days'), yaxis=dict(title='Temperature'))
    trace = go.Table(
        header=dict(values=list(['ProductID','Time','temperature','ItemName','price','shelflife']),
                    fill=dict(color='#228B22'),
                    align=['left'] * 5),
        cells=dict(values=[dfn.ProductID, dfn.Time, dfn.temperature, dfn.ItemName,dfn.price,dfn.shelflife],
                   fill=dict(color='#F5F8FF'),
                   align=['left'] * 5))

    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON2

#price()

