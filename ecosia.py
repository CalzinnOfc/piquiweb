# Engine: ecosia
import requests

def search(query, params):
    # Lógica de requisição para ecosia
    return [{
        'url': f'https://ecosia.com/search?q={query}',
        'title': f'Resultado do Ecosia para {query}',
        'content': f'Conteúdo de busca indexado via ecosia.'
    }]