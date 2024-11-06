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
    
# функция для получения пользователей с заданиями из Москвы.
def get_moscow_users_with_tasks(city):
    filials_id = c.execute('SELECT id FROM RD3_Подразделения WHERE Город = ?', (city,)).fetchall() # получение id подразделений, для поиска прикреплённых к ним пользователей.
    q = [] # создание списка, для записи нужного количества символов '?'.
    for i in filials_id: # цикл для для определения количества полученных id и создания такого же количества символов '?'.
        q.append('?')
    q = ', '.join(q) # перепись полученного списка в строку.
    flat_filials_id = [j[0] for j in filials_id] # перепись кортежа id в список, для правильной передачи в SQL.
    users = c.execute(f'SELECT Номер FROM RD2_Пользователи WHERE Подразделение IN ({q})', flat_filials_id).fetchall() # получение пользователей, прикреплённых к подразделениям по id.
    q = [] # повторение предыдущих операций для получения заданий у пользователей.
    for i in users:
        q.append('?')
    q = ', '.join(q)
    flat_users = [j[0] for j in users]
    tasks = c.execute(f'SELECT Текст FROM RD1_Задания WHERE Пользователь IN ({q})', flat_users).fetchall()
    flat_tasks = [j[0] for j in tasks]
    q = [] # повторение предыдущих операций для получения пользователей с заданиями
    for i in flat_tasks:
        q.append('?')
    q = ', '.join(q)
    user_with_task = c.execute(f'SELECT Пользователь FROM RD1_Задания WHERE Текст IN ({q})', flat_tasks).fetchall()
    flat_user_with_task = [j[0] for j in user_with_task]
    flat_user_with_task = list(set(map(str, flat_user_with_task))) # удаление повторений в полученном списке
    user_with_task = ', '.join(flat_user_with_task)
    return user_with_task
    
# def get_users_time(time, users):
#     q = []
#     for i in users:
#         q.append('?')
#     q = ', '.join(q)
#     users_filials = c.execute(f'SELECT Подразделение FROM RD2_Пользователи WHERE Номер IN ({q})', users).fetchall()
#     q = []
#     for i in users_filials:
#         q.append('?')
#     q = ', '.join(q)
#     flat_users_filials = [j[0] for j in users_filials]
#     filials_city = c.execute(f'SELECT Город FROM RD3_Подразделения WHERE id IN ({q})', flat_users_filials).fetchall()
#     flat_filials_city = [j[0] for j in filials_city]
#     city_time = c.execute(f'SELECT Часовой_пояс FROM RD4_Часовые_пояса WHERE Город IN ({q})', flat_filials_city).fetchall()
#     flat_city_time = [j[0] for j in city_time if j[0] == 4]
    
#     filials = c.execute('SELECT id FROM RD3_Подразделения WHERE Город IN (?, ?)', flat_city_time).fetchall()
#     flat_filials = [j[0] for j in filials]
#     print(flat_filials)
#     users_with_moscow_time = c.execute('SELECT Номер FROM RD2_Пользователи WHERE Подразделение IN ()')
    

def get_users_with_importment(time):
    users = c.execute('SELECT Пользователь FROM RD1_Задания WHERE Срочное = ?', (1,)).fetchall()
    users = [j[0] for j in users]
    users = list(set(map(str, users)))
    users = ', '.join(users)
    return users
    

# основная функция программы (входная точка программы).
def MAIN():
    western_city = get_western_city() # получение городов из функции.
    western_filials = get_western_filials(western_city) # получение филиалов из функции, по переданным городам.
    moscow_users_with_tasks = get_moscow_users_with_tasks('Москва')
    time = 3
    users_with_importment = get_users_with_importment(time)
    print(f'Подразделения, находящиеся западнее Москвы: {western_filials}') # вывод найденных филиалов.
    print(f'Пользователи с заданиями: {moscow_users_with_tasks}')
    print(f'Пользователи со срочными заданиями: {users_with_importment}')
    
# запуск программы.
if __name__ == '__main__':
    MAIN()