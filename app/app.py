import os
from build_db import *
from flask import Flask, render_template, request, session, redirect
import sqlite3   # Enable control of an sqlite database
import csv       # Facilitate CSV I/O

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def disp_homepage():
    logged = 'username' in session
    uname = session.get('username', "")
    myBlogname = getBlogname(uname) if logged else None
    other_entries = []

    # Gather up to 5 random entries not authored by the logged-in user
    while len(other_entries) < 5:
        entry = getRandomEntry()
        if entry and entry[0] != myBlogname:  # Check if entry exists and is not from the user's blog
            other_entries.append(entry)

    return render_template(
        "homepage.html",
        logged=logged,
        uname=uname,
        other_entries=other_entries  # Pass these entries to the template
    )

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
    if request.method == 'POST':  # Check if the form was submitted
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            existing_user = getPass(username)  # Check if the user already exists
            if existing_user:
                return render_template('create.html', error="Username already exists") 
            addUser(username, password)  # Add new user to the database
            session['username'] = username  # Log the user in automatically
            return redirect("/")  # Redirect to the homepage after successful signup
        else:
            return render_template('create.html', error="Please provide both a username and a password")
    
    # Render the signup page on GET request
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
    
    # For GET request, render the edit form (no post data yet)
    return render_template('edit.html', bname=session.get('username', 'example_blog_name'), dat='2024-11-07')

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
