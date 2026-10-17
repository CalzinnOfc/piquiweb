# Engine: openstreetmap
import requests

def search(query, params):
    # Lógica de requisição para openstreetmap
    return [{
        'url': f'https://openstreetmap.com/search?q={query}',
        'title': f'Resultado do Openstreetmap para {query}',
        'content': f'Conteúdo de busca indexado via openstreetmap.'
    }]