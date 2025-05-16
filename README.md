# EmotionMap 🌍


![Бейджи](https://img.shields.io/badge/Статус-В%20разработке-yellow) 
![Версия](https://img.shields.io/badge/Версия-0.0.1--preview-blue)

EmotionMap - это веб-приложение, позволяющее пользователям отмечать на карте места, связанные с их эмоциями и воспоминаниями. Проект создан с использованием Flask и современных веб-технологий.

## 📖 Оглавление
- [Основные возможности](#-основные-возможности)
- [Технологии](#-технологии)
- [Установка и запуск](#-установка-и-запуск)
- [Развертывание на хостинге](#-развертывание-на-хостинге)
- [Структура](#-структура-проекта)
- [Безопастность](#-безопасность)
- [Команда](#-команда)

---

## ✨ Основные возможности

- 🔐 Регистрация и авторизация пользователей
- 📍 Добавление маркеров с описанием эмоций и воспоминаний
- 🗺️ Интерактиваня карта с историей метс и эмоций
- 👤 Личный профиль пользователя
- 📱 Адаптивный дизайн

## 🛠 Технологии

- **Backend:**
  - Python 3.x
  - Flask 2.2.2
  - SQLAlchemy 1.4.27

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
  - Leaflet.js (для работы с картами)

## 🚀 Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/EmotionMap.git
cd EmotionMap
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
python main.py
```

Приложение будет доступно по адресу: `http://127.0.0.1:8080`

## 🌐 Развертывание на хостинге

### Render.com (рекомендуется)

1. Зарегистрируйтесь на [Render.com](https://render.com)
2. Создайте файл `render.yaml` в корне проекта:
```yaml
services:
  - type: web
    name: emotion-map
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

3. Добавьте gunicorn в `requirements.txt`:
```
gunicorn==20.1.0
```

4. Создайте файл `gunicorn_config.py`:
```python
bind = "0.0.0.0:10000"
workers = 4
threads = 4
timeout = 120
```

5. Шаги по деплою:
   - Подключите ваш GitHub репозиторий к Render
   - Создайте новый Web Service
   - Выберите ваш репозиторий
   - Настройте следующие параметры:
     - Name: emotion-map
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn main:app`
   - Добавьте переменные окружения:
     - `PYTHON_VERSION`: 3.9.0
     - `SECRET_KEY`: (сгенерируйте случайную строку)

6. Нажмите "Create Web Service"

### Важные замечания по безопасности

1. Измените `secret_key` в `main.py` на переменную окружения:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
```

2. Настройте переменные окружения для конфиденциальных данных
3. Включите HTTPS (Render предоставляет его автоматически)
4. Регулярно обновляйте зависимости

## 📁 Структура проекта

```
EmotionMap/
├── main.py              # Основной файл приложения
├── requirements.txt     # Зависимости проекта
├── data/               # Данные приложения
├── db/                 # База данных
├── static/             # Статические файлы (CSS, JS, изображения)
└── template/           # HTML шаблоны
```

## 🔒 Безопасность

- Использование сессий для аутентификации
- Безопасное хранение паролей
- Защита от CSRF-атак


## 👨‍💻 Команда
Created by:
- [Артемий](https://github.com/vazart-dude)
- [Даниил](https://github.com/sadsafxrx)
- [Александр](https://github.com/flyrey3)
- [Захар](https://github.com/ZaharLitvinov)

Ссылка на проект: [https://github.com/vazart-dude/EmotionMap](https://github.com/vazart-dude/EmotionMap)
