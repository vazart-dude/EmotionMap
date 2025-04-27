class User():
    def __init__(self):
        self.id = None
        self.login = ''
        self.password = ''
        self.email = ''

    def add_user(self, login, password, email):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Создание таблицы, если она не существует
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
        ''')

        # Проверка, существует ли уже пользователь с таким логином
        cursor.execute('SELECT * FROM users WHERE login = ?', (login))
        existing_user = cursor.fetchone()

        if existing_user is None:
            # Если пользователь не существует, добавляем нового
            cursor.execute('INSERT INTO users (login, password, email) VALUES (?, ?, ?)', (login, password, email))
            conn.commit()

            # Закрываем соединение
            conn.close()

            return True  # Пользователь добавлен
        else:
            # Если пользователь существует
            conn.close()
            return False  # Пользователь не добавлен