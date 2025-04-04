import requests
from bs4 import BeautifulSoup

class PasteEE:
    def get_text(url: str):
        r = requests.get(url.replace("https://paste.ee/p/", "https://paste.ee/d/"))
        return r.text