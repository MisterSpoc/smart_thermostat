import RPi.GPIO as GPIO
import time
from datetime import datetime

class UniversalVariables:
    is_recieving = False

def BinarytoTxt(clockPin, dataPin, lock):
    currentBit = ""
    message = ""
    bit_counter = 0
    end_message_checker = 0
    t1=0
    t2=0

    
    while True:
        message = message + str(currentBit)
 
        while not GPIO.input(clockPin):
            a=1
        lock.acquire()
        #print("setting universal variable True")
        UniversalVariables.is_recieving = True
        lock.release()
        bit_counter += 1
        
        if GPIO.input(dataPin):
            currentBit = 1
        else:
            currentBit = 0
            end_message_checker += 1
        while GPIO.input(clockPin):
            a=1
        #print("checking for end of message")
        t2 = time.time()
        
        if t2-t1 != t2:
            if t2-t1 >= 1:
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_data] Took too long to receive, force exiting")
                with open("/var/www/html/log.txt", "a") as myfile:
                    myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_data] Took too long to receive, force exiting\n")
                time.sleep(2)
                break

        t1 = time.time()
        
        if bit_counter%8 == 0:
            if end_message_checker == 8:
                break
            else:
                end_message_checker = 0
                bit_counter = 0
    print("\n")
    lock.acquire()
    UniversalVariables.is_recieving = False
    lock.release()
    counter = 0

    tempBinaryMessage = str()
    binaryMessage = int()
    messageString = str()
    for char in message:
        tempBinaryMessage = tempBinaryMessage + char
        counter += 1
        if counter%8 == 0:
            binaryMessage = int(tempBinaryMessage, 2)
            tempBinaryMessage = ''
            #print(binaryMessage)
            messageString = messageString + chr(binaryMessage)

    #print("message: ", messageString)
    return messageString


def gpioSetup():

    numList = getSettings()

    clockPin = numList[2]
    dataPin = numList[3]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clockPin, GPIO.IN)
    GPIO.setup(dataPin, GPIO.IN)

    return clockPin, dataPin, numList

def getSettings():
    settings = open("/var/www/html/settings.txt", "r")

    numList = list()

    for x in settings.readlines():
        if " " in x:
            numList.extend([int(y) for y in x.split() if y.isdigit()])

    settings.close()
    return numList

def main(lock):
    clockPin, dataPin, numList = gpioSetup()
    messageString = BinarytoTxt(clockPin, dataPin, lock)
    GPIO.cleanup(numList[2])
    GPIO.cleanup(numList[3])
    return messageString
    