import os
from flask import render_template, request
from project import app

# @app.route('/')
# def homepage():  # put application's code here
#     return render_template('home.html', title="MMA Home", head="Maximin Aware")
#
# @app.route('/divide-and-choose')
# def algo1():  # put application's code here
#     return render_template('algo1.html',title="MMA Divide and Choose", head="Divide and Choose")
#
# @app.route('/allocation-by-matching')
# def algo2():  # put application's code here
#     return render_template('algo2.html',title="MMA Allocation by Matching", head="Allocation by Matching")

@app.route('/', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join('the/path/to/save', f.filename))

    return render_template('base.html')
