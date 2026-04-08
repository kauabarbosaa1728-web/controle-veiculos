from flask import Blueprint
from banco import conectar, devolver_conexao
from layout import layout

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    conn = conectar()
    cursor = conn.cursor()

    try:
        # 💰 TOTAL GERAL
        cursor.execute("SELECT COALESCE(SUM(valor),0) FROM manutencoes")
        total_geral = cursor.fetchone()[0]

        # 🚗 TOTAL POR VEÍCULO
        cursor.execute("""
        SELECT v.placa, COALESCE(SUM(m.valor),0)
        FROM veiculos v
        LEFT JOIN manutencoes m ON v.id = m.veiculo_id
        GROUP BY v.placa
        ORDER BY 2 DESC
        """)

        dados = cursor.fetchall()

        cards = ""
        for d in dados:
            cards += f"""
            <div style="
                background:#111827;
                padding:15px;
                margin:10px 0;
                border:1px solid #3b82f6;
                border-radius:8px;
            ">
                <strong>🚗 {d[0]}</strong><br>
                💰 R$ {d[1]}
            </div>
            """

        return layout(f"""
            <h2>📊 Dashboard</h2>

            <div style="
                background:#1e3a8a;
                padding:20px;
                border-radius:10px;
                margin-bottom:20px;
            ">
                <h3>💰 Total Geral</h3>
                <h1>R$ {total_geral}</h1>
            </div>

            <h3>🚗 Gastos por Veículo:</h3>

            {cards}
        """)

    except Exception as e:
        return layout(f"""
            <h2>❌ Erro no Dashboard</h2>
            <pre>{str(e)}</pre>
        """)

    finally:
        cursor.close()
        devolver_conexao(conn)
