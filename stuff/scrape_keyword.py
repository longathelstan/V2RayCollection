import requests
import json
import webbrowser
import time
from bs4 import BeautifulSoup

with open("./keywords.json", "r", encoding="utf-8") as f:
	data = json.load(f)

start = time.time()

while True:
	try:
		s = requests.Session()
		r_st = s.get("https://123s.link/DC3RI")
		
		s.cookies.set("ab", "0", domain="123s.link")
		s.cookies.set("clientDeviceInfo", '{"screen":"1360 x 768","browser":"Chrome","browserVersion":"109.0.0.0","browserMajorVersion":109,"mobile":false,"os":"Windows","osVersion":"8.1","cookies":true,"flashVersion":"no check"}', domain="123s.link")

		r = s.get("https://123s.link/DC3RI", headers={
			"referer": "https://123s.link/DC3RI"
		})
		soup = BeautifulSoup(r.text, "lxml")
		keyword = soup.find("span", attrs={"id": "keyWord"}).strong.text
		image = soup.find("img", attrs={"class": "aligncenter wp-image-429 size-full"})["src"]

		if image in data["123s"]: continue
		webbrowser.open(image)
		webbrowser.open(f"https://www.google.com/search?q={keyword}")

		print(f"Mất {time.time() - start}s để tìm ra 1 từ khoá mới.")
		url = input(f"Nhập url trả về: ")

		data["123s"][image] = url
		start = time.time()
	except Exception as e:
		print(e)
		with open("files/keywords.json", "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
		break