import telebot
from config import TOKEN
from weather import get_weather

bot = telebot.TeleBot(TOKEN)


# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌍 Привет! Я Travel Assistant Bot.\n\n"
        "Я помогу узнать погоду и подготовиться к путешествию."
    )


# Команда /help
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


# Команда /menu
@bot.message_handler(commands=["menu"])
def menu(message):
    bot.send_message(
        message.chat.id,
        "🌤 Меню:\n\n"
        "/weather <город>\n"
        "/forecast\n"
        "/history"
    )


# Команда /weather
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

    weather = get_weather(city)

    if weather is None:
        bot.send_message(
            message.chat.id,
            "❌ Город не найден."
        )
        return

    answer = (
        f"🌤 Погода\n\n"
        f"📍 Город: {weather['city']}\n"
        f"🌍 Страна: {weather['country']}\n"
        f"🌡 Температура: {weather['temperature']}°C\n"
        f"💨 Ветер: {weather['wind']} км/ч\n"
        f"🕒 Последнее обновление: {weather['time']}"
    )

    bot.send_message(message.chat.id, answer)


print("Бот запущен!")

bot.infinity_polling()