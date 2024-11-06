import telebot
import sqlite3
from datetime import datetime, timedelta

# создание бот аи подключение токена
bot = telebot.TeleBot('1907307089:AAFzpiKk_n9rDCcpPmYNn4__6mPsbG8kvWg')

# подключение бд и создание курсора
db = sqlite3.connect('database.db', check_same_thread=False)
c = db.cursor()

# ---------------------
# РАБОТА С БАЗОЙ ДАННЫХ
# ---------------------
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram TEXT,
    name TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS studes (
    id INTEGER PRIMARY KEY,
    telegram TEXT,
    name TEXT,
    boolean INTEGER,
    date TEXT          
)
''')

# получение id пользователя и проверка на наличие пользователя в бд
def get_user(telegram):
    result = c.execute('SELECT * FROM users WHERE telegram = ?', (telegram,)).fetchall()
    return bool(len(result))

# получение id пользователя и имени, добавление в бд пользователей
def add_user(telegram, name):
    c.execute('INSERT INTO users (telegram, name) VALUES (?, ?)', (telegram, name))
    db.commit()

def save_name(message):
    user_id = message.from_user.id
    name = message.text  # Получение ФИО от пользователя
    add_user(user_id, name)  # Добавление пользователя в базу данных
    welcome(message)

def get_bool(name):
    boolean = c.execute('SELECT boolean FROM studes WHERE name = ?', (name,)).fetchone()  # Исправлено на кортеж
    return boolean[0] if boolean else None

def get_date(name):
    date = c.execute('SELECT date FROM studes WHERE name = ?', (name,)).fetchone()
    return date[0] if date else None

def all_names():
    l = {}
    names = c.execute('SELECT name FROM studes').fetchall()
    for index, name in enumerate(names, start=1):
        boolean = get_bool(name[0])
        if boolean == 0:
            boolean = '❌'
        elif boolean == 1:
            boolean = '✅'
        elif boolean == 2:
            date = get_date(name[0])
            days_left = (datetime.strptime(date, '%Y-%m-%d') - datetime.now()).days
            boolean = f'📃 ({days_left} дней, до {datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")})'

        l[f'{index}. {name[0]}'] = boolean
    output = '\n'.join(f'{key} — {value}' for key, value in l.items())
    return output

def update_status(name, status):
    if status == 2:
        current_date = c.execute('SELECT date FROM studes WHERE name = ?', (name,)).fetchone()
        if current_date and current_date[0]:
            new_date = (datetime.strptime(current_date[0], '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
        else:
            new_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        c.execute('UPDATE studes SET boolean = ?, date = ? WHERE name = ?', (status, new_date, name))
    else:
        c.execute('UPDATE studes SET boolean = ?, date = NULL WHERE name = ?', (status, name))  # Очистка столбца date
    db.commit()

# Хранение идентификаторов сообщений
message_ids = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id == 6665977826:
        keyboard = telebot.types.InlineKeyboardMarkup()  # Изменено на InlineKeyboardMarkup
        button_save = telebot.types.InlineKeyboardButton(
            text="Редактировать список", callback_data='edit')  # Добавлен callback_data
        keyboard.add(button_save)
        sent_message = bot.send_message(chat_id, f'❗️СПИСОК СТУДЕНТОВ❗️\n\n{all_names()}', reply_markup=keyboard)
        message_ids[chat_id] = sent_message.message_id
    elif user_id != 6665977826:
        if not get_user(user_id):
            sent_message = bot.send_message(chat_id, 'Для регистрации, напишите ФИО.')
            bot.register_next_step_handler(message, save_name)  # Ожидание следующего ввода
            message_ids[chat_id] = sent_message.message_id
        else:
            print(user_id)
            sent_message = bot.send_message(chat_id, 'Добро пожаловать в бота 05ИПо9481.')
            message_ids[chat_id] = sent_message.message_id

@bot.callback_query_handler(func=lambda call: call.data == 'edit')
def edit(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)  # Ответ на callback-запрос
    if chat_id in message_ids:
        bot.delete_message(chat_id, message_ids[chat_id])
    keyboard = telebot.types.InlineKeyboardMarkup()
    names = c.execute('SELECT name FROM studes').fetchall()
    for name in names:
        name = name[0]
        keyboard.add(
            telebot.types.InlineKeyboardButton(text=name, callback_data=f'select_{name}')
        )
    sent_message = bot.send_message(chat_id, 'Выберите студента', reply_markup=keyboard)
    message_ids[chat_id] = sent_message.message_id

@bot.callback_query_handler(func=lambda call: call.data.startswith('select_'))
def select_student(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)  # Ответ на callback-запрос
    if chat_id in message_ids:
        bot.delete_message(chat_id, message_ids[chat_id])
    name = call.data.split('_')[1]
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(text='❌', callback_data=f'edit_{name}_0'),
        telebot.types.InlineKeyboardButton(text='✅', callback_data=f'edit_{name}_1'),
        telebot.types.InlineKeyboardButton(text='📃', callback_data=f'edit_{name}_2')
    )
    sent_message = bot.send_message(chat_id, f'Выберите статус для {name}', reply_markup=keyboard)
    message_ids[chat_id] = sent_message.message_id

@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_'))
def edit_status(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)  # Ответ на callback-запрос
    if chat_id in message_ids:
        bot.delete_message(chat_id, message_ids[chat_id])
    data = call.data.split('_')
    name = data[1]
    status = int(data[2])
    update_status(name, status)
    keyboard = telebot.types.InlineKeyboardMarkup()  # Изменено на InlineKeyboardMarkup
    button_save = telebot.types.InlineKeyboardButton(
        text="Редактировать список", callback_data='edit')  # Добавлен callback_data
    keyboard.add(button_save)
    sent_message = bot.send_message(chat_id, f'❗️СПИСОК СТУДЕНТОВ❗️\n\n{all_names()}',reply_markup=keyboard)
    message_ids[chat_id] = sent_message.message_id

@bot.callback_query_handler(func=lambda call: call.data == 'say_stop')
def handle_support(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)  # Ответ на callback-запрос
    if chat_id in message_ids:
        bot.delete_message(chat_id, message_ids[chat_id])
    bot.send_message(chat_id, 'Вы нажали на кнопку "Стоп".')

if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()