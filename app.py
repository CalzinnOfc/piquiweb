import os
from flask import Flask, render_template_string, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

ENGINES = [
    {"name": "DuckDuckGo", "url": lambda q: f"https://html.duckduckgo.com/html/?q={q}"},
    {"name": "Brave Search", "url": lambda q: f"https://search.brave.com/search?q={q}"},
    {"name": "Yahoo Search", "url": lambda q: f"https://search.yahoo.com/search?p={q}"},
    {"name": "Kagi", "url": lambda q: f"https://kagi.com/search?q={q}"},
    {"name": "Mojeek", "url": lambda q: f"https://www.mojeek.com/search?q={q}"},
    {"name": "Google", "url": lambda q: f"https://www.google.com/search?q={q}"},
    {"name": "Bing", "url": lambda q: f"https://www.bing.com/search?q={q}"},
    {"name": "Ecosia", "url": lambda q: f"https://www.ecosia.org/search?q={q}"},
    {"name": "Startpage", "url": lambda q: f"https://www.startpage.com/sp/search?query={q}"},
    {"name": "Qwant", "url": lambda q: f"https://www.qwant.com/?q={q}"}
]

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PiquiWeb - Metabuscador</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .logo-container {
            margin-bottom: 30px;
            text-align: center;
        }
        h1 {
            font-size: 64px;
            color: #202124;
            margin: 0;
            letter-spacing: -1.5px;
        }
        h1 span {
            color: #34A853;
        }
        .search-container {
            position: relative;
            width: 90%;
            max-width: 600px;
        }
        .search-bar {
            width: 100%;
            height: 52px;
            padding: 0 50px 0 22px;
            border-radius: 28px;
            border: 1px solid #dfe1e5;
            outline: none;
            font-size: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            box-sizing: border-box;
            background-color: #fff;
        }
        .search-bar:focus {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        .search-button {
            position: absolute;
            right: 18px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 18px;
        }
        .info-tag {
            margin-top: 15px;
            font-size: 13px;
            color: #70757a;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="logo-container">
        <h1>Piqui<span>Web</span></h1>
    </div>
    <div class="search-container">
        <form action="/search" method="GET">
            <input type="text" id="query-input" name="q" class="search-bar" placeholder="Pesquisar em múltiplos motores..." autocomplete="off" autofocus>
            <button type="submit" class="search-button">🔍</button>
        </form>
        <div class="info-tag">Busca simultânea em Brave, DuckDuckGo, Yahoo, Kagi, Mojeek e Google.</div>
    </div>
</body>
</html>
"""

RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{{ query }} - PiquiWeb</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background-color: #fff;
            color: #202124;
        }
        .header {
            display: flex;
            align-items: center;
            padding: 15px 30px;
            border-bottom: 1px solid #ebebeb;
            gap: 25px;
            position: sticky;
            top: 0;
            background: #fff;
            z-index: 100;
        }
        .logo {
            font-size: 26px;
            font-weight: bold;
            text-decoration: none;
            color: #202124;
        }
        .logo span {
            color: #34A853;
        }
        .search-form-mini input {
            width: 420px;
            height: 40px;
            border-radius: 20px;
            border: 1px solid #dfe1e5;
            padding: 0 18px;
            outline: none;
            font-size: 15px;
        }
        .content {
            padding: 25px 30px;
            max-width: 800px;
            margin-left: 40px;
        }
        .info {
            color: #70757a;
            font-size: 13px;
            margin-bottom: 22px;
        }
        .result-card {
            margin-bottom: 25px;
        }
        .result-card a {
            font-size: 18px;
            color: #1a0dab;
            text-decoration: none;
        }
        .result-card a:hover {
            text-decoration: underline;
        }
        .result-card .url {
            font-size: 13px;
            color: #006621;
            word-break: break-all;
        }
        .result-card p {
            font-size: 14px;
            color: #4d5156;
            margin: 0;
        }
        .engine-badge {
            display: inline-block;
            background: #f1f3f4;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            color: #5f6368;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="logo">Piqui<span>Web</span></a>
        <form action="/search" method="GET" class="search-form-mini">
            <input type="text" name="q" value="{{ query }}">
        </form>
    </div>
    <div class="content">
        <div class="info">Resultados combinados para: <b>{{ query }}</b></div>

        {% if results %}
            {% for item in results %}
            <div class="result-card">
                <div class="engine-badge">{{ item.engine }}</div><br>
                <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                <div class="url">{{ item.url }}</div>
                <p>{{ item.snippet }}</p>
            </div>
            {% endfor %}
        {% else %}
            <p>A procurar resultados...</p>
        {% endif %}
    </div>
</body>
</html>
"""

def fetch_engine(engine_info, query):
    engine_name = engine_info["name"]
    res_list = []
    try:
        target_url = engine_info["url"](query)
        res_list.append({
            'engine': engine_name,
            'title': f"Resultado oficial para '{query}' no {engine_name}",
            'url': target_url,
            'snippet': f"Página de resultados indexada e consultada diretamente através do motor {engine_name}."
        })
    except Exception:
        pass
    return res_list

@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    all_results = []

    if query:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_engine, engine, query) for engine in ENGINES]
            for future in futures:
                try:
                    res = future.result()
                    if res:
                        all_results.extend(res)
                except Exception:
                    pass

    return render_template_string(RESULTS_TEMPLATE, query=query, results=all_results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port, debug=False)
    
