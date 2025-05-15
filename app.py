from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import random
import json

app = Flask(__name__)
app.secret_key = 'seu-segredo-aqui'

DB_NAME = 'database.db'

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 100
            )
        ''')
        c.execute('''
            CREATE TABLE bets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                number INTEGER,
                amount INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        # Cria admin padrão
        c.execute("INSERT INTO users (username, password, is_admin, coins) VALUES (?, ?, ?, ?)", ('Danilo', '12022005', 1, 9999))
        conn.commit()
        conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username,password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            session['coins'] = user['coins']
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos','error')
    return render_template('login.html')

# Registro
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            flash('Preencha todos os campos','error')
            return render_template('register.html')
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?,?)',(username,password))
            conn.commit()
            conn.close()
            flash('Cadastro realizado! Faça login','success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Usuário já existe','error')
            conn.close()
    return render_template('register.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Mock últimos 100 números da roleta (simulando)
    last_100 = [random.randint(0,36) for _ in range(100)]

    # Previsões simples - pegar os 5 números mais frequentes (simulação)
    counts = {}
    for n in last_100:
        counts[n] = counts.get(n, 0) + 1
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    predictions = [x[0] for x in sorted_counts[:5]]

    coins = session.get('coins', 0)

    return render_template('dashboard.html', username=session['username'], last_100=last_100, predictions=predictions, coins=coins)

# API para simular aposta (adicionar aposta)
@app.route('/bet', methods=['POST'])
def bet():
    if 'user_id' not in session:
        return jsonify({'error':'Sem sessão'}), 401

    data = request.json
    number = data.get('number')
    amount = data.get('amount')

    if number is None or amount is None:
        return jsonify({'error':'Número ou valor inválido'}), 400

    user_id = session['user_id']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user['coins'] < amount:
        conn.close()
        return jsonify({'error':'Moedas insuficientes'}), 400

    # Salvar aposta
    conn.execute('INSERT INTO bets (user_id, number, amount) VALUES (?, ?, ?)', (user_id, number, amount))
    # Deduzir moedas
    new_coins = user['coins'] - amount
    conn.execute('UPDATE users SET coins = ? WHERE id = ?', (new_coins, user_id))
    conn.commit()
    conn.close()
    session['coins'] = new_coins
    return jsonify({'success': True, 'new_coins': new_coins})

# Página Admin
@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect(url_for('login'))
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, coins FROM users').fetchall()
    conn.close()
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Roleta ao vivo iframe page
@app.route('/roleta')
def roleta():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('roleta.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
