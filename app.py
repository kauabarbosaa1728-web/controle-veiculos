from flask import Flask
from veiculos import veiculos_bp
from manutencoes import manutencoes_bp
from dashboard import dashboard_bp
from banco import criar_banco
from layout import layout  # 🔥 IMPORTANTE

app = Flask(__name__)

# 🔥 CRIA TABELAS AUTOMATICAMENTE
criar_banco()

# 🔥 REGISTRA ROTAS
app.register_blueprint(veiculos_bp)
app.register_blueprint(manutencoes_bp)
app.register_blueprint(dashboard_bp)

# 🔥 HOME ESTILO APP
@app.route("/")
def home():
    return layout("""
        <div class="card" style="text-align:center;">
            <h2>🚗 Controle de Veículos</h2>
            <p>Gerencie tudo de forma simples e rápida</p>
        </div>

        <div style="
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:15px;
            margin-top:20px;
        ">

            <a href="/veiculos" class="card" style="text-align:center;">
                <h2>🚗</h2>
                <p>Veículos</p>
            </a>

            <a href="/manutencoes" class="card" style="text-align:center;">
                <h2>🔧</h2>
                <p>Manutenções</p>
            </a>

            <a href="/dashboard" class="card" style="text-align:center;">
                <h2>📊</h2>
                <p>Dashboard</p>
            </a>

            <div class="card" style="text-align:center;">
                <h2>⚙️</h2>
                <p>Configurações</p>
            </div>

        </div>

        <br>

        <div style="text-align:center; font-size:12px; opacity:0.6;">
            Sistema rodando 🚀
        </div>
    """)

# 🔥 RODAR LOCAL (Render usa gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
