from flask import Flask, render_template, request, redirect, url_for
import sqlite3, bcrypt, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/AgileBank.db")

# ------------------ Registro ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha'].encode()
        senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt())

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nome,email,senha_hash) VALUES (?,?,?)",
                        (nome, email, senha_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Email já cadastrado!"
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

# ------------------ Login ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha'].encode()
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT senha_hash FROM usuarios WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()
        if user and bcrypt.checkpw(senha, user[0]):
            return "Login permitido!"
        else:
            return "Email ou senha incorretos"
    return render_template('login.html')

# ------------------ Página inicial ------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)