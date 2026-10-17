# Engine: bandcamp
import requests

def search(query, params):
    # Lógica de requisição para bandcamp
    return [{
        'url': f'https://bandcamp.com/search?q={query}',
        'title': f'Resultado do Bandcamp para {query}',
        'content': f'Conteúdo de busca indexado via bandcamp.'
    }]