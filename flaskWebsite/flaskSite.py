import time
from flask import Flask, url_for, render_template
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


app = Flask(__name__)
@app.route('/')
def index():
    return 'Please go to /profile/UserID'

#@app.route('/login')
#def login():
#    return 'login'
#
#@app.route('/user/<username>')
#def profile(username):
#    return '{}\'s profile'.format(escape(username))

@app.route('/profile/')
@app.route('/profile/<userID>')
def profile(userID=None):
    userAlarms = getFirebaseData(userID)
    return render_template('flaskHTML.html', name=userAlarms, userAlarms = userAlarms)


if __name__ == "__main__":
    app.run(debug=True)
