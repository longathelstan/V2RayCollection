import requests
import os

class SerperDev:
    @staticmethod
    def get_result(keyword, page = 1):
        r = requests.post("https://google.serper.dev/search", headers={
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json'
        }, json={
            "q": keyword,
            "gl": "vn",
            "hl": "vi",
            "page": page
        })
        return r.json()["organic"]