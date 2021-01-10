import schedule
import time
import threading
import datetime

import firebase_admin
from firebase_admin import credentials,firestore

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from spidev import SpiDev
from time import sleep
from gpiozero import LED, Button
from picamera import PiCamera
import RPi.GPIO as GPIO

import tensorflow as tf

from os import listdir
from os.path import isfile, join

import cv2
import numpy as np
from matplotlib import pyplot as plt

conv_model = tf.keras.models.load_model("hackathoncnn")

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
    lcd.message = name
    pwm.start(1)
    pwm.ChangeFrequency(300)
    
def checkPillBox(name):
    """This function checks lights up the correct led for the day and rings buzzer. 
        It checks that the correct day is open and alerts user if wrong. This function
        does not return untill the correct box has been opened

    Args:
        name (string): name of pill
    """
    #constants
    global DaysInWeek
    DaysInWeek = 7
    TodayDay = int(datetime.datetime.today().strftime('%w')) #hard coded the day in order of the days in the pill box (start at 0)

    #Variables
    DayValues=[0]*DaysInWeek
    DayStatus=[0]*DaysInWeek
    DayDesired = [0]*DaysInWeek
    Correct = False

    #Set correct LED and display message
    DayDesired[TodayDay] = 1
    lcd.cursor_position(0,1)
    lcd.message = 'Open Correct Day'
    print('Open Correct Day')
    DayLEDS[TodayDay].on()

    while Correct is False:
        daysSum = 0
        
        # Scanning all the day channels for their values and sum 
        for i in range(DaysInWeek):
            DayValues[i] = adc.read( channel = i) 
            daysSum = daysSum + DayValues[i]

        # Determaining if the days are opened or closed
        for i in range(DaysInWeek):
            dayAve = (daysSum - DayValues[i])/(DaysInWeek -1)
            # larger than allowed means bright and open
            if DayValues[i] > dayAve + 100:
                DayStatus[i] = 1
            else:
                DayStatus[i] = 0

        #print(DayStatus) #for debugging
        
        #turning on error LED when incorrect
        if DayStatus == DayDesired:
            lError.off()
            pwm.stop()
            Correct = True
        elif DayStatus == [0]*DaysInWeek:
            lError.off()
            #pwm.stop()
        else :
            lError.on()
            pwm.start(1)
            pwm.ChangeFrequency(300)
        
        sleep(0.2)

def captureImage():
    """This function waits for the button press and takes a jpg picture (250x250) with the pi 
        camera and saves it to location 
    """
    lcd.cursor_position(0,1)
    lcd.message = 'Press To Capture'
    button.wait_for_press()
    camera.capture('testIm.jpg')    

def runPillRecognition():
    """This function runs a CNN that recognises the pill. It gets the latest image from a fixed
        path on the pi.

        Returns: (string) name of the predicted pill or empty string if not recognised
    """
    #may need to change these names
    pills = {0:"white pill",
             1:"orange pill",
             2:"yellow pill",
             3:"multicolour pill"}

    img = cv2.imread('testIm.jpg')

    dim = (250,250)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    cv2.imshow("resized",resized)
    cv2.waitKey(3)
    re_img = resized/255.0
    img_aug = np.expand_dims(re_img, axis=0)
    y_predict = conv_model.predict(img_aug)[0]
    indices = [i for i, x in enumerate(y_predict) if x == max(y_predict)]

    pred_val = indices[0]
    if y_predict[pred_val] > 0.5:
        pill_string = pills[pred_val]
    else:
        pill_string = ""



    return pill_string

def checkRecognition(cnnName,actualName):
    """Checks if the two inputted names are the same. If wrong it alerts the user and returns false

    Args:
        cnnName (string): the name produced by the CNN

        actualName (string): the actual name of the pill that needs to be taken

    Returns: True if the names match and false if incorrect 
    """
    lcd.clear()
    if cnnName == actualName:
        lcd.message = 'Correct Pill'
        return True
    else:
        lcd.message = 'Incorrect Pill'
        return False

def alarmFinish():
    """clears all outstanding LEDs and and LCD display
    """
    for i in range(DaysInWeek):
        DayLEDS[i].off()
    sleep(2)
    lcd.clear()

def setup(userID):
    """This runs when the code runs for the first time. It loads the machine learning model
    and reads and sets up the alarms from the database.
    
    Args:
        userID (string): the id of the user
    """
    #load model 
    refresh(userID)

    # LCD object
    lcd_rs = digitalio.DigitalInOut(board.D5)
    lcd_en = digitalio.DigitalInOut(board.D6)
    lcd_d4 = digitalio.DigitalInOut(board.D12)
    lcd_d5 = digitalio.DigitalInOut(board.D13)
    lcd_d6 = digitalio.DigitalInOut(board.D19)
    lcd_d7 = digitalio.DigitalInOut(board.D16)
    lcd_columns = 16
    lcd_rows = 2

    global lcd
    lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                        lcd_d7, lcd_columns, lcd_rows)

    global adc
    adc = MCP3008()
    
    global camera
    camera = PiCamera()
    camera.resolution = (250, 250)
    
    #all LEDS
    lSun = LED(24)
    lMon = LED(23)
    lTue = LED(22)
    lWed = LED(27)
    lThu = LED(18)
    lFri = LED(17)
    lSat = LED(4)
    global DayLEDS
    DayLEDS = [lSun,lMon,lTue,lWed,lThu,lFri,lSat]
    global lError
    lError = LED(26)
    
    #button for sync and for picture 
    global button
    button = Button(3)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)

    global pwm
    pwm = GPIO.PWM(20, 0.5)
    
def getFirebaseData(userID):
    """
    This gets the data from the Firebase database and converts it to a readable dictionary
    
    Args:
        userID (string): the id of the user
    """
    cred = credentials.Certificate("serviceAccountKey.json")
    a = firebase_admin.initialize_app(cred)

    ourDatabase = firestore.client()  
    collection = ourDatabase.collection('pillboxes')
    doc = collection.document(userID)
    userInfo = doc.get().to_dict()
    userAlarms = userInfo['alarms']

    firebase_admin.delete_app(a)
    
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

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()

currentID = '1234'

setup(currentID)
while True:
    schedule.run_pending()
    if button.is_pressed: 
        refresh()
    sleep(1)
    lcd.clear()

