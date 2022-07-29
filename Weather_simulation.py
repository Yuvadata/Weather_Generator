##
## This Python code is toy simulation of the environment to get meteorological data for geo city
## Input - Geo City
## Output - Pipe delimimted values consisting of City,Latitude,Longitude,Elevation,ISO Datetime,Condition,Temperature(C),Pressure(hPa),Relative humidity(%) written to output .dat file
##

## Import required lib
import geocoder
from datetime import datetime
import time
import random
from array import *
import requests
from pprint import pprint
from geopy.geocoders import Nominatim

## Declare API Key
APIKey = "e0886416e801651caa3709e1799af846"

## Declare variables
Condition = ["Sunny","Rain"]
SnowTempCutoff = 0
SunnyTempCutoff = 30
TempMax = 40
TempMin = -5
HumMax = 100
HumMin = 20
PresMax = 1200
PresMin = 700
ElevationMin = 1
ElevationMax = 100
Timeloopcount = 10

## Declare City
Geocity = ["Sydney", "Melbourne", "Brisbane", "Canberra", "Perth", "Adelaide", "Hobart", "Darwin", "Geelong", "Townsville","Albury","Chennai", "Delhi", "New York", "California", "London"]

## Function to Convert Temperature from Kelvin to Celcuis, as openweathermap return Temp in Kelvin
def ConvertkelvinToCelsius(kelvin):
    return kelvin - 273.15

## Function to derive weather condition (Sunny, Rain, Snow)
def DeriveWeatherConditon(Temp):
    if Temp < SnowTempCutoff:
        Cond = "Snow"
    elif Temp >= SunnyTempCutoff:
        Cond = "Sunny"
    else:
        Cond = random.choice(Condition)

    return Cond

def strTimeProp(start, end, format, prop):
    """
    This function will help to shift time
    based on the random selection
    :return: Date Time
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)
    DT_datetime = datetime.strptime(time.strftime(format,time.localtime(ptime)),"%Y-%m-%d %H:%M:%S")
    return DT_datetime

# Random date time generator
def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d %H:%M:%S', prop)

## Function to generate realtime meteorology data through API call to openweathermap 
def GetAPIMeteorologyData(Lat,Long,APIKey):
    """API Call to openweathermap for realtime date"""
    API_Url='https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(Lat,Long,APIKey)
    city_weather=requests.get(API_Url).json()
    """Parse the results"""
    Temp = round(ConvertkelvinToCelsius(city_weather['main']['temp']),1)
    Cond = DeriveWeatherConditon(Temp)
    Humidity = city_weather['main']['humidity']
    Pressure = city_weather['main']['pressure']
    
    return str(Cond) + "|" + str(Temp) + "|" + str(Pressure) + "|" + str(Humidity)

## Function to generate random meteorology data through random function
def GetRandomMeteorologyData(Lat,Long):
    RTemp = round(random.uniform(TempMax, TempMin), 1)
    RCond = DeriveWeatherConditon(RTemp)
    RHumidity = round(random.uniform(HumMax, HumMin), 1)
    RPressure = round(random.uniform(PresMax, PresMin), 1)

    return str(RCond) + "|" + str(RTemp) + "|" + str(RPressure) + "|" + str(RHumidity)

## Open output file
WeatherFile = open("Weather_Data.dat", "w")

## Loop through various locations to get Meteorology data & write into the output file
for x in range(len(Geocity)):
    City = Geocity[x]
    geolocator = Nominatim(user_agent="CBA_Weather_App")
    location = geolocator.geocode(City)
    coordinates = (location.latitude,location.longitude)
    Lat = coordinates[0]
    Long = coordinates[1]
    Alt = str(random.randint(ElevationMin, ElevationMax))
    Geo = str(round(Lat,2)) + "," + str(round(Long,2)) + "," + str(Alt)
    Date = (datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    MetData = GetAPIMeteorologyData(Lat,Long,APIKey)
    OutputRow = str(City) + "|" + str(Geo) + "|" + str(Date) + "|" + str(MetData) + "\n" 
    pprint(OutputRow)
    WeatherFile.write(OutputRow)
    ## Loop through various times for each city & write into the output file
    Timeiterate=0
    while Timeiterate < Timeloopcount:
        Rdatetime = randomDate("2022-06-01 12:00:00", "2022-07-29 12:00:00", random.random())
        Rdatetimeiso = Rdatetime.isoformat()
        RMetData = GetRandomMeteorologyData(Lat,Long)
        ROutputRow = str(City) + "|" + str(Geo) + "|" + str(Rdatetimeiso) + "|" + str(RMetData) + "\n"
        pprint(ROutputRow)
        WeatherFile.write(ROutputRow)
        Timeiterate = Timeiterate + 1

WeatherFile.close()