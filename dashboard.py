from flask import Blueprint
from banco import conectar, devolver_conexao

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    conn = conectar()
    cursor = conn.cursor()

    # TOTAL GERAL
    cursor.execute("SELECT COALESCE(SUM(valor),0) FROM manutencoes")
    total_geral = cursor.fetchone()[0]

    # TOTAL POR VEÍCULO
    cursor.execute("""
    SELECT v.placa, COALESCE(SUM(m.valor),0)
    FROM veiculos v
    LEFT JOIN manutencoes m ON v.id = m.veiculo_id
    GROUP BY v.placa
    ORDER BY 2 DESC
    """)

    dados = cursor.fetchall()

    lista = ""
    for d in dados:
        lista += f"<li>{d[0]} → R$ {d[1]}</li>"

    cursor.close()
    devolver_conexao(conn)

    return f"""
    <h1>📊 Dashboard</h1>

    <h2>💰 Total Geral: R$ {total_geral}</h2>

    <h3>🚗 Gastos por Veículo:</h3>
    <ul>
        {lista}
    </ul>

    <br>
    <a href="/">⬅ Voltar</a>
    """
