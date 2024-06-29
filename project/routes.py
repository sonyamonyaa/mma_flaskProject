from flask import render_template
from project import app

@app.route('/')
def homepage():  # put application's code here
    return render_template('home.html', title="Maximin Aware")

@app.route('/divide')
def algo1():  # put application's code here
    return render_template('home.html')
