# Engine: arxiv
import requests

def search(query, params):
    # Lógica de requisição para arxiv
    return [{
        'url': f'https://arxiv.com/search?q={query}',
        'title': f'Resultado do Arxiv para {query}',
        'content': f'Conteúdo de busca indexado via arxiv.'
    }]