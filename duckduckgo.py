# Engine: duckduckgo
import requests

def search(query, params):
    # Lógica de requisição para duckduckgo
    return [{
        'url': f'https://duckduckgo.com/search?q={query}',
        'title': f'Resultado do Duckduckgo para {query}',
        'content': f'Conteúdo de busca indexado via duckduckgo.'
    }]