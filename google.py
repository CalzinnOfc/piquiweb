# Engine: google
import requests

def search(query, params):
    # Lógica de requisição para google
    return [{
        'url': f'https://google.com/search?q={query}',
        'title': f'Resultado do Google para {query}',
        'content': f'Conteúdo de busca indexado via google.'
    }]