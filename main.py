from time import sleep
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

def setup():
    """This runs when the code runs for the first time. It loads the machine learning model
    and reads and sets up the alarms from the database.
    """
    #load model TODO: michelle write command
    refresh()
    
def refresh():
    """This syncs the pi with the alarms on the database
    """
    #TODO: eran write this


setup()
while True:
    #check alarm
    sleep(1)