import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# Template da Página Inicial (Home)
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PiquiWeb - Pesquisa</title>
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
            margin-bottom: 25px;
            text-align: center;
        }
        h1 {
            font-size: 52px;
            color: #202124;
            margin: 0;
            letter-spacing: -1px;
        }
        h1 span {
            color: #34A853;
        }
        .search-container {
            position: relative;
            width: 90%;
            max-width: 580px;
        }
        .search-bar {
            width: 100%;
            height: 50px;
            padding: 0 50px 0 20px;
            border-radius: 28px;
            border: 1px solid #dfe1e5;
            outline: none;
            font-size: 16px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            box-sizing: border-box;
            background-color: #fff;
        }
        .search-bar:focus {
            box-shadow: 0 3px 10px rgba(0,0,0,0.15);
            border-color: rgba(223,225,229,0);
        }
        .search-button {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 18px;
        }
        .categories {
            margin-top: 20px;
            display: flex;
            gap: 15px;
            justify-content: center;
            font-size: 14px;
            color: #5f6368;
        }
        .categories label {
            cursor: pointer;
        }
        .suggestions-box {
            position: absolute;
            top: 55px;
            left: 0;
            right: 0;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
            z-index: 1000;
        }
        .suggestion-item {
            padding: 12px 20px;
            cursor: pointer;
            font-size: 15px;
            color: #202124;
        }
        .suggestion-item:hover {
            background-color: #f1f3f4;
        }
    </style>
</head>
<body>
    <div class="logo-container">
        <h1>Piqui<span>Web</span></h1>
    </div>
    <div class="search-container">
        <form action="/search" method="GET">
            <input type="text" id="query-input" name="q" class="search-bar" placeholder="Pesquisar no PiquiWeb..." autocomplete="off" autofocus>
            <button type="submit" class="search-button">🔍</button>
            <div class="categories">
                <label><input type="radio" name="category" value="general" checked> Geral</label>
                <label><input type="radio" name="category" value="images"> Imagens</label>
                <label><input type="radio" name="category" value="videos"> Vídeos</label>
                <label><input type="radio" name="category" value="news"> Notícias</label>
            </div>
        </form>
        <div id="suggestions" class="suggestions-box"></div>
    </div>

    <script>
        const input = document.getElementById('query-input');
        const suggestionsBox = document.getElementById('suggestions');

        input.addEventListener('input', async () => {
            const query = input.value.trim();
            if (query.length === 0) {
                suggestionsBox.innerHTML = '';
                return;
            }

            try {
                const res = await fetch(`https://suggestqueries.google.com/complete/search?client=chrome&q=${encodeURIComponent(query)}`);
                const data = await res.json();
                const suggestions = data[1] || [];

                suggestionsBox.innerHTML = suggestions.slice(0, 6).map(item => 
                    `<div class="suggestion-item" onclick="selectSuggestion('${item}')">${item}</div>`
                ).join('');
            } catch (e) {
                suggestionsBox.innerHTML = '';
            }
        });

        function selectSuggestion(value) {
            input.value = value;
            suggestionsBox.innerHTML = '';
            input.form.submit();
        }
    </script>
</body>
</html>
"""

# Template da Página de Resultados Interna
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
            gap: 20px;
        }
        .logo {
            font-size: 24px;
            font-weight: bold;
            text-decoration: none;
            color: #202124;
        }
        .logo span {
            color: #34A853;
        }
        .search-form-mini input {
            width: 400px;
            height: 40px;
            border-radius: 20px;
            border: 1px solid #dfe1e5;
            padding: 0 20px;
            outline: none;
            font-size: 15px;
            box-shadow: 0 1px 6px rgba(32,33,36,.1);
        }
        .content {
            padding: 20px 30px;
            max-width: 700px;
        }
        .info {
            color: #70757a;
            font-size: 14px;
            margin-bottom: 20px;
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
        }
        .result-card p {
            font-size: 14px;
            color: #4d5156;
            margin-top: 4px;
        }
        .back-home {
            display: inline-block;
            margin-top: 20px;
            color: #1a0dab;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="logo">Piqui<span>Web</span></a>
        <form action="/search" method="GET" class="search-form-mini">
            <input type="text" name="q" value="{{ query }}">
            <input type="hidden" name="category" value="{{ category }}">
        </form>
    </div>
    <div class="content">
        <div class="info">Resultados para a pesquisa: <b>{{ query }}</b> (Categoria: {{ category }})</div>
        
        <div class="result-card">
            <a href="https://www.google.com/search?q={{ query }}" target="_blank">Resultados da Web para {{ query }}</a>
            <div class="url">https://www.piquiweb.com/search?q={{ query }}</div>
            <p>Clique no link acima para ver os resultados completos indexados e processados pelas engrenagens de busca do PiquiWeb.</p>
        </div>

        <a href="/" class="back-home">← Voltar à página inicial</a>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    category = request.args.get("category", "general")
    return render_template_string(RESULTS_TEMPLATE, query=query, category=category)

@app.route("/autocomplete")
def autocomplete():
    q = request.args.get("q", "")
    if not q:
        return jsonify([])
    try:
        r = requests.get(f"https://suggestqueries.google.com/complete/search?client=chrome&q={q}")
        return jsonify(r.json()[1])
    except Exception:
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port, debug=False)
    
