import sqlite3
from fastapi import HTTPException


class Database:

    def __init__(self, db_name : str = "user.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        self.__connect()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        ''')
        self.connection.commit()
        self.__close()

    def add_user(self, username : str, password : str):
        self.__connect()
        try:
            self.cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
        finally:
            self.__close()

    def get_user_by_username(self, username: str):
        self.__connect()
        self.cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        tmp = self.cursor.fetchone()
        self.__close()
        return tmp

    def __connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def __close(self):
        self.connection.close()