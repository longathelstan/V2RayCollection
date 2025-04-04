from bs4 import BeautifulSoup
import requests
from utils.serperdev import SerperDev
from utils.cdkmocr import CDKMOCR
from utils.ocrspace import OCRSpace
from utils.image import Image
import re
import random
import time
from tqdm import trange
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from utils.selenium import Selenium
import config


class MemeLink:
    def get_ads(keyword: str, pattern: str, page=1):
        if page > 5:
            return ""
        pages = SerperDev.get_result(keyword, page)
        for item in pages:
            if pattern.lower() in item["link"]:
                return item["link"]
        return MemeLink.get_ads(keyword, pattern, page + 1)

    def get_pattern(pattern: str):
        check_1 = re.search(
            r"([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", pattern)
        if check_1:
            return check_1.group()
        check_2 = re.search(
            r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", pattern)
        if check_2:
            return check_2.group()

    def generate_rid():
        rid_base = '10000000-1000-4000-8000-100000000000'
        rid = ''
        for char in rid_base:
            if char in ['0', '1', '8']:
                a = int(char)
                bit = a ^ random.randint(0, 15) & 15 >> a // 4
                rid += str(hex(bit)).lstrip("0x")
            else:
                rid += char
        return rid

    def send_options_packet(s: requests.Session, url: str, ref_url: str, rid: str, user_agent: str):
        s.options(url, headers={
            "referer": ref_url,
            "user-agent": user_agent,
            "rid": rid
        }, proxies=config.proxy)

    def fix_image(img_url: str):
        img = requests.get(img_url).content
        img_cropped = Image.crop_image(img)
        return Image.upload_image(img_cropped)

    def find_page(keyword: str, img_url: str):
        # use cdkm api
        pattern_1 = MemeLink.get_pattern(CDKMOCR.get_text(img_url))
        if pattern_1:
            result = MemeLink.get_ads(keyword, pattern_1)
            if result != "":
                return result

        # use ocrspace api
        pattern_2 = MemeLink.get_pattern(OCRSpace.get_text(img_url))
        result = MemeLink.get_ads(keyword, pattern_2)
        return result

    def get_link(url: str):
        driver = Selenium.init_driver(proxy=True)
        return MemeLink.get_link_with_driver(url, driver)

    def get_link_with_driver(url: str, driver):
        user_agent = driver.execute_script("return navigator.userAgent;")
        driver.get(url)

        rid_ads = MemeLink.generate_rid()

        soup = BeautifulSoup(driver.page_source, "lxml")
        keyword = soup.find(
            "strong", attrs={"class": "text-strong notranslate"}).text
        img_url = MemeLink.fix_image(
            soup.find("img", attrs={"class": "guild-image"})["src"])
        ads_url = MemeLink.find_page(keyword, img_url)
        print(keyword, img_url, ads_url)
        s = requests.Session()
        MemeLink.send_options_packet(
            s, "https://apiclient.memelink.net/api/gen-code/ping", ads_url, rid_ads, user_agent)

        for _ in trange(60):
            time.sleep(1)
        parsed_url = urlparse(ads_url)
        r2 = s.post("https://apiclient.memelink.net/api/gen-code/get-code", json={
            "browser_major_version": "109",
            "browser_name": "Chrome",
            "browser_version": "109.0.0.0",
            "hostname": f"{parsed_url.scheme}://{parsed_url.netloc}/",
            "href": ads_url,
            "is_cookies": True,
            "is_mobile": False,
            "os_name": "Windows",
            "os_version": "8.1",
            "screen": "1360 x 768",
            "user_agent": user_agent
        }, headers={
            "referer": ads_url,
            "user-agent": user_agent,
            "rid": rid_ads
        }, proxies=config.proxy)
        print(r2.json())
        password = r2.json()["code"]
        time.sleep(2)

        code_input_element = driver.find_element(By.ID, "code-input")
        time.sleep(1)
        code_input_element.send_keys(password)

        time.sleep(1)

        submit_element = driver.find_element(By.CLASS_NAME, "password-btn")
        submit_element.click()
        time.sleep(5)
        retries = 30
        while retries > 0:
            try:
                button_element = driver.find_element(
                    By.CLASS_NAME, "btn-success")
                link = button_element.get_attribute("href")
                button_element.click()
                time.sleep(5)
                return link
            except:
                retries -= 1
                if retries % 15 == 0:
                    ss = driver.get_screenshot_as_png()
                    print(Image.upload_image(ss))
                time.sleep(1)
        raise Exception("Bypass failed.")
