# Engine: searxng
import requests

def search(query, params):
    # Lógica de requisição para searxng
    return [{
        'url': f'https://searxng.com/search?q={query}',
        'title': f'Resultado do Searxng para {query}',
        'content': f'Conteúdo de busca indexado via searxng.'
    }]