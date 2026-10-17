import os
from flask import Flask, render_template, request, jsonify
import yaml
import requests

app = Flask(__name__)

# Carrega as configurações do settings.yml
with open("settings.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    category = request.args.get("category", "general")
    return render_template("results.html", query=query, category=category)

@app.route("/preferences")
def preferences():
    return render_template("preferences.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

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
    # Pega a porta fornecida pelo Render automaticamente ou usa 8888 por padrão localmente
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port, debug=False)
