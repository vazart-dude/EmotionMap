from flask import Flask, request, render_template
from data import db_session
from data.users import User
import sqlite3

app = Flask(__name__, template_folder='template')


@app.route('/')
def page():
    return render_template("main_page.html")



@app.route('/registration', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        email = request.form['email']
        user = User()
        result = user.add_user(login, password, email)
        if result:
            return 'Пользователь успешно добавлен!'
        else:
            return 'Пользователь с таким логином или email уже существует!'
    return render_template("registration.html")

@app.route('/login')
def login():
    return 'Login page'

if __name__ == '__main__':
    db_session.global_init('db/users.db')
    
    app.run(port=8080, host='127.0.0.1')