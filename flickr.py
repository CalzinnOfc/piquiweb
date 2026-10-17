# Engine: flickr
import requests

def search(query, params):
    # Lógica de requisição para flickr
    return [{
        'url': f'https://flickr.com/search?q={query}',
        'title': f'Resultado do Flickr para {query}',
        'content': f'Conteúdo de busca indexado via flickr.'
    }]