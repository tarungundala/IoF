#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from flask_wtf import FlaskForm
import pandas as pd
from flask import jsonify,json
import requests

df = pd.read_csv("cfsc.csv")
import cgi
import urllib.request
def SimpleMess():
    z = "shwaaa"
    #shwa ={'name': z}
    #z = jsonify(shwa)
    #datanew1 = pd.DataFrame(shwa,index=[0])
    #datanew2 = datanew1.to_json(datanew1)
    #print(type(z))
    #print(z)
    #urllib.request.urlopen("http://127.0.0.1:5000/")
    return requests.get("http://127.0.0.1:5000",data=z)



def RetrievingTime():
    #z = open("jnew.html",'a')

    time = df[df["Food Description"]=='crab'].iloc[:,2]
    data = {'time':time}
    data2 = pd.DataFrame(data)
    data2.to_html("time.html")
    #data2 = json.jsonify(data2)
    data3 = pd.read_html("time.html")
   # new = z.write("jnew.html")
    #data2.to_html("data.html")
    #data4 = json.dumps(data3)
    return data3
    #return requests.post('http://127.0.0.1:5000', data=data3.all())





#RetrievingTime()







