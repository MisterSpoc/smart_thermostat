import time
import get_data
import send_data
import weather_scraper
import threading
import RPi.GPIO as GPIO
import numbers
import traceback
import multiprocessing as mp
from datetime import datetime


class UpdateTimes:
    get_data_update = datetime.now()
    send_data_update = datetime.now()
    weather_scraper_update = datetime.now()


class TempValues:
    high_temp = float(85)
    low_temp = float(60)
    ambient_temp = float(75)
    outer_tolerance = float(.5)
    inner_tolerance = float(.5)
    mode = "Idle"
    logging_mode = 0


def main():
    Q = mp.Queue()
    
    listen_thread = threading.Thread(target=ear)
    temp_data_thread = threading.Thread(target=temperature)
    weather_updater_thread = threading.Thread(target=get_weather)
    #weather_updater_process = mp.Process(target=get_weather, args=(Q,))
    
    listen_thread.start()
    #weather_updater_process.start()
    weather_updater_thread.start()
    temp_data_thread.start()
    
    #while True:
        #UpdateTimes.weather_scraper_update = Q.get()
    

def ear():
    while True:
        try:
            letter_code = ""
            while True:
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_data] Listening...")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_data] Listening...\n")
                command = get_data.main(lock)
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_data] ...end listening")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_data] ...end listening\n")
                '''print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " " + command)
                with open("/var/www/html/log.txt", "a") as myfile:
                    myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " " + command + "\n")'''
                letter_code, number = codes(command)
                try:
                    numberFloat = float(number)
                    '''if letter_code == "u":
                        if numberFloat != TempValues.potential_high:
                            TempValues.potential_high = numberFloat
                            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " Got " + number + " as a potential upper limit. Waiting for confirmation...")
                        else:
                            TempValues.high_temp = numberFloat
                            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " " + number + " confirmed as upper limit")
                    if letter_code == "l":
                        if numberFloat != TempValues.potential_low:
                            TempValues.potential_low = float(number)
                            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " Got " + number + " as a potential lower limit. Waiting for confirmation...")
                        else:
                            TempValues.low_temp = float(number)
                            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " " +  number + " confirmed as lower limit")'''
                    if letter_code == "a":
                        TempValues.ambient_temp = float(number)
                        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Ambient: " + number)
                        if int(TempValues.logging_mode) >= 1:
                            with open("temps.txt", "a") as myfile:
                                myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + "\t" + number + "\n")
                    if letter_code == "m":
                        if int(number) == 0 and TempValues.mode != "Cooling":
                            TempValues.mode = "Cooling"
                            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Mode: Cooling")
                            if int(TempValues.logging_mode) == 2:
                                with open("/var/www/html/log.txt", "a") as myfile:
                                    myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Mode: Cooling\n")
                        elif int(number) == 1 and TempValues.mode != "Heating":
                            TempValues.mode = "Heating"
                            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Mode: Heating")
                            if int(TempValues.logging_mode) == 2:
                                with open("/var/www/html/log.txt", "a") as myfile:
                                    myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Mode: Heating\n")
                        elif int(number) == 3 and TempValues.mode != "Idle":
                            TempValues.mode = "Idle"
                            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Mode: Idle")
                            if int(TempValues.logging_mode) == 2:
                                with open("/var/www/html/log.txt", "a") as myfile:
                                    myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Mode: Idle\n")

                    UpdateTimes.get_data_update = datetime.now()
                    write_to_file()
                except:
                    if "" not in command and "" not in command:
                        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Invalid code: " + command)
                        with open("/var/www/html/log.txt", "a") as myfile:
                            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Invalid code: " + command + "\n")
                    else:
                        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Invalid code containing illegal character. Not printing")
                        with open("/var/www/html/log.txt", "a") as myfile:
                            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Invalid code containing illegal character. Not printing\n")

            time.sleep(.1)
        except:
            print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Crashed, looping to restart")
            with open("/var/www/html/log.txt", "a") as myfile:
                myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear] Crashed, looping to restart\n")


def get_weather():
    sleep_time = 60
    while True:
        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [weather_scraper] Getting weather")                    
        weather_scraper.main()
        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [weather_scraper] Done getting weather")  
        UpdateTimes.weather_scraper_update = datetime.now()
        time.sleep(sleep_time)

    
def getTemps():
    try:
        time.sleep(1)
        settings = open("/var/www/html/testfile.txt", "r")

        numList = [0]*9
        counter = 0

        for x in settings.readlines():
            if " " in x:
                for y in x.split():
                    if is_float(y):
                    
                        numList[counter] = float(y)
                    
                        counter += 1

        settings.close()
    
        highTemp = numList[2]
        lowTemp = numList[3]
        outside_current = numList[0]
        out_tolerance = numList[5]
        in_tolerance = numList[6]
        TempValues.logging_mode = numList[7]
    
        return highTemp, lowTemp, outside_current, out_tolerance, in_tolerance
    except:
        traceback.print_exc()
    
