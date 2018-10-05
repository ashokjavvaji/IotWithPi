import requests
import sys
from datetime import datetime

forecastUrl='http://api.openweathermap.org/data/2.5/forecast?APPID=7fc3ac4f362f14bb2dfc885872364d9c&units=metric&id='
cityId='1277333' #Bangalore

class Forecast:
    def __init__(self, time, icon):
        self.time=time
        self.icon=icon

url=forecastUrl+cityId
forecast=requests.get(url).json()
print("------------------------------------------------------------")
fdict={}
lists=forecast["list"]
print(forecast["list"][0])

for index in range(6):
    fdict[index]=(lists[index]["dt"],lists[index]["weather"][0]["icon"])

print("------------------------------------------------------------")
print(fdict)
