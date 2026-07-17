
import telebot
from telebot import types
from config import TOKEN
from database import save_history, get_history, clear_history, save_favorite, get_favorite
from ai import get_ai_advice
from weather import get_weather, get_forecast


bot = telebot.TeleBot(TOKEN)

bot.set_my_commands([
    telebot.types.BotCommand("start", "Запуск бота"),
    telebot.types.BotCommand("help", "Помощь"),
    telebot.types.BotCommand("menu", "Меню"),
    telebot.types.BotCommand("weather", "Погода"),
    telebot.types.BotCommand("forecast", "Прогноз"),
    telebot.types.BotCommand("history", "История"),
    telebot.types.BotCommand("favorite", "Любимый город")
])


@bot.message_handler(commands=["start"])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🌤 Погода")
    btn2 = types.KeyboardButton("📅 Прогноз")
    btn3 = types.KeyboardButton("📜 История")
    btn4 = types.KeyboardButton("⭐ Мой город")
    btn5 = types.KeyboardButton("ℹ️ Помощь")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    bot.send_message(
        message.chat.id,
        "🌍 Привет! Я Travel Assistant Bot.\n\n"
        "Выберите действие:",
        reply_markup=markup
    )


@bot.message_handler(commands=["help"])
def help_command(message):

    bot.send_message(
        message.chat.id,
        "📌 Доступные команды:\n\n"
        "/start - запуск бота\n"
        "/help - помощь\n"
        "/menu - меню\n"
        "/weather <город> - узнать погоду"
    )


@bot.message_handler(commands=["menu"])
def menu(message):

    bot.send_message(
        message.chat.id,
        "🌤 Меню:\n\n"
        "/weather <город>\n"
        "/forecast\n"
        "/history"
    )


@bot.message_handler(commands=["weather"])
def weather_command(message):

    text = message.text.split()

    if len(text) < 2:
        bot.send_message(
            message.chat.id,
            "❗Введите город.\n\n"
            "Пример:\n"
            "/weather Bishkek"
        )
        return

    city = " ".join(text[1:])

    


    answer = (
        f"🌤 Погода\n\n"
        f"📍 Город: {weather['city']}\n"
        f"🌍 Страна: {weather['country']}\n"
        f"🌡 Температура: {weather['temperature']}°C\n"
        f"💨 Ветер: {weather['wind']} км/ч\n"
        f"🕒 Последнее обновление: {weather['time']}\n\n"
        f"🤖 AI Совет\n\n"
        f"{advice}"
    )


    bot.send_message(
        chat_id,
        answer
    )


@bot.message_handler(func=lambda message: message.text == "🌤 Погода")
def weather_button(message):

    msg = bot.send_message(
        message.chat.id,
        "🏙️ Введите название города:"
    )

    bot.register_next_step_handler(
        msg,
        get_city_weather
    )


def get_city_weather(message):

    print("ПОЛУЧЕН ГОРОД:", message.text)

    city = message.text

    weather = get_weather(city)

    print("ОТВЕТ API:", weather)

    if weather is None:
        bot.send_message(
            message.chat.id,
            "❌ Город не найден."
        )
        return

    save_history(
        message.from_user.id,
        weather["city"],
        weather["temperature"]
    )

    answer = (
        f"🌤 Погода\n\n"
        f"📍 Город: {weather['city']}\n"
        f"🌍 Страна: {weather['country']}\n"
        f"🌡 Температура: {weather['temperature']}°C\n"
        f"💨 Ветер: {weather['wind']} км/ч\n"
        f"🕒 Обновление: {weather['time']}"
    )

    bot.send_message(
        message.chat.id,
        answer
    )


def get_city_forecast(message):

    city = message.text

    forecast = get_forecast(city)

    if forecast is None:

        bot.send_message(
            message.chat.id,
            "❌ Город не найден."
        )

        return


    answer = (
        f"📅 Прогноз погоды\n\n"
        f"📍 {forecast['city']}, {forecast['country']}\n\n"
    )


    for i in range(3):

        answer += (
            f"🗓 {forecast['dates'][i]}\n"
            f"☀️ Днём: {forecast['max'][i]}°C\n"
            f"🌙 Ночью: {forecast['min'][i]}°C\n\n"
        )


    bot.send_message(
        message.chat.id,
        answer
    )


@bot.message_handler(func=lambda message: message.text == "📅 Прогноз")
def forecast_button(message):

    msg = bot.send_message(
        message.chat.id,
        "🏙️ Введите город для прогноза:"
    )

    bot.register_next_step_handler(
        msg,
        get_city_forecast
    )


@bot.message_handler(func=lambda message: message.text == "ℹ️ Помощь")
def help_button(message):

    help_command(message)


@bot.message_handler(func=lambda message: message.text == "📜 История")
def history_button(message):

    history = get_history()

    user_history = []

    for item in history:
        if item["user_id"] == message.from_user.id:
            user_history.append(item)

    if not user_history:
        bot.send_message(
            message.chat.id,
            "📜 История пока пустая."
        )
        return

    text = "📜 Ваша история запросов:\n\n"

    for item in user_history[-5:]:
        text += (
            f"🏙 Город: {item['city']}\n"
            f"🌡 Температура: {item['temperature']}°C\n\n"
        )

    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler(commands=["favorite"])
def favorite_command(message):

    city = message.text.split()

    if len(city) < 2:
        bot.send_message(
            message.chat.id,
            "Пример:\n/favorite Bishkek"
        )
        return


    city = " ".join(city[1:])


    save_favorite(
        message.from_user.id,
        city
    )


    bot.send_message(
        message.chat.id,
           (f"⭐ Любимый город установлен:\n📍 {city}\n\nЧтобы изменить город, снова используйте /favorite"))
    





@bot.message_handler(func=lambda message: message.text == "⭐ Мой город")
def favorite_button(message):
    city = get_favorite(message.from_user.id)

    if city is None:
        bot.send_message(
            message.chat.id,
            "⭐ Любимый город не установлен.\nИспользуйте:\n/favorite Бишкек"
        )
        return

    bot.send_message(
        message.chat.id,
        f"⭐ Ваш любимый город: {city}"
    )





@bot.message_handler(commands=["clear"])
def clear_history_command(message):

    clear_history()

    bot.send_message(
        message.chat.id,
        "🗑 История очищена."
    )

print("Бот запущен!")

bot.infinity_polling()