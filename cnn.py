# Engine: cnn
import requests

def search(query, params):
    # Lógica de requisição para cnn
    return [{
        'url': f'https://cnn.com/search?q={query}',
        'title': f'Resultado do Cnn para {query}',
        'content': f'Conteúdo de busca indexado via cnn.'
    }]