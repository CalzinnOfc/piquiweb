# Engine: soundcloud
import requests

def search(query, params):
    # Lógica de requisição para soundcloud
    return [{
        'url': f'https://soundcloud.com/search?q={query}',
        'title': f'Resultado do Soundcloud para {query}',
        'content': f'Conteúdo de busca indexado via soundcloud.'
    }]