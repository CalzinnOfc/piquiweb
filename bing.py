# Engine: bing
import requests

def search(query, params):
    # Lógica de requisição para bing
    return [{
        'url': f'https://bing.com/search?q={query}',
        'title': f'Resultado do Bing para {query}',
        'content': f'Conteúdo de busca indexado via bing.'
    }]