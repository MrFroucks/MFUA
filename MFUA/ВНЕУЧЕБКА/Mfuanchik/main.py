import telebot
import sqlite3 as sq
from telebot import types
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton

# определение переменных для работы с ботом
API_TOKEN = '7291353629:AAG0Y0mK93dQ2hPcEQLnmzsbhqBAXtL7JgE'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

# определение переменных дб
db = sq.connect('database.db', check_same_thread=False)
c = db.cursor()

# создание таблицы в дб
c.execute('''
          CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY,
          user_name TEXT,
          mfua TEXT,
          name TEXT,
          desc TEXT,
          photo TEXT
          )
          ''')

# получение id пользователя и проверка на наличие пользователя в бд
def get_user(user_id):
    result = c.execute('SELECT * FROM users WHERE telegram = ?', (user_id,)).fetchall()
    return bool(len(result))


@bot.message_handler(commands=['start'])
def START(message):
    user_id = message.from_user.id
    user_name = message.from_user.username 
    chat_id = message.chat.id

    if get_user(user_id):
        keyboard = InlineKeyboardMarkup()
        buttons = {
            InlineKeyboardButton(text = 'Калужский' )

        }
    else:
        bot.reply_to(message, f'Ваше имя пользователя: @{user_name}')  # Отправляем имя пользователя

if __name__ == '__main__':
    bot.polling()