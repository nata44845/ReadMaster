import os
import sqlite3

DB_PATH = 'knowledge.db'
DOCS_DIR = 'docs'

# Создание базы данных и таблицы с поддержкой полнотекстового поиска
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id NOT NULL PRIMARY_KEY IDENTITY(1,1) 
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NULL
)
''')

conn.commit()
conn.close()
print('Импорт завершён.') 