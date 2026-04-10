from flask import Flask, request, redirect
from veiculos import veiculos_bp
from manutencoes import manutencoes_bp
from dashboard import dashboard_bp
from banco import criar_banco, conectar, devolver_conexao
from layout import layout
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# 🔥 PASTA DE UPLOAD (SEM CRIAR AUTOMATICAMENTE)
UPLOAD_FOLDER = "static/uploads"

# 🔥 CRIA TABELAS AUTOMATICAMENTE
criar_banco()

# 🔥 REGISTRA ROTAS
app.register_blueprint(veiculos_bp)
app.register_blueprint(manutencoes_bp)
app.register_blueprint(dashboard_bp)

# ================= 🔥 ROTA PING =================
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
                nome_arquivo = secure_filename(f"{datetime.now().timestamp()}_{foto.filename}")
                caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

                # 🔥 GARANTE QUE A PASTA EXISTE (AQUI DENTRO, NÃO NO INÍCIO)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                foto.save(caminho)
            except:
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
            <textarea name="descricao" placeholder="Ex: carro está sem óleo..." required style="width:100%;height:100px;"></textarea>

            <br><br>

            <button type="submit">🚀 Enviar</button>

        </form>
    """)


# ================= 📸 VER PROBLEMAS =================
@app.route("/ver_problemas")
def ver_problemas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT descricao, foto, data FROM problemas ORDER BY id DESC")
    dados = cursor.fetchall()

    cursor.close()
    devolver_conexao(conn)

    html = "<h2>📸 Problemas Registrados</h2>"

    for d in dados:
        descricao, foto, data = d

        html += f"""
        <div style="background:#111;padding:15px;margin-bottom:15px;border-radius:10px;">
            <p><b>📅 {data}</b></p>

            {"<img src='/static/uploads/" + foto + "' style='width:100%;max-width:300px;border-radius:10px;'><br><br>" if foto else ""}

            <p>{descricao}</p>
        </div>
        """

    return layout(html)


# ================= 🔥 HOME =================
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

        <div style="margin-top:20px;">
            <a href="/problemas" class="card" style="text-align:center; display:block;">
                <h2>🚨</h2>
                <p>Enviar Problema</p>
            </a>
        </div>

        <div style="margin-top:10px;">
            <a href="/ver_problemas" class="card" style="text-align:center; display:block;">
                <h2>📸</h2>
                <p>Ver Problemas</p>
            </a>
        </div>

        <br>

        <div style="text-align:center; font-size:12px; opacity:0.6;">
            Sistema rodando 🚀
        </div>
    """)

# 🔥 RODAR LOCAL
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
