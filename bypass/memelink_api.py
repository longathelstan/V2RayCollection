from bs4 import BeautifulSoup
import requests
from utils.serperdev import SerperDev
from utils.cdkmocr import CDKMOCR
import re
import random
from utils.twocaptcha import TwoCaptcha
import time
from tqdm import trange


class MemeLink:
    def get_ads(keyword, pattern, page = 1):
        pages = SerperDev.get_result(keyword, page)
        for item in pages:
            if pattern in item["link"]: return item["link"]
            keywords = keyword.split(" ")
            for keywork in keywords:
                if keywork in item["link"]: return item["link"]
        return MemeLink.get_ads(keyword, pattern, page + 1)
    
    def get_pattern(img_url: str):
        data = CDKMOCR.get_text(img_url)
        return re.search(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", data).group()
    
    def generate_rid():
        rid_base = '10000000-1000-4000-8000-100000000000'
        rid = ''
        for char in rid_base:
            if char in ['0', '1', '8']:
                a = int(char)
                bit = a ^ random.randint(0, 15) & 15 >> a // 4
                rid += str(hex(bit)).lstrip("0x")
            else: rid += char
        return rid
    
    def send_options_packet(s: requests.Session, url: str, ref_url: str, rid: str):
        s.options(url, headers={
            "referer": ref_url,
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "rid": rid
        })
    
    def get_link(url: str):
        GOOGLE_SITE_KEY = "6LfR9-EmAAAAAGW1SkaYla3dm9PKtGuiM4AX8PGw"
        s = requests.Session()
        r = s.get(url)
        
        data_js = list(re.finditer(r"data:{id:\"(?P<keyword_id>.+)\",keyword_text:.+,source:\"(?P<img_url>.+)\",source_type.+,IP:\"(?P<ip>.+)\",id:.+rid:\"(?P<rid>.+)\"},linkExist", r.text, re.MULTILINE))
        
        keyword_id = data_js[0].groupdict()["keyword_id"]
        img_url = data_js[0].groupdict()["img_url"].replace("\\u002F", "/")
        ip = data_js[0].groupdict()["ip"]
        rid = data_js[0].groupdict()["rid"]
        rid_ads = MemeLink.generate_rid()

        soup = BeautifulSoup(r.text, "lxml")
        keyword = soup.find("strong", attrs={"class": "text-strong notranslate"}).text
        pattern = MemeLink.get_pattern(img_url)
        ads_url = MemeLink.get_ads(keyword, pattern)
        
        MemeLink.send_options_packet(s, "https://apiclient.memelink.net/api/gen-code/ping", ads_url, rid_ads)
        
        for _ in trange(50):
            time.sleep(1)
            
        grecaptcha_response = TwoCaptcha.solve_recaptchav3(url, GOOGLE_SITE_KEY)
        
        r2 = s.post("https://apiclient.memelink.net/api/gen-code/get-code", json={
            "browser_major_version": "109",
            "browser_name": "Chrome",
            "browser_version": "109.0.0.0",
            "hostname": "https://" + ads_url.split("/")[2],
            "href": ads_url,
            "is_cookies": True,
            "is_mobile": False,
            "os_name": "Windows",
            "os_version": "8.1",
            "screen": "1360 x 768",
            "user_agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }, headers={
            "referer": ads_url,
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "rid": rid_ads
        })

        password = r2.json()["code"]
    
        time.sleep(5)
        
        data = {
            "browser_name": "Chrome",
            "browser_version": "109.0.0.0",
            "os_name": "Windows",
            "os_version": "8.1",
            "os_version_name": "109",
            "keyword_answer": password,
            "link_shorten_id": url.split("/")[-1],
            "keyword": keyword,
            "ip": ip,
            "user_agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "device_name": "desktop",
            "token": grecaptcha_response,
            "keyword_id": keyword_id,
        }
        
        MemeLink.send_options_packet(s, "https://apiclient.memelink.net/api/gen-link/access-link", 'https://memelink.net/', rid)
        
        r3 = s.post("https://apiclient.memelink.net/api/gen-link/access-link", headers = {
            'authority': 'apiclient.memelink.net',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=31536000',
            'content-type': 'application/json',
            'lg': 'vi',
            'ncl': '000011111',
            'origin': 'https://memelink.net',
            'referer': 'https://memelink.net/',
            'rid': rid,
            'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }, json=data)
        print(r3.json())
        
        MemeLink.send_options_packet(s, f"https://apiclient.memelink.net/api/gen-link/finish?answer={password}", 'https://memelink.net/', rid)
        
        r4 = s.get(f"https://apiclient.memelink.net/api/gen-link/finish?answer={password}", headers = {
            'content-type': 'application/json',
            'lg': 'vi',
            'ncl': '000011111',
            'referer': 'https://memelink.net/',
            'rid': rid,
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        })
        print(r4.text)
        
        return r3.json()["data_link"]["url"]
        
        