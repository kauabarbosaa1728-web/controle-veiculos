from flask import Blueprint
from banco import conectar, devolver_conexao
from layout import layout
import json

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    conn = conectar()
    cursor = conn.cursor()

    try:
        # 💰 TOTAL GERAL
        cursor.execute("SELECT COALESCE(SUM(valor),0) FROM manutencoes")
        total_geral = cursor.fetchone()[0]

        # 🚗 DADOS PARA GRÁFICO
        cursor.execute("""
        SELECT v.placa, COALESCE(SUM(m.valor),0)
        FROM veiculos v
        LEFT JOIN manutencoes m ON v.id = m.veiculo_id
        GROUP BY v.placa
        ORDER BY 2 DESC
        """)

        dados = cursor.fetchall()

        placas = [d[0] for d in dados]
        valores = [float(d[1]) for d in dados]

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

            <canvas id="grafico" height="100"></canvas>

            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

            <script>
                const ctx = document.getElementById('grafico');

                new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: {json.dumps(placas)},
                        datasets: [{{
                            label: 'Gastos (R$)',
                            data: {json.dumps(valores)},
                            backgroundColor: '#3b82f6'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            legend: {{
                                labels: {{
                                    color: '#e5e7eb'
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                ticks: {{ color: '#e5e7eb' }}
                            }},
                            y: {{
                                ticks: {{ color: '#e5e7eb' }}
                            }}
                        }}
                    }}
                }});
            </script>
        """)

    except Exception as e:
        return layout(f"""
            <h2>❌ Erro no Dashboard</h2>
            <pre>{str(e)}</pre>
        """)

    finally:
        cursor.close()
        devolver_conexao(conn)
