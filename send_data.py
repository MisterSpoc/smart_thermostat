import RPi.GPIO as GPIO
import time
from datetime import datetime

def gpioSetup():

    numList = getSettings()

    clockPin = numList[0]
    dataPin = numList[1]
    #thermoPin = numList[]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clockPin, GPIO.OUT)
    GPIO.setup(dataPin, GPIO.OUT)
    #GPIO.setup(thermoPin, GPIO.IN)

    GPIO.output(clockPin, GPIO.LOW)
    return clockPin, dataPin, numList

def getSettings():
    settings = open("/var/www/html/settings.txt", "r")

    numList = list()

    for x in settings.readlines():
        if " " in x:
            numList.extend([int(y) for y in x.split() if y.isdigit()])

    settings.close()
    return numList

def TxtToBinary(testString, clockPin, dataPin):
    sleep_time = 0.01 #wait time in s
    testBinary =' '.join(format(ord(x), 'b').zfill(8) for x in testString) #convert string to string of binary representation
    testBinary = testBinary + " 00000000" #add binary "null" to end of binary expression to signify end of transmission
    print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending " + testBinary)
    #with open("log.txt", "a") as myfile:
        #myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending " + testBinary + "\n")
            
    for char in testBinary:
        GPIO.output(dataPin, GPIO.LOW)
        try:
            if int(char)==1:
                GPIO.output(dataPin, GPIO.HIGH)
        #clock cycle happens here, outside of except as that signifies a space between characters and no data
            time.sleep(0.0001)
            GPIO.output(clockPin, GPIO.HIGH)
            time.sleep(sleep_time)
            GPIO.output(clockPin, GPIO.LOW)
            time.sleep(sleep_time)

        except:
            time.sleep(0.01)

def main(testString):
    clockPin, dataPin, numList = gpioSetup()
    TxtToBinary(testString, clockPin, dataPin)
    GPIO.cleanup(numList[0])
    GPIO.cleanup(numList[1])
    