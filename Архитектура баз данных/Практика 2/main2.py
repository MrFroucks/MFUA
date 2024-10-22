import sqlite3 as sq

db = sq.connect('database2.db')
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

# функция для получения городов, в которых часовой пояс меньше чем МСК. Таким образом можно понять какие города находятся западнее Москвы.
def get_western_city():
    moscow_time = c.execute('SELECT Часовой_пояс FROM RD4_Часовые_пояса WHERE Город = ?', ('Москва',)).fetchone() # получение часового пояса Москвы.
    moscow_time = moscow_time[0] # изменение типа переменной из кортежа в строку.
    return c.execute('SELECT Город FROM RD4_Часовые_пояса WHERE Часовой_пояс < ?', (moscow_time,)).fetchall() # привоение значения функции — города, в которых часовой пояс меньше чем у Москвы.
    
# функция для получения филиалов,которые находятся в городах, западнее Москвы.
def get_western_filials(western_city):
    res = [] # создание списка для сохранения полученных филиалов.
    for i in western_city: # цикл, который вытаскивает 1 город из списка, дальше работа проводится с ним.
        pod = c.execute('SELECT Название FROM RD3_Подразделения WHERE Город = ?', (i[0],)).fetchone() # получение филиала (i — список из кортежа -> мы должны передать город в строковом виде).
        res.append(pod[0]) # добавление полученного филиала в список.
    res = ', '.join(res) # перепиь полученного списка в строку, для более удобной работы.
    return res # привоение функции полученных филиалов.
    
def get_users_with_tasks(city):
    filials_id = c.execute('SELECT id FROM RD3_Подразделения WHERE Город = ?', (city,)).fetchall()
    q = []
    for i in filials_id:
        q.append('?')
    q = ', '.join(q)
    flat_filials_id = [j[0] for j in filials_id]
    users = c.execute(f'SELECT Номер FROM RD2_Пользователи WHERE Подразделение IN ({q})', flat_filials_id).fetchall()
    q = []
    for i in users:
        q.append('?')
    q = ', '.join(q)
    flat_users = [j[0] for j in users]
    res = c.execute(f'SELECT * FROM RD1_Задания WHERE Пользователь = ({q})', flat_users).fetchone()
    
    return user_with_task
        
def get_users_with_importment(ids):
    for i in ids:
        c.execute('')
    
# основная функция программы (входная точка программы).
def MAIN():
    western_city = get_western_city() # получение городов из функции.
    western_filials = get_western_filials(western_city) # получение филиалов из функции, по переданным городам.
    users_with_tasks = get_users_with_tasks('Москва')
    users_with_importment = get_users_with_importment(users_with_tasks)
    print(f'Филиалы, находящиеся западнее Москвы: {western_filials}') # вывод найденных филиалов.
    print(f'Пользователи со срочными заданиями, с таким же временем: {users_with_importment}')
    
# запуск программы.
if __name__ == '__main__':
    MAIN()