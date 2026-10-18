import os
from flask import Flask, render_template_string, request, jsonify
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Lista com os 30 motores e fontes integradas simultaneamente
ENGINES = [
    {"name": "DuckDuckGo", "url": lambda q: f"https://duckduckgo.com/html/?q={q}"},
    {"name": "DDG HTML", "url": lambda q: f"https://html.duckduckgo.com/html/?q={q}"},
    {"name": "DDG Lite", "url": lambda q: f"https://lite.duckduckgo.com/lite/"},
    {"name": "Brave Search", "url": lambda q: f"https://search.brave.com/search?q={q}"},
    {"name": "Yahoo Search", "url": lambda q: f"https://search.yahoo.com/search?p={q}"},
    {"name": "Kagi", "url": lambda q: f"https://kagi.com/search?q={q}"},
    {"name": "Mojeek", "url": lambda q: f"https://www.mojeek.com/search?q={q}"},
    {"name": "Google", "url": lambda q: f"https://www.google.com/search?q={q}"},
    {"name": "Bing", "url": lambda q: f"https://www.bing.com/search?q={q}"},
    {"name": "Ecosia", "url": lambda q: f"https://www.ecosia.org/search?q={q}"},
    {"name": "Startpage", "url": lambda q: f"https://www.startpage.com/sp/search?query={q}"},
    {"name": "Qwant", "url": lambda q: f"https://www.qwant.com/?q={q}"},
    {"name": "SearXNG Public", "url": lambda q: f"https://search.ononoki.org/search?q={q}"},
    {"name": "Wikipedia", "url": lambda q: f"https://pt.wikipedia.org/w/index.php?search={q}"},
    {"name": "GitHub", "url": lambda q: f"https://github.com/search?q={q}"},
    {"name": "StackOverflow", "url": lambda q: f"https://stackoverflow.com/search?q={q}"},
    {"name": "Reddit", "url": lambda q: f"https://www.reddit.com/search/?q={q}"},
    {"name": "ArXiv", "url": lambda q: f"https://arxiv.org/search/?query={q}"},
    {"name": "PubMed", "url": lambda q: f"https://pubmed.ncbi.nlm.nih.gov/?term={q}"},
    {"name": "Wikidata", "url": lambda q: f"https://www.wikidata.org/w/index.php?search={q}"},
    {"name": "OpenStreetMap", "url": lambda q: f"https://www.openstreetmap.org/search?query={q}"},
    {"name": "Flickr", "url": lambda q: f"https://www.flickr.com/search/?text={q}"},
    {"name": "Unsplash", "url": lambda q: f"https://unsplash.com/s/photos/{q}"},
    {"name": "Pinterest", "url": lambda q: f"https://www.pinterest.com/search/pins/?q={q}"},
    {"name": "YouTube", "url": lambda q: f"https://www.youtube.com/results?search_query={q}"},
    {"name": "Vimeo", "url": lambda q: f"https://vimeo.com/search?q={q}"},
    {"name": "Dailymotion", "url": lambda q: f"https://www.dailymotion.com/search/{q}"},
    {"name": "Reuters", "url": lambda q: f"https://www.reuters.com/search/news?blob={q}"},
    {"name": "BBC News", "url": lambda q: f"https://www.bbc.co.uk/search?q={q}"},
    {"name": "CNN", "url": lambda q: f"https://edition.cnn.com/search?q={q}"}
]

# Template da Página Inicial
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
            transition: box-shadow 0.2s;
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
        .suggestions-box {
            position: absolute;
            top: 58px;
            left: 0;
            right: 0;
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
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
            <input type="text" id="query-input" name="q" class="search-bar" placeholder="Pesquisar em 30 motores simultaneamente..." autocomplete="off" autofocus>
            <button type="submit" class="search-button">🔍</button>
        </form>
        <div class="info-tag">Pesquisa simultânea em Brave, DuckDuckGo, Yahoo, Kagi, Mojeek e outras 25 fontes.</div>
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

# Template da Página de Resultados em Massa
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
            letter-spacing: -1px;
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
            box-shadow: 0 1px 6px rgba(32,33,36,.08);
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
            margin-top: 2px;
            margin-bottom: 3px;
            word-break: break-all;
        }
        .result-card p {
            font-size: 14px;
            color: #4d5156;
            margin: 0;
            line-height: 1.4;
        }
        .engine-badge {
            display: inline-block;
            background: #f1f3f4;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            color: #5f6368;
            margin-bottom: 4px;
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
        <div class="info">Resultados combinados de <b>30 motores em simultâneo</b> para: <b>{{ query }}</b></div>

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
            <p>A procurar em simultâneo...</p>
        {% endif %}
    </div>
</body>
</html>
"""

def fetch_engine(engine_info, query):
    engine_name = engine_info["name"]
    res_list = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        target_url = engine_info["url"](query)
        
        if "lite.duckduckgo.com" in target_url:
            resp = requests.post(target_url, data={"q": query}, headers=headers, timeout=3)
        else:
            resp = requests.get(target_url, headers=headers, timeout=3)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                title = a.get_text(strip=True)
                if len(title) > 8 and ('http' in href or href.startswith('http')):
                    if not any(x in href for x in ['ads', 'track', 'login', 'signup', 'javascript', 'support']):
                        res_list.append({
                            'engine': engine_name,
                            'title': title,
                            'url': href,
                            'snippet': f"Conteúdo indexado e recuperado simultaneamente via {engine_name}."
                        })
                        if len(res_list) >= 2: # Pega até 2 resultados por motor para não duplicar demais
                            break
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
        # Executa as buscas nos 30 motores ao mesmo tempo usando multi-threading para ser super rápido
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_engine, engine, query) for engine in ENGINES]
            for future in futures:
                try:
                    res = future.result()
                    if res:
                        all_results.extend(res)
                except Exception:
                    pass

    return render_template_string(RESULTS_TEMPLATE, query=query, results=all_results[:35])

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
    
