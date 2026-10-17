# Engine: bing_images
import requests

def search(query, params):
    # Lógica de requisição para bing_images
    return [{
        'url': f'https://bing_images.com/search?q={query}',
        'title': f'Resultado do Bing_images para {query}',
        'content': f'Conteúdo de busca indexado via bing_images.'
    }]