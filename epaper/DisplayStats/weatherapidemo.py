# Program to send requests to OpenWeatherAPI and get the weather data
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import subprocess
from datetime import datetime

EPD_WIDTH = 400
EPD_HEIGHT = 300

baseUrl='http://api.openweathermap.org/data/2.5/weather?APPID=7fc3ac4f362f14bb2dfc885872364d9c&units=metric&id='
forecastUrl='http://api.openweathermap.org/data/2.5/forecast?APPID=7fc3ac4f362f14bb2dfc885872364d9c&units=metric&id='
cityId='1277333' #Bangalore

url=baseUrl+cityId

json_data=requests.get(url).json()
print(json_data)

url=forecastUrl+cityId
forecast=requests.get(url).json()

weather=json_data["weather"][0]
print(weather)
print(datetime.today())

icon=json_data["weather"][0]["icon"]

temp = json_data["main"]["temp"]
print(temp)

currDate = datetime.today().strftime('%d-%B')
currTime = datetime.today().strftime('%I:%M %p')

image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
draw = ImageDraw.Draw(image)
font16 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
font24 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
font32 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)
font40 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 40)
font100 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 100)
draw.rectangle((0, 0, EPD_WIDTH, EPD_HEIGHT), fill = 255)
# Row-1 (Temp and Date)
currWeather = Image.open('images/weather/'+icon+'.jpg')
offset=(2,5)
image.paste(currWeather,offset)
draw.text((40, 2), ('%.0f' % temp), font = font40, fill = 0)
draw.arc((90, 5, 100, 15), 0, 360, fill = 0)
draw.text((102, 2), "C", font = font40, fill = 0)
draw.rectangle((139, 0, 141, 50),fill=0)
draw.text((150, 2), str(currDate), font = font40, fill = 0)
draw.rectangle((0, 50, EPD_WIDTH, 52), fill = 0)

# Rpw-2 (Time)
draw.text((45, 55), str(currTime), font = font100, fill = 0)
draw.rectangle((0, 150, EPD_WIDTH, 152), fill = 0)

# Row-3 (Hourly Forecast)
row3=160
imagey=row3
text1=imagey+40
text2=text1+20
fdict={}
itemsToShow=4
fcastSpacing=(400//itemsToShow)
for x in range(itemsToShow):
    fdict[x]=((25+(x*fcastSpacing),imagey),(5+(x*fcastSpacing),text1),(5+(x*fcastSpacing),text2))
lists=forecast["list"]
for index in range(itemsToShow):
    img = Image.open('images/weather/'+lists[index]["weather"][0]["icon"]+'.jpg')
    opic,otext1,otext2=fdict[index]
    image.paste(img,opic)
    draw.text(otext1,datetime.fromtimestamp(lists[index]["dt"]).strftime('%I:%M %p'), font = font16, fill = 0)
    draw.text(otext2,lists[index]["weather"][0]["main"], font = font16, fill = 0)

#draw.text((5, 170), "More Information Coming soon", font = font24, fill = 0)
draw.rectangle((0, 240, EPD_WIDTH, 242), fill = 0)

#Row-4 (IP Address, CPU temp and RAM usage)
# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
row4=245
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell = True )
cmd = "top -bn1 | grep load | awk '{print $(NF-2)}' | awk '{split($0,load,\",\"); print load[1]}'"
CPU = subprocess.check_output(cmd, shell = True )
cmd = "/opt/vc/bin/vcgencmd measure_temp | awk '{split($0,temp,\"=\"); print temp[2]}'"
TEMP = subprocess.check_output(cmd, shell = True )
TEMP = TEMP.rstrip()
print(TEMP)
cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", (100-($3*100/$2)) }'"
MemUsage = subprocess.check_output(cmd, shell = True )
internet = Image.open('images/stats/wifi.jpg')
offset=(2,row4)
image.paste(internet,offset)
draw.text((30, row4+4), IP, font = font16, fill = 0)
internet = Image.open('images/stats/globe.jpg')
offset=(2,row4+25)
image.paste(internet,offset)
draw.text((30, row4+29), "CONNECTED", font = font16, fill = 0)
draw.rectangle((184, row4, 186, EPD_HEIGHT),fill=0)
img = Image.open('images/stats/thermometer.jpg')
offset=(195,row4)
image.paste(img,offset)
draw.text((223, row4+4), TEMP, font = font16, fill = 0)
img = Image.open('images/stats/chip.jpg')
offset=(195,row4+25)
image.paste(img,offset)
draw.text((223, row4+29), CPU, font = font16, fill = 0)
draw.rectangle((309, row4, 311, EPD_HEIGHT),fill=0)
img = Image.open('images/stats/ram.jpg')
offset=(322,row4)
image.paste(img,offset)
draw.text((322, row4+27), MemUsage, font = font16, fill = 0)


image.save("temp2.jpg", "JPEG")

