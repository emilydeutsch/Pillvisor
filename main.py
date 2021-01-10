import schedule
import time
import threading

import firebase_admin
from firebase_admin import credentials,firestore

def alarmActuated(name):
    """This in the main function that runs when an alarm occurs

    Args:
        name (string): the name of the pill
    """
    displayPillName(name)
    checkPillBox(name)
    correctPillScanned = False
    while correctPillScanned is False:
        captureImage()
        cnnName = runPillRecognition()
        correctPillScanned = checkRecognition(cnnName,name)
    alarmFinish()




def displayPillName(name):
    """displays the name on LCD

    Args:
        name (string): the name of the pill
    """

def checkPillBox(name):
    """This function checks lights up the correct led for the day and rings buzzer. 
        It checks that the correct day is open and alerts user if wrong. This function
        does not return untill the correct box has been opened

    Args:
        name (string): name of pill
    """
    #TODO: dana this is you

def captureImage():
    """This function waits for the button press and takes a jpg picture (250x250) with the pi 
        camera and saves it to location 
    """
    waitForCameraButtonPress()
    #take picture

def waitForCameraButtonPress():
    """This function busy waits for button to be pressed. When it is pressed the camera
        will take a picture
    """

def runPillRecognition():
    """This function runs a CNN that recognises the pill. It gets the latest image from a fixed
        path on the pi.

        Returns: (string) name of the predicted pill or empty string if not recognised
    """
    #TODO: michelle this is you

def checkRecognition(cnnName,actualName):
    """Checks if the two inputted names are the same. If wrong it alerts the user and returns false

    Args:
        cnnName (string): the name produced by the CNN

        actualName (string): the actual name of the pill that needs to be taken

    Returns: True if the names match and false if incorrect 
    """
def alarmFinish():
    """clears all outstanding LEDs and and LCD display
    """

def setup(userID):
    """This runs when the code runs for the first time. It loads the machine learning model
    and reads and sets up the alarms from the database.
    
    Args:
        userID (string): the id of the user
    """
    #load model TODO: michelle write command
    refresh(userID)

def getFirebaseData(userID):
    """
    This gets the data from the Firebase database and converts it to a readable dictionary
    
    Args:
        userID (string): the id of the user
    """
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    ourDatabase = firestore.client()  
    collection = ourDatabase.collection('pillboxes')
    doc = collection.document(userID)
    userInfo = doc.get().to_dict()
    userAlarms = userInfo['alarms']
    
    return userAlarms    
    
def refresh(userID):
    """This syncs the pi with the alarms on the database
    
    Args:
        userID (string): the id of the user
    """
    userAlarms = getFirebaseData(userID)

    

    for alarm in userAlarms:
        #print(alarm['name']+ " " +str(alarm['hour']) + ":" + str(alarm['minute']) + str(alarm['days']))

        pillName = alarm['name']
        hour = alarm['hour']
        minute = alarm['minute']
        days = alarm['days']


        
        if (int(hour) < 10):
            if (int(minute) < 10):
                alarmTime = "0" + str(hour) + ":0" + str(minute)
            else:
                alarmTime = "0" + str(hour) + ":" + str(minute)
        else:
            if (int(minute) < 10):
                alarmTime = str(hour) + ":0" + str(minute)
            else:
                alarmTime = str(hour) + ":" + str(minute)
        


        if (days[0] == 1):
            schedule.every().sunday.at(alarmTime).do(alarmActuated, pillName)
        if (days[1] == 1):
            schedule.every().monday.at(alarmTime).do(alarmActuated, pillName)
        if (days[2] == 1):
            schedule.every().tuesday.at(alarmTime).do(alarmActuated, pillName)
        if (days[3] == 1):
            schedule.every().wednesday.at(alarmTime).do(alarmActuated, pillName)
        if (days[4] == 1):
            schedule.every().thursday.at(alarmTime).do(alarmActuated, pillName)
        if (days[5] == 1):
            schedule.every().friday.at(alarmTime).do(alarmActuated, pillName)
        if (days[6] == 1):
            schedule.every().saturday.at(alarmTime).do(alarmActuated, pillName)

currentID = '1234'

setup(currentID)
while True:
    schedule.run_pending()
    time.sleep(1)
    print(schedule.idle_seconds())
