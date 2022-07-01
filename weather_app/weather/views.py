from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.conf import settings

def index(request):
    url = 'https://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'
    cities = City.objects.all()
    form = CityForm()
    weather_data = []

    if request.method=='POST':
        form = CityForm(request.POST)
        form.save()
    
    
    for city in cities:
        city_weather = requests.get(url.format(settings.API_KEY,city)).json()
        if len(city_weather)==1:
            continue

        weather = {
        'city':city_weather['location']['name'],
        'temprature': city_weather['current']['temp_c'],
        'description':city_weather['current']['condition']['text'],
        'icon': city_weather['current']['condition']['icon']
        }
        weather['icon'] = "http:" + weather['icon']
        weather_data.append(weather)
    
    context = {'weather_data':weather_data, 'form':form}
    return render(request,'weather/index.html',context)


    


    



