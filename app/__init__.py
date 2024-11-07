import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(32) #Session Key
    with app.app_context():
        from . import app  # Imports 'app.py'
    return app
