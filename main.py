import secrets
from flask import Flask, request, render_template, flash, redirect, url_for, session, jsonify
from data import db_session
from data.users import User
from data.markers import Marker
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, template_folder='template')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Настройка подключения к базе данных
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db/users.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/')
def page():
    is_logged_in = 'username' in session
    return render_template("main_page.html", is_logged_in=is_logged_in)

@app.route('/registration', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        if password != confirm_password:
            flash("Пароли не совпадают", "error")
            return render_template('registration.html')
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
            return redirect(url_for('profile'))
        else:
            flash("Неверный логин или пароль", "error")
    return render_template("login.html")

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/save_marker', methods=['POST'])
def save_marker():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    data = request.get_json()
    db_sess = Session()
    
    try:
        marker = Marker(
            emotion=data.get('emotion'),
            title=data.get('title'),
            description=data.get('description'),
            date=data.get('date'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            username=session['username']
        )
        db_sess.add(marker)
        db_sess.commit()
        return jsonify({'success': True})
    except Exception as e:
        db_sess.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db_sess.close()

@app.route('/get_markers', methods=['GET'])
def get_markers():
    if 'username' not in session:
        return jsonify([])
    
    db_sess = Session()
    try:
        markers = db_sess.query(Marker).filter(Marker.username == session['username']).all()
        return jsonify([{
            'emotion': m.emotion,
            'title': m.title,
            'description': m.description,
            'date': m.date,
            'latitude': m.latitude,
            'longitude': m.longitude,
            'username': m.username
        } for m in markers])
    finally:
        db_sess.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('page'))

if __name__ == '__main__':
    db_session.global_init(DATABASE_URL)
    app.run()
