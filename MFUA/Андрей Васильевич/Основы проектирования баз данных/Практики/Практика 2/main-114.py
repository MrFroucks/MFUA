import sqlite3 as sq

db = sq.connect(r"C:\Users\User\Documents\MFUA\MFUA\Андрей Васильевич\Основы проектирования баз данных\Практики\Практика 2\database6.db")
c = db.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS S_1 (
          id INTEGER PRIMARY KEY UNIQUE,
          Фамилия TEXT
          )
          ''')

def get_users():
    users_words = {}
    users = c.execute('SELECT id, ФИО FROM R1 WHERE Оценка = 5').fetchall()
    for i, j in users:
        one, two, three = j.split(' ')
        users_words[i] = one
    return users_words
    
def add_users(users):
    for i in users:
        id = i
        name = users[id]
        c.execute('INSERT INTO S_1 (id, Фамилия) VALUES (?, ?)', (id, name,))
        db.commit()

def MAIN():
    users = get_users()
    add_users(users)

if __name__ == '__main__':
    MAIN()