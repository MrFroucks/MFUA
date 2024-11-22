import sqlite3 as sq

db = sq.connect(r"C:\Users\User\Documents\MFUA\MFUA\Андрей Васильевич\Основы проектирования баз данных\Практики\Практика 2\database3.db")
c = db.cursor()

# создание базы данных R10
c.execute('''
          CREATE TABLE IF NOT EXISTS R10 (
          Артикул INTEGER,
          Товар TEXT,
          Склад TEXT
          )
          ''')

# создание базы данных R15
c.execute('''
          CREATE TABLE IF NOT EXISTS R15 (
          Артикул INTEGER UNIQUE,
          Товар TEXT UNIQUE,
          Упаковка TEXT
          )
          ''')

def get_OEM_id():
    OEM_id = c.execute('SELECT Артикул FROM R15 WHERE Упаковка = ?', ('OEM',)).fetchall()
    OEM_id = [j[0] for j in OEM_id]
    return OEM_id


def get_product(OEM_id, store):
    q = ['?' for j in OEM_id]
    q = ', '.join(q)
    product_id = c.execute(f'SELECT Товар FROM R10 WHERE Артикул IN ({q}) AND Склад = ?', (*OEM_id, store)).fetchall() # символ * у OEM_id укажет execute, что сначала нужно обработать все элементы этого списка, а потиом уже передавать в Склад переменную store
    product_id = [j[0] for j in product_id]
    return product_id


def MAIN():
    OEM_id = get_OEM_id()
    store = 'Cклад 1'
    product = get_product(OEM_id, store) 
    print(f'Все товары на складе 1 в упаковке OEM: {', '.join(product)}')


if __name__ == '__main__':
    MAIN()