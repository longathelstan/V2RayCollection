from dotenv import load_dotenv
load_dotenv()
from bypass.linkvipio import LinkVipIo
from bypass.memelink import MemeLink

#print(LinkVipIo.get_link("https://linkvip.io/v/ZHBwYa411599"))
print(MemeLink.get_link("https://memelink.net/P4Ct1k8").text)