def layout(conteudo):
    return f"""
    <html>
    <head>
        <title>KBSISTEMAS AUTO</title>
        <link rel="manifest" href="/static/manifest.json">

        <!-- 🔥 RESPONSIVO -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {{
                background: #0b0f19;
                color: #e5e7eb;
                font-family: Arial;
                padding: 15px;
                margin: 0;
            }}

            h1 {{
                color: #3b82f6;
                font-size: 22px;
                text-align: center;
            }}

            h2, h3 {{
                color: #60a5fa;
            }}

            .menu {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
                margin-bottom: 15px;
            }}

            .menu a {{
                background: #1e3a8a;
                padding: 10px 12px;
                border-radius: 8px;
                color: white;
                text-decoration: none;
                font-size: 14px;
                font-weight: bold;
            }}

            .menu a:hover {{
                background: #2563eb;
            }}

            input, select {{
                width: 100%;
                padding: 10px;
                margin: 6px 0;
                background: #111827;
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
            }}

            button:hover {{
                background: #2563eb;
            }}

            table {{
                width: 100%;
                margin-top: 15px;
                display: block;
                overflow-x: auto;
                white-space: nowrap;
                font-size: 12px;
                background: #111827;
            }}

            th, td {{
                padding: 8px;
                border: 1px solid #1f2937;
            }}

            th {{
                background: #1e3a8a;
            }}

            tr:nth-child(even) {{
                background: #0f172a;
            }}

            .card {{
                background: #111827;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                border: 1px solid #1f2937;
            }}

            hr {{
                border: 1px solid #1f2937;
                margin: 15px 0;
            }}
        </style>
    </head>

    <body>

        <!-- 🔥 SPLASH SCREEN -->
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

        <h1>🚗 KBSISTEMAS AUTO</h1>

        <div class="menu">
            <a href="/">🏠</a>
            <a href="/veiculos">🚗</a>
            <a href="/manutencoes">🔧</a>
            <a href="/dashboard">📊</a>
        </div>

        <hr>

        {conteudo}

        <!-- 🔥 BOTÃO INSTALAR APP -->
        <script>
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;

            const btn = document.createElement("button");
            btn.innerText = "📲 Instalar App";
            btn.style.marginTop = "15px";

            btn.onclick = () => {{
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(() => {{
                    deferredPrompt = null;
                }});
            }};

            document.body.appendChild(btn);
        }});
        </script>

        <!-- 🔥 SUMIR SPLASH -->
        <script>
        window.addEventListener("load", () => {{
            setTimeout(() => {{
                const splash = document.getElementById("splash");
                if (splash) splash.style.display = "none";
            }}, 1000);
        }});
        </script>

    </body>
    </html>
    """
