import sqlite3 as sq

db = sq.connect(r"C:\Users\User\Documents\MFUA\MFUA\Андрей Васильевич\Основы проектирования баз данных\Практики\Практика 2\database5.db")
c = db.cursor()

# создание базы данных R9
c.execute('''
          CREATE TABLE IF NOT EXISTS R9 (
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
          CREATE TABLE IF NOT EXISTS R8 (
              Склад TEXT
          )
          ''')

def get_product_and_id():
    product_and_id = {}
    words = c.execute('SELECT * FROM R7').fetchall()
    for i, j in words:
        product_and_id[i] = j
    return product_and_id

def get_all_stories():
    all_stories = c.execute('SELECT Склад FROM R8').fetchall()
    all_stories = [j[0] for j in all_stories]
    return all_stories

def add_product_and_id(product_and_id, all_stories):
    for j in all_stories:
        for i in product_and_id:
            store = j
            product_id = i
            product = product_and_id[product_id]
            c.execute('INSERT INTO R9 (Артикул, Товар, Склад) VALUES (?, ?, ?)', (product_id, product, store,))        
    db.commit()
    
    
def MAIN():
    product_and_id = get_product_and_id()
    all_stories = get_all_stories()
    add_product_and_id(product_and_id, all_stories)


if __name__ == '__main__':
    MAIN()