import requests
import time
import os

class TwoCaptcha:
    def solve_recaptchav2(url: str, googlekey: str):
        API_KEY = os.getenv("TWOCAPTCHA_API_KEY")
        r = requests.get("http://2captcha.com/in.php", params={
            "key": API_KEY,
            "method": "userrecaptcha",
            "googlekey": googlekey,
            "pageurl": url,
            "json": "1"
        })

        request_id = r.json()["request"]

        while True:
            time.sleep(5)
            r2 = requests.get("http://2captcha.com/res.php", params={
                "key": API_KEY,
                "action": "get",
                "id": request_id,
                "json": "1"
            })
            if r2.json()["status"] == 1:
                print("Solved captcha.")
                return r2.json()["request"]
            
    def solve_recaptchav3(url: str, googlekey: str):
        API_KEY = os.getenv("TWOCAPTCHA_API_KEY")
        r = requests.get("http://2captcha.com/in.php", params={
            "key": API_KEY,
            "method": "userrecaptcha",
            "googlekey": googlekey,
            "version": "V3",
            "pageurl": url,
            "min_score": "0.6",
            "json": "1"
        })

        request_id = r.json()["request"]

        while True:
            time.sleep(5)
            r2 = requests.get("http://2captcha.com/res.php", params={
                "key": API_KEY,
                "action": "get",
                "id": request_id,
                "json": "1"
            })
            if r2.json()["status"] == 1:
                print("Solved captcha.")
                return r2.json()["request"]