def temperature():
    prev_lowTemp = float(0)
    prev_highTemp = float(0)
    prev_outside_current = float(0)
    prev_outer = float(0)
    prev_inner = float(0)
    
    while True:
        try:
            highTemp, lowTemp, outside_current, outer_current, inner_current = getTemps()
        
            if prev_highTemp != highTemp and highTemp != 0:
                prev_highTemp = highTemp
                lock.acquire()
                TempValues.high_temp = highTemp
                lock.release()
                message = "u"+str(highTemp)
                check_for_sending()
                lock.release()
                UpdateTimes.send_data_update = datetime.now()
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting upper limit to " + str(highTemp) + " from file")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting upper limit to " + str(highTemp) + " from file\n")
                        
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...\n")
                send_data.main(message)
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data\n")
                  
            if prev_lowTemp != lowTemp and lowTemp != 0:
                prev_lowTemp = lowTemp
                lock.acquire()
                TempValues.low_temp = lowTemp
                lock.release()
                message = "l"+str(lowTemp)
                check_for_sending()
                lock.release()
                UpdateTimes.send_data_update = datetime.now()
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting lower limit to " + str(lowTemp) + " from file")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting lower limit to " + str(lowTemp) + " from file\n")
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...\n")
                send_data.main(message)
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data\n")
                 
            if prev_outside_current != outside_current and outside_current != 0:
                lock.acquire()
                prev_outside_current = outside_current
                lock.release()
                message = "o"+str(outside_current)
                check_for_sending()
                lock.release()
                UpdateTimes.send_data_update = datetime.now()
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting outside temp to " + str(outside_current) + " from file")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting outside temp to " + str(outside_current) + " from file\n")
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...\n")
                send_data.main(message)
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data\n")
                
            if prev_outer != outer_current and outer_current != 0:
                prev_outer = outer_current
                lock.acquire()
                TempValues.outer_tolerance = outer_current
                lock.release()
                message = "b"+str(outer_current)
                check_for_sending()
                lock.release()
                UpdateTimes.send_data_update = datetime.now()
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting outer tolerance to " + str(outer_current) + " from file")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting outer tolerance to " + str(outer_current) + " from file\n")
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...\n")
                send_data.main(message)
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data\n")
                
            if prev_inner != inner_current and inner_current != 0:
                prev_inner = inner_current
                lock.acquire()
                TempValues.inner_tolerance = inner_current
                lock.release()
                message = "e"+str(inner_current)
                check_for_sending()
                lock.release()
                UpdateTimes.send_data_update = datetime.now()
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting inner tolerance to " + str(inner_current) + " from file")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [temperature] Setting outer tolerance to " + str(inner_current) + " from file\n")
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Sending data...\n")
                send_data.main(message)
                print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data")
                if int(TempValues.logging_mode) == 2:
                    with open("/var/www/html/log.txt", "a") as myfile:
                        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [send_data] Done sending data\n")

        except:
            traceback.print_exc()
            
def codes(code):
    #a = ambient, u = upper bound, l = lower bound, b = outer tolerance, e = inner tolerance
    i = 0
    new_char = ""
    letter_code = ""
    for char in code:
        if i == 0:
            letter_code = char
        else:
            new_char += char
        i += 1
    return letter_code, new_char

def check_for_sending():
    lock.acquire()
    while get_data.UniversalVariables.is_recieving is True:
        lock.release()
        time.sleep(1)
        lock.acquire()
        
def is_float(y):
    try:
        float(y)
        return True
    except:
        return False

def write_to_file():
    try:
        l.acquire()
        test_file = open("/var/www/html/testfile.txt" , 'r')
        all_text = test_file.readlines()
        
        
        all_text[5] = "Indoor-Ambient = " + str(TempValues.ambient_temp) + "\n"
        '''print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing ambient temp as " + str(TempValues.ambient_temp) + " to file")
        with open("/var/www/html/log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing ambient temp as " + str(TempValues.ambient_temp) + " to file\n")'''
        
        all_text[6] = "SendData-Update = " + UpdateTimes.send_data_update.strftime("%m-%d-%Y %H:%M:%S") + "\n"
        all_text[7] = "GetData-Update = " + UpdateTimes.get_data_update.strftime("%m-%d-%Y %H:%M:%S") + "\n"
        all_text[8] = "Weather-Update = " + UpdateTimes.weather_scraper_update.strftime("%m-%d-%Y %H:%M:%S") + "\n"
        
        all_text[9] = "Mode = " + TempValues.mode + "\n"
        '''print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing mode as " + TempValues.mode + " to file")
        with open("/var/www/html/log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing mode as " + TempValues.mode + " to file\n")'''
        
        '''all_text[10] = "Outer-tolerance = " + str(TempValues.outer_tolerance) + "\n"
        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing outer tolerance as " + str(TempValues.outer_tolerance) + " to file")
        with open("/var/www/html/log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing outer tolerance as " + str(TempValues.outer_tolerance) + " to file\n")
            
        all_text[11] = "Inner-tolerance = " + str(TempValues.inner_tolerance)
        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing inner tolerance as " + str(TempValues.inner_tolerance) + " to file")
        with open("/var/www/html/log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Writing inner tolerance as " + str(TempValues.inner_tolerance) + " to file\n")'''
            
            
        test_file.close()

        rewrite_file = open("/var/www/html/testfile.txt" , 'w')
        
        for i in range (0, len(all_text)):
            rewrite_file.write(all_text[i])
        l.release()
    except:
        l.release()
        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Crashed, will try again next time")
        with open("/var/www/html/log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [ear/write_to_file] Crashed, will try again next time\n")
            
lock = threading.Lock()
l = mp.Lock()

if __name__ == "__main__":
    main()
