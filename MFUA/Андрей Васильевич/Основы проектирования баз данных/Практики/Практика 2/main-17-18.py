import sqlite3 as sq # импорт библиотеки для работы с sqlite

db = sq.connect('database.db') # подключение базы данных
c = db.cursor() # создание курсора для обращения к языку SQL

# создание базы данных R10
c.execute('''
          CREATE TABLE IF NOT EXISTS R10 (
          Артикул INTEGER,
          Товар TEXT,
          Склад TEXT
          )
          ''')

# создание базы данных R12
c.execute('''
          CREATE TABLE IF NOT EXISTS R12 (
          Артикул INTEGER,
          Товар TEXT,
          Склад TEXT
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS R14 (
          Склад TEXT
          )
          ''')


# функция, добавляющая новый товар в таблицу R12
def add_in_R12(art, product, base):
    c.execute('INSERT INTO R12 (Артикул, Товар, Склад) VALUES (?, ?, ?)',(art, product, base))
    db.commit()

all_lines = c.execute('SELECT * FROM R10 WHERE Артикул = ?', (5,)).fetchall() # получение всех строк с артиклом 5
for i in all_lines: # цикл, разделяющий полученный кортеж на списки. Каждый список — полученная строчка таблицы
    add_in_R12(i[0], i[1], i[2]) # передача в функцию для добавления строк артикла, товара и склада, взятые из разделённых списков

# функция добавляющая склады в таблицу R14
def add_in_R14(base):
    c.execute('INSERT INTO R14 (Склад) VALUES (?)', (base))
    db.commit()

bases = c.execute('SELECT Склад FROM R10 WHERE Товар = ?', ('Колонки SVEN',)).fetchall() # получение складов, где лежит товар Колонки SVEN
for j in bases: # цикл, разделяющий полученный кортеж на отдельные элементы. Элементы кортежа — все полученные склады
    add_in_R14(j) # передача складов в функцию для добавления в таблицу R14