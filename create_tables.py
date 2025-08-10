import os
import sqlite3

DB_PATH = 'knowledge.db'
DOCS_DIR = 'docs'

# Создание базы данных и таблицы с поддержкой полнотекстового поиска
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# users

c.execute('''
DROP TABLE IF EXISTS users;
''')

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(32) NOT NULL,
    passw varchar(32) NOT NULL,
    role varchar(10) NOT NULL,
    admin int(11) DEFAULT NULL,
    name varchar(64) DEFAULT NULL
);   
''')

c.execute('''
INSERT INTO users (login, passw, role, admin, name)
VALUES("admin","admin","superadmin",NULL,NULL) 
''')

# documents

c.execute('''
DROP TABLE IF EXISTS documents;
''')

c.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NULL
);   
''')

c.execute('''
SELECT * FROM users
''')

docs = c.fetchall()
for doc in docs:
    lines = str(doc[0])+' '+str(doc[1])
    print(lines)

conn.commit()
conn.close()
print('Импорт завершён.') 