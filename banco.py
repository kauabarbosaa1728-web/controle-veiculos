import psycopg2
from psycopg2 import pool

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

# 🔥 CRIAR TABELAS
def criar_banco():
    conn = conectar()
    if conn is None:
        print("SEM CONEXÃO COM BANCO")
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id SERIAL PRIMARY KEY,
            placa TEXT,
            nome TEXT
        )
        """)

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

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS problemas (
            id SERIAL PRIMARY KEY,
            descricao TEXT,
            foto TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            senha TEXT
        )
        """)

        conn.commit()

    except Exception as e:
        print("ERRO AO CRIAR TABELAS:", e)

    finally:
        cursor.close()
        devolver_conexao(conn)
