from flask import Blueprint, request, redirect

veiculos_bp = Blueprint("veiculos_bp", __name__)

veiculos = []

@veiculos_bp.route("/veiculos", methods=["GET", "POST"])
def veiculos_page():
    if request.method == "POST":
        placa = request.form.get("placa")
        nome = request.form.get("nome")

        veiculos.append({
            "placa": placa,
            "nome": nome
        })

        return redirect("/veiculos")

    lista_html = ""
    for v in veiculos:
        lista_html += f"<li>{v['placa']} - {v['nome']}</li>"

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
