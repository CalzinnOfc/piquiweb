# Engine: unsplash
import requests

def search(query, params):
    # Lógica de requisição para unsplash
    return [{
        'url': f'https://unsplash.com/search?q={query}',
        'title': f'Resultado do Unsplash para {query}',
        'content': f'Conteúdo de busca indexado via unsplash.'
    }]