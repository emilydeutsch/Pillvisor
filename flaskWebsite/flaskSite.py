import time
from flask import Flask, request, url_for, render_template, redirect
from markupsafe import escape

import firebase_admin
from firebase_admin import credentials,firestore


def getFirebaseData(userID):

    cred = credentials.Certificate("serviceAccountKey.json")
    a = firebase_admin.initialize_app(cred)

    ourDatabase = firestore.client()  
    collection = ourDatabase.collection('pillboxes')
    doc = collection.document(userID)
    userInfo = doc.get().to_dict()
    userAlarms = userInfo['alarms']

    firebase_admin.delete_app(a)
    
    return userAlarms 


def writeFirebaseData(name, hour, minute, days):
    cred = credentials.Certificate("serviceAccountKey.json")
    a = firebase_admin.initialize_app(cred)

    ourDatabase = firestore.client()  
    collection = ourDatabase.collection('pillboxes')
    doc = collection.document('1234')

    doc.update({
        'alarms': firestore.ArrayUnion([
            {"name": str(name),
            "hour": str(hour),
            "minute": str(minute),
            "days": days}

        ])
    })

    firebase_admin.delete_app(a)

def deleteFirebaseData(userID, i):
    cred = credentials.Certificate("serviceAccountKey.json")
    a = firebase_admin.initialize_app(cred)

    ourDatabase = firestore.client()  
    collection = ourDatabase.collection('pillboxes')
    doc = collection.document(userID)
    userInfo = doc.get().to_dict()
    userAlarms = userInfo['alarms']

    firebase_admin.delete_app(a)

    userAlarms.pop(int(i))

    doc.update({
        'alarms': userAlarms
    })

app = Flask(__name__)

@app.route('/')
def index():
    return 'Please go to /profile'

#@app.route('/login')
#def login():
#    return 'login'
#
#@app.route('/user/<username>')
#def profile(username):
#    return '{}\'s profile'.format(escape(username))


@app.route('/profile/')
def profile(userID='1234'):

    userAlarms = getFirebaseData(userID)
    return render_template('flaskHTML.html', userAlarms = userAlarms, writing = writeFirebaseData)

@app.route('/profile/', methods=['POST'])
def profile_post(userID='1234'):
    if request.form['hidden'] == "creating":
        name = request.form['name']
        hour = request.form['hour']
        minute = request.form['minute']

        writeFirebaseData(name, hour, minute, [1,1,1,1,1,1,1])
    else:
        deleteFirebaseData(userID, request.form['hidden'])
    
    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.run(debug=True)
