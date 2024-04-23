import requests
import telebot
from data import token, api_key

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello, do you wont know the weather? \n digit you location!")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        weather_data = response.json()
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        image = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{image}.png"
        #print(image)
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        wind_direction = weather_data['wind']['deg'] if 'deg' in weather_data['wind'] else None
        if wind_direction is not None:
            dirs = ["Nord", "NordEst", "Est", "SouthEst", "South", "SouthWest", "West", "NordWest", "Nord"]
            ix = round(wind_direction / (360. / len(dirs)))
            wind_direction_cardinal = dirs[ix % len(dirs)]
            wind_direction_str = f"Wind Direction: {wind_direction_cardinal}"
        else:
            wind_direction_str = ""

        bot.reply_to(message,
                     f"Country: {country} \n Temp: in {city}: {temperature}°C \n {icon_url} \n  HUM: {humidity}% \n"
                     f" Pressure: {pressure}mmHg \n"
                     f"{ wind_direction_str} \n Wind speed: {wind_speed} m/s \n {description}")
    else:
        bot.send_message(message.chat.id, f"Sorry, I can't find {city} weather")


bot.polling(none_stop=True)
