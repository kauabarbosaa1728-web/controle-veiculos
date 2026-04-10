from flask import Flask, request, redirect, session
from veiculos import veiculos_bp
from manutencoes import manutencoes_bp
from dashboard import dashboard_bp
from banco import criar_banco, conectar, devolver_conexao
from layout import layout
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "segredo123"

UPLOAD_FOLDER = "static/uploads"

criar_banco()

app.register_blueprint(veiculos_bp)
app.register_blueprint(manutencoes_bp)
app.register_blueprint(dashboard_bp)

# ================= 🔥 PROTEGER =================
@app.before_request
def proteger():
    rotas_livres = ["/login", "/ping"]

    if request.path not in rotas_livres:
        if "user" not in session:
            return redirect("/login")

# ================= 🔐 LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM usuarios WHERE nome=%s AND senha=%s", (nome, senha))
        user = cursor.fetchone()

        cursor.close()
        devolver_conexao(conn)

        if user:
            session["user"] = nome
            return redirect("/")
        else:
            return layout("<h2>❌ Login inválido</h2>")

    return layout("""
        <h2>🔐 Login</h2>

        <form method="POST">
            <input name="nome" placeholder="Usuário" required><br><br>
            <input name="senha" type="password" placeholder="Senha" required><br><br>
            <button type="submit">Entrar</button>
        </form>
    """)

# ================= 🚪 LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= 🔥 PING =================
@app.route("/ping")
def ping():
    return "ok", 200

# ================= 🚨 PROBLEMAS =================
@app.route("/problemas", methods=["GET", "POST"])
def problemas():
    if request.method == "POST":
        descricao = request.form.get("descricao")
        foto = request.files.get("foto")

        nome_arquivo = ""

        if foto:
            try:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                nome_arquivo = secure_filename(f"{datetime.now().timestamp()}_{foto.filename}")
                caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

                foto.save(caminho)
            except Exception as e:
                print("ERRO AO SALVAR FOTO:", e)
                nome_arquivo = ""

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO problemas (descricao, foto)
            VALUES (%s, %s)
        """, (descricao, nome_arquivo))

        conn.commit()
        cursor.close()
        devolver_conexao(conn)

        return redirect("/problemas")

    return layout("""
        <h2>🚨 Registrar Problema</h2>

        <form method="POST" enctype="multipart/form-data">

            <p>📸 Foto do problema:</p>
            <input type="file" name="foto" accept="image/*" capture="environment" required>

            <br><br>

            <p>🧾 Descrição:</p>
            <textarea name="descricao" required style="width:100%;height:100px;"></textarea>

            <br><br>

            <button type="submit">🚀 Enviar</button>

        </form>
    """)

# ================= ❌ DELETAR =================
@app.route("/deletar_problema/<int:id>")
def deletar_problema(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM problemas WHERE id=%s", (id,))
    resultado = cursor.fetchone()

    if resultado:
        foto = resultado[0]
        if foto:
            caminho = os.path.join(UPLOAD_FOLDER, foto)
            if os.path.exists(caminho):
                os.remove(caminho)

    cursor.execute("DELETE FROM problemas WHERE id=%s", (id,))

    conn.commit()
    cursor.close()
    devolver_conexao(conn)

    return redirect("/ver_problemas")

# ================= 📸 VER PROBLEMAS =================
@app.route("/ver_problemas")
def ver_problemas():
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, descricao, foto, data FROM problemas ORDER BY id DESC")
        dados = cursor.fetchall()
    except:
        dados = []

    cursor.close()
    devolver_conexao(conn)

    html = "<h2>📸 Problemas Registrados</h2>"

    if not dados:
        html += "<p>Nenhum problema ainda.</p>"

    for d in dados:
        id, descricao, foto, data = d

        html += "<div style='background:#111;padding:15px;margin-bottom:15px;border-radius:10px;'>"
        html += f"<p><b>📅 {data}</b></p>"

        if foto:
            html += f"<img src='/static/uploads/{foto}' style='width:100%;max-width:300px;border-radius:10px;'><br><br>"

        html += f"<p>{descricao}</p>"
        html += f"<a href='/deletar_problema/{id}' style='color:red;'>❌ Excluir</a>"
        html += "</div>"

    return layout(html)

# ================= 👤 USUÁRIOS =================
@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (nome, senha))
        conn.commit()

    cursor.execute("SELECT id, nome FROM usuarios")
    dados = cursor.fetchall()

    html = """
    <h2>👤 Usuários</h2>

    <form method="POST">
        <input name="nome" placeholder="Nome" required><br><br>
        <input name="senha" placeholder="Senha" required><br><br>
        <button type="submit">Criar</button>
    </form>

    <hr>
    """

    for u in dados:
        html += f"<p>{u[1]}</p>"

    cursor.close()
    devolver_conexao(conn)

    return layout(html)

# ================= 🔥 HOME =================
@app.route("/")
def home():
    return layout(f"""
        <div style="text-align:right;">
            <a href="/logout">🚪 Sair</a>
        </div>

        <div class="card" style="text-align:center;">
            <h2>🚗 Controle de Veículos</h2>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:20px;">

            <a href="/veiculos" class="card"><h2>🚗</h2><p>Veículos</p></a>
            <a href="/manutencoes" class="card"><h2>🔧</h2><p>Manutenções</p></a>
            <a href="/dashboard" class="card"><h2>📊</h2><p>Dashboard</p></a>
            <a href="/usuarios" class="card"><h2>👤</h2><p>Usuários</p></a>

        </div>

        <div style="margin-top:20px;">
            <a href="/problemas" class="card" style="display:block;text-align:center;">
                <h2>🚨</h2>
                <p>Enviar Problema</p>
            </a>
        </div>

        <div style="margin-top:10px;">
            <a href="/ver_problemas" class="card" style="display:block;text-align:center;">
                <h2>📸</h2>
                <p>Ver Problemas</p>
            </a>
        </div>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

        
