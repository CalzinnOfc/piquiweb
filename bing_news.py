# Engine: bing_news
import requests

def search(query, params):
    # Lógica de requisição para bing_news
    return [{
        'url': f'https://bing_news.com/search?q={query}',
        'title': f'Resultado do Bing_news para {query}',
        'content': f'Conteúdo de busca indexado via bing_news.'
    }]