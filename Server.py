import flask
import requests
import json
import argparse
import time
import re
import sys

key = 'd71ae24b-7c35-44d4-8b77-1b1eea6ec137'
url = 'http://infosys.csh.rit.edu:5000'
app = flask.Flask(__name__)
app.secret_key = ''

@app.route('/', methods=['GET'])
def createMessagePage():
	#if 'username' in session:
		return flask.render_template('createMessage.html')
	#else:
	#	return flask.redirect(flask.url_for("homePage"))

@app.route('/image', methods=['POST'])
def editImage():
	#if 'username' in session:
		response = requests.post(url + '/spaces/' + flask.request.form['space'] + '/picture', data=json.dumps({'height' : int(flask.request.form['height']), 'width' : int(flask.request.form['width']), 'dots' : flask.request.form['image'].split(',')}), headers={'X-INFOSYS-KEY':flask.request.form['key']})
		print(response.status_code, file=sys.stderr)
		if(response.status_code<200 or response.status_code>299):
			print(response.json()['reason'], file=sys.stderr)
		return flask.redirect(flask.url_for("createMessagePage"))
	#else:
	#	return flask.redirect(flask.url_for("homePage"))

@app.route('/text', methods=['POST'])
def editText():
	#if 'username' in session:
		response = requests.post(url+'/spaces/' + flask.request.form['space'] + '/text', data=json.dumps({'text': flask.request.form['text'], 'mode':flask.request.form['mode']}), headers={'X-INFOSYS-KEY':flask.request.form['key']})
		print(response.status_code, file=sys.stderr)
		if(response.status_code<200 or response.status_code>299):
			print(response.json()['reason'], file=sys.stderr)
		return flask.redirect(flask.url_for("createMessagePage"))
	#else:
	#	return flask.redirect(flask.url_for("homePage"))

if __name__ == '__main__':
    app.run(debug=True)