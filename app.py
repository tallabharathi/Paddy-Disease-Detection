#app.py
import os
from uuid import uuid4
from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import seaborn as sns
import cv2
import random as rand
import mysql.connector
from PIL import Image
from pylab import *
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.inception_v3 import preprocess_input
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route('/registration')
def registration():
    return render_template("ureg.html", msg='Successfully Registered!!')

@app.route('/adminhome')
def adminhome():
    return render_template("adminhome.html", msg='Successfully Registered!!')

@app.route('/admin')
def admin():
    return render_template("admin.html", msg='Successfully Registered!!')

@app.route('/adminlog', methods=['POST', 'GET'])
def adminlog():
    if request.method == "POST":
        username = request.form['uname']
        password1 = request.form['pass']
        if username == 'admin' and password1 == 'admin':
            return render_template('adminhome.html', msg="Login Success")
        else:
            return render_template('admin.html', msg="Login Failure!!!")
    return render_template('admin.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/userlog', methods=['POST', 'GET'])
def userlog():
    if request.method == "POST":
        email = request.form['email']
        password1 = request.form['pass']
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="facial_diagnosis")
        cursor = mydb.cursor()
        sql = "select * from ureg where email='%s' and pass='%s'" % (email, password1)
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            return render_template('userhome.html', msg="Login Success")
        else:
            return render_template('user.html', msg="Login Failure!!!")
    return render_template('user.html')

@app.route('/uregback', methods=['POST','GET'])
def uregback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pass']
        addr = request.form['addr']
        ph = request.form['ph']
        dob = request.form['dob']
        gender = request.form['gender']
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="facial_diagnosis")
        mycursor = mydb.cursor()
        sql = "INSERT INTO ureg (name,email,pass,dob,addr,ph,gender) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (name, email, pwd, dob, addr, ph, gender)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('user.html', msg="registered successfully")

@app.route('/userhome')
def userhome():
    return render_template("userhome.html", msg='Successfully logined!!')

@app.route('/upload1')
def upload1():
    return render_template("upload.html")

@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == 'POST':
        m = int(request.form['alg'])
        acc = pd.read_csv("Acc1.csv")
        myfile = request.files['file']
        fn = myfile.filename
        mypath = os.path.join('images/', fn)
        myfile.save(mypath)
        print("Uploaded file:", fn)
        # Add model prediction logic here
        return "Prediction code not included yet"

if __name__ == '__main__':
    app.run(debug=True)
