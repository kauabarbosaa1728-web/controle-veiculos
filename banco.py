import psycopg2
from psycopg2 import pool

# 🔥 SUA URL DO NEON (já configurada)
DATABASE_URL = "postgresql://neondb_owner:npg_1jUl6SpdBMNg@ep-little-sky-anfi8c6a-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 🔥 POOL DE CONEXÃO
conexao_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10, DATABASE_URL
)

def conectar():
    return conexao_pool.getconn()

def devolver_conexao(conn):
    conexao_pool.putconn(conn)


# 🔥 CRIAR TABELAS AUTOMATICAMENTE
def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # 🚗 TABELA DE VEÍCULOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id SERIAL PRIMARY KEY,
        placa TEXT,
        nome TEXT
    )
    """)

    # 🔧 TABELA DE MANUTENÇÕES (já preparada pro próximo módulo 😈)
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
