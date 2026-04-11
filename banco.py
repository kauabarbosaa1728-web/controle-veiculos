import psycopg2
from psycopg2 import pool
from werkzeug.security import generate_password_hash

DATABASE_URL = "postgresql://neondb_owner:npg_1jUl6SpdBMNg@ep-little-sky-anfi8c6a-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require"

# 🔥 POOL DE CONEXÃO
connection_pool = pool.SimpleConnectionPool(
    1,
    10,
    DATABASE_URL
)

# 🔥 CONECTAR
def conectar():
    try:
        return connection_pool.getconn()
    except Exception as e:
        print("ERRO AO CONECTAR:", e)
        return None

# 🔥 DEVOLVER CONEXÃO
def devolver_conexao(conn):
    try:
        if conn:
            connection_pool.putconn(conn)
    except Exception as e:
        print("ERRO AO DEVOLVER CONEXÃO:", e)

# 🔥 CRIAR TABELAS + ADMIN
def criar_banco():
    conn = conectar()
    if conn is None:
        print("SEM CONEXÃO COM BANCO")
        return

    cursor = conn.cursor()

    try:
        # ================= 🚗 VEÍCULOS =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id SERIAL PRIMARY KEY,
            placa TEXT,
            nome TEXT
        )
        """)

        # ================= 🔧 MANUTENÇÕES =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS manutencoes (
            id SERIAL PRIMARY KEY,
            data DATE,
            valor NUMERIC,
            veiculo_id INTEGER,
            oficina TEXT,
            descricao TEXT,
            quantidade INTEGER,
            validade DATE
        )
        """)

        # ================= 🚨 PROBLEMAS =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS problemas (
            id SERIAL PRIMARY KEY,
            descricao TEXT,
            foto TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ================= 👤 USUÁRIOS =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT UNIQUE,
            senha TEXT
        )
        """)

        # 🔥 VERIFICA SE EXISTE ADMIN
        cursor.execute("SELECT * FROM usuarios WHERE nome='admin'")
        admin = cursor.fetchone()

        if not admin:
            senha_hash = generate_password_hash("123")

            cursor.execute(
                "INSERT INTO usuarios (nome, senha) VALUES (%s, %s)",
                ("admin", senha_hash)
            )

            print("✅ ADMIN CRIADO: login=admin senha=123")

        conn.commit()

    except Exception as e:
        print("ERRO AO CRIAR TABELAS:", e)

    finally:
        cursor.close()
        devolver_conexao(conn)
