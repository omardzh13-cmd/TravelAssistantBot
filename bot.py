import telebot
from telebot import types

from config import TOKEN

from database import (
    save_history,
    get_history,
    clear_history,
    save_favorite,
    get_favorite,
    get_stats
)

from weather import get_weather, get_forecast


bot = telebot.TeleBot(TOKEN)


# =========================
# КОМАНДЫ БОТА
# =========================

def set_commands():

    commands = [
        telebot.types.BotCommand("start", "Запуск бота"),
        telebot.types.BotCommand("help", "Помощь"),
        telebot.types.BotCommand("menu", "Меню"),
        telebot.types.BotCommand("weather", "Погода"),
        telebot.types.BotCommand("forecast", "Прогноз"),
        telebot.types.BotCommand("history", "История"),
        telebot.types.BotCommand("favorite", "Любимый город"),
        telebot.types.BotCommand("stats", "Статистика"),
        telebot.types.BotCommand("clear", "Очистить историю")
    ]

    try:
        bot.set_my_commands(commands)
        print("Команды установлены!")

    except Exception as error:
        print("Команды пока не установлены.")
# =========================
# КЛАВИАТУРА
# =========================

def create_menu():

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.add(
        types.KeyboardButton("🌤 Погода"),
        types.KeyboardButton("📅 Прогноз")
    )

    markup.add(
        types.KeyboardButton("📜 История"),
        types.KeyboardButton("⭐ Мой город")
    )

    markup.add(
        types.KeyboardButton("ℹ️ Помощь"),
        types.KeyboardButton("🗑 Очистить историю")
    )

    markup.add(
        types.KeyboardButton("📊 Статистика")
    )

    return markup


# =========================
# START
# =========================

@bot.message_handler(commands=["start"])
def start(message):

    bot.send_message(
        message.chat.id,
        "🌍 Привет! Я Travel Assistant Bot.\n\n"
        "Выберите действие:",
        reply_markup=create_menu()
    )


# =========================
# HELP
# =========================

@bot.message_handler(commands=["help"])
def help_command(message):

    bot.send_message(
        message.chat.id,
        "📌 Доступные команды:\n\n"
        "/start — запуск бота\n"
        "/help — помощь\n"
        "/menu — меню\n"
        "/weather — погода\n"
        "/forecast — прогноз\n"
        "/history — история\n"
        "/favorite — любимый город\n"
        "/stats — статистика\n"
        "/clear — очистить историю"
    )


# =========================
# MENU
# =========================

@bot.message_handler(commands=["menu"])
def menu_command(message):

    start(message)


# =========================
# ПОГОДА
# =========================

@bot.message_handler(commands=["weather"])
def weather_command(message):

    parts = message.text.split()

    if len(parts) < 2:

        bot.send_message(
            message.chat.id,
            "❗Напишите город.\n\n"
            "Пример:\n"
            "/weather Bishkek"
        )

        return

    city = " ".join(parts[1:])

    send_weather(message, city)


@bot.message_handler(
    func=lambda message: message.text == "🌤 Погода"
)
def weather_button(message):

    msg = bot.send_message(
        message.chat.id,
        "🏙️ Введите название города:"
    )

    bot.register_next_step_handler(
        msg,
        weather_from_text
    )


def weather_from_text(message):

    city = message.text.strip()

    send_weather(message, city)


def send_weather(message, city):

    weather = get_weather(city)

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

    text = (
        f"🌤 Погода\n\n"
        f"📍 Город: {weather['city']}\n"
        f"🌍 Страна: {weather['country']}\n"
        f"🌡 Температура: {weather['temperature']}°C\n"
        f"💨 Ветер: {weather['wind']} км/ч\n"
        f"🕒 Обновление: {weather['time']}"
    )

    bot.send_message(
        message.chat.id,
        text
    )


# =========================
# ПРОГНОЗ
# =========================

