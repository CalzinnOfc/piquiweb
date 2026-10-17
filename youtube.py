# Engine: youtube
import requests

def search(query, params):
    # Lógica de requisição para youtube
    return [{
        'url': f'https://youtube.com/search?q={query}',
        'title': f'Resultado do Youtube para {query}',
        'content': f'Conteúdo de busca indexado via youtube.'
    }]