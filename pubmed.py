# Engine: pubmed
import requests

def search(query, params):
    # Lógica de requisição para pubmed
    return [{
        'url': f'https://pubmed.com/search?q={query}',
        'title': f'Resultado do Pubmed para {query}',
        'content': f'Conteúdo de busca indexado via pubmed.'
    }]