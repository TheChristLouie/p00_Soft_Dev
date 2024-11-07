import os
from build_db import *
from flask import Flask, render_template, request, session, redirect
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def disp_homepage():
    # Fetch random entries to display
    rentry1 = getRandomEntry() or (None, None, None, None)
    blogname1, title1, entry1, date1 = rentry1

    rentry2 = getRandomEntry() or (None, None, None, None)
    blogname2, title2, entry2, date2 = rentry2

    rentry3 = getRandomEntry() or (None, None, None, None)
    blogname3, title3, entry3, date3 = rentry3

    rentry4 = getRandomEntry() or (None, None, None, None)
    blogname4, title4, entry4, date4 = rentry4

    rentry5 = getRandomEntry() or (None, None, None, None)
    blogname5, title5, entry5, date5 = rentry5

    # Default values for blog-related data
    myTitle, myBlogname, myText, myDate = "", "", "", ""  # Default values

    # Check if logged in
    if 'username' in session:
        logged = True
        uname = session['username']
        myEntry = getMostRecentEntry(uname)
        if myEntry:
            myBlogname, myTitle, myText, myDate = myEntry  # Unpack the latest entry if it exists
    else:
        logged = False
    return render_template("homepage.html", myTitle=myTitle, title1=title1, title2=title2, title3=title3, title4=title4, title5=title5)


@app.route("/login")
def disp_loginpage():
    return render_template('login.html')

@app.route("/response", methods=['GET', 'POST'])
def authenticate():
    if(request.args.get('username') != None):
        session['username'] = request.args.get('username')
    return render_template('response.html', username=session['username'])

@app.route("/create", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # Check if the form was submitted
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            existing_user = getPass(username)
            if existing_user:
                return render_template('create.html', error="Username already exists") 
            addUser(username, password)
            session['username'] = username
            return redirect("/")  # Redirect to the homepage after successful signup
        else:
            return render_template('create.html', error="Please provide both a username and a password")
    return render_template('create.html')  # Render the sign-up page on GET request

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')

@app.route("/thisBlog")
def thisBlog():
    thisTitle = request.args.get('title')
    thisEntry = getEntry(thisTitle)
    blogname, entry, date = thisEntry
    return render_template('thisBlog.html', bname=blogname, dat=date, Title=thisTitle, txt=entry)

@app.route("/edit", methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        newTitle = request.form.get('newTitle')
        newText = request.form.get('newText')
        newDate = request.form.get('newDate')

        # Assuming bname is passed as part of the blog (you may want to update this logic)
        bname = 'example_blog_name'  # You can dynamically pass the blog name here

        # Add new entry to the database
        addEntry(bname, newTitle, newText, newDate)

        # Redirect to the newly created blog post page (or the blog overview page)
        return redirect(f"/thisBlog?title={newTitle}")
    
    # Render the page when visiting /create (GET request)
    return render_template('edit.html', bname='example_blog_name', dat='2024-11-07')

@app.route("/submit", methods=['GET', 'POST'])
def submitEntry():
    nextTitle = request.form.get('newTitle')
    nextText = request.form.get('newText')
    nextDate = request.form.get('newDate')

    if nextTitle and nextText and nextDate:
        # Fetch most recent entry details
        myEntry = getMostRecentEntry(session['username'])
        myBlogname, myTitle, myText, myDate = myEntry

        # Add the new entry
        addEntry(myBlogname, nextTitle, nextText, nextDate)

        return render_template('thisBlog.html', bname=myBlogname, dat=nextDate, Title=nextTitle, txt=nextText)

    # If any required fields are missing, return to the form with an error
    return render_template('thisBlog.html', error="Please fill in all fields.")

if __name__ == "__main__":
    app.debug = True
    app.run()
