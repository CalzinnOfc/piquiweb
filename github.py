# Engine: github
import requests

def search(query, params):
    # Lógica de requisição para github
    return [{
        'url': f'https://github.com/search?q={query}',
        'title': f'Resultado do Github para {query}',
        'content': f'Conteúdo de busca indexado via github.'
    }]