from dotenv import load_dotenv
load_dotenv()

from bypass import *

url = input("Nhập url cần bypass: ")

if "memelink.net" in url:
	print(MemeLink.get_link(url))
if "dilink.net" in url:
	print(DiLink.get_link(url))
if "link4m.com" in url:
	print(Link4M.get_link(url))
if "vnlinkvip.top" in url:
	print(VNLinkVipTop.get_link(url))
