from flask import Blueprint, request, redirect
from banco import conectar, devolver_conexao

manutencoes_bp = Blueprint("manutencoes_bp", __name__)

@manutencoes_bp.route("/manutencoes", methods=["GET", "POST"])
def manutencoes_page():
    conn = conectar()
    cursor = conn.cursor()

    # CADASTRAR
    if request.method == "POST":
        data = request.form.get("data")
        valor = request.form.get("valor")
        veiculo_id = request.form.get("veiculo_id")
        oficina = request.form.get("oficina")
        descricao = request.form.get("descricao")
        quantidade = request.form.get("quantidade")
        validade = request.form.get("validade")

        cursor.execute("""
        INSERT INTO manutencoes 
        (data, valor, veiculo_id, oficina, descricao, quantidade, validade)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (data, valor, veiculo_id, oficina, descricao, quantidade, validade))

        conn.commit()
        return redirect("/manutencoes")

    # PEGAR VEÍCULOS
    cursor.execute("SELECT id, placa FROM veiculos")
    veiculos = cursor.fetchall()

    opcoes = ""
    for v in veiculos:
        opcoes += f"<option value='{v[0]}'>{v[1]}</option>"

    # LISTAR MANUTENÇÕES
    cursor.execute("""
    SELECT m.data, m.valor, v.placa, m.oficina, m.descricao, m.quantidade, m.validade
    FROM manutencoes m
    JOIN veiculos v ON m.veiculo_id = v.id
    ORDER BY m.id DESC
    """)

    dados = cursor.fetchall()

    tabela = ""
    for d in dados:
        tabela += f"""
        <tr>
            <td>{d[0]}</td>
            <td>R$ {d[1]}</td>
            <td>{d[2]}</td>
            <td>{d[3]}</td>
            <td>{d[4]}</td>
            <td>{d[5]}</td>
            <td>{d[6]}</td>
        </tr>
        """

    cursor.close()
    devolver_conexao(conn)

    return f"""
    <h1>🔧 Manutenções</h1>

    <form method="POST">
        <input type="date" name="data" required>
        <input type="number" step="0.01" name="valor" placeholder="Valor" required>

        <select name="veiculo_id">
            {opcoes}
        </select>

        <input name="oficina" placeholder="Oficina">
        <input name="descricao" placeholder="Descrição">
        <input type="number" name="quantidade" placeholder="Qtd">
        <input type="date" name="validade">

        <button>Salvar</button>
    </form>

    <h2>Histórico:</h2>

    <table border="1">
        <tr>
            <th>Data</th>
            <th>Valor</th>
            <th>Veículo</th>
            <th>Oficina</th>
            <th>Descrição</th>
            <th>Qtd</th>
            <th>Validade</th>
        </tr>
        {tabela}
    </table>

    <br>
    <a href="/">⬅ Voltar</a>
    """
