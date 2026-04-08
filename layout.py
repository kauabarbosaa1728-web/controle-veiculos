def layout(conteudo):
    return f"""
    <html>
    <head>
        <title>KBSISTEMAS AUTO</title>

        <style>
            body {{
                background: #0b0f19;
                color: #e5e7eb;
                font-family: Arial;
                padding: 20px;
            }}

            h1 {{
                color: #3b82f6;
            }}

            h2, h3 {{
                color: #60a5fa;
            }}

            a {{
                color: #3b82f6;
                text-decoration: none;
                display: block;
                margin: 10px 0;
                font-weight: bold;
            }}

            a:hover {{
                color: #93c5fd;
            }}

            input, select {{
                padding: 10px;
                margin: 5px;
                background: #111827;
                color: #e5e7eb;
                border: 1px solid #3b82f6;
                border-radius: 5px;
            }}

            button {{
                background: #3b82f6;
                color: white;
                border: none;
                padding: 10px 15px;
                cursor: pointer;
                border-radius: 5px;
                font-weight: bold;
            }}

            button:hover {{
                background: #2563eb;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: #111827;
            }}

            th, td {{
                border: 1px solid #1f2937;
                padding: 10px;
                text-align: left;
            }}

            th {{
                background: #1e3a8a;
                color: #e5e7eb;
            }}

            tr:nth-child(even) {{
                background: #0f172a;
            }}

            hr {{
                border: 1px solid #1f2937;
                margin: 20px 0;
            }}

            .menu a {{
                display: inline-block;
                margin-right: 15px;
            }}
        </style>
    </head>

    <body>

        <h1>🚗 KBSISTEMAS AUTO</h1>

        <div class="menu">
            <a href="/">🏠 Home</a>
            <a href="/veiculos">🚗 Veículos</a>
            <a href="/manutencoes">🔧 Manutenções</a>
            <a href="/dashboard">📊 Dashboard</a>
        </div>

        <hr>

        {conteudo}

    </body>
    </html>
    """
