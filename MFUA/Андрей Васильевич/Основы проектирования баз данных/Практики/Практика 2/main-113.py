import sqlite3 as sq

db = sq.connect(r"C:\Users\User\Documents\MFUA\MFUA\Андрей Васильевич\Основы проектирования баз данных\Практики\Практика 2\database4.db")
c = db.cursor()

# создание базы данных R10
c.execute('''
          CREATE TABLE IF NOT EXISTS R10 (
          Артикул INTEGER,
          Товар TEXT,
          Склад TEXT
          )
          ''')

# создание базы данных R7
c.execute('''
          CREATE TABLE IF NOT EXISTS R7 (
          Артикул INTEGER UNIQUE,
          Товар TEXT UNIQUE
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS R17 (
              Склад TEXT
          )
          ''')

def get_product_id():
    product_id = c.execute('SELECT Артикул FROM R7').fetchall()
    product_id = [j[0] for j in product_id]
    return product_id

def get_store(product_id):
    q = ['?' for j in product_id]
    q = ', '.join(q)
    store = c.execute(f'SELECT Склад FROM R10 WHERE Артикул IN ({q})', product_id).fetchall()
    store = [j[0] for j in store]
    return list(set(store))
    
def add_store(store):
    for i in store:
        c.execute('INSERT INTO R17 (Склад) VALUES (?)', (i,))
    db.commit()
    
def MAIN():
    product_id = get_product_id()
    store = get_store(product_id)
    add_store(store)


if __name__ == '__main__':
    MAIN()