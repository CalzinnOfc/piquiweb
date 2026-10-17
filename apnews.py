# Engine: apnews
import requests

def search(query, params):
    # Lógica de requisição para apnews
    return [{
        'url': f'https://apnews.com/search?q={query}',
        'title': f'Resultado do Apnews para {query}',
        'content': f'Conteúdo de busca indexado via apnews.'
    }]