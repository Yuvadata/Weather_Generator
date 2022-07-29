# Weather_Generator
Toy simulation to generate weather for various city & locations

Pre-requisite:
Python3.9 version

Install below PIP:
PIP Install geopy
PIP Install geopandas

Code decode:

Input: 16 City names

Output: Pipe delimimted values consisting of City,Latitude,Longitude,Elevation,ISODatetime,Condition,Temperature(C),Pressure(hPa),Relative humidity(%) written to output .dat file

Logic: 
1. Pass city name to geopy Nominatim service to get Latitude & Longitude. Elevation is comes with googlemaps api, so derived random elevation.
2. API call to openweathermap by passing Lat Long & APIKey parameters, get the realtime weather measurements (Temp, Pressure, humidity) & derive weather condition
3. Historic weather data through API incur cost. For the purpose of this exercise, weather measurments for various point in time (10 time slices) is derived random for each city
4. Realtime & historic data is written into output.dat file
5. Script takes ~30 seconds to complete 
