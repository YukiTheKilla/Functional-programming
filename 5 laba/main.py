import telebot
import config
import random
import requests
import json
from telebot import types
from datetime import datetime
import logging
import sys

# Configure logging with Unicode support
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[
    logging.StreamHandler(stream=sys.stdout),  # No encoding argument
])

bot = telebot.TeleBot(config.token)

previous_section = None

button_history = []

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🤖 OpenAI API")
    btn2 = types.KeyboardButton("📰 News API")
    btn3 = types.KeyboardButton("💱 Exchange API")
    btn4 = types.KeyboardButton("🌦️ Weather API")
    btn5 = types.KeyboardButton("Игры 🎮")
    btn6 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    global previous_section

    # Log the button press in real-time
    logging.info(f"Button Pressed: {message.text}")

    button_history.append({"timestamp": str(datetime.now()), "button_pressed": message.text})

    with open('5 laba/history.json', 'w', encoding='utf-8') as json_file:
        json.dump(button_history, json_file, indent=4, ensure_ascii=False)

    if message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Кто делал этого бота?")
        btn2 = types.KeyboardButton("Что ты умеешь?")
        btn3 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Выбери вопрос из списка:", reply_markup=markup)

    elif message.text == "Кто делал этого бота?":
        bot.send_message(message.chat.id, text="Этот бот был создан чумным доктором!🖤 \n"
                                               "\n"
                                               "Спасибо статье на [Хабр](https://habr.com/ru/sandbox/163347/) за помощь в создании", parse_mode='Markdown', disable_web_page_preview=False)

    elif message.text == "Что ты умеешь?":
        bot.send_message(message.chat.id, text="Предоставлять различные функции. Попробуй выбрать что-то из меню!")

    elif message.text == "Вернуться в главное меню":
        previous_section = None
        start(message)

    elif message.text == "Игры 🎮":
        previous_section = "Главное меню"
        show_games_menu(message)

    elif message.text == "Орел 🦅 Решка 🪙":
        previous_section = "Игры 🎮"
        play_coin_flip(message)

    elif message.text == "Монополия 🎲":
        previous_section = "Игры 🎮"
        bot.send_message(message.chat.id, text="Играй в Монополию здесь: [MonopolyOne](https://monopoly-one.com/games)", parse_mode='Markdown', disable_web_page_preview=False)

    elif message.text == "Шахматы ♟️":
        previous_section = "Игры 🎮"
        bot.send_message(message.chat.id, text="Играй в шахматы здесь: [Lichess](https://lichess.org)", parse_mode='Markdown', disable_web_page_preview=False)

    if message.text == "🤖 OpenAI API":
        bot.send_message(message.chat.id, text="Пока в разработке...", parse_mode='Markdown')

    elif message.text == "📰 News API":
        implement_news_api(message,config.news_api)

    elif message.text == "💱 Exchange API":
        implement_exchange_api(message,config.exchange_api)

    elif message.text == "🌦️ Weather API":
        implement_weather_api(message, config.weather_api)

def show_games_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("Орел 🦅 Решка 🪙")
    btn3 = types.KeyboardButton("Монополия 🎲")
    btn4 = types.KeyboardButton("Шахматы ♟️")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn2, btn3, btn4, back)

    bot.send_message(message.chat.id, text="...", reply_markup=markup)


def play_coin_flip(message):
    choices = ["Орел 🦅", "Решка 🪙"]
    bot_choice = random.choice(choices)

    result = "Ты бросил монету и выпал(а): {}".format(bot_choice)
    bot.send_message(message.chat.id, result)
    show_previous_section(message)

def show_previous_section(message):
    global previous_section

    if previous_section == "Главное меню":
        start(message)
    elif previous_section == "Игры 🎮":
        show_games_menu(message)


def implement_news_api(message, api_key):
    # API endpoint URL
    news_url = ('https://newsapi.org/v2/top-headlines?'
                'country=us&'
                'pageSize=10&'
                f'apiKey={api_key}')

    try:
        response = requests.get(news_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            news_data = response.json()

            if news_data['status'] == 'ok':
                articles = news_data['articles']

                for article in articles:
                    title = article['title']
                    url = article['url']
                    message_text = f"Title: {title}\nURL: {url}\n"
                    bot.send_message(message.chat.id, text=message_text)

            else:
                error_message = f"Error: {news_data.get('message', 'unknown')}"
                bot.send_message(message.chat.id, text=error_message)

        else:
            error_message = f"Error: Failed to retrieve news. Status Code: {response.status_code}"
            bot.send_message(message.chat.id, text=error_message)

    except Exception as e:
        error_message = f"An error occurred: {e}"
        bot.send_message(message.chat.id, text=error_message)


def implement_exchange_api(message,api_key):
    base_currency = "USD"
    # API endpoint URL
    endpoint_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"

    try:
        response = requests.get(endpoint_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            exchange_data = response.json()
            if exchange_data['result'] == 'success':
                base_code = exchange_data['base_code']
                conversion_rates = exchange_data['conversion_rates']

                currencies_to_display = ['RUB', 'EUR', 'KZT', 'CNY']

                # Create a message with exchange rates
                message_text = f"Exchange rates for {base_code}:\n"
                for currency in currencies_to_display:
                    rate = conversion_rates.get(currency, 'N/A')
                    message_text += f"{currency}: {rate}\n"
                bot.send_message(message.chat.id, text=message_text)

            else:
                error_type = exchange_data.get('error-type', 'unknown')
                error_message = f"Error: {error_type}"
                bot.send_message(message.chat.id, text=error_message)

        else:
            error_message = f"Error: Failed to retrieve data. Status Code: {response.status_code}"
            bot.send_message(message.chat.id, text=error_message)

    except Exception as e:
        error_message = f"An error occurred: {e}"
        bot.send_message(message.chat.id, text=error_message)

def implement_weather_api(message, api_key):
    # API endpoint URL
    base_url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": "St Petersburg",
        "lang": "ru",
        "alerts": "yes",
        "aqi": "yes"
    }


    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        weather_data = response.json()

        # Extract relevant information
        location = weather_data.get("location", {})
        current_weather = weather_data.get("current", {})
        city_name = location.get("name")
        country = location.get("country")
        temperature_c = current_weather.get("temp_c")
        temperature_f = current_weather.get("temp_f")
        condition_text = current_weather["condition"]["text"]

        response_message = (
            f"{message.text}\n"  # Use the 'text' attribute to access the message content
            f"Weather in {city_name}, {country}:\n"
            f"Temperature: {temperature_c}°C / {temperature_f}°F\n"
            f"Condition: {condition_text}"
        )

        bot.send_message(message.chat.id, text=response_message)
    except requests.exceptions.RequestException as e:
        # Handle exceptions if the request fails
        error_message = f"Error fetching weather data: {e}"
        bot.send_message(message.chat.id, text=error_message)


bot.polling(none_stop=True)
