import requests
import json
from app.que import que


def get_weather(location="Kazan"):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(location,
                                                                        '56fc8aec39b10f93f585bed51188f0e1')
    response = requests.get(url)
    weatherData = json.loads(response.text)


    # print(round(float(weatherData["main"]["temp"])-273.15,1))
    # print(weatherData['weather'][0]['description'])
    # print(weatherData['weather'][0]['icon'])

    return round(float(weatherData["main"]["temp"])-273.15,1), weatherData['weather'][0]['description']
    my_return = round(float(weatherData["main"]["temp"])-273.15,1), weatherData['weather'][0]['description']#, weatherData['weather'][0]['icon']
    que.put(my_return)



