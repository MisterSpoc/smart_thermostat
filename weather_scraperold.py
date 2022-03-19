import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
from datetime import datetime
lock = mp.Lock()


def main():
    print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [weather_scraper] Getting weather")
    with open("log.txt", "a") as myfile:
        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [weather_scraper] Getting weather\n")

    result = requests.get("https://weather.com/weather/today/l/cd3c4009a039ea0b0cddeac12179278b828f463850c87e575588c92048844e55", timeout=5)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")

    
    #Current Temperature and Feels-Like Temperature
    for tags in soup.find_all('div'):
        testString = str(tags.get('class'))
        if 'today_nowcard-temp' in testString:
            CurrentTemp = textToInteger(tags)
        if 'today_nowcard-feels' in testString:
            for stuff in tags:
                if 'deg-feels' in stuff['class']:
                    FeelTemp = textToInteger(stuff)
                    
    #Humidity
    for tags in soup.find_all('tr'):
        for otherTags in tags:
            if '%' in otherTags.text:
                Humidity = textToInteger(otherTags)

    #Sunrise and Sunset times
    for tags in soup.find_all('span'):
        testString = str(tags.get('class'))
        if 'wx-dsxdate' in testString:
            if tags['id'] == 'dp0-details-sunrise':
                Sunrise = tags.text
            if tags['id'] == 'dp0-details-sunset':
                Sunset = tags.text
    
    """print("The current temperature is %d, but it feels like %d" %(CurrentTemp, FeelTemp))
    print("There is ", Humidity, "% humidity at the moment")
    print("The Sun will rise at", Sunrise, "and set at", Sunset)
    """
    lock.acquire()
    test_file = open("testfile.txt" , 'r')
    all_text = test_file.readlines()
    
    now = datetime.now()	
    
    all_text[0] = "Current-Temperature = " + str(CurrentTemp) + "\n"
    all_text[1] = "Feels-Like = " + str(FeelTemp) + "\n"
    all_text[2] = "High = 100\n"
    all_text[3] = "Low = 76\n"
    all_text[4] = "Humidity = " + str(Humidity) + "\n"
    all_text[5] = "Sunrise = " + Sunrise.strip(" am") + "\n"
    all_text[6] = "Sunset = " + Sunset.strip(" pm") + "\n"
    
    test_file.close()

    rewrite_file = open("testfile.txt" , 'w')
    
    for i in range (0, len(all_text)):
        rewrite_file.write(all_text[i])
            
    lock.release()
    print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [weather_scraper] Done getting weather")
    with open("log.txt", "a") as myfile:
        myfile.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " [weather_scraper] Done getting weather\n")
    
    
        
def textToInteger(tags):
    if len(tags.text) == 4:
        CurrentTemp = 100*int(tags.text[0]) + 10*int(tags.text[1]) + int(tags.text[2])
    elif len(tags.text) == 3:
        CurrentTemp = 10*int(tags.text[0]) + int(tags.text[1])
    else:
        CurrentTemp = int(tags.text[0])
    
    return CurrentTemp