@bot.message_handler(
    func=lambda message: message.text == "📅 Прогноз"
)
def forecast_button(message):

    msg = bot.send_message(
        message.chat.id,
        "🏙️ Введите город для прогноза:"
    )

    bot.register_next_step_handler(
        msg,
        forecast_from_text
    )


@bot.message_handler(commands=["forecast"])
def forecast_command(message):

    parts = message.text.split()

    if len(parts) < 2:

        bot.send_message(
            message.chat.id,
            "❗Напишите город.\n\n"
            "Пример:\n"
            "/forecast Bishkek"
        )

        return

    city = " ".join(parts[1:])

    send_forecast(message, city)


def forecast_from_text(message):

    city = message.text.strip()

    send_forecast(message, city)


def send_forecast(message, city):

    forecast = get_forecast(city)

    if forecast is None:

        bot.send_message(
            message.chat.id,
            "❌ Город не найден."
        )

        return

    text = (
        f"📅 Прогноз погоды\n\n"
        f"📍 {forecast['city']}, {forecast['country']}\n\n"
    )

    for i in range(min(3, len(forecast["dates"]))):

        text += (
            f"🗓 {forecast['dates'][i]}\n"
            f"☀️ Днём: {forecast['max'][i]}°C\n"
            f"🌙 Ночью: {forecast['min'][i]}°C\n\n"
        )

    bot.send_message(
        message.chat.id,
        text
    )


# =========================
# ИСТОРИЯ
# =========================

@bot.message_handler(commands=["history"])
def history_command(message):

    show_history(message)


@bot.message_handler(
    func=lambda message: message.text == "📜 История"
)
def history_button(message):

    show_history(message)


def show_history(message):

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


# =========================
# ЛЮБИМЫЙ ГОРОД
# =========================

@bot.message_handler(commands=["favorite"])
def favorite_command(message):

    parts = message.text.split()

    if len(parts) < 2:

        bot.send_message(
            message.chat.id,
            "❗Напишите город.\n\n"
            "Пример:\n"
            "/favorite Bishkek"
        )

        return

    city = " ".join(parts[1:])

    save_favorite(
        message.from_user.id,
        city
    )

    bot.send_message(
        message.chat.id,
        f"⭐ Любимый город установлен:\n"
        f"📍 {city}"
    )


@bot.message_handler(
    func=lambda message: message.text == "⭐ Мой город"
)
def favorite_button(message):

    city = get_favorite(
        message.from_user.id
    )

    if city is None:

        bot.send_message(
            message.chat.id,
            "⭐ Любимый город не установлен.\n\n"
            "Используйте:\n"
            "/favorite Bishkek"
        )

        return

    send_weather(
        message,
        city
    )


# =========================
# ОЧИСТКА ИСТОРИИ
# =========================

@bot.message_handler(commands=["clear"])
def clear_command(message):

    clear_history()

    bot.send_message(
        message.chat.id,
        "🗑 История очищена."
    )


@bot.message_handler(
    func=lambda message: message.text == "🗑 Очистить историю"
)
def clear_button(message):

    clear_history()

    bot.send_message(
        message.chat.id,
        "🗑 История очищена."
    )


# =========================
# СТАТИСТИКА
# =========================

@bot.message_handler(commands=["stats"])
def stats_command(message):

    count = get_stats()

    bot.send_message(
        message.chat.id,
        f"📊 Всего запросов погоды: {count}"
    )


@bot.message_handler(
    func=lambda message: message.text == "📊 Статистика"
)
def stats_button(message):

    count = get_stats()

    bot.send_message(
        message.chat.id,
        f"📊 Всего запросов погоды: {count}"
    )


# =========================
# ПОМОЩЬ КНОПКОЙ
# =========================

@bot.message_handler(
    func=lambda message: message.text == "ℹ️ Помощь"
)
def help_button(message):

    help_command(message)


# =========================
# ЗАПУСК
# =========================
set_commands()

print("Бот запущен!")

bot.infinity_polling(
    skip_pending=True
)