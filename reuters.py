# Engine: reuters
import requests

def search(query, params):
    # Lógica de requisição para reuters
    return [{
        'url': f'https://reuters.com/search?q={query}',
        'title': f'Resultado do Reuters para {query}',
        'content': f'Conteúdo de busca indexado via reuters.'
    }]