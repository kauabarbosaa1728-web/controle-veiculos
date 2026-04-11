from flask import Flask, request, redirect, session
from veiculos import veiculos_bp
from manutencoes import manutencoes_bp
from dashboard import dashboard_bp
from banco import criar_banco, conectar, devolver_conexao
from layout import layout
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "segredo123"

UPLOAD_FOLDER = os.path.join("static", "uploads")

# 🔥 CRIA BANCO + ADMIN
criar_banco()

app.register_blueprint(veiculos_bp)
app.register_blueprint(manutencoes_bp)
app.register_blueprint(dashboard_bp)

# ================= 🔒 PROTEGER =================
@app.before_request
def proteger():
    rotas_livres = ["/login", "/ping"]

    if request.path not in rotas_livres:
        if "user" not in session:
            return redirect("/login")

# ================= 🔐 LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect("/")

    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT nome, senha, cargo,
                       pode_veiculos,
                       pode_manutencoes,
                       pode_dashboard,
                       pode_usuarios
                FROM usuarios
                WHERE nome=%s
            """, (nome,))
            user = cursor.fetchone()

            cursor.close()
            devolver_conexao(conn)

        except Exception as e:
            print("ERRO LOGIN:", e)
            return layout("<h2>❌ Erro no servidor (login)</h2>")

        if user:
            (nome_db, senha_db, cargo,
             pode_veiculos,
             pode_manutencoes,
             pode_dashboard,
             pode_usuarios) = user

            if check_password_hash(senha_db, senha):
                session["user"] = nome_db
                session["cargo"] = cargo

                # 🔥 PERMISSÕES
                session["pode_veiculos"] = pode_veiculos
                session["pode_manutencoes"] = pode_manutencoes
                session["pode_dashboard"] = pode_dashboard
                session["pode_usuarios"] = pode_usuarios

                return redirect("/")
            else:
                return layout("<h2>❌ Senha incorreta</h2>")
        else:
            return layout("<h2>❌ Usuário não encontrado</h2>")

    return layout("""
        <h2>🔐 Login</h2>
        <form method="POST">
            <input name="nome" placeholder="Usuário" required><br><br>
            <input name="senha" type="password" placeholder="Senha" required><br><br>
            <button>Entrar</button>
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
                print("ERRO FOTO:", e)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO problemas (descricao, foto) VALUES (%s, %s)", (descricao, nome_arquivo))
        conn.commit()
        cursor.close()
        devolver_conexao(conn)

        return redirect("/problemas")

    return layout("""
        <h2>🚨 Registrar Problema</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="foto" required><br><br>
            <textarea name="descricao" required></textarea><br><br>
            <button>Enviar</button>
        </form>
    """)

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

    html = "<h2>📸 Problemas</h2>"

    for id, descricao, foto, data in dados:
        html += "<div style='background:#111;padding:10px;margin:10px;'>"
        html += f"<p>{data}</p>"

        if foto:
            html += f"<img src='/static/uploads/{foto}' width='200'><br>"

        html += f"<p>{descricao}</p>"
        html += f"<a href='/deletar_problema/{id}'>❌ Excluir</a>"
        html += "</div>"

    return layout(html)

# ================= ❌ DELETAR =================
@app.route("/deletar_problema/<int:id>")
def deletar_problema(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM problemas WHERE id=%s", (id,))
    r = cursor.fetchone()

    if r and r[0]:
        caminho = os.path.join(UPLOAD_FOLDER, r[0])
        if os.path.exists(caminho):
            os.remove(caminho)

    cursor.execute("DELETE FROM problemas WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    devolver_conexao(conn)

    return redirect("/ver_problemas")

# ================= 👤 USUÁRIOS =================
@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if session.get("cargo") != "admin":
        return "<h1 style='color:red;text-align:center;'>🚫 Apenas admin</h1>"

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        try:
            senha_hash = generate_password_hash(senha)

            cursor.execute("""
                INSERT INTO usuarios 
                (nome, senha, cargo)
                VALUES (%s, %s, 'usuario')
            """, (nome, senha_hash))

            conn.commit()

        except Exception as e:
            print("ERRO USUARIO:", e)

    cursor.execute("SELECT nome, cargo FROM usuarios")
    dados = cursor.fetchall()

    html = "<h2>👤 Usuários</h2>"

    html += """
    <form method="POST">
        <input name="nome" placeholder="Usuário" required>
        <input name="senha" placeholder="Senha" required>
        <button>Criar</button>
    </form>
    """

    for u in dados:
        html += f"<p>{u[0]} - ({u[1]})</p>"

    cursor.close()
    devolver_conexao(conn)

    return layout(html)

# ================= HOME =================
@app.route("/")
def home():
    return layout("""
        <a href="/logout">Sair</a>
        <h2>🚗 Sistema</h2>

        <div class="grid-botoes">
            <a href="/veiculos">🚗 Veículos</a>
            <a href="/manutencoes">🔧 Manutenções</a>
            <a href="/dashboard">📊 Dashboard</a>
            <a href="/usuarios">👤 Usuários</a>
            <a href="/problemas">⚠️ Problemas</a>
            <a href="/ver_problemas">📋 Ver Problemas</a>
        </div>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
