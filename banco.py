import psycopg
from psycopg_pool import ConnectionPool

DATABASE_URL = "postgresql://neondb_owner:npg_1jUl6SpdBMNg@ep-little-sky-anfi8c6a-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require"

pool = ConnectionPool(conninfo=DATABASE_URL)

def conectar():
    return pool.getconn()

def devolver_conexao(conn):
    pool.putconn(conn)


def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

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

    conn.commit()
    cursor.close()
    devolver_conexao(conn)
