from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests

def index(request):
    if request.POST.get('city'):
        #get values from form
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        url = 'https://api.openweathermap.org/geo/1.0/direct?q='+city+','+state+','+country+'&limit=5&appid=37e0a97bb124748fad11dbf6732b85aa'
        returnData = requests.get(url).json()

    elif request.POST.get('zip'):
        #get values from form
        zipCode = request.POST.get('zip')
        country = request.POST.get('country')

        url = 'http://api.openweathermap.org/geo/1.0/zip?zip='+zipCode+','+country+'&appid=37e0a97bb124748fad11dbf6732b85aa'
        returnData = requests.get(url).json()

    else:
        #initialize values
        city = ' '
        state = ' '
        country = ' '

        url = 'https://api.openweathermap.org/geo/1.0/direct?q='+city+','+state+','+country+'&limit=5&appid=37e0a97bb124748fad11dbf6732b85aa'
        returnData = requests.get(url).json()

    context = {
    "data" : returnData,
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def currentWeather(request, lat = 0, lon = 0):

    # Current Weather
    url = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid=37e0a97bb124748fad11dbf6732b85aa&units=imperial'
    returnData = requests.get(url).json()

    c_weatherData = returnData['weather']
    c_weather = c_weatherData[0]['main']
    c_iconData = c_weatherData[0]['icon']
    c_main = returnData['main']

    # Five Days Forecast
    url_2 = 'https://api.openweathermap.org/data/2.5/forecast?lat='+str(lat)+'&lon='+str(lon)+'&appid=37e0a97bb124748fad11dbf6732b85aa&units=imperial'
    returnData_2 = requests.get(url_2).json()

    c_list = returnData_2['list']

    # Get forecast Info
    f_weatherData = []   # empty list
    for i in range(0,5):
        date = c_list[i*8]["dt_txt"].split()[0]
        icon = c_list[i*8]["weather"][0]["icon"]
        main = c_list[i*8]["weather"][0]["main"]
        min_temp = c_list[i*8]["main"]["temp_min"]
        max_temp = c_list[i*8]["main"]["temp_max"]
        humidity = c_list[i*8]["main"]["humidity"]
        weather = {
            "date": date,
            "icon": icon,
            "main": main,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "humidity": humidity
        }
        f_weatherData.append(weather)

    context = {
        "lat" : lat,
        "lon" : lon, 

        # Current Weather
        "c_weather" : c_weather, 
        "icon" : c_iconData,
        "main" : c_main,

        # Five Days Forecast
        "f_weather" : f_weatherData,
    }

    template = loader.get_template('current.html')
    return HttpResponse(template.render(context, request))