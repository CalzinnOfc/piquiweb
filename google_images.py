# Engine: google_images
import requests

def search(query, params):
    # Lógica de requisição para google_images
    return [{
        'url': f'https://google_images.com/search?q={query}',
        'title': f'Resultado do Google_images para {query}',
        'content': f'Conteúdo de busca indexado via google_images.'
    }]