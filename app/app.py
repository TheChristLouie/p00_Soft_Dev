# SexyMermaids
# Death Row Coders
# SoftDev
# October 11, 2024
# 1

import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def disp_loginpage():
    if 'username' in session:
        return redirect("/response.html")
    return render_template( 'login.html' )

@app.route("/response.html" , methods=['GET','POST'])
def authenticate():
    if(request.args.get('username') != None):
        session['username'] = request.args.get('username')
    return render_template( 'response.html', username = session['username'])

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')
    
if __name__ == "__main__":
    app.debug = True 
    app.run()
