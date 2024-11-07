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

logged = False
uname = "" #THESE NEED TO BE UPDATED AFTER LOGGING IN TO TRUE AND THE USERNAME OF THE PERSON WHO LOGGED IN

@app.route("/")
def disp_homepage():
    #will know whether you are logged in or not and will allow you to edit
    #and view posts if you are logged in
    rentry1 = getRandomEntry()
    blogname1, title1, entry1, date1 = rentry1
    
    rentry2 = getRandomEntry()
    blogname2, title2, entry2, date2 = rentry2
    
    rentry3 = getRandomEntry()
    blogname3, title3, entry3, date3 = rentry3
    
    rentry4 = getRandomEntry()
    blogname4, title4, entry4, date4 = rentry4
    
    rentry5 = getRandomEntry()
    blogname5, title5, entry5, date5 = rentry5

    if logged:
        myEntry = getMostRecentEntry(uname)
        myBlogname, myTitle, myText, myDate = myEntry
    return render_template("homepage.html", myTitle=myTitle, title1=title1, title2=title2, title3=title3, title4=title4, title5=title5)

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

@app.route("/create", methods=['GET', 'POST'])
def signup():
    if username and password:
        existing_user = getPass(username)
        if existing_user:
            return render_template('create.html', error="Username already exists") 
        addUser(username, password)
        session['username'] = username  
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')

'''
@app.route("/blogs")
def blog():
    # add data to the page here from the database
    return render_template('blogs.html') #there will be more than just "blog.html" here
'''
@app.route("/thisBlog")
def thisBlog():
    thisTitle = request.args.get('title')
    thisEntry = getEntry(thisTitle)
    blogname, entry, date = thisEntry
    return render_template('thisBlog.html', bname=blogname, dat=date, Title=thisTitle, txt=entry)

@app.route("/edit")
def edit():
    thisTitle = request.args.get('title')
    thisEntry = getEntry(thisTitle)
    blogname,entry,date = thisEntry
    return render_template('edit.html', bname=blogname, dat=date, Title=thisTitle, txt=entry)

@app.route("/submit", methods=['GET"])
def submitEntry():
    nextTitle = request.args.get('newTitle')
    nextText = request.args.get('newText')
    nextDate = request.args.get('newDate')
    myEntry = getMostRecentEntry(uname)
    myBlogname, myTitle, myText, myDate = myEntry
    addEntry(myBlogname, nextTitle, nextText, nextDate)
    return render_template('thisBlog.html', bname=myBlogname, dat=nextDate, Title=nextTitle, txt=nextText)


if __name__ == "__main__":
    app.debug = True 
    app.run()
