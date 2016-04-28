from flask import render_template
from app import app
from 

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Alex'}
	return render_template('index.html', title='Dank memer', user=user)

@app.route('graphs')
def graphs():
