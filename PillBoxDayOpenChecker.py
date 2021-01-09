from spidev import SpiDev
from time import sleep
from gpiozero import LED

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


#constants
DayNames = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
DaysInWeek = 7
TodayDay = 5 #hard coded the day in order of the days in the pill box (start at 0)

#Variables
DayValues=[0]*DaysInWeek
DayStatus=[0]*DaysInWeek
DayDesired = [0]*DaysInWeek
Correct = False

#Objects
adc = MCP3008()
lSun = LED(24)
lMon = LED(23)
lTue = LED(22)
lWed = LED(27)
lThu = LED(18)
lFri = LED(17)
lSat = LED(4)
DayLEDS = [lSun,lMon,lTue,lWed,lThu,lFri,lSat]

DayDesired[TodayDay] = 1
DayLEDS[TodayDay].on()

while Correct is False:
    daysSum = 0
    
    # Scanning all the day channels for their values and sum 
    for i in range(DaysInWeek):
        DayValues[i] = adc.read( channel = i) 
        #print(DayNames[i] + ': ' + str(DayValues[i]))
        daysSum = daysSum + DayValues[i]

    # Determaining if the days are opened or closed
    for i in range(DaysInWeek):
        dayAve = (daysSum - DayValues[i])/(DaysInWeek -1)
        # larger than allowed means bright and open
        if DayValues[i] > dayAve + 100:
            DayStatus[i] = 1
        else:
            DayStatus[i] = 0

    print(DayStatus)
    
    for i in range(DaysInWeek):
        if DayStatus[i] != DayDesired[i]:
            break
        if i == DaysInWeek-1:
            Correct = True
            DayLEDS[TodayDay].off()
            
    sleep(0.2)
    

print('Correct')