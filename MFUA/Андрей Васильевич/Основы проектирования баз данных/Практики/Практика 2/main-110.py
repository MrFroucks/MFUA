import sqlite3 as sq

db = sq.connect("database2.db")
c = db.cursor()

# создание необходимых таблиц для работы
c.execute('''
          CREATE TABLE IF NOT EXISTS RD1_Задания (
          id PRIMARY KEY UNIQUE,
          Текст TEXT,
          Пользователь INTERGER,
          Срочное INTEGER
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS RD2_Пользователи (
          Номер INTEGER UNIQUE,
          ФИО TEXT,
          Подразделение INTEGER
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS RD3_Подразделения (
          id PRIMARY KEY UNIQUE,
          Название TEXT,
          Город TEXT
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS RD4_Часовые_пояса (
          Город TEXT,
          Часовой_пояс INTEGER
          )
          ''')

# ----------------------------------
# РАБОТА С БД
# ----------------------------------
# id подразделений города
def get_filials_id(city):
    filials_id = c.execute('SELECT id FROM RD3_Подразделения WHERE Город = ?', (city,)).fetchall()
    filials_id = [j[0] for j in filials_id]
    return filials_id

# список пользователей из списка переданных филиалов
def get_users_id(filials_id):
    q = ['?' for j in filials_id]
    q = ', '.join(q) 
    users_id = c.execute(f'SELECT Номер FROM RD2_Пользователи WHERE Подразделение IN ({q})', filials_id).fetchall()
    users_id = [j[0] for j in users_id]
    return users_id

# список пользователей с заданиями
def get_users_with_tasks(users_id):
    q = ['?' for j in users_id]
    q = ', '.join(q)
    tasks = c.execute(f'SELECT Пользователь FROM RD1_Задания WHERE Пользователь IN ({q})', users_id).fetchall()
    tasks = list(set(map(str, [j[0] for j in tasks])))
    return tasks


# -----------------------
# ВХОДНАЯ ТОЧКА ПРОГРАММЫ
# -----------------------
def MAIN():
    city = 'Москва'
    filials_id = get_filials_id(city)
    users_id = get_users_id(filials_id)
    users_with_tasks = get_users_with_tasks(users_id)
    print(f'Пользователи из Москвы с заданиями: {', '.join(users_with_tasks)}')
    


if __name__ == '__main__':
    MAIN()