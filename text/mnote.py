import requests
from bs4 import BeautifulSoup

class MNote:
    def get_text(url):
        anti_ddos_url = url.replace("https://mnote.biz", "https://mnote.biz/auth?m=er&dm=mnote.biz&url=")
        s = requests.Session()
        s.get(anti_ddos_url)
        
        r = s.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        return soup.find("div", attrs={"class": "form-control mb-4"}).text.strip()