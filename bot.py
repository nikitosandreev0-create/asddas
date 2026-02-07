import telebot
from telebot import types
import google.generativeai as genai
import os

# Берем ключи из настроек сервера (Environment Variables)
# Если еще не настроил их там, можешь временно вписать строкой
TG_TOKEN = os.getenv('TG_TOKEN', 'ТВОЙ_ТОКЕН_ТУТ')
GEMINI_KEY = os.getenv('GEMINI_KEY', 'ТВОЙ_КЛЮЧ_ТУТ')

genai.configure(api_key=GEMINI_KEY)
bot = telebot.TeleBot(TG_TOKEN)

roles = {
    "school": "Ты помощник по учебе. Объясняй понятно.",
    "funny": "Ты комик, шути в каждом сообщении.",
    "default": "Ты вежливый ИИ помощник."
}

user_modes = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏫 Школа", "🤡 Юмор", "🤖 Обычный")
    bot.send_message(message.chat.id, "Выбери режим:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def chat(message):
    if message.text == "🏫 Школа":
        user_modes[message.chat.id] = roles["school"]
        bot.reply_to(message, "Режим школы включен!")
        return
    
    # ... тут остальные проверки кнопок ...

    current_role = user_modes.get(message.chat.id, roles["default"])
    try:
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=current_role)
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Ошибка API. Попробуй позже.")

# Запуск
print("Бот запущен...")
bot.infinity_polling() # Этот метод лучше для серверов, он сам перезапускается
