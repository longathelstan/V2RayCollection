import requests
from bs4 import BeautifulSoup
import time


class VNLinkVipTop:
    def get_link(url: str):
        url_bypass = url.replace("vnlinkvip.top", "v.vnlinkvip.top")
        s = requests.Session()
        
        r = s.get(url_bypass)
        soup = BeautifulSoup(r.text, "lxml")
        
        _csrfToken = soup.find("input", attrs={"name": "_csrfToken"})["value"]
        ad_form_data = soup.find("input", attrs={"name": "ad_form_data"})["value"]
        _tokenfields = soup.find("input", attrs={"name": "_Token[fields]"})["value"]
        _tokenunlocked = soup.find("input", attrs={"name": "_Token[unlocked]"})["value"]
        
        time.sleep(5)
        
        r2 = s.post("https://v.vnlinkvip.top/links/go", data={
            "_method": "POST",
            "_csrfToken": _csrfToken,
            "ad_form_data": ad_form_data,
            "_Token[fields]": _tokenfields,
            "_Token[unlocked]": _tokenunlocked
        }, headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "referer": url_bypass,
        })
        return r2.json()["url"]