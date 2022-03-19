import urllib.request
import multiprocessing as mp
from datetime import datetime
lock = mp.Lock()


def main():
    lock_locked = False
    try:
        data = urllib.request.urlopen("ftp://tgftp.nws.noaa.gov/data/observations/metar/decoded/KATT.TXT").read()
        data = data.decode()
        weather_data = data.split('\n')

        with open("/var/www/html/weather.txt", "a") as weather_report:
            weather_report.write(data)
            weather_report.write("Read at " + datetime.now().strftime("%m-%d-%Y %H:%M:%S") + "\n\n")

        for line in weather_data:
            if "Sky" in line:
                condition_line = line
            elif "Temperature" in line:
                temperature_line = line
            elif "Humidity" in line:
                humidity_line = line

        condition_arr = condition_line.split(":")
        condition_value = condition_arr[1]
        condition_value = condition_value[1:].capitalize()

        temperature_arr = temperature_line.split(" ")
        temperature_value = temperature_arr[1]

        humidity_arr = humidity_line.split(" ")
        humidity_value = humidity_arr[2].strip('%')

        #print("Condition: " + condition_value + "\nTemperature: " + temperature_value + "\nHumidity: " + humidity_value)

        lock.acquire()
        lock_locked = True
        with open("/var/www/html/testfile.txt", "r") as test_file:
            all_text = test_file.readlines()

            all_text[0] = "Current-Temperature = " + temperature_value + "\n"
            all_text[1] = "Humidity = " + humidity_value + "\n"
            all_text[2] = "Condition = " + condition_value + "\n"

            with open("/var/www/html/testfile.txt", "w") as rewrite_file:
                for i in range(0, len(all_text)):
                    rewrite_file.write(all_text[i])
                
        lock.release()
        lock_locked = False
    except Exception:
        if lock_locked:
            lock.release()

        print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_weather] There is probably an internet issue")
        with open("/var/www/html/log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [get_weather] There is probably an internet issue\n")
            