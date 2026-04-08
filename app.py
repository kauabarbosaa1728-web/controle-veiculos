from flask import Flask

from veiculos import veiculos_bp

app = Flask(__name__)

app.register_blueprint(veiculos_bp)

@app.route("/")
def home():
    return """
    <h1>🚗 Sistema de Controle de Veículos</h1>
    <a href="/veiculos">👉 Ir para veículos</a>
    """

if __name__ == "__main__":
    app.run()
