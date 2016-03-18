import flask
import requests
import json
import argparse
import time
import re

key = ''
url = 'http://infosys.csh.rit.edu:5000"
app = flask.Flask(__name__)
app.secret_key = ''

@app.route('/', methods=['GET'])
def homePage():
	

@app.route('/image', methods=['GET'])
def editImagePage():
	#if 'username' in session:
		return flask.render_template('editImage.html')
	#else:
	#	return flask.redirect(flask.url_for("homePage"))

@app.route('/image', methods=['POST'])
def editImage():
	#if 'username' in session:
		return flask.render_template('editImage.html')
	#else:
	#	return flask.redirect(flask.url_for("homePage"))

@app.route('/text', methods=['GET'])
def editTextPage():
	#if 'username' in session:
		return flask.render_template('editText.html')
	#else:
	#	return flask.redirect(flask.url_for("homePage"))

@app.route('/text', methods=['POST'])
def editText():
	#if 'username' in session:
		response = requests.post(url+'/spaces/' + flask.request.form['space'] + '/text', data=json.dumps({'text': flask.request.form['text'], 'mode':flask.request.form['mode']}), headers={'X-INFOSYS-KEY':key})
		return flask.redirect(flask.url_for("editTextPage"))
	#else:
	#	return flask.redirect(flask.url_for("homePage"))

if __name__ == '__main__':
    app.run(debug=True)