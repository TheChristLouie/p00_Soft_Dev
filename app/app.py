
import os
from build_db import *
from flask import Flask, render_template, request, session, redirect
import sqlite3   
import csv       

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def disp_homepage():
    rentry1 = getRandomEntry()
    if not rentry1[0]: 
        rentry1 = None
    rentry2 = getRandomEntry()
    if not rentry2[0]:  
        rentry2 = None
    rentry3 = getRandomEntry()
    if not rentry3[0]:  
        rentry3 = None
    rentry4 = getRandomEntry()
    if not rentry4[0]:  
        rentry4 = None
    rentry5 = getRandomEntry()
    if not rentry5[0]: 
        rentry5 = None
    entries = [rentry1, rentry2, rentry3, rentry4, rentry5]
    entries = [entry for entry in entries if entry is not None]  # Remove None entries
    myTitle, myBlogname, myText, myDate = "", "", "", ""  # Default values
    uname = ""
    if 'username' in session:
        logged = True
        uname = session['username']  # Assign uname if logged in
        myEntry = getMostRecentEntry(uname)
        if myEntry:
            myBlogname, myTitle, myText, myDate = myEntry
        else:
            myBlogname, myTitle, myText, myDate = "", "", "You have no entries yet.", ""  # Default message when no entries
    else:
        logged = False
    return render_template("homepage.html", 
                           myTitle=myTitle, 
                           entries=entries, 
                           no_entries_message=myText, 
                           logged=logged, 
                           uname=uname)




@app.route("/login")
def disp_loginpage():
    return render_template('login.html')

@app.route("/auth", methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    stored_password = getPass(username)
    if stored_password and stored_password[0] == password:
        session['username'] = username
        return redirect("/")
    return render_template('login.html', error="Invalid username or password")


@app.route("/create", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            existing_user = getPass(username)
            if existing_user:
                return render_template('create.html', error="Username already exists") 
            addUser(username, password) 
            session['username'] = username  
            return redirect("/")  
        else:
            return render_template('create.html', error="Please provide both a username and a password")
    return render_template('create.html')

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
def edit_post():
    if request.method == 'POST':
        newTitle = request.form.get('newTitle')
        newText = request.form.get('newText')
        newDate = request.form.get('newDate')
        if newTitle and newText and newDate:
            # Add the new post to the blog
            bname = session.get('username', 'example_blog_name')  # Use the logged-in user's name as blog name
            addEntry(bname, newTitle, newText, newDate)
            return redirect(f"/thisBlog?title={newTitle}")
        else:
            return render_template('edit.html', error="Please fill in all fields.")
    title = request.args.get('title')
    if title:
        thisEntry = getEntry(title)
        blogname, entry, date = thisEntry
        return render_template('edit.html', bname=session.get('username', 'example_blog_name'), dat=date, currentTitle=title, currentText=entry, currentDate=date)
    return render_template('edit.html', bname=session.get('username', 'example_blog_name'), dat='2024-11-07')
@app.route("/submit", methods=['GET', 'POST'])
def submitEntry():
    nextTitle = request.form.get('newTitle')
    nextText = request.form.get('newText')
    nextDate = request.form.get('newDate')
    if nextTitle and nextText and nextDate:
        myEntry = getMostRecentEntry(session['username'])
        myBlogname, myTitle, myText, myDate = myEntry
        addEntry(myBlogname, nextTitle, nextText, nextDate)
        return render_template('thisBlog.html', bname=myBlogname, dat=nextDate, Title=nextTitle, txt=nextText)
    return render_template('thisBlog.html', error="Please fill in all fields.")

if __name__ == "__main__":
    app.debug = True
    app.run()
