def layout(conteudo):
    return f"""
    <html>
    <head>
        <title>KBSISTEMAS AUTO</title>
        <link rel="manifest" href="/static/manifest.json">

        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {{
                background: #0b0f19;
                color: #e5e7eb;
                font-family: Arial;
                margin: 0;
            }}

            h1 {{
                color: #3b82f6;
                font-size: 22px;
                text-align: center;
                margin: 10px 0;
            }}

            h2, h3 {{
                color: #60a5fa;
            }}

            /* 🔥 TOPO */
            .topo {{
                text-align: center;
                padding: 10px;
                background: #020617;
                border-bottom: 1px solid #1f2937;
            }}

            /* 🔥 ABAS */
            .menu {{
                display: flex;
                justify-content: center;
                gap: 10px;
                padding: 10px;
                flex-wrap: wrap;
                background: #020617;
                border-bottom: 1px solid #1f2937;
            }}

            .menu a {{
                background: #1e3a8a;
                padding: 10px 14px;
                border-radius: 8px;
                color: white;
                text-decoration: none;
                font-size: 14px;
                font-weight: bold;
                transition: 0.2s;
            }}

            .menu a:hover {{
                background: #2563eb;
                transform: scale(1.05);
            }}

            /* 🔥 CONTEÚDO CENTRAL */
            .conteudo {{
                max-width: 1000px;
                margin: auto;
                padding: 20px;
            }}

            /* 🔥 CARDS */
            .card {{
                background: #111827;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 15px;
                border: 1px solid #1f2937;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }}

            /* FORM */
            input, select {{
                width: 100%;
                padding: 10px;
                margin: 6px 0;
                background: #020617;
                color: #e5e7eb;
                border: 1px solid #3b82f6;
                border-radius: 6px;
            }}

            button {{
                width: 100%;
                background: #3b82f6;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                margin-top: 10px;
                cursor: pointer;
            }}

            button:hover {{
                background: #2563eb;
            }}

            /* TABELA */
            table {{
                width: 100%;
                margin-top: 15px;
                display: block;
                overflow-x: auto;
                white-space: nowrap;
                font-size: 12px;
                background: #020617;
                border-radius: 8px;
            }}

            th, td {{
                padding: 10px;
                border: 1px solid #1f2937;
            }}

            th {{
                background: #1e3a8a;
            }}

            tr:nth-child(even) {{
                background: #0f172a;
            }}

            hr {{
                border: 1px solid #1f2937;
                margin: 15px 0;
            }}
        </style>
    </head>

    <body>

        <!-- 🔥 SPLASH -->
        <div id="splash" style="
            position:fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            background:#0b0f19;
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            z-index:9999;
        ">
            <h1 style="color:#3b82f6;">🚗 KBS AUTO</h1>
            <p>Carregando...</p>
        </div>

        <!-- 🔥 TOPO -->
        <div class="topo">
            <h1>🚗 KBSISTEMAS AUTO</h1>
        </div>

        <!-- 🔥 MENU EM ABAS -->
        <div class="menu">
            <a href="/">🏠 Início</a>
            <a href="/veiculos">🚗 Veículos</a>
            <a href="/manutencoes">🔧 Manutenções</a>
            <a href="/dashboard">📊 Dashboard</a>
            <a href="/usuarios">👤 Usuários</a>
            <a href="/problemas">⚠️ Problemas</a>
        </div>

        <!-- 🔥 CONTEÚDO -->
        <div class="conteudo">
            <div class="card">
                {conteudo}
            </div>
        </div>

        <!-- 🔥 INSTALAR APP -->
        <script>
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;

            const btn = document.createElement("button");
            btn.innerText = "📲 Instalar App";
            btn.style.margin = "20px";

            btn.onclick = () => {{
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(() => {{
                    deferredPrompt = null;
                }});
            }};

            document.body.appendChild(btn);
        }});
        </script>

        <!-- 🔥 SPLASH SOME -->
        <script>
        window.addEventListener("load", () => {{
            setTimeout(() => {{
                const splash = document.getElementById("splash");
                if (splash) splash.style.display = "none";
            }}, 800);
        }});
        </script>

    </body>
    </html>
    """
