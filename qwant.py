# Engine: qwant
import requests

def search(query, params):
    # Lógica de requisição para qwant
    return [{
        'url': f'https://qwant.com/search?q={query}',
        'title': f'Resultado do Qwant para {query}',
        'content': f'Conteúdo de busca indexado via qwant.'
    }]