from flask import Flask
from veiculos import veiculos_bp
from manutencoes import manutencoes_bp
from banco import criar_banco

app = Flask(__name__)

# 🔥 CRIA TABELAS AUTOMATICAMENTE
criar_banco()

# 🔥 REGISTRA ROTAS
app.register_blueprint(veiculos_bp)
app.register_blueprint(manutencoes_bp)

# 🔥 HOME
@app.route("/")
def home():
    return """
    <h1>🚗 Sistema de Controle de Veículos</h1>

    <hr>

    <a href="/veiculos">🚗 Gerenciar Veículos</a><br><br>
    <a href="/manutencoes">🔧 Registrar Manutenções</a>

    <br><br>
    <p>Sistema rodando online 🚀</p>
    """

if __name__ == "__main__":
    app.run()
