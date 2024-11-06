# SexyMermaids
# SoftDev
# October 11, 2024
# 1

import os
from build_db import *
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def disp_homepage():
    #will know whether you are logged in or not and will allow you to edit
    #and view posts if you are logged in
    return render_template("homepage.html")

@app.route("/login")
def disp_loginpage():
    if 'username' in session:
        return redirect("response.html")
    return render_template( 'login.html' )

@app.route("/response" , methods=['GET','POST'])
def authenticate():
    if(request.args.get('username') != None):
        session['username'] = request.args.get('username')
    return render_template( 'response.html', username = session['username'])

@app.route("/create", methods=['GET','POST'])
def signup():
    if(request.args.get('username') != None):
        session['username'] = request.args.get('username')
        session['password'] = request.args.get('password')
    addUser(session['username']),(session['password'])
    return render_template( 'create.html', username = session['username'])
    

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')

'''
@app.route("/blogs")
def blog():
    # add data to the page here from the database
    return render_template('blogs.html') #there will be more than just "blog.html" here

@app.route("/thisblog")
def thisblog():
    # add data to this page based on which blog is selected, probably through an if statment
    # in other words, take data from the blog entry with the same title as the one that was clicked on
    return render_template('thisblog.html') #there will be more than just "thisblog.html" here
'''
    
if __name__ == "__main__":
    app.debug = True 
    app.run()