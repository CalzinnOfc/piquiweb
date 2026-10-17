# Engine: wikipedia
import requests

def search(query, params):
    # Lógica de requisição para wikipedia
    return [{
        'url': f'https://wikipedia.com/search?q={query}',
        'title': f'Resultado do Wikipedia para {query}',
        'content': f'Conteúdo de busca indexado via wikipedia.'
    }]