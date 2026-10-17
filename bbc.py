# Engine: bbc
import requests

def search(query, params):
    # Lógica de requisição para bbc
    return [{
        'url': f'https://bbc.com/search?q={query}',
        'title': f'Resultado do Bbc para {query}',
        'content': f'Conteúdo de busca indexado via bbc.'
    }]