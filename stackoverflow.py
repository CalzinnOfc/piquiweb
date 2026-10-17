# Engine: stackoverflow
import requests

def search(query, params):
    # Lógica de requisição para stackoverflow
    return [{
        'url': f'https://stackoverflow.com/search?q={query}',
        'title': f'Resultado do Stackoverflow para {query}',
        'content': f'Conteúdo de busca indexado via stackoverflow.'
    }]