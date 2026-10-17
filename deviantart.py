# Engine: deviantart
import requests

def search(query, params):
    # Lógica de requisição para deviantart
    return [{
        'url': f'https://deviantart.com/search?q={query}',
        'title': f'Resultado do Deviantart para {query}',
        'content': f'Conteúdo de busca indexado via deviantart.'
    }]