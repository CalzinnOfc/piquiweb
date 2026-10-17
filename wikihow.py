# Engine: wikihow
import requests

def search(query, params):
    # Lógica de requisição para wikihow
    return [{
        'url': f'https://wikihow.com/search?q={query}',
        'title': f'Resultado do Wikihow para {query}',
        'content': f'Conteúdo de busca indexado via wikihow.'
    }]