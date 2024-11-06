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
# СПИСОК ГОРОДОВ И ИХ ЧАСОВЫХ ПОЯСОВ
# ----------------------------------
def get_cities_timezones():
    cities_timezones = {}
    all_cities_timezones = c.execute('SELECT * FROM RD4_Часовые_пояса').fetchall()
    for i, j in all_cities_timezones:
        cities_timezones[i] = j
    return cities_timezones

# получение часового пояса города
def get_city_timezone(city):
    city_timezone = get_cities_timezones()
    getting_city_timezone = city_timezone[city]
    return getting_city_timezone

# получение списка городов, которые находятся западнее передаваемого города
def check_western_cities(city_timezone):
    western_cities = c.execute('SELECT Город FROM RD4_Часовые_пояса WHERE Часовой_пояс < ?', (city_timezone,)).fetchall()
    western_cities = [i[0] for i in western_cities]
    return western_cities

# получение подразделений из города
def get_filials(cities):
    l = []
    for i in cities:
        l.append('?')
    q = ', '.join(l)
    filials_from_cities = c.execute(f'SELECT Название FROM RD3_Подразделения WHERE Город IN ({q})', (cities)).fetchall()
    filials_from_cities = [j[0] for j in filials_from_cities]
    return filials_from_cities



# -----------------------
# ВХОДНАЯ ТОЧКА ПРОГРАММЫ
# -----------------------
def MAIN():
    city = 'Москва'
    getting_city_timezone = get_city_timezone(city)
    western_cities = check_western_cities(getting_city_timezone)
    filials = get_filials(western_cities)
    print(f'Подразделения, находяшиеся западнее Москвы: {', '.join(filials)}')
    


if __name__ == '__main__':
    MAIN()