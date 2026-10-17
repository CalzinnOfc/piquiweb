# Engine: brave
import requests

def search(query, params):
    # Lógica de requisição para brave
    return [{
        'url': f'https://brave.com/search?q={query}',
        'title': f'Resultado do Brave para {query}',
        'content': f'Conteúdo de busca indexado via brave.'
    }]