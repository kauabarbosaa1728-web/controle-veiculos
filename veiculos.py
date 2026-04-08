from flask import Blueprint, request, redirect
from banco import conectar, devolver_conexao

veiculos_bp = Blueprint("veiculos_bp", __name__)

@veiculos_bp.route("/veiculos", methods=["GET", "POST"])
def veiculos_page():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        placa = request.form.get("placa")
        nome = request.form.get("nome")

        cursor.execute(
            "INSERT INTO veiculos (placa, nome) VALUES (%s, %s)",
            (placa, nome)
        )
        conn.commit()

        return redirect("/veiculos")

    cursor.execute("SELECT placa, nome FROM veiculos")
    dados = cursor.fetchall()

    lista_html = ""
    for v in dados:
        lista_html += f"<li>{v[0]} - {v[1]}</li>"

    cursor.close()
    devolver_conexao(conn)

    return f"""
    <h1>🚗 Veículos</h1>

    <form method="POST">
        <input name="placa" placeholder="Placa" required>
        <input name="nome" placeholder="Nome do veículo" required>
        <button>Cadastrar</button>
    </form>

    <h2>Lista:</h2>
    <ul>
        {lista_html}
    </ul>

    <br>
    <a href="/">⬅ Voltar</a>
    """
