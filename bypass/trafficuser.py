from bs4 import BeautifulSoup
import requests
from utils.serperdev import SerperDev
from utils.cdkmocr import CDKMOCR
import re
import base64
from utils.selenium import Selenium
from selenium.webdriver.common.by import By
import config
import time


class TrafficUser:
    def get_ads(keyword, pattern, page=1):
        pages = SerperDev.get_result(keyword, page)
        for item in pages:
            if pattern in item["link"]:
                return item["link"]
        return TrafficUser.get_ads(keyword, pattern, page + 1)

    def get_pattern(img_url: str):
        data = CDKMOCR.get_text(img_url)
        check_1 = re.search(
            r"([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", data)
        if check_1:
            return check_1.group()
        return re.search(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", data).group()

    def get_link(url: str):
        driver = Selenium.init_driver(proxy=True)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "lxml")

        keyword = soup.find("input", attrs={"name": "keyword"})["value"]
        img_url = soup.find(
            "img", attrs={"style": "border: 1px solid red;"})["src"]
        pattern = TrafficUser.get_pattern(img_url)

        print(keyword, img_url, pattern)

        ads_url = TrafficUser.get_ads(keyword, pattern)
        s2 = requests.Session()
        r2 = s2.get("https://my.trafficuser.net/que?q=status,azauth,q,t,z&filter=connection", headers={
            "referer": ads_url,
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }, proxies=config.proxy)
        data = r2.json()

        r3 = s2.get("https://my.trafficuser.net/publisher", params={
            "azauth": data["azauth"],
            "q": data["q"],
            "t": data["t"],
            "opa": "123",
            "z": base64.b64encode(ads_url.encode("ascii")).decode("ascii"),
        }, headers={
            "referer": ads_url,
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }, proxies=config.proxy)

        password = r3.json()["password"]

        password_element = driver.find_element(By.NAME, "password")
        password_element.send_keys(password)

        btn_submit = driver.find_element(By.CLASS_NAME, "btn-primary")
        btn_submit.click()

        retries = 100
        while retries > 0:
            try:
                btn_success = driver.find_element(By.CLASS_NAME, "btn-success")
                link = btn_success.get_attribute("href")
                if link.startswith("https://"):
                    return link
                raise Exception
            except Exception as e:
                time.sleep(1)
                retries -= 1
