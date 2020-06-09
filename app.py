
from flask import Flask, request,url_for, render_template
import _sqlite3 as sql
import models as dbHandler

import sys
import re
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import config
import cgi
import timestamp
import sensor
import requests
from timestamp import SimpleMess
from forms import LoginForm
from sensor import table
import io
from sensor import create_serial_obj, clean_serial_data, read_serial_data, newframefinal,createdatabase,price
from flask import make_response

#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask_wtf import FlaskForm
import pandas as pd
from flask import jsonify,json
import requests
import cgi
import urllib.request
#import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
#import matplotlib
#import matplotlib.pyplot as plt
portPath = "COM3"
from sensor import serial_obj
baud = 38400
timeout = 15
rate = 15
#filename = "data.csv"
#max_num_readings = 5
#num_signals = 1
#str1 = input("Enter Product ID: ");
#str2 = input("Enter Item Name:  ")
app = Flask(__name__)
config.Config()
import os
from sensor import read,clean
#from bs4 import BeautifulSoup
# import matplotlib.pyplot as plt
#from graphical import crabGraph
import timestamp
from timestamp import RetrievingTime
from sensor import tableshelf
#serial_obj.close()
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
@app.route('/new',methods=['GET', 'POST'])
def home():
    #if request == 'GET':
    #json.dumps(data2)
   # get = requests.get('http://search.html/timestable')
    #request.__getattribute__('timestable')
    #RetrievingTime()
    return render_template('/SearchProduct.html/')

@app.route('/SearchProduct.html/',methods=['GET', 'POST'])
def searchButton():

    #alt = RetrievingTime()
    if request.method == 'POST':
        global result
        result = request.form['fooput']
        return redirect('/ProductDetail.html/')
        #print(result)
        #serial_obj = create_serial_obj(portPath, baud, timeout)
        #serial_data = read_serial_data(serial_obj)
        #clean_data = clean_serial_data(serial_data)
        #j = newframefinal(clean_data)
        #r = createdatabase()
        #p = price()

        #z = crabGraph(result)
        #return render_template('/SearchProduct.html', z = p)


    if request.method == 'GET':

        return render_template('/SearchProduct.html')


    #print(result)
    #soup = BeautifulSoup(open('templates/SearchProduct.html'), 'lxml')
    #value = soup.find('input', {'id': 'search'}).get('value')

    #print(value)
    #p = re.compile('\s+iframe.setAttribute("src",\s+"(.*)");')
    #all_script = soup.find_all("script", {"src": False})
    #for individual_script in all_script:
     #   all_value = individual_script.string
      #  if all_value:
       #     m = p.match(all_value)
    #        print(m)
            #soup = BeautifulSoup(open('templates/SearchProduct.html'), 'lxml')
    #input = soup.find(('input'),type = 'submit')
    #new = input.attrs['class']
    #print(new)
    # try:
    #     get = requests.post(' http://SearchProduct.html/mainSearch')
    # except requests.exceptions.RequestException as e:  # This is the correct syntax
    #     print(e)
    #     sys.exit(1)
    #
    # data = get.json()
    # print(data)
    #json.dumps(data2)
    #requests.post('http://search.html/')
    #RetrievingTime()
    # return Response(output.getvalue(), mimetype='image/png')
    return render_template('/SearchProduct.html/')#,alt = alt)
app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.route('/ProductDetail.html/')
def ProductDetail():
    print(result)
    print("Reading serial data...")
    read()
    cleand = clean()
    newframefinal(cleand)
    createdatabase()
    z = price(result)
    n = table()
    return render_template('/ProductDetail.html/',z = z,n = n)

@app.route('/ProductDetail.html/ShelfLifeManagement.html/')
def shelflifemanagement1():
    return redirect('/ShelfLifeManagement.html/')
@app.route('/ShelfLifeManagement.html/')
def shelflifemanagement():
    read()
    cleand = clean()
    newframefinal(cleand)
    createdatabase()
    price(result)
    h = tableshelf()
    return render_template('/ShelfLifeManagement.html',h = h)

@app.route('/login.html/')
def login():
    form = LoginForm()
    return render_template('/login.html/', title='login', form=form)
from flask import render_template, flash, redirect

@app.route('/', methods=['GET', 'POST'])
def login2():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.password.data))
        global new1
        new1=print(form.username.data)
        global new2
        new2=print(form.password.data)
        dbHandler.insertUser(form.username, form.password)
        global users
        users = dbHandler.retrieveUsers()
        return redirect('/SearchProduct.html/')

    return render_template('login.html', title='login', form=form)



if __name__ == '__main__':
    app.run(debug=False)
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    #options.setdefault('use_reloader', self.debug)

