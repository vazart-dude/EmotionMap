import secrets
from flask import Flask, request, render_template, flash, redirect, url_for, session, jsonify
from data import db_session
from data.users import User
import os
import json

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
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        if password != confirm_password:
            flash("Пароли не совпадают", "error")
            return render_template('registration.html')
        user = User()
        result = user.add_user(login, password, email)
        if result:
            login = request.form['login']
            password = request.form['password']
            user = User()
            result = user.login_user(login, password)
            session['username'] = login
            return redirect(url_for('profile'))
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
    marker = {
        'emotion': data.get('emotion'),
        'title': data.get('title'),
        'description': data.get('description'),
        'date': data.get('date'),
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'username': session['username']
    }
    os.makedirs('data', exist_ok=True)
    file_path = os.path.join('data', 'markers.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                markers = json.load(f)
            except Exception:
                markers = []
    else:
        markers = []
    markers.append(marker)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(markers, f, ensure_ascii=False, indent=2)
    return jsonify({'success': True})

@app.route('/get_markers', methods=['GET'])
def get_markers():
    if 'username' not in session:
        return jsonify([])
    file_path = os.path.join('data', 'markers.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                markers = json.load(f)
            except Exception:
                markers = []
    else:
        markers = []
    user_markers = [m for m in markers if m.get('username') == session['username']]
    return jsonify(user_markers)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('page'))

if __name__ == '__main__':
    db_session.global_init('db/users.db')
    
    app.run(port=0000, host='127.0.0.1', debug=False)
