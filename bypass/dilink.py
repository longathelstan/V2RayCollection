import requests
import re

class DiLink:
    def get_link(url: str):
        r = requests.get(url)
        url_raw = re.search(r"url: '.+'", r.text).group()
        return url_raw.replace("url: \'", "").replace("'", "")

