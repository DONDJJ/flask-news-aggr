import requests
import json

def get_weather(location="Kazan"):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(location,
                                                                        '56fc8aec39b10f93f585bed51188f0e1')
    response = requests.get(url)
    weatherData = json.loads(response.text)

    return round(float(weatherData["main"]["temp"])-273.15,1), weatherData['weather'][0]['description']




