import telebot
import sqlite3

# создание бот аи подключение токена
bot = telebot.TeleBot('1907307089:AAFzpiKk_n9rDCcpPmYNn4__6mPsbG8kvWg')

# подключение бд и создание курсора
db = sqlite3.connect('database.db',check_same_thread=False)
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


def get_user(telegram):
    result = c.execute('SELECT * FROM users WHERE telegram = ?',(telegram,)).fetchall()
    return bool(len(result))


def add_user(telegram,name):
    c.execute('INSERT INTO users (telegram, name) VALUES (?, ?)',(telegram,name))
    db.commit()


def save_name(message):
    user_id = message.from_user.id
    name = message.text  # Получение ФИО от пользователя
    add_user(user_id, name)  # Добавление пользователя в базу данных
    welcome(message)


def get_bool(name):
    boolean = c.execute('SELECT boolean FROM studes WHERE name = ?', (name,)).fetchone()  # Исправлено на кортеж
    return boolean[0] if boolean else None


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
            boolean = '📃'

        l[f'{index}. {name[0]}'] = boolean
    output = '\n'.join(f'{key} — {value}' for key,value in l.items())
    return output




@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id == 6665977826:
        keyboard = telebot.types.InlineKeyboardMarkup()  # Изменено на InlineKeyboardMarkup
        button_save = telebot.types.InlineKeyboardButton(
            text="Редактировать список", callback_data='edit')  # Добавлен callback_data
        keyboard.add(button_save)
        bot.send_message(chat_id, f'❗️СПИСОК СТУДЕНТОВ❗️\n\n{all_names()}', reply_markup=keyboard)
    elif user_id != 6665977826:
        if not get_user(user_id):
            bot.send_message(chat_id,
                             'Для регистрации, напишите ФИО.')
            bot.register_next_step_handler(message, save_name)  # Ожидание следующего ввода
        else:
            print(user_id)
            bot.send_message(chat_id,
                             'Добро пожаловать в бота 05ИПо9481.',
                             )



@bot.callback_query_handler(func=lambda call: call.data == 'edit')
def edit(call):
    chat_id = call.message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = {
        telebot.types.InlineKeyboardButton(text='1',callback_data='1'),
        telebot.types.InlineKeyboardButton(text='2',callback_data='2'),
        telebot.types.InlineKeyboardButton(text='3',callback_data='3'),
        telebot.types.InlineKeyboardButton(text='4',callback_data='4'),
        telebot.types.InlineKeyboardButton(text='5',callback_data='5'),
        telebot.types.InlineKeyboardButton(text='6',callback_data='6'),
        telebot.types.InlineKeyboardButton(text='7',callback_data='7')
    }
    keyboard.add(buttons)
    bot.send_message(chat_id, 'Требуется номер студента',reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data == 'say_stop')
def handle_support(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Вы нажали на кнопку "Стоп".')



if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()