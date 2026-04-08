import psycopg2
from psycopg2 import pool

# 🔥 COLOCA SUA URL DO NEON AQUI
DATABASE_URL = "SUA_URL_AQUI"

conexao_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10, DATABASE_URL
)

def conectar():
    return conexao_pool.getconn()

def devolver_conexao(conn):
    conexao_pool.putconn(conn)


# 🔥 CRIAR TABELAS
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

    conn.commit()
    cursor.close()
    devolver_conexao(conn)
