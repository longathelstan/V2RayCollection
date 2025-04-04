from bs4 import BeautifulSoup
import requests
import config
import re
from utils.twocaptcha import TwoCaptcha

class Link4M:    
    def get_code(url: str):
        r = requests.get(url, proxies=config.proxy, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        })
        soup = BeautifulSoup(r.text, "lxml")
        code_element = soup.find("div", attrs={"id": "captcha-html-wrapper"})
        if code_element:
            return code_element["data-code"]
        return ""
    
    def get_ads(id_url: str, code: str):
        r = requests.post('https://link4m.com/api/campaign/get-advertise', data={'alias': id_url, 'codes': code}, proxies=config.proxy, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        })
        return r.json()
    
    '''
    def get_form_data(data: dict):
        data_arr_string = re.findall(r"\[([^[\]]*)\]", data["run"])[0]
        data_arr_string = data_arr_string.replace("\"", "").replace("\\x", "")
        data_arr = data_arr_string.split(",")
        return {
            "campaign_id": bytes.fromhex(data_arr[0]).decode("utf-8"),
            "display_id": bytes.fromhex(data_arr[1]).decode("utf-8"),
            "prefix": bytes.fromhex(data_arr[2]).decode("utf-8")
        }
    '''
    
    def get_form_data(data: dict):
        data_arr_string = re.findall(r"\[([^[\]]*)\]", data["run"])[0]
        data_arr_string = data_arr_string.replace("\"", "").replace("\\x", "")
        data_arr = data_arr_string.split(",")
        def safe_fromhex(hex_str):
            try:
                if len(hex_str) % 2 != 0:
                    hex_str = '0' + hex_str
                return bytes.fromhex(hex_str).decode("utf-8")
            except ValueError:
                #print(f"Invalid hex: {hex_str}")
                return None
        return {
            "campaign_id": safe_fromhex(data_arr[0]),
            "display_id": safe_fromhex(data_arr[1]),
            "prefix": safe_fromhex(data_arr[2])
        }

    def get_link_bypass(id_url: str, data_request: dict, recaptcha_data: str):
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': f"https://link4m.com/go/{id_url}",
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        data = {
            "alias": id_url,
            "campaign_id": data_request["campaign_id"],
            "display_id": data_request["display_id"],
            "prefix": data_request["prefix"],
            "g-recaptcha-response": recaptcha_data
        } 
        r = requests.post("https://link4m.com/links/check-captcha", headers=headers, data=data, proxies=config.proxy)
        if r.json()["success"]:
            return r.json()["url"]
        else:
            print("Error:", r.text)
            return ""

    def get_link(url: str):
        GOOGLE_KEY = "6LcQsTQgAAAAADNQ_pCfukfvS0i9lk4oJTVSs5bZ"
        id = url.split("/")[-1]
        code = Link4M.get_code(url)
        data_ads = Link4M.get_ads(id, code)
        data_request = Link4M.get_form_data(data_ads)
        
        grecaptcha_response = TwoCaptcha.solve_recaptchav2(url, GOOGLE_KEY)
        return Link4M.get_link_bypass(id, data_request, grecaptcha_response)
    
'''
if __name__ == "__main__":
    link4m = Link4M()  

    url = "https://link4m.com/GtpAXQ"
    result = link4m.get_link(url)  

    if result:
        print(f"Final Link: {result}")
    else:
        print("Failed to get the final link")
'''