import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# Template HTML completo embutido para evitar erros de diretório de templates no Render
HTML_TEMPLATE = """
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
            font-size: 48px;
            color: #202124;
            margin: 0;
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
        }
        .search-bar:focus {
            box-shadow: 0 3px 10px rgba(0,0,0,0.15);
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
        <form action="https://www.google.com/search" method="GET">
            <input type="text" id="query-input" name="q" class="search-bar" placeholder="Pesquisar no PiquiWeb..." autocomplete="off">
            <button type="submit" class="search-button">🔍</button>
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

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

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
    
