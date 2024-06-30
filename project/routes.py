from flask import render_template
from project import app

@app.route('/')
def homepage():  # put application's code here
    return render_template('home.html', title="MMA Home", head="Maximin Aware")

@app.route('/divide-and-choose')
def algo1():  # put application's code here
    return render_template('algo1.html',title="MMA Divide and Choose", head="Divide and Choose")

@app.route('/allocation-by-matching')
def algo2():  # put application's code here
    return render_template('algo2.html',title="MMA Allocation by Matching", head="Allocation by Matching")
