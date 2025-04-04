import requests

class ShortURL:
    def tinyurl_get(url: str): return requests.get(url).url