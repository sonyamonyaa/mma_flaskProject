import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
app.config['SECRET_KEY'] =  os.environ.get("SECRET_KEY")
from project import routes
