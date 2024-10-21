import sqlite3 as sq

db = sq.connect('database2.db')
c = db.cursor()

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