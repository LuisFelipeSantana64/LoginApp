import sqlite3

# Caminho do banco de dados
db_path = "database/AgileBank.db"

# Conectar (ou criar) o banco
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Criar tabela de usuários
cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash BLOB NOT NULL
)
""")

conn.commit()
conn.close()

print("Tabela 'usuarios' criada com sucesso!")
