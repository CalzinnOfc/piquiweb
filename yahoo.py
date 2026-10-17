# Engine: yahoo
import requests

def search(query, params):
    # Lógica de requisição para yahoo
    return [{
        'url': f'https://yahoo.com/search?q={query}',
        'title': f'Resultado do Yahoo para {query}',
        'content': f'Conteúdo de busca indexado via yahoo.'
    }]