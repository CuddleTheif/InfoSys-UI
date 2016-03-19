import flask
import requests
import re
import sys
import json

url = 'http://infosys.csh.rit.edu:5000/'
app = flask.Flask(__name__)
app.secret_key = ''

@app.route('/clear', methods=['GET'])
def clearSessionPage():
	deleteKey()
	clearSession()
	print('cleared!', file=sys.stderr)
	return flask.redirect(flask.url_for("createMessagePage"))

@app.route('/', methods=['GET'])
def createMessagePage():
	if 'done' in flask.session and flask.session['done']:
		return flask.redirect(flask.url_for("createdMessagePage"))
	if 'text' in flask.session:
		return flask.render_template('createMessage.html', texts=flask.session['text'])
	return flask.render_template('createMessage.html')
	
@app.route('/done', methods=['GET'])
def createdMessagePage():
	if 'key' in flask.session:
		flask.session['done'] = True
		return flask.render_template('createdMessage.html', texts=flask.session['text'], modes=flask.session['mode'], key=flask.session['key'])
	return flask.redirect(flask.url_for("createMessagePage"))

@app.route('/delete', methods=['GET'])
def deleteKeyPage():
	return flask.render_template('deleteKey.html')
	
@app.route('/reload', methods=['GET'])
def reloadServer():
	requests.put(url+"reboot")
	return flask.redirect(flask.url_for("createMessagePage"))
	
@app.route('/delete', methods=['POST'])
def deleteKey():
	response = requests.delete(url + 'spaces', headers={'X-INFOSYS-KEY' : flask.request.form['key']})
	result = str(response.status_code)
	if(response.status_code<200 or response.status_code>299):
		result += " : "+response.json()['reason']
	return flask.render_template('deleteKey.html', message=result)

@app.route('/message', methods=['POST'])
def createMessage():
	if 'text' not in flask.session:
		deleteKey()
		createSession()
	
	if flask.request.form['submit']=="Add Line":
		flask.session['text'].append(flask.request.form['text'])
		flask.session['mode'].append(flask.request.form['mode'])
		flask.session['finalText'].append(convertText(flask.request.form['text']))
		return flask.redirect(flask.url_for("createMessagePage"))
	response = requests.post(url + 'spaces', data=json.dumps({'count':int(flask.session['numFiles'])+len(flask.session['finalText'])}))
	if(response.status_code<200 or response.status_code>299):
		print(response.json()['reason'], file=sys.stderr)
		clearSession()
		return flask.redirect(flask.url_for("createMessagePage"))
	print(response.json()['userKey'], file=sys.stderr)
	flask.session['key'] = response.json()['userKey']
	for i in range(len(flask.session['finalText'])):
		response = requests.post(url+'spaces/'+str(i+flask.session['numFiles'])+'/text', data=json.dumps({'text': flask.session['finalText'][i], 'mode': flask.session['mode'][i]}), headers={'X-INFOSYS-KEY':flask.session['key']})
	print(response.status_code, file=sys.stderr)
	if(response.status_code<200 or response.status_code>299):
		print(response.json()['reason'], file=sys.stderr)
	return nextFilePage()
		
@app.route('/image', methods=['GET'])
def createImagePage():
	return flask.render_template('createImage.html', name=getKey(flask.session['counter'], flask.session['pictures']), texts=flask.session['text'], modes=flask.session['mode'])
		
@app.route('/string', methods=['GET'])
def createStringPage():
	return flask.render_template('createString.html', name=getKey(flask.session['counter'], flask.session['strings']), texts=flask.session['text'], modes=flask.session['mode'])

@app.route('/image', methods=['POST'])
def createImage():
	if 'key' in flask.session:
		print("pic:"+str(flask.session['counter'])+":"+getKey(flask.session['counter'], flask.session['pictures']), file=sys.stderr)
		response = requests.post(url + 'spaces/' + str(flask.session['counter']) + '/picture', data=json.dumps({'height' : int(flask.request.form['height']), 'width' : int(flask.request.form['width']), 'dots' : flask.request.form['image'].split(',')}), headers={'X-INFOSYS-KEY':flask.session['key']})
		print(response.status_code, file=sys.stderr)
		if(response.status_code<200 or response.status_code>299):
			print(response.json()['reason'], file=sys.stderr)
		return nextFilePage()
	return flask.redirect(flask.url_for("createMessagePage"))
		
@app.route('/string', methods=['POST'])
def createString():
	if 'key' in flask.session:
		print("string:"+str(flask.session['counter'])+":"+getKey(flask.session['counter'], flask.session['strings']), file=sys.stderr)
		response = requests.post(url + 'spaces/' + str(flask.session['counter']) + '/string', data=json.dumps({'string' : flask.request.form['string']}), headers={'X-INFOSYS-KEY':flask.session['key']})
		print(response.status_code, file=sys.stderr)
		if(response.status_code<200 or response.status_code>299):
			print(response.json()['reason'], file=sys.stderr)
		return nextFilePage()
	return flask.redirect(flask.url_for("createMessagePage"))

def nextFilePage():
	flask.session['counter']+=1
	if flask.session['counter']==flask.session['numFiles']:
		requests.put(url+"reboot")
		return flask.redirect(flask.url_for("createdMessagePage"))
	elif flask.session['counter'] in flask.session['strings'].values():
		return flask.redirect(flask.url_for("createStringPage"))
	else:
		return flask.redirect(flask.url_for("createImagePage"))
		
def deleteKey():
	if 'key' in flask.session:
		response = requests.delete(url + 'spaces', headers={'X-INFOSYS-KEY' : flask.session['key']})
		clearSession()
		if(response.status_code<200 or response.status_code>299):
				print(response.json()['reason'], file=sys.stderr)
		print('deleted!', file=sys.stderr)

def clearSession():
	flask.session.pop('key', None)
	flask.session.pop('text', None)
	flask.session.pop('mode', None)
	flask.session.pop('pictures', None)
	flask.session.pop('strings', None)
	flask.session.pop('numFiles', None)
	flask.session.pop('counter', None)
	flask.session.pop('finalText', None)
	flask.session.pop('done', None)
	
def createSession():
	flask.session['text'] = []
	flask.session['mode'] = []
	flask.session['finalText'] = []
	flask.session['strings'] = {}
	flask.session['pictures'] = {}
	flask.session['numFiles'] = 0
	flask.session['counter'] = -1
	flask.session['done'] = False

def convertText(text):
	text = re.sub(r"\\(?:p|P){(.+?)}", infosysFilePicture, text)
	text = re.sub(r"\\(?:s|S){(.+?)}", infosysFileString, text)
	print(text, file=sys.stderr)
	return text

def infosysFileString(match):
	if match.group(1) not in flask.session['strings']:
		flask.session['strings'][match.group(1)] = flask.session['numFiles']
		flask.session['numFiles']+=1
	print("string:"+str(flask.session['strings'][match.group(1)])+":"+match.group(1), file=sys.stderr)
	return "<STRINGFILE:"+str(flask.session['strings'][match.group(1)])+">"

def infosysFilePicture(match):
	if match.group(1) not in flask.session['pictures']:
		flask.session['pictures'][match.group(1)] = flask.session['numFiles']
		flask.session['numFiles']+=1
	print("pic:"+str(flask.session['pictures'][match.group(1)])+":"+match.group(1), file=sys.stderr)
	return "<PICTUREFILE:"+str(flask.session['pictures'][match.group(1)])+">"
	
def getKey(index, dict):
	return list(dict.keys())[list(dict.values()).index(index)]

if __name__ == '__main__':
    app.run(debug=True)