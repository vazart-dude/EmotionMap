import secrets
from flask import Flask, request, render_template, flash, redirect, url_for, session
from data import db_session
from data.users import User
import sqlite3

app = Flask(__name__, template_folder='template')
app.secret_key = secrets.token_hex(16)


@app.route('/')
def page():
    is_logged_in = 'username' in session
    return render_template("main_page.html", is_logged_in=is_logged_in)



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
            flash("Пользователь с таким логином или email уже существует", "error")
    return render_template("registration.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        user = User()
        result = user.login_user(login, password)
        if result:
            session['username'] = login
            return redirect(url_for('page'))
        else:
            flash("Неверный логин или пароль", "error")
    return render_template("login.html")

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))

@app.route("/guide")
def guide():
    return render_template(
        "guide.html",
        title="Гайд по проекту EmotionMap",
        welcome_message="Добро пожаловать в EmotionMap!",
        description="Спасибо за регистрацию! Вот как пользоваться проектом:",
        guide_items=[
            "Нажмите на карту, чтобы добавить свою эмоцию в выбранной точке.",
            "Посмотрите, что другие пользователи чувствуют в разных местах.",
            "Делитесь эмоциями, чтобы сделать карту живой!",
        ],
    )


if __name__ == '__main__':
    db_session.global_init('db/users.db')
    
    app.run(port=8080, host='127.0.0.1', debug=True)
