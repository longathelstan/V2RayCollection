import requests
from bs4 import BeautifulSoup
from utils.cloudflare import Cloudflare
import config
class Note1s:
    def get_text(url):
        s = requests.Session()
        
        r = s.get(url, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }, proxies=config.proxy)
        soup = BeautifulSoup(r.text, "lxml")
        
        token = soup.find("input", attrs={"name": "_token"})["value"]
        r2 = s.post(f"{url}/next", data={
            "_token": token
        }, headers={
            "referer": url,
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }, proxies=config.proxy)
        soup2 = BeautifulSoup(r2.text, "lxml")
        data = soup2.find("div", attrs={"class": "form-control mb-4"})
        data_fix = Cloudflare.replace_html(str(data))
        soup3 = BeautifulSoup(data_fix, "lxml")
        return soup3.text