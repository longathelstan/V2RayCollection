import requests
from bs4 import BeautifulSoup
from utils.twocaptcha import TwoCaptcha

class Web1sNoteLvl3:
    def get_links_from_text(url: str):
        GOOGLE_KEY = "6LeLfAslAAAAAF-EeUZGqaG2BeDCnSiMX14mUlaI"
        
        s = requests.Session()
        r = s.get(url)
        url = r.url
        
        soup = BeautifulSoup(r.text, "lxml")
        token = soup.find("input", attrs={"name": "_token"})["value"]
        
        grecaptcha_response = TwoCaptcha.solve_recaptchav2(url, GOOGLE_KEY)
        
        r2 = s.post(url, data={
            "_token": token,
            "g-recaptcha-response": grecaptcha_response
        }, headers={
            "content-type": "application/x-www-form-urlencoded"
        })
        
        soup2 = BeautifulSoup(r2.text, "lxml")
        token2 = soup2.find("input", attrs={"name": "_token"})["value"]
        
        r3 = s.post(url, data={
            "_token": token2,
            "countdown": "1"
        }, headers={
            "content-type": "application/x-www-form-urlencoded"
        })
        
        soup3 = BeautifulSoup(r3.text, "lxml")
        return [item["href"] for item in soup3.find("div", attrs={"class": "ql-editor"}).find_all("a")]
        
        